"""Triage rule engine for Hospital Triage Queue System.

This module implements a configurable symptom-to-urgency mapping based on the
Emergency Severity Index (ESI) standard. Rules are loaded from a JSON file
and used to automatically assign urgency levels to patients.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Default rules based on common ESI indicators
# Urgency: 1 (critical) to 5 (non-urgent)
_DEFAULT_RULES: Dict[str, int] = {
    "cardiac arrest": 1,
    "chest pain": 1,
    "severe respiratory distress": 1,
    "unconscious": 1,
    "severe allergic reaction": 1,
    "major trauma": 1,
    "stroke symptoms": 1,
    "severe abdominal pain": 2,
    "high fever": 2,
    "moderate respiratory distress": 2,
    "severe headache": 2,
    "active bleeding": 2,
    "fracture": 3,
    "moderate pain": 3,
    "vomiting": 3,
    "dehydration": 3,
    "mild respiratory symptoms": 3,
    "minor laceration": 4,
    "mild pain": 4,
    "rash": 4,
    "cold symptoms": 5,
    "minor complaint": 5,
    "routine check": 5,
}

_DEFAULT_URGENCY: int = 3  # Default urgency when no rule matches


class TriageRuleEngine:
    """Configurable rule engine for assigning triage urgency based on symptoms.

    Uses a keyword-based matching system against a set of rules loaded from
    a JSON file. The rules map symptom keywords to ESI urgency levels (1-5).

    Attributes:
        symptom_urgency_map: Dictionary mapping symptom keywords to urgency levels.
        default_urgency: Urgency level to assign when no rule matches.
    """

    def __init__(self, rule_file: str = "rules.json") -> None:
        """Initialize the triage rule engine.

        Args:
            rule_file: Path to the JSON file containing symptom-urgency mappings.
                       Defaults to 'rules.json' in the current working directory.
        """
        self.symptom_urgency_map: Dict[str, int] = {}
        self.default_urgency: int = _DEFAULT_URGENCY
        self._rule_file: str = rule_file
        self.load_rules()

    def load_rules(self) -> None:
        """Load symptom-urgency rules from the configured JSON file.

        If the file does not exist or is invalid, falls back to the default
        built-in rules. Logs warnings for missing or malformed files.
        """
        rule_path = Path(self._rule_file)
        if rule_path.exists():
            try:
                with open(rule_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("Rules file must contain a JSON object")
                # Validate all values are integers in [1,5]
                validated: Dict[str, int] = {}
                for key, value in data.items():
                    if not isinstance(key, str) or not key.strip():
                        logger.warning("Skipping invalid rule key: %s", key)
                        continue
                    if not isinstance(value, int) or not (1 <= value <= 5):
                        logger.warning(
                            "Skipping rule '%s': urgency must be integer 1-5, got %s",
                            key, value
                        )
                        continue
                    validated[key.strip().lower()] = value
                if validated:
                    self.symptom_urgency_map = validated
                    logger.info("Loaded %d rules from %s", len(validated), self._rule_file)
                else:
                    logger.warning("No valid rules found in %s, using defaults", self._rule_file)
                    self.symptom_urgency_map = _DEFAULT_RULES.copy()
            except (json.JSONDecodeError, OSError, ValueError) as exc:
                logger.warning(
                    "Failed to load rules from %s: %s. Using default rules.",
                    self._rule_file, exc
                )
                self.symptom_urgency_map = _DEFAULT_RULES.copy()
        else:
            logger.info("Rule file %s not found. Using default rules.", self._rule_file)
            self.symptom_urgency_map = _DEFAULT_RULES.copy()

    def assign_urgency(self, symptoms: str) -> int:
        """Assign an urgency level based on the patient's symptoms.

        Performs case-insensitive keyword matching against the loaded rules.
        If multiple rules match, the highest priority (lowest urgency number)
        is returned. If no rule matches, returns the default urgency.

        Args:
            symptoms: A string describing the patient's symptoms.

        Returns:
            int: Urgency level from 1 (critical) to 5 (non-urgent).

        Raises:
            ValueError: If symptoms is empty or not a string.
        """
        if not symptoms or not isinstance(symptoms, str):
            raise ValueError("Symptoms must be a non-empty string")

        symptoms_lower = symptoms.lower()
        best_urgency: Optional[int] = None

        for keyword, urgency in self.symptom_urgency_map.items():
            if keyword in symptoms_lower:
                if best_urgency is None or urgency < best_urgency:
                    best_urgency = urgency

        if best_urgency is not None:
            return best_urgency

        logger.debug("No matching rule for symptoms: '%s'. Using default urgency %d",
                      symptoms, self.default_urgency)
        return self.default_urgency

    def add_rule(self, keyword: str, urgency: int) -> None:
        """Add or update a single rule dynamically.

        Args:
            keyword: Symptom keyword to match.
            urgency: Urgency level (1-5).

        Raises:
            ValueError: If keyword is empty or urgency is out of range.
        """
        if not keyword or not isinstance(keyword, str):
            raise ValueError("Keyword must be a non-empty string")
        if not (1 <= urgency <= 5):
            raise ValueError(f"Urgency must be between 1 and 5, got {urgency}")

        self.symptom_urgency_map[keyword.strip().lower()] = urgency

    def remove_rule(self, keyword: str) -> None:
        """Remove a rule by keyword.

        Args:
            keyword: The symptom keyword to remove.
        """
        key = keyword.strip().lower()
        self.symptom_urgency_map.pop(key, None)

    def get_rules(self) -> Dict[str, int]:
        """Return a copy of the current rules.

        Returns:
            Dict[str, int]: Current symptom-urgency mapping.
        """
        return self.symptom_urgency_map.copy()

    def save_rules(self, file_path: Optional[str] = None) -> None:
        """Save the current rules to a JSON file.

        Args:
            file_path: Path to save the rules. If None, uses the configured rule file.
        """
        path = file_path or self._rule_file
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.symptom_urgency_map, f, indent=2, ensure_ascii=False)
            logger.info("Saved %d rules to %s", len(self.symptom_urgency_map), path)
        except OSError as exc:
            logger.error("Failed to save rules to %s: %s", path, exc)
            raise
