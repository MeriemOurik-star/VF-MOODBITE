"""
controllers/client_controller.py — ClientController
Handles: /  (accueil) + /name (saisir nom)
Matches UML: saisirNom(), choisirMode()
Matches SD1 sequence diagram
"""
 
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, jsonify
)
 
from models.client import Client
from config import config
 
client_bp = Blueprint("client", __name__)
 
 
# ---------------------------------------------------------------------------
# GET /  — Accueil (Welcome screen)
# SD1: Client ouvre l'application → Affiche l'écran d'accueil
# ---------------------------------------------------------------------------
 
@client_bp.route("/")
def accueil():
    # 1. Resolve language BEFORE clearing session
    selected_lang = (
        request.args.get("lang")
        or session.get("lang")
        or config.DEFAULT_LANG
    )
 
    # 2. Only clear order-related keys — never the lang preference
    for key in ("user_name", "humeur", "panier", "commande", "detection_mode"):
        session.pop(key, None)
 
    # 3. Re-apply resolved language
    session["lang"] = selected_lang
 
    return render_template("accueil.html")
 
 
# ---------------------------------------------------------------------------
# POST /name  — Saisir nom / pseudo
# SD1: Client saisit son nom → validerNom(nom) → OK / Erreur
# ---------------------------------------------------------------------------
 
@client_bp.route("/name", methods=["POST"])
def saisir_nom():
    lang = session.get("lang", config.DEFAULT_LANG)
    data = request.get_json(silent=True) or {}
    nom  = data.get("nom", "").strip()
 
    client = Client()
    try:
        client.saisir_nom(nom)
    except ValueError:
        msg = (
            "Please enter your name first 👀"
            if lang == "en" else
            "Entre ton prénom d'abord 👀"
        )
        return jsonify({"ok": False, "error": msg}), 400
 
    session["user_name"] = client.nom
 
    return jsonify({
        "ok":      True,
        "nom":     client.nom,
        "message": (
            f"Hey {client.nom}! Let's find your vibe 🎯"
            if lang == "en" else
            f"Salut {client.nom} ! On va trouver ton vibe 🎯"
        ),
    })
 
 
# ---------------------------------------------------------------------------
# GET /mode  — Choisir mode de détection (rendered view)
# SD1 end → SD2 start: passe à l'étape choix du mode de détection
# ---------------------------------------------------------------------------
 
@client_bp.route("/mode")
def choisir_mode():
    if not session.get("user_name"):
        return redirect(url_for("client.accueil"))
    return render_template("humeur.html")
 
 
# ---------------------------------------------------------------------------
# POST /mode  — Valider le mode choisi (IA ou Manuel)
# ---------------------------------------------------------------------------
 
@client_bp.route("/mode", methods=["POST"])
def set_mode():
    lang = session.get("lang", config.DEFAULT_LANG)
    data = request.get_json(silent=True) or {}
    mode = data.get("mode", "").strip().lower()
 
    client = Client(nom=session.get("user_name", ""))
    try:
        validated_mode = client.choisir_mode(mode)
    except ValueError:
        return jsonify({
            "ok":    False,
            "error": "Invalid mode. Choose 'ia' or 'manuel'."
        }), 400
 
    session["detection_mode"] = validated_mode
 
    redirect_url = (
        url_for("mood.scan") if validated_mode == "ia"
        else url_for("mood.manuel")
    )
    return jsonify({"ok": True, "mode": validated_mode, "redirect": redirect_url})
