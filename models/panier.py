"""
models/panier.py — Panier (Cart) Model
Matches UML: -plats: List<Plat>, -total: float
"""

from dataclasses import dataclass, field
from typing import List

from models.plat import Plat


@dataclass
class Panier:
    plats: List[Plat] = field(default_factory=list)
    total: float = 0.0

    # ── UML methods ──────────────────────────────────────────────────────────

    def toggle_dish(self, plat: Plat) -> bool:
        """
        Add the dish if not in cart, remove it if already there.
        Returns True if dish was added, False if removed.
        Matches SD3 sequence diagram toggleDish(dish) call.
        """
        existing = next((p for p in self.plats if p.id == plat.id), None)
        if existing:
            self.plats.remove(existing)
            self._recalculate()
            return False   # removed
        else:
            self.plats.append(plat)
            self._recalculate()
            return True    # added

    def get_panier(self) -> List[Plat]:
        """Return current list of dishes in cart."""
        return self.plats

    def calculer_total(self) -> float:
        """Recompute and return cart total."""
        self._recalculate()
        return self.total

    def vider(self) -> None:
        """Empty the cart."""
        self.plats.clear()
        self.total = 0.0

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _recalculate(self) -> None:
        self.total = round(sum(p.prix for p in self.plats), 2)

    def contains(self, plat_id: str) -> bool:
        return any(p.id == plat_id for p in self.plats)

    def is_empty(self) -> bool:
        return len(self.plats) == 0

    def count(self) -> int:
        return len(self.plats)

    # ── Serialisation ────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "plats": [p.to_dict() for p in self.plats],
            "total": self.total,
        }

    @classmethod
    def from_session(cls, session_data: list) -> "Panier":
        """Rebuild Panier from the list stored in Flask session."""
        panier = cls()
        for item in (session_data or []):
            panier.plats.append(Plat.from_dict(item))
        panier._recalculate()
        return panier

    def to_session(self) -> list:
        """Serialise cart to a JSON-safe list for Flask session storage."""
        return [p.to_dict() for p in self.plats]

    def __str__(self) -> str:
        return f"Panier({self.count()} plats, {self.total} dhs)"
