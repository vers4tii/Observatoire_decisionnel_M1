"""Nettoyage et typage.

Règle : chaque fonction fait une seule chose, est testée dans tests/test_clean.py,
et chaque choix non évident est justifié dans DECISIONS.md.
"""

from __future__ import annotations

import re
import unicodedata

import pandas as pd


def normalize_column_name(name: str) -> str:
    """« Code Commune » → « code_commune » (minuscules, sans accents, sans espaces)."""
    text = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode()
    text = re.sub(r"[^0-9a-zA-Z]+", "_", text.strip().lower())
    return text.strip("_")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={c: normalize_column_name(c) for c in df.columns})


def clean_code_commune(codes: pd.Series) -> pd.Series:
    """Codes INSEE en texte sur 5 caractères ; « 1001 » devient « 01001 », « 2A004 » reste tel quel.

    Piège classique : un code lu comme un nombre perd son zéro initial.
    """
    as_text = codes.astype("string").str.strip().str.upper()
    as_text = as_text.str.replace(r"\.0$", "", regex=True)  # 1001.0 si la colonne a été lue en float
    return as_text.where(~as_text.str.fullmatch(r"\d{1,5}", na=False), as_text.str.zfill(5))


def departement_from_code(codes: pd.Series) -> pd.Series:
    """Département déduit du code commune : 3 caractères en outre-mer (97x), 2 sinon."""
    codes = codes.astype("string")
    outre_mer = codes.str.startswith("97", na=False)
    return codes.str[:2].where(~outre_mer, codes.str[:3])


def to_numeric_fr(values: pd.Series) -> pd.Series:
    """Convertit « 1 234,5 » en 1234.5 ; une valeur illisible devient NaN (jamais 0)."""
    text = (
        values.astype("string")
        .str.replace(" ", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    return pd.to_numeric(text, errors="coerce")


def clean_sample(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoyage de l'échantillon fourni. À adapter (ou dupliquer) pour chacune de vos sources."""
    out = normalize_columns(df)
    out["code_commune"] = clean_code_commune(out["code_commune"])
    out["nom_commune"] = out["nom_commune"].astype("string").str.strip()
    out["annee"] = pd.to_numeric(out["annee"], errors="coerce").astype("Int64")
    out["population"] = to_numeric_fr(out["population"]).astype("Int64")
    out["indicateur"] = to_numeric_fr(out["indicateur"])
    out["departement"] = departement_from_code(out["code_commune"])
    # Doublons stricts : supprimés. Doublons de clé avec valeurs différentes : laissés, le contrôle qualité les signale.
    out = out.drop_duplicates()
    return out[["code_commune", "nom_commune", "departement", "annee", "population", "indicateur"]]
