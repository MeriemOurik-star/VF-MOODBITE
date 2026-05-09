"""
seed_firebase.py — MoodBite Database Seeder
============================================
Populates Firestore /plats with ALL real OBAYOLI dishes.
Photos served from local dish_sources/Plats/ folder via Flask static route.
 
Real menu (from OBAYOLI menu photos):
  Sandwichs · Bowls · Gratins · Crêpes · Gaufres ·
  Milkshakes · Smoothies · Mojitos · Tiramisu · Jus
 
Usage:
    python seed_firebase.py
"""
 
import firebase_admin
from firebase_admin import credentials, firestore
import os
 
# ── Init Firebase ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(BASE_DIR, "serviceAccountKey.json"))
firebase_admin.initialize_app(cred)
db = firestore.client()
 
# ── Photo base path helper ────────────────────────────────────────────────────
# Photos live in:  dish_sources/Plats/<filename>
# Flask serves them at: /static/dishes/<filename>
# Fallback Unsplash URLs provided if local file missing.
 
def ph(filename, fallback=""):
    """Return the Flask static URL for a dish photo."""
    return f"/static/dishes/{filename}"
 
# ── Full dish catalogue ───────────────────────────────────────────────────────
DISHES = [
 
    # ══════════════════════════════════════════════════════════════
    # LES SANDWICHS
    # ══════════════════════════════════════════════════════════════
 
    {
        "nom":              "L'Obayoli",
        "categorie_en":     "Sandwich",
        "categorie_fr":     "Sandwich",
        "prix":             39,
        "emoji":            "🌯",
        "photo":            ph("obayoli.jpg",     "https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=600&q=80"),
        "ingredients":      "Kebab grillé, Tortilla, sauce Blanche, salade, tomate, oignon — uniquement en tortilla",
        "justification_en": "The OG OBAYOLI. Simple, reliable, no thinking required 🌯",
        "justification_fr": "L'OG OBAYOLI. Simple, fiable, commande sans réfléchir 🌯",
        "science_en":       "Familiar foods lower cortisol by activating predictive reward circuits. Your brain already knows it's good.",
        "science_fr":       "Les aliments familiers baissent le cortisol en activant les circuits de récompense prédictifs.",
        "moods":            ["stressed", "neutral", "sad"],
    },
    {
        "nom":              "Grec",
        "categorie_en":     "Sandwich",
        "categorie_fr":     "Sandwich",
        "prix":             59,
        "emoji":            "🥗",
        "photo":            ph("grec_sandwich.jpg", "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80"),
        "ingredients":      "Kebab grillé, sauce Blanche, salade, tomate, oignon rouge",
        "justification_en": "Safe bet, no surprises — exactly what you need rn 🥗",
        "justification_fr": "Valeur sûre, pas de surprises — exactement ce qu'il te faut 🥗",
        "science_en":       "Simple predictable meals reduce cognitive load during stress. Less mental effort = faster recovery.",
        "science_fr":       "Les repas simples réduisent la charge cognitive. Moins d'effort mental = récupération plus rapide.",
        "moods":            ["stressed", "neutral"],
    },
    {
        "nom":              "Marrakchi",
        "categorie_en":     "Sandwich",
        "categorie_fr":     "Sandwich",
        "prix":             59,
        "emoji":            "🫒",
        "photo":            ph("marrakchi.jpg",   "https://images.unsplash.com/photo-1529006557810-274b9b2fc783?w=600&q=80"),
        "ingredients":      "Kebab grillé, sauce secrète maison, salade, tomate, oignon cuit, poivrons, coriandre, olives",
        "justification_en": "Secret house sauce = instant social proof 🤫",
        "justification_fr": "Sauce secrète = preuve sociale instantanée 🤫",
        "science_en":       "Exotic spice combos stimulate novelty-seeking dopamine circuits. Mystery = excitement.",
        "science_fr":       "Les combinaisons d'épices exotiques stimulent les circuits dopaminergiques de nouveauté.",
        "moods":            ["neutral", "happy", "excited"],
    },
    {
        "nom":              "Chèvre Miel",
        "categorie_en":     "Sandwich",
        "categorie_fr":     "Sandwich",
        "prix":             69,
        "emoji":            "🍯",
        "photo":            ph("chevre_miel_sandwich.jpg", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80"),
        "ingredients":      "Kebab grillé, sauce sucrée, salade, tomate, chou rouge, fromage de chèvre, miel",
        "justification_en": "Sweet + salty — your open mind is craving this contrast 🍯",
        "justification_fr": "Sucré + salé — ton esprit ouvert le veut 🍯",
        "science_en":       "Happy brains love flavour contrasts. Goat cheese + honey stimulates taste receptors unexpectedly.",
        "science_fr":       "Les cerveaux heureux adorent les contrastes. Chèvre + miel stimule les récepteurs de façon inattendue.",
        "moods":            ["happy", "neutral", "excited"],
    },
    {
        "nom":              "Fuego",
        "categorie_en":     "Sandwich",
        "categorie_fr":     "Sandwich",
        "prix":             65,
        "emoji":            "🔥",
        "photo":            ph("fuego_sandwich.jpg", "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=600&q=80"),
        "ingredients":      "Kebab grillé, sauce spicy, salade, tomate, oignon rouge, chou rouge, sauce cheddar, jalapeños",
        "justification_en": "Capsaicin hits the same receptors as anger. Use it 🔥",
        "justification_fr": "La capsaïcine touche les mêmes récepteurs que la colère. Utilise-la 🔥",
        "science_en":       "TRPV1 receptor activation releases adrenaline — which you're already producing. Redirect, don't suppress.",
        "science_fr":       "Activation des récepteurs TRPV1 libérant de l'adrénaline — que tu produis déjà.",
        "moods":            ["angry", "excited"],
    },
    {
        "nom":              "Fondant",
        "categorie_en":     "Sandwich",
        "categorie_fr":     "Sandwich",
        "prix":             69,
        "emoji":            "🧀",
        "photo":            ph("fondant.jpg",     "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80"),
        "ingredients":      "Kebab grillé, samourai, salade, tomate, chou rouge, mozza fondu, lardinettes",
        "justification_en": "Rich & indulgent — the ultimate feel-good choice 🧀",
        "justification_fr": "Riche et gourmand — le choix feel-good ultime 🧀",
        "science_en":       "Dopamine + reward circuits love indulgent meals. You're wired for max satisfaction.",
        "science_fr":       "Dopamine + circuits de récompense adorent les repas gourmands. Satisfaction maximale garantie.",
        "moods":            ["happy", "excited", "sad"],
    },
    {
        "nom":              "Raclette",
        "categorie_en":     "Sandwich",
        "categorie_fr":     "Sandwich",
        "prix":             69,
        "emoji":            "🧀",
        "photo":            ph("raclette_sandwich.jpg", "https://images.unsplash.com/photo-1574484284002-952d92456975?w=600&q=80"),
        "ingredients":      "Kebab grillé, sauce mango, salade, tomate, chou rouge, bacon dinde, fromage raclette",
        "justification_en": "Bacon + mango + raclette — complex like your feelings 🧀",
        "justification_fr": "Bacon + mangue + raclette — complexe comme tes émotions 🧀",
        "science_en":       "Umami + fat + sweet engages multiple taste receptors simultaneously — maximum distraction.",
        "science_fr":       "Umami + gras + sucré engage plusieurs récepteurs gustatifs — distraction maximale.",
        "moods":            ["angry", "happy"],
    },
    {
        "nom":              "Boursin",
        "categorie_en":     "Sandwich",
        "categorie_fr":     "Sandwich",
        "prix":             65,
        "emoji":            "🧅",
        "photo":            ph("boursin.jpg",     "https://images.unsplash.com/photo-1528736235302-52922df5c122?w=600&q=80"),
        "ingredients":      "Kebab grillé, sauce pitta, salade, tomate, oignon rouge, boursin",
        "justification_en": "Boursin sauce = creamy calm in every bite 🧅",
        "justification_fr": "Sauce boursin = calme crémeux à chaque bouchée 🧅",
        "science_en":       "Creamy textures reduce stress response. Fat + herbs = natural anxiolytic effect.",
        "science_fr":       "Les textures crémeuses réduisent la réponse au stress. Gras + herbes = effet anxiolytique naturel.",
        "moods":            ["stressed", "neutral", "sad"],
    },
    {
        "nom":              "Orientale",
        "categorie_en":     "Sandwich",
        "categorie_fr":     "Sandwich",
        "prix":             69,
        "emoji":            "💪",
        "photo":            ph("orientale_sandwich.jpg", "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=600&q=80"),
        "ingredients":      "Kebab, merguez, sauce Algérienne, salade, tomate, oignon rouge, poivrons, cheddar",
        "justification_en": "Merguez + algerian sauce — bold and unapologetic 💪",
        "justification_fr": "Merguez + algérienne — audacieux et sans excuse 💪",
        "science_en":       "Complex intense flavours demand total sensory attention — redirecting anger toward pleasure.",
        "science_fr":       "Les saveurs intenses exigent une attention sensorielle totale — redirigeant la colère vers le plaisir.",
        "moods":            ["angry", "happy", "excited"],
    },
    {
        "nom":              "Merguez",
        "categorie_en":     "Sandwich",
        "categorie_fr":     "Sandwich",
        "prix":             55,
        "emoji":            "🌭",
        "photo":            ph("merguez_sandwich.jpg", "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80"),
        "ingredients":      "2 Merguez, sauce au choix, oignons grillés",
        "justification_en": "Keep it real, keep it simple 🌭",
        "justification_fr": "Simple et efficace 🌭",
        "science_en":       "Protein-dense meals stabilise blood sugar and mood. Grilled onions add sweetness that calms.",
        "science_fr":       "Les repas riches en protéines stabilisent la glycémie et l'humeur.",
        "moods":            ["neutral", "stressed", "angry"],
    },
 
    # ══════════════════════════════════════════════════════════════
    # LES BOWLS
    # ══════════════════════════════════════════════════════════════
 
    {
        "nom":              "Chèvre Miel Bowl",
        "categorie_en":     "Bowl",
        "categorie_fr":     "Bowl",
        "prix":             75,
        "emoji":            "🍯",
        "photo":            ph("chevre_miel_bowl.jpg", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80"),
        "ingredients":      "Kebab grillé, fromage, sauce sucrée, salade, tomate, oignon, chou rouge, chèvre miel, coriandre, sauce fromagère, tomate cerise, maïs",
        "justification_en": "Sweet + salty contrast — your happy brain LOVES this 🍯",
        "justification_fr": "Contraste sucré-salé — ton cerveau heureux adore ça 🍯",
        "science_en":       "Contrasting flavours in a bowl stimulate multiple dopamine pathways simultaneously.",
        "science_fr":       "Les contrastes de saveurs stimulent plusieurs voies dopaminergiques simultanément.",
        "moods":            ["happy", "neutral", "excited"],
    },
    {
        "nom":              "Fuego Bowl",
        "categorie_en":     "Bowl",
        "categorie_fr":     "Bowl",
        "prix":             69,
        "emoji":            "🌶️",
        "photo":            ph("fuego_bowl.jpg",  "https://images.unsplash.com/photo-1606851091851-e8c8c0fca5ba?w=600&q=80"),
        "ingredients":      "Kebab grillé, sauce spicy, sauce cheddar, salade, tomate, oignon, chou rouge, jalapeños, coriandre, tomate cerise, maïs",
        "justification_en": "Jalapeños + spicy sauce — channel that fire 🌶️",
        "justification_fr": "Jalapeños + sauce spicy — canalise cette énergie 🌶️",
        "science_en":       "Capsaicin triggers an endorphin rush — same mechanism as exercise. Anger → spice → euphoria.",
        "science_fr":       "La capsaïcine déclenche une libération d'endorphines. Colère → épice → euphorie.",
        "moods":            ["angry", "excited"],
    },
    {
        "nom":              "Oriental Bowl",
        "categorie_en":     "Bowl",
        "categorie_fr":     "Bowl",
        "prix":             75,
        "emoji":            "💪",
        "photo":            ph("oriental_bowl.jpg", "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=600&q=80"),
        "ingredients":      "Kebab grillé, merguez, sauce Algérienne, salade, tomate, oignon rouge, sauce fromagère, tomate cerise, maïs",
        "justification_en": "Merguez + algerian sauce — bold flavours for a bold mood 💪",
        "justification_fr": "Merguez + sauce algérienne — saveurs audacieuses pour humeur audacieuse 💪",
        "science_en":       "High-protein + spiced meals boost norepinephrine — natural energy and mood amplifier.",
        "science_fr":       "Les repas riches en protéines épicées boostent la norépinéphrine — énergie et humeur naturelles.",
        "moods":            ["angry", "happy", "excited"],
    },
    {
        "nom":              "Grec Bowl",
        "categorie_en":     "Bowl",
        "categorie_fr":     "Bowl",
        "prix":             65,
        "emoji":            "🥙",
        "photo":            ph("grec_bowl.jpg",   "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80"),
        "ingredients":      "Kebab grillé, fromage, sauce blanche, salade, tomate, oignon rouge, tomate cerise, maïs",
        "justification_en": "Balanced and reliable — solid safe bet 🥙",
        "justification_fr": "Équilibré et fiable — valeur sûre absolue 🥙",
        "science_en":       "Balanced macros maintain stable blood sugar, keeping you in optimal cognitive state.",
        "science_fr":       "Les macros équilibrées maintiennent une glycémie stable — état cognitif optimal.",
        "moods":            ["neutral", "stressed"],
    },
 
    # ══════════════════════════════════════════════════════════════
    # LES GRATINS
    # ══════════════════════════════════════════════════════════════
 
    {
        "nom":              "Gratin Classique",
        "categorie_en":     "Gratin",
        "categorie_fr":     "Gratin",
        "prix":             65,
        "emoji":            "🥔",
        "photo":            ph("gratin_classique.jpg", "https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a?w=600&q=80"),
        "ingredients":      "Viande de kebab, pomme de terre, mozza, oignon rouge",
        "justification_en": "Warm, cozy, no drama — exactly what you need 🥔",
        "justification_fr": "Chaud, cosy, sans prise de tête — exactement ce qu'il te faut 🥔",
        "science_en":       "Warm carb-rich meals activate the parasympathetic 'rest & digest' system. Calm in a dish.",
        "science_fr":       "Les repas chauds et riches en glucides activent le système parasympathique. Calme garanti.",
        "moods":            ["sad", "stressed", "neutral"],
    },
    {
        "nom":              "Gratin Savoyard",
        "categorie_en":     "Gratin",
        "categorie_fr":     "Gratin",
        "prix":             75,
        "emoji":            "🧀",
        "photo":            ph("gratin_savoyard.jpg", "https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a?w=600&q=80"),
        "ingredients":      "Pomme de terre, Kebab, Chèvre miel, mozza, oignon rouge",
        "justification_en": "Warm comfort food hits different when you're sad 🧀",
        "justification_fr": "La comfort food chaude touche autrement quand tu es triste 🧀",
        "science_en":       "Cheese + potato = max serotonin precursors. The ultimate emotional regulation dish.",
        "science_fr":       "Fromage + pomme de terre = précurseurs de sérotonine maximaux.",
        "moods":            ["sad", "stressed"],
    },
    {
        "nom":              "Gratin Raclette",
        "categorie_en":     "Gratin",
        "categorie_fr":     "Gratin",
        "prix":             75,
        "emoji":            "🫕",
        "photo":            ph("gratin_raclette.jpg", "https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a?w=600&q=80"),
        "ingredients":      "Pomme de terre, Kebab, oignon rouge, mozza, fromage raclette",
        "justification_en": "Raclette on everything = instant happiness 🫕",
        "justification_fr": "Raclette sur tout = bonheur instantané 🫕",
        "science_en":       "Melted cheese triggers a primal comfort response. Warm + melty = maximum serotonin boost.",
        "science_fr":       "Le fromage fondu déclenche une réponse de confort primaire. Chaud + fondant = sérotonine max.",
        "moods":            ["sad", "happy", "neutral"],
    },
    {
        "nom":              "Gratin Merguez",
        "categorie_en":     "Gratin",
        "categorie_fr":     "Gratin",
        "prix":             69,
        "emoji":            "🌭",
        "photo":            ph("gratin_merguez.jpg", "https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a?w=600&q=80"),
        "ingredients":      "Pomme de terre, merguez, oignon rouge, poivrons, mozza",
        "justification_en": "Spiced merguez + potato = fuel for the fire inside 🌭",
        "justification_fr": "Merguez épicée + pomme de terre = carburant pour le feu intérieur 🌭",
        "science_en":       "Spiced protein on carbs = sustained energy release + endorphin hit from capsaicin.",
        "science_fr":       "Protéines épicées sur glucides = libération d'énergie prolongée + endorphines.",
        "moods":            ["angry", "stressed", "neutral"],
    },
 
    # ══════════════════════════════════════════════════════════════
    # LES CRÊPES
    # ══════════════════════════════════════════════════════════════
 
    {
        "nom":              "Crêpe Nutella",
        "categorie_en":     "Crêpe",
        "categorie_fr":     "Crêpe",
        "prix":             25,
        "emoji":            "🍫",
        "photo":            ph("crepe_nutella.jpg", "https://images.unsplash.com/photo-1519676867240-f03562e64548?w=600&q=80"),
        "ingredients":      "Farine maison, œufs frais, lait, Nutella",
        "justification_en": "Classic comfort, no questions asked 🍫",
        "justification_fr": "Réconfort classique, aucune question posée 🍫",
        "science_en":       "Chocolate triggers phenylethylamine + theobromine release — the mood elevation combo.",
        "science_fr":       "Le chocolat déclenche la phényléthylamine + la théobromine — le duo élévateur d'humeur.",
        "moods":            ["sad", "neutral"],
    },
    {
        "nom":              "Crêpe Nutella Banane",
        "categorie_en":     "Crêpe",
        "categorie_fr":     "Crêpe",
        "prix":             30,
        "emoji":            "🍌",
        "photo":            ph("crepe_nutella_banane.jpg", "https://images.unsplash.com/photo-1519676867240-f03562e64548?w=600&q=80"),
        "ingredients":      "Farine maison, œufs frais, lait, Nutella, banane fraîche tranchée",
        "justification_en": "Warm + sweet = instant mood boost 🍌",
        "justification_fr": "Chaud + sucré = boost d'humeur instantané 🍌",
        "science_en":       "Serotonin via banana tryptophan + sugar spike = biological comfort mechanism.",
        "science_fr":       "Sérotonine via le tryptophane de la banane + pic de sucre = mécanisme de confort biologique.",
        "moods":            ["sad", "neutral", "happy"],
    },
    {
        "nom":              "Crêpe Oréo",
        "categorie_en":     "Crêpe",
        "categorie_fr":     "Crêpe",
        "prix":             35,
        "emoji":            "🖤",
        "photo":            ph("crepe_oreo.jpg",  "https://images.unsplash.com/photo-1519676867240-f03562e64548?w=600&q=80"),
        "ingredients":      "Farine maison, œufs frais, lait, Nutella, biscuits Oréo écrasés",
        "justification_en": "Crunch therapy — stress has no chance 🖤",
        "justification_fr": "Thérapie par le croquant — le stress n'a aucune chance 🖤",
        "science_en":       "Crunchy textures provide oral sensory stimulation that relieves tension. Real stress buster.",
        "science_fr":       "Les textures croquantes fournissent une stimulation sensorielle qui soulage la tension.",
        "moods":            ["stressed", "sad", "neutral"],
    },
    {
        "nom":              "Crêpe Speculoos",
        "categorie_en":     "Crêpe",
        "categorie_fr":     "Crêpe",
        "prix":             35,
        "emoji":            "🍪",
        "photo":            ph("crepe_speculoos.jpg", "https://images.unsplash.com/photo-1519676867240-f03562e64548?w=600&q=80"),
        "ingredients":      "Farine maison, œufs frais, lait, pâte de Speculoos belge, beurre doux",
        "justification_en": "Not too basic, not too wild — just right 🍪",
        "justification_fr": "Ni trop basique, ni trop wild — just right 🍪",
        "science_en":       "Cinnamon in Speculoos mildly elevates heart rate and mood without overstimulation.",
        "science_fr":       "La cannelle dans le Speculoos élève légèrement le rythme cardiaque et l'humeur.",
        "moods":            ["stressed", "neutral", "sad"],
    },
    {
        "nom":              "Crêpe Kinder Bueno",
        "categorie_en":     "Crêpe",
        "categorie_fr":     "Crêpe",
        "prix":             39,
        "emoji":            "🤎",
        "photo":            ph("crepe_kinder.jpg", "https://images.unsplash.com/photo-1519676867240-f03562e64548?w=600&q=80"),
        "ingredients":      "Farine maison, œufs frais, lait, Nutella, Kinder Bueno",
        "justification_en": "Hazelnut + wafer = nostalgia on a plate 🤎",
        "justification_fr": "Noisette + gaufrette = nostalgie dans une assiette 🤎",
        "science_en":       "Nostalgic foods reduce anxiety by 40% — Kinder is pure childhood comfort.",
        "science_fr":       "Les aliments nostalgiques réduisent l'anxiété de 40% — Kinder, c'est l'enfance.",
        "moods":            ["sad", "happy", "excited"],
    },
    {
        "nom":              "Crêpe KitKat",
        "categorie_en":     "Crêpe",
        "categorie_fr":     "Crêpe",
        "prix":             35,
        "emoji":            "🍫",
        "photo":            ph("crepe_kitkat.jpg", "https://images.unsplash.com/photo-1519676867240-f03562e64548?w=600&q=80"),
        "ingredients":      "Farine maison, œufs frais, lait, Nutella, KitKat",
        "justification_en": "Have a break. No literally, have a KitKat break 🍫",
        "justification_fr": "Fais une pause. Genre vraiment une pause KitKat 🍫",
        "science_en":       "Dark chocolate pieces trigger cocoa-derived mood elevation. Stress literally breaks apart.",
        "science_fr":       "Les morceaux de chocolat déclenchent une élévation d'humeur. Le stress se brise littéralement.",
        "moods":            ["stressed", "neutral"],
    },
    {
        "nom":              "Crêpe Pistache",
        "categorie_en":     "Crêpe",
        "categorie_fr":     "Crêpe",
        "prix":             39,
        "emoji":            "💚",
        "photo":            ph("crepe_pistache.jpg", "https://images.unsplash.com/photo-1519676867240-f03562e64548?w=600&q=80"),
        "ingredients":      "Farine maison, œufs frais, lait, pâte de pistache, beurre doux",
        "justification_en": "Main character energy — pistachio is having a moment 💚",
        "justification_fr": "Énergie personnage principal — la pistache est en train de tout déchirer 💚",
        "science_en":       "Pistachios contain antioxidants + B6 which directly support serotonin synthesis.",
        "science_fr":       "Les pistaches contiennent des antioxydants + B6 qui soutiennent la synthèse de sérotonine.",
        "moods":            ["excited", "happy", "neutral"],
    },
 
    # ══════════════════════════════════════════════════════════════
    # LES GAUFRES
    # ══════════════════════════════════════════════════════════════
 
    {
        "nom":              "Gaufre Nutella",
        "categorie_en":     "Waffle",
        "categorie_fr":     "Gaufre",
        "prix":             25,
        "emoji":            "🧇",
        "photo":            ph("gaufre_nutella.jpg", "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=600&q=80"),
        "ingredients":      "Pâte gaufre maison, Nutella, sucre glace",
        "justification_en": "Crispy outside, warm inside — like a hug 🧇",
        "justification_fr": "Croustillant dehors, chaud dedans — comme un câlin 🧇",
        "science_en":       "Warm + crispy texture contrast activates multiple reward centers simultaneously.",
        "science_fr":       "Le contraste de textures active plusieurs centres de récompense simultanément.",
        "moods":            ["sad", "neutral"],
    },
    {
        "nom":              "Gaufre Nutella Banane",
        "categorie_en":     "Waffle",
        "categorie_fr":     "Gaufre",
        "prix":             30,
        "emoji":            "🍌",
        "photo":            ph("gaufre_nutella_banane.jpg", "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=600&q=80"),
        "ingredients":      "Pâte gaufre maison, Nutella, banane fraîche, sucre glace",
        "justification_en": "Sweet celebration for your energy 🍌",
        "justification_fr": "Célébration sucrée pour ton énergie 🍌",
        "science_en":       "Banana serotonin precursors + waffle carbs = sustained happy hormone boost.",
        "science_fr":       "Précurseurs de sérotonine de la banane + glucides = boost d'hormones du bonheur.",
        "moods":            ["happy", "sad", "excited"],
    },
    {
        "nom":              "Gaufre Oréo",
        "categorie_en":     "Waffle",
        "categorie_fr":     "Gaufre",
        "prix":             35,
        "emoji":            "🖤",
        "photo":            ph("gaufre_oreo.jpg",  "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=600&q=80"),
        "ingredients":      "Pâte gaufre maison, Nutella, Oréo écrasé, chantilly",
        "justification_en": "Dark crunch on warm waffle = stress relief mode 🖤",
        "justification_fr": "Croquant noir sur gaufre chaude = mode anti-stress 🖤",
        "science_en":       "Crunching + sweetness = dual sensory stress relief pathway.",
        "science_fr":       "Croquer + sucré = double voie de soulagement du stress sensoriel.",
        "moods":            ["stressed", "neutral"],
    },
    {
        "nom":              "Gaufre Speculoos",
        "categorie_en":     "Waffle",
        "categorie_fr":     "Gaufre",
        "prix":             35,
        "emoji":            "🍪",
        "photo":            ph("gaufre_speculoos.jpg", "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=600&q=80"),
        "ingredients":      "Pâte gaufre maison, pâte de Speculoos, sucre glace",
        "justification_en": "Caramel-spiced warmth — autumn in a waffle 🍪",
        "justification_fr": "Chaleur épicée caramel — l'automne dans une gaufre 🍪",
        "science_en":       "Cinnamon aroma reduces anxiety and improves mood within minutes of exposure.",
        "science_fr":       "L'arôme de cannelle réduit l'anxiété et améliore l'humeur en quelques minutes.",
        "moods":            ["stressed", "sad", "neutral"],
    },
    {
        "nom":              "Gaufre Kinder Bueno",
        "categorie_en":     "Waffle",
        "categorie_fr":     "Gaufre",
        "prix":             39,
        "emoji":            "🤎",
        "photo":            ph("gaufre_kinder.jpg", "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=600&q=80"),
        "ingredients":      "Pâte gaufre maison, Nutella, Kinder Bueno, chantilly",
        "justification_en": "Nostalgia + crunch = the emotional reset button 🤎",
        "justification_fr": "Nostalgie + croquant = le bouton de réinitialisation émotionnelle 🤎",
        "science_en":       "Nostalgic foods reduce perceived stress by activating childhood comfort memories.",
        "science_fr":       "Les aliments nostalgiques réduisent le stress perçu en activant les souvenirs de confort d'enfance.",
        "moods":            ["sad", "happy", "stressed"],
    },
    {
        "nom":              "Gaufre KitKat",
        "categorie_en":     "Waffle",
        "categorie_fr":     "Gaufre",
        "prix":             35,
        "emoji":            "🍫",
        "photo":            ph("gaufre_kitkat.jpg", "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=600&q=80"),
        "ingredients":      "Pâte gaufre maison, Nutella, KitKat émietté, chantilly",
        "justification_en": "Break the tension, literally 🍫",
        "justification_fr": "Casse la tension, littéralement 🍫",
        "science_en":       "Biting through layers of waffle + KitKat = satisfying stress outlet.",
        "science_fr":       "Mordre dans les couches gaufre + KitKat = exutoire de stress satisfaisant.",
        "moods":            ["stressed", "angry"],
    },
    {
        "nom":              "Gaufre Pistache",
        "categorie_en":     "Waffle",
        "categorie_fr":     "Gaufre",
        "prix":             39,
        "emoji":            "💚",
        "photo":            ph("gaufre_pistache.jpg", "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=600&q=80"),
        "ingredients":      "Pâte gaufre maison, crème pistache, sucre glace, pistaches concassées",
        "justification_en": "Trendy AND delicious. You have taste 💚",
        "justification_fr": "Tendance ET délicieux. T'as du goût 💚",
        "science_en":       "Green foods psychologically signal health + energy. Pistachios boost B6 for mood.",
        "science_fr":       "Les aliments verts signalent psychologiquement la santé. La pistache booste la B6 pour l'humeur.",
        "moods":            ["excited", "happy"],
    },
 
    # ══════════════════════════════════════════════════════════════
    # MILKSHAKES (tous à 39dhs, ingrédient au choix)
    # ══════════════════════════════════════════════════════════════
 
    {
        "nom":              "Milkshake Oréo",
        "categorie_en":     "Milkshake",
        "categorie_fr":     "Milkshake",
        "prix":             39,
        "emoji":            "🖤",
        "photo":            ph("milkshake_oreo.jpg", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&q=80"),
        "ingredients":      "Lait entier, glace vanille, Oréo, chantilly maison",
        "justification_en": "Dark + creamy — moody milkshake for a moody moment 🖤",
        "justification_fr": "Sombre + crémeux — milkshake moody pour un moment moody 🖤",
        "science_en":       "Cold + creamy + chocolate = triple sensory comfort response.",
        "science_fr":       "Froid + crémeux + chocolat = triple réponse de confort sensoriel.",
        "moods":            ["sad", "stressed", "neutral"],
    },
    {
        "nom":              "Milkshake M&M's",
        "categorie_en":     "Milkshake",
        "categorie_fr":     "Milkshake",
        "prix":             39,
        "emoji":            "🍫",
        "photo":            ph("milkshake_mms.jpg", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&q=80"),
        "ingredients":      "Lait entier, glace vanille, M&M's colorés, chantilly maison",
        "justification_en": "Zero-guilt, max fun mode activated 🍫",
        "justification_fr": "Mode zéro culpabilité, plaisir maximal activé 🍫",
        "science_en":       "Sugar + fat = maximum dopamine release. Literally the scientifically optimal reward.",
        "science_fr":       "Sucre + gras = libération maximale de dopamine. La récompense scientifiquement optimale.",
        "moods":            ["happy", "sad", "excited"],
    },
    {
        "nom":              "Milkshake Kinder Bueno",
        "categorie_en":     "Milkshake",
        "categorie_fr":     "Milkshake",
        "prix":             39,
        "emoji":            "🤎",
        "photo":            ph("milkshake_kinder.jpg", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&q=80"),
        "ingredients":      "Lait entier, glace vanille, Kinder Bueno, chantilly maison",
        "justification_en": "Childhood nostalgia in a cup 🤎",
        "justification_fr": "Nostalgie de l'enfance dans un verre 🤎",
        "science_en":       "Nostalgic flavour profiles reduce cortisol by engaging positive autobiographical memory.",
        "science_fr":       "Les profils de saveurs nostalgiques réduisent le cortisol en activant la mémoire autobiographique positive.",
        "moods":            ["sad", "happy"],
    },
    {
        "nom":              "Milkshake Speculoos",
        "categorie_en":     "Milkshake",
        "categorie_fr":     "Milkshake",
        "prix":             39,
        "emoji":            "🍪",
        "photo":            ph("milkshake_speculoos.jpg", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&q=80"),
        "ingredients":      "Lait entier, glace vanille, pâte Speculoos, chantilly maison",
        "justification_en": "Cinnamon-spiced calm in a glass 🍪",
        "justification_fr": "Calme épicé à la cannelle dans un verre 🍪",
        "science_en":       "Cinnamon reduces blood glucose spikes — prevents stress-inducing sugar crashes.",
        "science_fr":       "La cannelle réduit les pics de glycémie — évite les crashes de sucre stressants.",
        "moods":            ["stressed", "neutral", "sad"],
    },
    {
        "nom":              "Milkshake Banane",
        "categorie_en":     "Milkshake",
        "categorie_fr":     "Milkshake",
        "prix":             39,
        "emoji":            "🍌",
        "photo":            ph("milkshake_banane.jpg", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&q=80"),
        "ingredients":      "Lait entier, glace vanille, banane fraîche, chantilly maison",
        "justification_en": "Natural serotonin boost in a glass 🍌",
        "justification_fr": "Boost de sérotonine naturelle dans un verre 🍌",
        "science_en":       "Banana tryptophan + milk casein = optimal serotonin synthesis. Proven anti-sadness combo.",
        "science_fr":       "Tryptophane de banane + caséine du lait = synthèse de sérotonine optimale.",
        "moods":            ["sad", "neutral", "happy"],
    },
    {
        "nom":              "Milkshake Nutella",
        "categorie_en":     "Milkshake",
        "categorie_fr":     "Milkshake",
        "prix":             39,
        "emoji":            "🍫",
        "photo":            ph("milkshake_nutella.jpg", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&q=80"),
        "ingredients":      "Lait entier, glace vanille, Nutella, chantilly maison",
        "justification_en": "The classic. Always the right call 🍫",
        "justification_fr": "Le classique. Toujours le bon choix 🍫",
        "science_en":       "Hazelnut + cocoa stimulate both opioid and dopamine reward systems simultaneously.",
        "science_fr":       "Noisette + cacao stimulent simultanément les systèmes de récompense opioïde et dopaminergique.",
        "moods":            ["sad", "neutral", "happy"],
    },
    {
        "nom":              "Milkshake Mangue",
        "categorie_en":     "Milkshake",
        "categorie_fr":     "Milkshake",
        "prix":             39,
        "emoji":            "🥭",
        "photo":            ph("milkshake_mangue.jpg", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&q=80"),
        "ingredients":      "Lait entier, glace vanille, mangue fraîche, chantilly maison",
        "justification_en": "Tropical escape mode on 🥭",
        "justification_fr": "Mode évasion tropicale activé 🥭",
        "science_en":       "Mango contains linalool which has proven anxiety-reducing effects.",
        "science_fr":       "La mangue contient du linalol qui a des effets prouvés de réduction de l'anxiété.",
        "moods":            ["stressed", "happy", "excited"],
    },
    {
        "nom":              "Milkshake Fraise",
        "categorie_en":     "Milkshake",
        "categorie_fr":     "Milkshake",
        "prix":             39,
        "emoji":            "🍓",
        "photo":            ph("milkshake_fraise.jpg", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&q=80"),
        "ingredients":      "Lait entier, glace vanille, fraise fraîche, chantilly maison",
        "justification_en": "Pink and powerful 🍓",
        "justification_fr": "Rose et puissant 🍓",
        "science_en":       "Strawberry red pigments signal joy. Folic acid in strawberries supports dopamine production.",
        "science_fr":       "Les pigments rouges de la fraise signalent la joie. L'acide folique soutient la production de dopamine.",
        "moods":            ["happy", "excited", "neutral"],
    },
    {
        "nom":              "Milkshake Vanille",
        "categorie_en":     "Milkshake",
        "categorie_fr":     "Milkshake",
        "prix":             39,
        "emoji":            "🍦",
        "photo":            ph("milkshake_vanille.jpg", "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=600&q=80"),
        "ingredients":      "Lait entier, glace vanille premium, arôme naturel, chantilly",
        "justification_en": "Soft & creamy — fast emotional relief 🍦",
        "justification_fr": "Doux & onctueux — soulagement émotionnel rapide 🍦",
        "science_en":       "Vanilla scent reduces anxiety markers by 65%. Cold + sweet = immediate sensory comfort.",
        "science_fr":       "L'arôme vanille réduit les marqueurs d'anxiété de 65%. Froid + sucré = confort immédiat.",
        "moods":            ["sad", "stressed", "neutral"],
    },
 
    # ══════════════════════════════════════════════════════════════
    # SMOOTHIES (35dhs)
    # ══════════════════════════════════════════════════════════════
 
    {
        "nom":              "Smoothie Banane-Mangue",
        "categorie_en":     "Smoothie",
        "categorie_fr":     "Smoothie",
        "prix":             35,
        "emoji":            "🥭",
        "photo":            ph("smoothie_banane_mangue.jpg", "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600&q=80"),
        "ingredients":      "Banane fraîche, mangue fraîche, lait, glaçons, sucre de canne",
        "justification_en": "Tropical + comforting — easy yes 🥭",
        "justification_fr": "Tropical + rassurant — facile à dire oui 🥭",
        "science_en":       "Tropical fruits raise serotonin via tryptophan conversion. Natural mood regulation.",
        "science_fr":       "Les fruits tropicaux élèvent la sérotonine via la conversion du tryptophane.",
        "moods":            ["neutral", "happy", "sad"],
    },
    {
        "nom":              "Smoothie Fraise",
        "categorie_en":     "Smoothie",
        "categorie_fr":     "Smoothie",
        "prix":             35,
        "emoji":            "🍓",
        "photo":            ph("smoothie_fraise.jpg", "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600&q=80"),
        "ingredients":      "Fraise fraîche, lait, glaçons, sucre de canne",
        "justification_en": "Fresh, bright, energising 🍓",
        "justification_fr": "Frais, vif, énergisant 🍓",
        "science_en":       "Vitamin C in strawberries reduces cortisol levels. Natural stress buffer.",
        "science_fr":       "La vitamine C des fraises réduit les niveaux de cortisol. Tampon naturel anti-stress.",
        "moods":            ["happy", "excited", "stressed"],
    },
    {
        "nom":              "Smoothie Avocat",
        "categorie_en":     "Smoothie",
        "categorie_fr":     "Smoothie",
        "prix":             35,
        "emoji":            "🥑",
        "photo":            ph("smoothie_avocat.jpg", "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=600&q=80"),
        "ingredients":      "Avocat frais, lait, glaçons, miel, sucre de canne",
        "justification_en": "Creamy wellness in a cup 🥑",
        "justification_fr": "Bien-être crémeux dans un verre 🥑",
        "science_en":       "Avocado healthy fats support myelin in the brain — literally feeds your calmness.",
        "science_fr":       "Les graisses saines de l'avocat soutiennent la myéline cérébrale — nourrit littéralement ton calme.",
        "moods":            ["stressed", "neutral"],
    },
 
    # ══════════════════════════════════════════════════════════════
    # MOJITOS (39dhs) + L'OBAYOLI Redbull (49dhs)
    # ══════════════════════════════════════════════════════════════
 
    {
        "nom":              "Mojito Fraise",
        "categorie_en":     "Drink",
        "categorie_fr":     "Boisson",
        "prix":             39,
        "emoji":            "🍓",
        "photo":            ph("mojito_fraise.jpg", "https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=600&q=80"),
        "ingredients":      "Fraise fraîche, menthe, citron, sucre de canne, eau gazeuse",
        "justification_en": "Colourful & festive — matches your energy 🍓",
        "justification_fr": "Coloré & festif — à la hauteur de ton énergie 🍓",
        "science_en":       "Red visual signals reinforce positive emotional states. Proven excitement amplifier.",
        "science_fr":       "Les signaux visuels rouges renforcent les états émotionnels positifs.",
        "moods":            ["happy", "excited", "neutral"],
    },
    {
        "nom":              "Mojito Passion",
        "categorie_en":     "Drink",
        "categorie_fr":     "Boisson",
        "prix":             39,
        "emoji":            "💛",
        "photo":            ph("mojito_passion.jpg", "https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=600&q=80"),
        "ingredients":      "Fruit de la passion, menthe, citron, sucre de canne, eau gazeuse",
        "justification_en": "Exotic & tangy — like a mood awakening 💛",
        "justification_fr": "Exotique & acidulé — comme un réveil d'humeur 💛",
        "science_en":       "Citric acid triggers salivation and alertness. Passion fruit aroma boosts positive arousal.",
        "science_fr":       "L'acide citrique déclenche l'éveil. L'arôme du fruit de la passion stimule l'éveil positif.",
        "moods":            ["neutral", "excited", "happy"],
    },
    {
        "nom":              "Mojito Grenadine",
        "categorie_en":     "Drink",
        "categorie_fr":     "Boisson",
        "prix":             39,
        "emoji":            "❤️",
        "photo":            ph("mojito_grenadine.jpg", "https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=600&q=80"),
        "ingredients":      "Grenadine, menthe, citron, sucre de canne, eau gazeuse",
        "justification_en": "Sweet & bold — matches your passion 🍹",
        "justification_fr": "Sucré & audacieux — à la hauteur de ta passion 🍹",
        "science_en":       "Deep red colour psychologically signals intensity and passion — reinforces excited state.",
        "science_fr":       "La couleur rouge profond signale psychologiquement l'intensité — renforce l'état d'excitation.",
        "moods":            ["excited", "happy", "angry"],
    },
    {
        "nom":              "Mojito Blueberry",
        "categorie_en":     "Drink",
        "categorie_fr":     "Boisson",
        "prix":             39,
        "emoji":            "🫐",
        "photo":            ph("mojito_blueberry.jpg", "https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=600&q=80"),
        "ingredients":      "Myrtilles fraîches, menthe, citron, sucre de canne, eau gazeuse",
        "justification_en": "Antioxidants meet good vibes 🫐",
        "justification_fr": "Antioxydants rencontrent les bonnes vibes 🫐",
        "science_en":       "Blueberry anthocyanins cross the blood-brain barrier and directly reduce inflammation-based mood dips.",
        "science_fr":       "Les anthocyanes de myrtille traversent la barrière hémato-encéphalique et réduisent directement les baisses d'humeur.",
        "moods":            ["sad", "neutral", "stressed"],
    },
    {
        "nom":              "Mojito Classic",
        "categorie_en":     "Drink",
        "categorie_fr":     "Boisson",
        "prix":             39,
        "emoji":            "🍃",
        "photo":            ph("mojito_classic.jpg", "https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=600&q=80"),
        "ingredients":      "Menthe fraîche, citron, sucre de canne, eau gazeuse",
        "justification_en": "The OG. Never fails 🍃",
        "justification_fr": "L'original. Ne déçoit jamais 🍃",
        "science_en":       "Menthol activates TRPM8 receptors creating a cooling sensation that lowers perceived stress.",
        "science_fr":       "Le menthol active les récepteurs TRPM8 créant une sensation rafraîchissante qui réduit le stress perçu.",
        "moods":            ["stressed", "neutral", "happy"],
    },
    {
        "nom":              "L'Obayoli Redbull",
        "categorie_en":     "Drink",
        "categorie_fr":     "Boisson",
        "prix":             49,
        "emoji":            "🐂",
        "photo":            ph("obayoli_redbull.jpg", "https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=600&q=80"),
        "ingredients":      "Redbull, menthe fraîche, citron, sucre de canne",
        "justification_en": "Redbull gives you wings. OBAYOLI gives you the vibe 🐂",
        "justification_fr": "Redbull te donne des ailes. OBAYOLI te donne la vibe 🐂",
        "science_en":       "Taurine + caffeine = maximum alertness boost. For when you need to go full beast mode.",
        "science_fr":       "Taurine + caféine = boost d'alertness maximal. Pour quand tu dois tout donner.",
        "moods":            ["excited", "angry", "happy"],
    },
 
    # ══════════════════════════════════════════════════════════════
    # TIRAMISU
    # ══════════════════════════════════════════════════════════════
 
    {
        "nom":              "Tiramisu",
        "categorie_en":     "Dessert",
        "categorie_fr":     "Dessert",
        "prix":             29,
        "emoji":            "☕",
        "photo":            ph("tiramisu.jpg",    "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=600&q=80"),
        "ingredients":      "Mascarpone, café espresso, biscuit savourade, cacao en poudre",
        "justification_en": "Soft & creamy — a little Italian hug ☕",
        "justification_fr": "Doux, crémeux — un petit câlin italien ☕",
        "science_en":       "Coffee + cocoa = stimulant + phenylethylamine (the love molecule). Real mood booster.",
        "science_fr":       "Café + cacao = stimulant + phényléthylamine (la molécule de l'amour). Vrai boosteur d'humeur.",
        "moods":            ["sad", "neutral", "stressed"],
    },
 
    # ══════════════════════════════════════════════════════════════
    # JUS FRAIS
    # ══════════════════════════════════════════════════════════════
 
    {
        "nom":              "Jus Frais Maison",
        "categorie_en":     "Juice",
        "categorie_fr":     "Jus",
        "prix":             25,
        "emoji":            "🍊",
        "photo":            ph("jus_frais.jpg",   "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&q=80"),
        "ingredients":      "Orange fraîche pressée, citron, menthe, gingembre",
        "justification_en": "Fresh energy boost — amplify that vibe 🍊",
        "justification_fr": "Boost d'énergie fraîche — amplifier cette vibe 🍊",
        "science_en":       "Vitamin C + ginger = natural adrenaline amplifier. Enhances alertness and excitement.",
        "science_fr":       "Vitamine C + gingembre = amplificateur naturel d'adrénaline.",
        "moods":            ["excited", "happy", "neutral"],
    },
]
 
# ── Seed function ─────────────────────────────────────────────────────────────
def seed():
    collection = db.collection("plats")
 
    # Clear existing dishes
    print("🧹 Clearing existing /plats collection...")
    existing = collection.stream()
    deleted = 0
    for doc in existing:
        doc.reference.delete()
        deleted += 1
    print(f"   Deleted {deleted} existing documents.\n")
 
    print(f"🌱 Seeding {len(DISHES)} OBAYOLI dishes into Firestore /plats...\n")
 
    by_mood = {}
    for i, dish in enumerate(DISHES):
        ref = collection.document()
        ref.set(dish)
        moods_str = ", ".join(dish["moods"])
        cat = dish.get("categorie_fr", "?")
        print(f"  ✅ [{i+1:02d}/{len(DISHES)}] {dish['emoji']}  {dish['nom']:35s} {dish['prix']}dhs  [{cat}]  moods: [{moods_str}]")
 
        for m in dish["moods"]:
            by_mood.setdefault(m, []).append(dish["nom"])
 
    print(f"\n🎉 Done! {len(DISHES)} dishes seeded successfully.\n")
    print("📊 Dishes per mood:")
    for mood, names in sorted(by_mood.items()):
        print(f"   {mood:12s} → {len(names)} dishes")
 
    print("\n   Firebase /plats is ready. Restart your Flask app and go! 🚀")
    print("\n💡 Reminder: serve local photos from dish_sources/Plats/ via Flask:")
    print("   app.py → app.static_folder or a dedicated /static/dishes/ route.\n")
 
if __name__ == "__main__":
    seed()