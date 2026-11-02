"""Chemins du projet et lecture de sources.yaml."""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
SAMPLE = DATA / "sample"
SOURCES_FILE = ROOT / "sources.yaml"

OUTPUT_CSV = PROCESSED / "observatoire.csv"
QUALITY_REPORT = PROCESSED / "rapport_qualite.md"

# Clé qui identifie une ligne du jeu final. À adapter à votre maille.
KEY = ["code_commune", "annee"]


def load_sources(path: Path = SOURCES_FILE) -> list[dict]:
    """Retourne la liste des sources déclarées dans sources.yaml."""
    with open(path, encoding="utf-8") as f:
        content = yaml.safe_load(f) or {}
    return content.get("sources", [])
