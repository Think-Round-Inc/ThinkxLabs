from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from typing import Dict

class EmpathyLabel(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    CONCERN = "concern"
    DISTRESS = "distress"

@dataclass
class EmpathyScore:
    label: EmpathyLabel
    confidence: float  # 0–1
    rationale: str | None = None

class EmpathyScorer:
    """Lightweight wrapper for the underlying empathy"""

    def __init__(self, model_name: str | None = None):
        
        self._keywords: Dict[str, EmpathyLabel] = {
            "happy": EmpathyLabel.POSITIVE,
            "glad": EmpathyLabel.POSITIVE,
            "sad": EmpathyLabel.DISTRESS,
            "depressed": EmpathyLabel.DISTRESS,
            "okay": EmpathyLabel.NEUTRAL,
            "worried": EmpathyLabel.CONCERN,
        }

    def score_text(self, text: str) -> EmpathyScore:
        """Return the top empathy label with a dummy confidence."""
        lowered = text.lower()
        for kw, label in self._keywords.items():
            if kw in lowered:
                return EmpathyScore(label=label, confidence=0.8, rationale=f"keyword '{kw}' detected")
        # fallback
        return EmpathyScore(label=EmpathyLabel.NEUTRAL, confidence=0.2, rationale="no keyword match")

    __call__ = score_text