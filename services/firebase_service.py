"""
services/firebase_service.py — Firebase Service Layer
All Firestore + Realtime Database interactions live here.
Controllers and Models never touch the SDK directly.
 
SINGLE SOURCE OF TRUTH — supprime firebase_service.py à la racine du projet.
Tous les imports doivent pointer vers : services.firebase_service
"""
 
import logging
import random
from typing import List, Optional
from datetime import datetime
 
import firebase_admin
from firebase_admin import credentials, firestore, db as rtdb
 
from config import config, FIREBASE_SERVICE_ACCOUNT_PATH, FIREBASE_DATABASE_URL
 
logger = logging.getLogger(__name__)
 
 
# ---------------------------------------------------------------------------
# SDK Initialisation (singleton — only runs once)
# ---------------------------------------------------------------------------
 
def _init_firebase():
    """Initialise Firebase Admin SDK if not already done."""
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)
            firebase_admin.initialize_app(cred, {
                "databaseURL": FIREBASE_DATABASE_URL
            })
            logger.info("✅ Firebase Admin SDK initialised.")
        except Exception as e:
            logger.error(f"❌ Firebase init failed: {e}")
            raise
 
 
_init_firebase()
 
 
# ---------------------------------------------------------------------------
# FirebaseService
# ---------------------------------------------------------------------------
 
class FirebaseService:
    """
    Single access point for all Firebase operations.
    Matches the Firebase class in UML (Partie 2 — Côté Restaurant).
 
    Methods:
        save_order()            → Firestore /commandes
        get_orders()            → Firestore /commandes
        get_order_by_numero()   → Firestore /commandes (by numeroCommande)
        update_order_status()   → Firestore /commandes/{id}
        get_dishes_by_mood()    → Firestore /plats  (scored + ranked)
        get_all_dishes()        → Firestore /plats  (all)
        add_dish()              → Firestore /plats
        get_stats()             → Aggregated from /commandes
        on_snapshot()           → Realtime DB listener (dashboard live)
        push_live_order()       → Realtime DB mirror
    """
 
    def __init__(self):
        self._db   = firestore.client()     # Firestore
        self._rtdb = rtdb.reference("/")    # Realtime DB root
 
    # ── /commandes ───────────────────────────────────────────────────────────
 
    def save_order(self, order_dict: dict) -> str:
        """
        Persist a new order to Firestore.
        Returns the auto-generated document ID.
        Matches UML saveOrder(commande: Commande): void
        """
        try:
            order_dict["createdAt"] = firestore.SERVER_TIMESTAMP
            ref = self._db.collection(config.ORDERS_COLLECTION).document()
            ref.set(order_dict)
            logger.info(
                f"💾 Order saved: {order_dict.get('numeroCommande')} → doc {ref.id}"
            )
            return ref.id
        except Exception as e:
            logger.error(f"❌ save_order failed: {e}")
            raise
 
    def get_orders(self, limit: int = 100) -> List[dict]:
        """
        Fetch recent orders, newest first.
        Matches UML getOrders(): List<Commande>
        """
        try:
            docs = (
                self._db.collection(config.ORDERS_COLLECTION)
                .order_by("createdAt", direction=firestore.Query.DESCENDING)
                .limit(limit)
                .stream(retry=None, timeout=4)
            )
            orders = []
            for doc in docs:
                data = doc.to_dict()
                data["_id"] = doc.id
                # Convert Firestore timestamp → ISO string for JSON safety
                if "createdAt" in data and hasattr(data["createdAt"], "isoformat"):
                    data["createdAt"] = data["createdAt"].isoformat()
                orders.append(data)
            return orders
        except Exception as e:
            logger.error(f"❌ get_orders failed: {e}")
            return []
 
    def get_order_by_numero(self, numero: str) -> Optional[dict]:
        """Fetch a single order by its #MB-XXXXX number."""
        try:
            docs = (
                self._db.collection(config.ORDERS_COLLECTION)
                .where("numeroCommande", "==", numero)
                .limit(1)
                .stream(retry=None, timeout=4)
            )
            for doc in docs:
                data = doc.to_dict()
                data["_id"] = doc.id
                return data
            return None
        except Exception as e:
            logger.error(f"❌ get_order_by_numero failed: {e}")
            return None
 
    def update_order_status(self, doc_id: str, statut: str) -> None:
        """
        Update the status field of an order document.
        Matches UML updateOrderStatus(id, statut): void
        Also mirrors SD6: updateOrder(id, { statut: 'En préparation' })
        """
        try:
            self._db.collection(config.ORDERS_COLLECTION).document(doc_id).update({
                "statut":    statut,
                "updatedAt": firestore.SERVER_TIMESTAMP,
            })
            logger.info(f"🔄 Order {doc_id} → statut: {statut}")
        except Exception as e:
            logger.error(f"❌ update_order_status failed: {e}")
            raise
    def patch_order(self, doc_id: str, fields: dict) -> None:
        """
        Patch specific fields of an order document.
        Used by Commande.sauvegarder() to write the numeroCommande
        after the doc_id is known (guarantees uniqueness).
        """
        try:
            self._db.collection(config.ORDERS_COLLECTION).document(doc_id).update(fields)
            logger.info(f"🩹 Order {doc_id} patched: {list(fields.keys())}")
        except Exception as e:
            logger.error(f"❌ patch_order failed: {e}")
            raise
 
    # ── /plats ───────────────────────────────────────────────────────────────
 
    def get_dishes_by_mood(self, mood: str, max_results: int = None) -> List[dict]:
        """
        Fetch dishes filtered and SCORED by mood from Firestore /plats.
        Returns max_results dishes ranked by mood relevance.
 
        Scoring logic:
          +3  → mood is at index 0 in moods[]  (primary match)
          +2  → mood is at index 1             (secondary match)
          +1  → mood appears at index 2+       (tertiary match)
          tie-break: prix ascending (cheaper first within same score)
 
        Falls back to random sample from all dishes if none tagged.
 
        Firestore structure:
            /plats/{doc_id} → { nom, categorie, prix, ingredients,
                                photo, justification, moods: ["sad", …] }
        """
        if max_results is None:
            max_results = config.MAX_DISHES_PER_MOOD
 
        try:
            docs = (
                self._db.collection(config.DISHES_COLLECTION)
                .where("moods", "array_contains", mood)
                .stream(retry=None, timeout=4)
            )
            dishes = []
            for doc in docs:
                data = doc.to_dict()
                data["id"] = doc.id
                dishes.append(data)
 
            # Fallback: no tagged dishes → random sample from all
            if not dishes:
                logger.warning(
                    f"⚠️  No dishes tagged for mood '{mood}', fallback to random."
                )
                all_dishes = self.get_all_dishes()
                random.shuffle(all_dishes)
                return all_dishes[:max_results]
 
            # Score each dish by position of mood in its moods[]
            def _score(dish: dict) -> tuple:
                moods_list = dish.get("moods", [])
                try:
                    idx   = moods_list.index(mood)
                    score = max(0, 3 - idx)   # idx0→3pts, idx1→2pts, idx2+→1pt
                except ValueError:
                    score = 0
                prix = float(dish.get("prix", dish.get("price", 999)))
                return (-score, prix)         # negative → higher score first
 
            dishes.sort(key=_score)
            result = dishes[:max_results]
 
            logger.info(
                f"🍽️  get_dishes_by_mood('{mood}') → "
                f"{len(dishes)} trouvés, {len(result)} retournés "
                f"(top: {[d.get('nom', '?') for d in result]})"
            )
            return result
 
        except Exception as e:
            logger.error(f"❌ get_dishes_by_mood failed: {e}")
            return []
 
    def get_all_dishes(self) -> List[dict]:
        """Return every dish in /plats."""
        try:
            docs = (
                self._db.collection(config.DISHES_COLLECTION)
                .stream(retry=None, timeout=4)
            )
            result = []
            for doc in docs:
                data = doc.to_dict()
                data["id"] = doc.id
                result.append(data)
            return result
        except Exception as e:
            logger.error(f"❌ get_all_dishes failed: {e}")
            return []
 
    def add_dish(self, dish_dict: dict) -> str:
        """Add a new dish to /plats. Returns doc ID."""
        try:
            ref = self._db.collection(config.DISHES_COLLECTION).document()
            ref.set(dish_dict)
            return ref.id
        except Exception as e:
            logger.error(f"❌ add_dish failed: {e}")
            raise
 
    # ── /stats ───────────────────────────────────────────────────────────────
 
    def get_stats(self) -> dict:
        """
        Compute and return aggregated stats from /commandes.
        Matches UML getStats(): Stats  and  SD7 données agrégées.
 
        Returns:
            totalCommandes       int
            humeursFrequentes    dict  { mood: count }
            platsPopulaires      list  [ { nom, count } ]
            commandesParStatut   dict  { statut: count }
            commandesParPeriode  dict  { 'YYYY-MM-DD': count }  ← SD7 compliance
        """
        try:
            orders = self.get_orders(limit=500)
 
            if not orders:
                return {
                    "totalCommandes":      0,
                    "humeursFrequentes":   {},
                    "platsPopulaires":     [],
                    "commandesParStatut":  {},
                    "commandesParPeriode": {},
                }
 
            # Humeurs frequency
            humeurs: dict = {}
            for o in orders:
                h = o.get("humeur", "unknown")
                humeurs[h] = humeurs.get(h, 0) + 1
 
            # Plats popularity
            plats_count: dict = {}
            for o in orders:
                for p in o.get("plats", []):
                    nom = p.get("nom", "?")
                    plats_count[nom] = plats_count.get(nom, 0) + 1
 
            plats_populaires = sorted(
                [{"nom": k, "count": v} for k, v in plats_count.items()],
                key=lambda x: x["count"],
                reverse=True,
            )[:10]
 
            # Status breakdown
            statuts: dict = {}
            for o in orders:
                s = o.get("statut", "unknown")
                statuts[s] = statuts.get(s, 0) + 1
 
            # Commandes par période (par jour) — SD7 compliance
            par_periode: dict = {}
            for o in orders:
                created = o.get("createdAt", "")
                if created:
                    # createdAt is already ISO string after get_orders() conversion
                    day = str(created)[:10]   # 'YYYY-MM-DD'
                    par_periode[day] = par_periode.get(day, 0) + 1
 
            return {
                "totalCommandes":      len(orders),
                "humeursFrequentes":   humeurs,
                "platsPopulaires":     plats_populaires,
                "commandesParStatut":  statuts,
                "commandesParPeriode": par_periode,
            }
 
        except Exception as e:
            logger.error(f"❌ get_stats failed: {e}")
            return {}
 
    # ── Realtime DB — live dashboard ─────────────────────────────────────────
 
    def on_snapshot(self, callback) -> None:
        """
        Attach a Realtime Database listener for live order updates.
        Matches UML onSnapshot(): void
        SD6: Firebase → Dashboard onSnapshot() → Nouvelle commande reçue
        """
        try:
            ref = self._rtdb.child("commandes_live")
            ref.listen(lambda event: callback(event.data))
            logger.info("👂 Realtime DB listener attached on /commandes_live")
        except Exception as e:
            logger.error(f"❌ on_snapshot failed: {e}")
 
    def push_live_order(self, order_dict: dict) -> None:
        """
        Mirror a new order to Realtime DB for instant dashboard push.
        Called alongside save_order() from OrderController.
        """
        try:
            safe_key = (
                order_dict.get("numeroCommande", "MB-00000")
                .replace("#", "")
                .replace("-", "_")
            )
            self._rtdb.child("commandes_live").child(safe_key).set({
                "numeroCommande": order_dict.get("numeroCommande"),
                "nom":            order_dict.get("nom"),
                "humeur":         order_dict.get("humeur"),
                "total":          order_dict.get("total"),
                "statut":         order_dict.get("statut"),
                "plats":          [p.get("nom") for p in order_dict.get("plats", [])],
                "timestamp":      datetime.utcnow().isoformat(),
            })
            logger.info(f"📡 Live order pushed: {safe_key}")
        except Exception as e:
            logger.error(f"❌ push_live_order failed: {e}")
 
 
# ---------------------------------------------------------------------------
# Module-level singleton — import this everywhere
# ---------------------------------------------------------------------------
firebase_service = FirebaseService()
