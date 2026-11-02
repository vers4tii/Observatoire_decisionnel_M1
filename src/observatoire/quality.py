"""Contrôles qualité.

Un contrôle « bloquant » arrête le pipeline ; une « alerte » est rapportée mais n'arrête rien.
Le rapport est écrit dans data/processed/rapport_qualite.md et alimente la data card.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

BLOQUANT = "bloquant"
ALERTE = "alerte"


@dataclass
class Check:
    nom: str
    ok: bool
    detail: str
    gravite: str = BLOQUANT


@dataclass
class QualityReport:
    checks: list[Check] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(c.ok for c in self.checks if c.gravite == BLOQUANT)

    def add(self, check: Check) -> None:
        self.checks.append(check)

    def to_markdown(self) -> str:
        lines = ["# Rapport qualité", "", "| Contrôle | Gravité | Résultat | Détail |", "| --- | --- | --- | --- |"]
        for c in self.checks:
            lines.append(f"| {c.nom} | {c.gravite} | {'OK' if c.ok else 'ÉCHEC'} | {c.detail} |")
        return "\n".join(lines) + "\n"


class QualityError(Exception):
    pass


def check_required_columns(df: pd.DataFrame, required: list[str]) -> Check:
    missing = [c for c in required if c not in df.columns]
    return Check("Colonnes attendues présentes", not missing, f"manquantes : {missing}" if missing else "toutes présentes")


def check_unique_key(df: pd.DataFrame, key: list[str]) -> Check:
    n = int(df.duplicated(subset=key, keep=False).sum())
    return Check(f"Clé unique {key}", n == 0, f"{n} lignes en doublon sur la clé")


def check_code_commune_format(df: pd.DataFrame, column: str = "code_commune") -> Check:
    valid = df[column].astype("string").str.fullmatch(r"\d{5}|2[AB]\d{3}", na=False)
    n = int((~valid).sum())
    return Check("Format des codes communes", n == 0, f"{n} codes invalides")


def check_missing(df: pd.DataFrame, columns: list[str]) -> Check:
    counts = {c: int(df[c].isna().sum()) for c in columns}
    total = sum(counts.values())
    detail = ", ".join(f"{c} : {n} ({n / len(df):.0%})" for c, n in counts.items()) if len(df) else "table vide"
    return Check("Valeurs manquantes", total == 0, detail, gravite=ALERTE)


def check_range(df: pd.DataFrame, column: str, low: float | None = None, high: float | None = None) -> Check:
    values = df[column].dropna()
    bad = pd.Series(False, index=values.index)
    if low is not None:
        bad |= values < low
    if high is not None:
        bad |= values > high
    return Check(f"Plage de {column} [{low} ; {high}]", not bad.any(), f"{int(bad.sum())} valeurs hors plage")


def check_not_empty(df: pd.DataFrame) -> Check:
    return Check("Table non vide", len(df) > 0, f"{len(df)} lignes")


def run_checks(df: pd.DataFrame, key: list[str]) -> QualityReport:
    """Contrôles par défaut. Ajoutez les vôtres : chaque hypothèse sur les données mérite un contrôle."""
    report = QualityReport()
    required = ["code_commune", "nom_commune", "departement", "annee", "population", "indicateur"]
    report.add(check_not_empty(df))
    report.add(check_required_columns(df, required))
    if not report.ok:
        return report
    report.add(check_unique_key(df, key))
    report.add(check_code_commune_format(df))
    report.add(check_range(df, "population", low=0))
    report.add(check_range(df, "annee", low=1900, high=2100))
    report.add(check_missing(df, ["population", "indicateur"]))
    return report
