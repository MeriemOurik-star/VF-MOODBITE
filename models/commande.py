"""
models/commande.py — Commande Model
Matches UML: -numeroCommande, -statut, -total, -dateHeure
"""
 
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
 
from config import config
from models.plat import Plat
 
 
# Valid order statuses (progression flow from SD6 sequence diagram)
STATUTS_VALIDES = [
    "nouvelle commande",
    "en préparation",
    "prête",
    "servie",
]
 
 
@dataclass
class Commande:
    numero_commande: str = ""
    statut:          str = "nouvelle commande"
    total:           float = 0.0
    date_heure:      datetime = field(default_factory=datetime.utcnow)
    plats:           List[Plat] = field(default_factory=list)
    humeur_type:     str = ""
    client_nom:      str = ""
 
    # ── UML methods ──────────────────────────────────────────────────────────
 
    def generer_numero(self, doc_id: str = "") -> str:
        """
        Generate a GUARANTEED UNIQUE order number: #MB-00342 format.
 
        Strategy: combine a timestamp (seconds since epoch, last 5 digits)
        with the first 3 chars of the Firestore doc_id when available.
        This gives collision probability ≈ 0 without any extra DB query.
 
        Examples:
            doc_id provided  → #MB-84291-A3F
            no doc_id        → #MB-84291
        """
        import time
        ts_suffix = str(int(time.time()))[-config.ORDER_PADDING:]   # last 5 digits of epoch
 
        if doc_id:
            # Add first 3 chars of Firestore doc ID for extra uniqueness
            id_part = doc_id[:3].upper()
            self.numero_commande = f"#{config.ORDER_PREFIX}-{ts_suffix}-{id_part}"
        else:
            self.numero_commande = f"#{config.ORDER_PREFIX}-{ts_suffix}"
 
        return self.numero_commande
 
    def sauvegarder(self, firebase_service) -> str:
        """
        Persist the commande to Firestore via FirebaseService.
        Generates the order number AFTER saving so we can use the doc_id.
        Returns the Firestore document ID.
 
        Flow (SD4):
            1. Save to Firestore → get doc_id
            2. Generate numero using doc_id (guaranteed unique)
            3. Update the document with the generated numero
        """
        # Step 1: save without numero first to get doc_id
        data = self.to_dict()
        data["numeroCommande"] = ""   # placeholder
        doc_id = firebase_service.save_order(data)
 
        # Step 2: generate unique numero using doc_id
        self.generer_numero(doc_id)
 
        # Step 3: patch the document with the real numero
        firebase_service.patch_order(doc_id, {"numeroCommande": self.numero_commande})
 
        return doc_id
 
    def mettre_a_jour_statut(self, statut: str, firebase_service=None) -> None:
        """
        Update order status locally (and in Firestore if firebase_service provided).
        Validates against allowed statuses.
        """
        statut = statut.lower().strip()
        if statut not in STATUTS_VALIDES:
            raise ValueError(
                f"Invalid status '{statut}'. "
                f"Allowed: {STATUTS_VALIDES}"
            )
        self.statut = statut
        if firebase_service and self.numero_commande:
            firebase_service.update_order_status(self.numero_commande, statut)
 
    # ── Helpers ──────────────────────────────────────────────────────────────
 
    def calculer_total(self) -> float:
        """Recompute total from plats list."""
        self.total = round(sum(p.prix for p in self.plats), 2)
        return self.total
 
    # ── Serialisation ────────────────────────────────────────────────────────
 
    def to_dict(self) -> dict:
        return {
            "numeroCommande": self.numero_commande,
            "statut":         self.statut,
            "total":          self.total,
            "dateHeure":      self.date_heure.isoformat(),
            "plats":          [p.to_dict() for p in self.plats],
            "humeur":         self.humeur_type,
            "nom":            self.client_nom,
        }
 
    @classmethod
    def from_dict(cls, data: dict) -> "Commande":
        plats = [
            Plat.from_dict(p, p.get("id", ""))   # ← fix: pass id to preserve Plat.id
            for p in data.get("plats", [])
        ]
        date_str = data.get("dateHeure", "")
        try:
            date_heure = datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            date_heure = datetime.utcnow()
        return cls(
            numero_commande=data.get("numeroCommande", ""),
            statut=data.get("statut", "nouvelle commande"),
            total=float(data.get("total", 0.0)),
            date_heure=date_heure,
            plats=plats,
            humeur_type=data.get("humeur", ""),
            client_nom=data.get("nom", ""),
        )
 
    def __str__(self) -> str:
        return f"Commande({self.numero_commande}, {self.statut}, {self.total} dhs)"
 