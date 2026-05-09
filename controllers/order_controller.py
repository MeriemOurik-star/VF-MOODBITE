"""
controllers/order_controller.py — OrderController
Handles: /menu  /cart/toggle  /order/confirm  /confirmation
Matches UML: confirmerCommande(), genererNumero()
Matches SD3 + SD4 sequence diagrams
"""
 
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, jsonify
)
 
from models.commande import Commande
from models.panier import Panier
from models.plat import Plat
from models.humeur import Humeur
from services.firebase_service import firebase_service
from config import config
 
order_bp = Blueprint("order", __name__)
 
 
def _guard_mood():
    """Ensure client has both name and mood in session."""
    return not (session.get("user_name") and session.get("humeur"))
 
 
# ---------------------------------------------------------------------------
# GET /menu  — Dish menu screen
# SD3: getDishesbyMood(mood) → dishes[] → Affiche la liste des plats
# ---------------------------------------------------------------------------
 
@order_bp.route("/menu")
def menu():
    if _guard_mood():
        return redirect(url_for("client.accueil"))
 
    lang     = session.get("lang", config.DEFAULT_LANG)
    humeur_d = session.get("humeur", {})
    humeur   = Humeur.from_dict(humeur_d)
 
    # Fetch dishes for this mood from Firestore
    plats_raw = firebase_service.get_dishes_by_mood(humeur.type)
    plats     = [Plat.from_dict(p, p.get("id", "")) for p in plats_raw]
 
    # Rebuild cart from session
    panier = Panier.from_session(session.get("panier", []))
 
    return render_template(
        "menu.html",
        humeur       = humeur,
        plats        = [p.to_dict() for p in plats],
        panier       = panier.to_dict(),
        selected_ids = [p.id for p in panier.get_panier()],
        lang         = lang,
        mood_meta    = config.MOOD_META,
    )
 
 
# ---------------------------------------------------------------------------
# POST /cart/toggle  — Add / remove a dish from cart
# SD3: toggleDish(dish) → panier mis à jour
# ---------------------------------------------------------------------------
 
@order_bp.route("/cart/toggle", methods=["POST"])
def toggle_cart():
    lang = session.get("lang", config.DEFAULT_LANG)
    data = request.get_json(silent=True) or {}
 
    plat_data = data.get("plat")
    if not plat_data:
        return jsonify({"ok": False, "error": "No dish data provided"}), 400
 
    plat   = Plat.from_dict(plat_data, plat_data.get("id", ""))
    panier = Panier.from_session(session.get("panier", []))
    added  = panier.toggle_dish(plat)
 
    # Persist updated cart to session
    session["panier"] = panier.to_session()
 
    action = (
        ("added to cart 🛒" if lang == "en" else "ajouté au panier 🛒")
        if added else
        ("removed from cart" if lang == "en" else "retiré du panier")
    )
 
    return jsonify({
        "ok":         True,
        "added":      added,
        "message":    f"{plat.nom} {action}",
        "cart_count": panier.count(),
        "cart_total": panier.total,
        "cart_ids":   [p.id for p in panier.get_panier()],
    })
 
 
# ---------------------------------------------------------------------------
# GET /order/confirm  — Order summary / récapitulatif
# SD4: Affiche le récapitulatif (nom, humeur, plats, total)
# ---------------------------------------------------------------------------
 
@order_bp.route("/order/confirm")
def confirm_view():
    if _guard_mood():
        return redirect(url_for("client.accueil"))
 
    lang   = session.get("lang", config.DEFAULT_LANG)
    panier = Panier.from_session(session.get("panier", []))
 
    # SD4 guard: panier vide
    if panier.is_empty():
        msg = (
            "Your cart is empty — pick at least one dish! 🍽️"
            if lang == "en" else
            "Ton panier est vide — choisis au moins un plat ! 🍽️"
        )
        return redirect(url_for("order.menu") + f"?error={msg}")
 
    humeur = Humeur.from_dict(session.get("humeur", {}))
 
    return render_template(
        "menu.html",
        view      = "recap",
        user_name = session.get("user_name"),
        humeur    = humeur,
        panier    = panier.to_dict(),
        lang      = lang,
        mood_meta = config.MOOD_META,
    )
 
 
# ---------------------------------------------------------------------------
# POST /order/confirm  — Confirm & save order to Firebase
# SD4: genererNumeroCommande() → saveOrder({…}) → Firebase
#
# IMPORTANT: commande.generer_numero() is NO LONGER called here.
# sauvegarder() handles it internally using the Firestore doc_id
# to guarantee uniqueness. See models/commande.py → sauvegarder().
# ---------------------------------------------------------------------------
 
@order_bp.route("/order/confirm", methods=["POST"])
def confirm_order():
    lang     = session.get("lang", config.DEFAULT_LANG)
    panier   = Panier.from_session(session.get("panier", []))
    humeur_d = session.get("humeur", {})
 
    # Validation
    if panier.is_empty():
        return jsonify({
            "ok":   False,
            "error": (
                "Select at least one dish first 🍽️"
                if lang == "en" else
                "Sélectionne au moins un plat 🍽️"
            )
        }), 400
 
    # Build Commande
    commande = Commande(
        plats       = panier.get_panier(),
        humeur_type = humeur_d.get("type", "neutral"),
        client_nom  = session.get("user_name", ""),
        statut      = "nouvelle commande",
    )
    commande.calculer_total()
    # ↑ generer_numero() removed — sauvegarder() generates it using doc_id
 
    # SD4: saveOrder → Firebase (numero generated inside sauvegarder)
    try:
        doc_id = commande.sauvegarder(firebase_service)
        firebase_service.push_live_order(commande.to_dict())
    except Exception:
        return jsonify({
            "ok":   False,
            "error": (
                "Something went wrong, please try again 😬"
                if lang == "en" else
                "Une erreur est survenue, veuillez réessayer 😬"
            )
        }), 500
 
    # Persist confirmed order info to session for confirmation screen
    session["commande"] = {
        "numero":     commande.numero_commande,
        "total":      commande.total,
        "doc_id":     doc_id,
        "humeur":     humeur_d,
        "plats":      [p.to_dict() for p in commande.plats],
        "client_nom": commande.client_nom,
    }
    # Clear cart after successful order
    session.pop("panier", None)
 
    humeur = Humeur.from_dict(humeur_d)
 
    return jsonify({
        "ok":      True,
        "numero":  commande.numero_commande,
        "total":   commande.total,
        "quote":   humeur.get_quote(lang),
        "redirect": url_for("order.confirmation"),
    })
 
 
# ---------------------------------------------------------------------------
# GET /confirmation  — Order confirmed screen
# SD4: Affiche l'écran de confirmation (numéro, récapitulatif, quote)
# ---------------------------------------------------------------------------
 
@order_bp.route("/confirmation")
def confirmation():
    commande_d = session.get("commande")
    if not commande_d:
        return redirect(url_for("client.accueil"))
 
    lang   = session.get("lang", config.DEFAULT_LANG)
    humeur = Humeur.from_dict(commande_d.get("humeur", {}))
 
    return render_template(
        "confirmation.html",
        commande  = commande_d,
        humeur    = humeur,
        quote     = humeur.get_quote(lang),
        lang      = lang,
        mood_meta = config.MOOD_META,
    )
 
 
# ---------------------------------------------------------------------------
# POST /order/reset  — Start a new order (reset state)
# SD4: Clique "Nouvelle commande" → resetState() → Retour à l'accueil
# ---------------------------------------------------------------------------
 
@order_bp.route("/order/reset", methods=["POST"])
def reset_order():
    # Keep language preference, clear everything else
    lang = session.get("lang", config.DEFAULT_LANG)
    session.clear()
    session["lang"] = lang
    return jsonify({"ok": True, "redirect": url_for("client.accueil")})
 