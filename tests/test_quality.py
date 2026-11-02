import pandas as pd

from observatoire.config import KEY
from observatoire.pipeline import load_sample
from observatoire.quality import ALERTE, check_code_commune_format, check_unique_key, run_checks


def test_echantillon_passe_les_controles_bloquants():
    df = load_sample()
    report = run_checks(df, key=KEY)
    assert report.ok, report.to_markdown()


def test_echantillon_doublon_strict_supprime():
    df = load_sample()
    assert not df.duplicated(subset=KEY).any()


def test_valeur_manquante_signalee_en_alerte():
    report = run_checks(load_sample(), key=KEY)
    manquants = [c for c in report.checks if c.nom == "Valeurs manquantes"][0]
    assert manquants.gravite == ALERTE
    assert not manquants.ok


def test_doublon_de_cle_detecte():
    df = pd.DataFrame({"code_commune": ["01001", "01001"], "annee": [2024, 2024]})
    assert not check_unique_key(df, ["code_commune", "annee"]).ok


def test_code_invalide_detecte():
    df = pd.DataFrame({"code_commune": ["1001", "75056"]})
    assert not check_code_commune_format(df).ok
