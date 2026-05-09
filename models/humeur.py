"""
models/humeur.py — Humeur Model
Matches UML: -type: String, -quote: String
"""

from dataclasses import dataclass, field
from typing import List, Optional
from config import config


@dataclass
class Humeur:
    type:  str = "neutral"   # one of config.SUPPORTED_MOODS
    quote: str = ""

    # ── UML methods ─────────────────────────────────────────────────────────

    def get_quote(self, lang: str = "en") -> str:
        """
        Return the personalised mood quote in the requested language.
        Falls back to the stored quote if lang key not found in config.
        """
        meta = config.MOOD_META.get(self.type, {})
        key  = f"quote_{lang}"
        return meta.get(key, self.quote or "")

    def get_plats_recommandes(self, firebase_service) -> List[dict]:
        """
        Delegate to FirebaseService to fetch dishes filtered by this mood.
        Returns a list of Plat-compatible dicts.
        """
        return firebase_service.get_dishes_by_mood(self.type)

    # ── Helpers ──────────────────────────────────────────────────────────────

    @property
    def emoji(self) -> str:
        return config.MOOD_META.get(self.type, {}).get("emoji", "😐")

    @property
    def color(self) -> str:
        return config.MOOD_META.get(self.type, {}).get("color", "#7B7F86")

    @property
    def bg(self) -> str:
        return config.MOOD_META.get(self.type, {}).get("bg", "#F4F4F5")

    def label(self, lang: str = "en") -> str:
        meta = config.MOOD_META.get(self.type, {})
        return meta.get(f"label_{lang}", self.type.capitalize())

    def is_valid(self) -> bool:
        return self.type in config.SUPPORTED_MOODS

    # ── Serialisation ────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {"type": self.type, "quote": self.quote}

    @classmethod
    def from_dict(cls, data: dict) -> "Humeur":
        return cls(
            type=data.get("type", "neutral"),
            quote=data.get("quote", ""),
        )

    def __str__(self) -> str:
        return f"Humeur({self.emoji} {self.type})"
