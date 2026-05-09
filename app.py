"""
app.py — MoodBite Flask Entry Point
"""
 
from flask import Flask, session, redirect, request
from config import config, FIREBASE_CONFIG
 
from controllers.client_controller    import client_bp
from controllers.mood_controller      import mood_bp
from controllers.order_controller     import order_bp
from controllers.dashboard_controller import dashboard_bp
 
app = Flask(__name__)
app.secret_key = config.SECRET_KEY
 
app.register_blueprint(client_bp)
app.register_blueprint(mood_bp)
app.register_blueprint(order_bp)
app.register_blueprint(dashboard_bp)
 
# ── Language switcher route ──────────────────────────────────────────────────
@app.route("/lang/<lang_code>")
def switch_lang(lang_code):
    if lang_code in config.SUPPORTED_LANGS:
        session["lang"] = lang_code
    return redirect(request.referrer or "/")
 
# ── Context processor ────────────────────────────────────────────────────────
# Injects into EVERY template automatically
@app.context_processor
def inject_globals():
    lang = session.get("lang", config.DEFAULT_LANG)
    return {
        "lang":            lang,
        "fr":              lang == "fr",
        "firebase_config": FIREBASE_CONFIG,
        "mood_meta":       config.MOOD_META,        # ← fix: humeur.html needs this
        "supported_moods": config.SUPPORTED_MOODS,  # ← bonus: might be needed too
    }
 
if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)