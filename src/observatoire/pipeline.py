"""Pipeline reproductible : collecte → nettoyage → jointure → contrôles → export.

Usage :
    python -m observatoire.pipeline --sample   # échantillon versionné, sans réseau
    python -m observatoire.pipeline            # vraies sources de sources.yaml
"""

from __future__ import annotations

import argparse
import sys

import pandas as pd

from observatoire.clean import clean_sample
from observatoire.collect import collect_all
from observatoire.config import KEY, OUTPUT_CSV, PROCESSED, QUALITY_REPORT, SAMPLE
from observatoire.quality import QualityError, run_checks


def load_sample() -> pd.DataFrame:
    raw = pd.read_csv(SAMPLE / "exemple_communes.csv", sep=";", dtype=str, encoding="utf-8")
    return clean_sample(raw)


def build_dataset(paths: dict) -> pd.DataFrame:
    """À ÉCRIRE PAR LE BINÔME (jalon J2).

    1. Lire chaque fichier de `paths` (séparateur, encodage, types : voir sources.yaml).
    2. Nettoyer chaque source (fonctions de clean.py ; ajoutez les vôtres, testées).
    3. Joindre les sources sur la clé commune, en mesurant les lignes perdues :
           merged = left.merge(right, on="code_commune", how="left", indicator=True)
           perdues = (merged["_merge"] == "left_only").sum()
       et consigner ce chiffre dans la data card.
    4. Retourner une table aux colonnes attendues par quality.run_checks.
    """
    raise NotImplementedError(
        "build_dataset() n'est pas encore écrit : lancez `python -m observatoire.pipeline --sample` "
        "en attendant, puis complétez src/observatoire/pipeline.py."
    )


def run(sample: bool = False) -> pd.DataFrame:
    if sample:
        print("[pipeline] Mode échantillon (data/sample/)")
        df = load_sample()
    else:
        paths = collect_all()
        df = build_dataset(paths)

    report = run_checks(df, key=KEY)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    QUALITY_REPORT.write_text(report.to_markdown(), encoding="utf-8")
    print(report.to_markdown())

    if not report.ok:
        raise QualityError(f"Contrôle bloquant en échec, voir {QUALITY_REPORT}")

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"[pipeline] {len(df)} lignes écrites dans {OUTPUT_CSV}")
    return df


def main() -> int:
    parser = argparse.ArgumentParser(description="Pipeline de l'observatoire")
    parser.add_argument("--sample", action="store_true", help="utiliser l'échantillon versionné")
    args = parser.parse_args()
    try:
        run(sample=args.sample)
    except (QualityError, NotImplementedError, ValueError) as error:
        print(f"[pipeline] ERREUR : {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
