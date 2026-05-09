"""
models/plat.py — Plat Model
Matches UML: -id, -nom, -categorie, -prix, -ingredients, -photo, -justification
"""
 
from dataclasses import dataclass, field
from typing import List
 
 
@dataclass
class Plat:
    id:            str = ""
    nom:           str = ""
    categorie:     str = ""
    prix:          float = 0.0
    ingredients:   List[str] = field(default_factory=list)
    photo:         str = ""
    justification: str = ""
    science:       str = ""
 
    # ── UML method ───────────────────────────────────────────────────────────
 
    def get_details(self) -> str:
        ing_str = ", ".join(self.ingredients) if self.ingredients else "N/A"
        return (
            f"{self.nom} ({self.categorie}) — {self.prix:.2f} dhs\n"
            f"Ingredients: {ing_str}\n"
            f"Why: {self.justification}\n"
            f"Science: {self.science}"
        )
 
    # ── Serialisation ────────────────────────────────────────────────────────
 
    def to_dict(self) -> dict:
        return {
            "id":            self.id,
            "nom":           self.nom,
            "categorie":     self.categorie,
            "prix":          self.prix,
            "ingredients":   self.ingredients,
            "photo":         self.photo,
            "justification": self.justification,
            "science":       self.science,
        }
 
    @classmethod
    def from_dict(cls, data: dict, doc_id: str = "") -> "Plat":
        """Build a Plat from a Firestore document dict."""
        # Normalize ingredients — Firestore may store as string or array
        ingredients = data.get("ingredients", [])
        if isinstance(ingredients, str):
            ingredients = [i.strip() for i in ingredients.split(",") if i.strip()]
 
        return cls(
            id=doc_id or data.get("id", ""),
            nom=data.get("nom", data.get("name", "")),
            categorie=data.get("categorie", data.get("category", "")),
            prix=float(data.get("prix", data.get("price", 0.0))),
            ingredients=ingredients,
            photo=data.get("photo", data.get("image", "")),
            justification=data.get("justification", data.get("why", "")),
            science=data.get("science", ""),
        )
 
    def __str__(self) -> str:
        return f"Plat({self.nom!r}, {self.prix} dhs)"