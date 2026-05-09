"""
controllers/mood_controller.py — MoodController
Handles: /mood/scan  /mood/analyse  /mood/manuel  /mood/set  /mood/data
Matches UML: lancerDetection(), getMoodData()
Matches SD2 sequence diagram
"""
 
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, jsonify
)
 
from models.face_scan import FaceScan
from models.humeur import Humeur
from services.firebase_service import firebase_service
from config import config
 
mood_bp = Blueprint("mood", __name__, url_prefix="/mood")
 
 
def _guard_name():
    """Redirect to accueil if no name in session."""
    return not bool(session.get("user_name"))
 
 
# ---------------------------------------------------------------------------
# GET /mood/scan  — IA Face Scan screen
# SD2: Client choisit Mode IA → affiche écran scan
# ---------------------------------------------------------------------------
 
@mood_bp.route("/scan")
def scan():
    if _guard_name():
        return redirect(url_for("client.accueil"))
    return render_template(
        "humeur.html",
        mode      = "ia",
        user_name = session.get("user_name", ""),
    )
 
 
# ---------------------------------------------------------------------------
# POST /mood/analyse  — Process face-api.js result from frontend
# SD2: humeurDétectée(mood) → getMoodData(mood) → plats[], science, quote
# ---------------------------------------------------------------------------
 
@mood_bp.route("/analyse", methods=["POST"])
def analyse():
    lang = session.get("lang", config.DEFAULT_LANG)
    data = request.get_json(silent=True) or {}
 
    face_scan = FaceScan()
    face_scan.analyser_visage(data)
 
    if face_scan.statut == "error":
        msg = (
            data.get("error") or
            (
                "Scan failed — try again or pick your mood manually 🙈"
                if lang == "en" else
                "Scan raté — réessaie ou choisis ton humeur manuellement 🙈"
            )
        )
        return jsonify({"ok": False, "error": msg}), 422
 
    humeur = face_scan.retourner_humeur()
    session["humeur"]          = humeur.to_dict()
    session["detection_mode"]  = "ia"
 
    plats = firebase_service.get_dishes_by_mood(
        humeur.type, max_results=config.MAX_DISHES_PER_MOOD
    )
 
    return jsonify({
        "ok":      True,
        "mood":    humeur.type,
        "emoji":   humeur.emoji,
        "label":   humeur.label(lang),
        "quote":   humeur.get_quote(lang),
        "color":   humeur.color,
        "plats":   plats,
        "redirect": url_for("order.menu"),
    })
 
 
# ---------------------------------------------------------------------------
# GET /mood/manuel  — Manual mood picker screen
# SD2: Client choisit Mode Manuel → liste des humeurs
# ---------------------------------------------------------------------------
 
@mood_bp.route("/manuel")
def manuel():
    if _guard_name():
        return redirect(url_for("client.accueil"))
    lang = session.get("lang", config.DEFAULT_LANG)
    return render_template(
        "humeur.html",
        mode      = "manuel",
        lang      = lang,
        user_name = session.get("user_name", ""),
    )
 
 
# ---------------------------------------------------------------------------
# POST /mood/set  — Set mood manually (no AI)
# SD2: Sélectionne une humeur → getMoodData → plats[]
# ---------------------------------------------------------------------------
 
@mood_bp.route("/set", methods=["POST"])
def set_mood():
    lang = session.get("lang", config.DEFAULT_LANG)
    data = request.get_json(silent=True) or {}
    mood_type = data.get("mood", "").lower().strip()
 
    if mood_type not in config.SUPPORTED_MOODS:
        return jsonify({
            "ok":    False,
            "error": f"Unknown mood '{mood_type}'. Pick one of: {config.SUPPORTED_MOODS}"
        }), 400
 
    humeur = Humeur(type=mood_type)
    session["humeur"]          = humeur.to_dict()
    session["detection_mode"]  = "manuel"
 
    plats = firebase_service.get_dishes_by_mood(
        mood_type, max_results=config.MAX_DISHES_PER_MOOD
    )
 
    return jsonify({
        "ok":      True,
        "mood":    humeur.type,
        "emoji":   humeur.emoji,
        "label":   humeur.label(lang),
        "quote":   humeur.get_quote(lang),
        "color":   humeur.color,
        "plats":   plats,
        "redirect": url_for("order.menu"),
    })
 
 
# ---------------------------------------------------------------------------
# GET /mood/data  — Lightweight endpoint: mood metadata + dishes
# Used by menu page to refresh dish list without full page reload
# ---------------------------------------------------------------------------
 
@mood_bp.route("/data")
def get_mood_data():
    lang     = session.get("lang", config.DEFAULT_LANG)
    humeur_d = session.get("humeur")
 
    if not humeur_d:
        return jsonify({"ok": False, "error": "No mood in session"}), 400
 
    humeur = Humeur.from_dict(humeur_d)
    plats  = firebase_service.get_dishes_by_mood(
        humeur.type, max_results=config.MAX_DISHES_PER_MOOD
    )
 
    return jsonify({
        "ok":    True,
        "mood":  humeur.type,
        "emoji": humeur.emoji,
        "label": humeur.label(lang),
        "quote": humeur.get_quote(lang),
        "color": humeur.color,
        "bg":    humeur.bg,
        "plats": plats,
    })