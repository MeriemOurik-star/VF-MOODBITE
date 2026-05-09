"""
models/face_scan.py — FaceScan Model
Matches UML: -statut: String, -progress: int
Server-side representation; actual detection runs in face_scan.js (client).
"""

from dataclasses import dataclass, field
from typing import Optional

from models.humeur import Humeur
from config import config


# All states the scan can be in (mirrors JS FSM)
SCAN_STATUTS = ["idle", "loading", "scanning", "success", "error"]


@dataclass
class FaceScan:
    statut:   str = "idle"    # idle | loading | scanning | success | error
    progress: int = 0         # 0 → 100

    # Detected result (populated after analyser_visage completes)
    _humeur_detectee: Optional[Humeur] = field(default=None, repr=False)
    _error_message:   str = field(default="", repr=False)

    # ── UML methods ──────────────────────────────────────────────────────────

    def lancer_detection(self) -> dict:
        """
        Initialise scan state — called when user clicks "Start Scan".
        Returns a config dict consumed by face_scan.js via /mood/start-scan.
        """
        self.statut   = "loading"
        self.progress = 0
        self._humeur_detectee = None
        self._error_message   = ""
        return self.to_dict()

    def analyser_visage(self, raw_result: dict) -> "FaceScan":
        """
        Process the result payload sent from face_scan.js
        after client-side face-api.js analysis completes.

        raw_result expected keys:
            mood       – detected mood string (e.g. 'happy')
            confidence – float 0-1
            progress   – int 0-100
            error      – optional error string
        """
        error = raw_result.get("error", "")
        if error:
            self.statut         = "error"
            self._error_message = error
            return self

        mood_str = raw_result.get("mood", "neutral").lower()

        # Validate detected mood
        if mood_str not in config.SUPPORTED_MOODS:
            mood_str = "neutral"

        self.progress        = int(raw_result.get("progress", 100))
        self.statut          = "success"
        self._humeur_detectee = Humeur(type=mood_str)
        return self

    def retourner_humeur(self) -> Optional[Humeur]:
        """Return the detected Humeur, or None if scan not successful."""
        if self.statut == "success":
            return self._humeur_detectee
        return None

    def arreter_stream(self) -> None:
        """
        Signal to stop the webcam stream.
        Actual MediaStream.stop() happens in JS; this resets server state.
        """
        if self.statut not in ("success", "error"):
            self.statut = "idle"
        self.progress = 0

    # ── Helpers ──────────────────────────────────────────────────────────────

    @property
    def is_running(self) -> bool:
        return self.statut in ("loading", "scanning")

    @property
    def error_message(self) -> str:
        return self._error_message

    # ── Serialisation ────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "statut":   self.statut,
            "progress": self.progress,
            "humeur":   self._humeur_detectee.to_dict() if self._humeur_detectee else None,
            "error":    self._error_message,
        }

    def __str__(self) -> str:
        return f"FaceScan(statut={self.statut}, progress={self.progress}%)"
