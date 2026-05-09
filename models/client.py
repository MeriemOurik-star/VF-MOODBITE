"""
models/client.py — Client Model
Matches UML: -nom: String, -humeur: Humeur
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Client:
    nom: str = ""
    humeur: Optional[object] = field(default=None, repr=False)  # Humeur instance

    # ── UML methods ─────────────────────────────────────────────────────────

    def saisir_nom(self, nom: str) -> None:
        """Validate and set the client's name / pseudo."""
        nom = nom.strip()
        if not nom:
            raise ValueError("Name cannot be empty — entrez votre prénom !")
        if len(nom) > 50:
            raise ValueError("Name too long (max 50 chars).")
        self.nom = nom

    def choisir_mode(self, mode: str) -> str:
        """
        Choose mood-detection mode.
        Returns 'ia' or 'manuel' — anything else raises ValueError.
        """
        mode = mode.lower().strip()
        if mode not in ("ia", "manuel"):
            raise ValueError(f"Unknown mode '{mode}'. Use 'ia' or 'manuel'.")
        return mode

    def confirmer_commande(self) -> bool:
        """
        Gate: a commande can only be confirmed if the client has a name
        and a detected humeur.
        """
        return bool(self.nom and self.humeur)

    # ── Serialisation ────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "nom":    self.nom,
            "humeur": self.humeur.to_dict() if self.humeur else None,
        }

    @classmethod
    def from_session(cls, session: dict) -> "Client":
        """Reconstruct a lightweight Client from Flask session data."""
        from models.humeur import Humeur
        client = cls(nom=session.get("user_name", ""))
        humeur_data = session.get("humeur")
        if humeur_data:
            client.humeur = Humeur(
                type=humeur_data.get("type", "neutral"),
                quote=humeur_data.get("quote", ""),
            )
        return client

    def __str__(self) -> str:
        return f"Client(nom={self.nom!r}, humeur={self.humeur})"
