"""
config.py — MoodBite Configuration
Firebase credentials + app settings
"""
 
import os
import json
import tempfile
 
# ---------------------------------------------------------------------------
# Firebase Web Config (frontend JS)
# ---------------------------------------------------------------------------
 
FIREBASE_CONFIG = {
    "apiKey":            "AIzaSyAt5IYGf5wB5guuWkilCvqUMAcUPw7N4t4",
    "authDomain":        "moodbite-project-2cd7c.firebaseapp.com",
    "projectId":         "moodbite-project-2cd7c",
    "storageBucket":     "moodbite-project-2cd7c.firebasestorage.app",
    "messagingSenderId": "904877069142",
    "appId":             "1:904877069142:web:35248c2514f270fe113cf7",
}
 
# ---------------------------------------------------------------------------
# Firebase Admin SDK — supporte local (fichier) ET production (env var)
# ---------------------------------------------------------------------------
 
def _resolve_service_account_path() -> str:
    """
    En local     → lit serviceAccountKey.json depuis la racine du projet
    En production → lit la variable d'env FIREBASE_SERVICE_ACCOUNT_JSON
                    (contenu JSON complet) et l'écrit dans un fichier temp
    """
    # Production : variable d'environnement contient le JSON complet
    json_env = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    if json_env:
        try:
            data = json.loads(json_env)
            tmp  = tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            )
            json.dump(data, tmp)
            tmp.close()
            return tmp.name
        except Exception as e:
            raise RuntimeError(f"Invalid FIREBASE_SERVICE_ACCOUNT_JSON: {e}")
 
    # Local : fichier classique
    path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "serviceAccountKey.json")
    return path
 
 
FIREBASE_SERVICE_ACCOUNT_PATH = _resolve_service_account_path()
FIREBASE_DATABASE_URL = "https://moodbite-project-2cd7c-default-rtdb.firebaseio.com"
 
# ---------------------------------------------------------------------------
# Flask App Settings
# ---------------------------------------------------------------------------
 
class Config:
    SECRET_KEY  = os.getenv("SECRET_KEY", "moodbite-obayoli-secret-2024")
    DEBUG       = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    HOST        = os.getenv("HOST", "0.0.0.0")
    PORT        = int(os.getenv("PORT", 5000))
 
    DASHBOARD_PASSWORD = os.getenv("DASHBOARD_PASSWORD", "obayoli2024")
 
    # Firestore collections
    ORDERS_COLLECTION = "commandes"
    DISHES_COLLECTION = "plats"
    STATS_COLLECTION  = "stats"
 
    SUPPORTED_MOODS = [
        "happy", "sad", "stressed", "angry", "neutral", "excited",
    ]
 
    MOOD_META = {
        "happy": {
            "emoji": "😄",
            "label_en": "Happy",     "label_fr": "Heureux",
            "color": "#F6C945",      "bg": "#FFFBEA",
            "quote_en": "Good vibes only — your plate matches your energy! ✨",
            "quote_fr": "Bonne humeur = bon repas, c'est prouvé ✨",
        },
        "sad": {
            "emoji": "😢",
            "label_en": "Sad",       "label_fr": "Triste",
            "color": "#6EA8D8",      "bg": "#EBF4FC",
            "quote_en": "We got you. Comfort food incoming 🫂",
            "quote_fr": "On a ce qu'il te faut. Un vrai câlin dans l'assiette 🫂",
        },
        "stressed": {
            "emoji": "😤",
            "label_en": "Stressed",  "label_fr": "Stressé",
            "color": "#E4686E",      "bg": "#FEF0F0",
            "quote_en": "Deep breaths. Your food will handle the rest 🧘",
            "quote_fr": "Respire. Ton assiette s'occupe du reste 🧘",
        },
        "angry": {
            "emoji": "😠",
            "label_en": "Angry",     "label_fr": "Énervé",
            "color": "#FF6B35",      "bg": "#FFF3EE",
            "quote_en": "Channel that energy into epic flavor 🔥",
            "quote_fr": "Transforme cette énergie en quelque chose de délicieux 🔥",
        },
        "neutral": {
            "emoji": "😐",
            "label_en": "Neutral",   "label_fr": "Neutre",
            "color": "#7B7F86",      "bg": "#F4F4F5",
            "quote_en": "Steady mode — let's keep that balance 🎯",
            "quote_fr": "Mode équilibre activé 🎯",
        },
        "excited": {
            "emoji": "🤩",
            "label_en": "Excited",   "label_fr": "Excité",
            "color": "#2E9CA3",      "bg": "#E8F8F9",
            "quote_en": "That energy is CONTAGIOUS — match it with the menu! 🚀",
            "quote_fr": "Cette énergie est CONTAGIEUSE — ton menu va kiffer! 🚀",
        },
    }
 
    MAX_DISHES_PER_MOOD = 4
    ORDER_PREFIX        = "MB"
    ORDER_PADDING       = 5
    DEFAULT_LANG        = "en"
    SUPPORTED_LANGS     = ["en", "fr"]
 
 
config = Config()