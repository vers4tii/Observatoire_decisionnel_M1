import pandas as pd

from observatoire.clean import (
    clean_code_commune,
    departement_from_code,
    normalize_column_name,
    to_numeric_fr,
)


def test_normalize_column_name():
    assert normalize_column_name(" Code Commune ") == "code_commune"
    assert normalize_column_name("Année") == "annee"


def test_code_commune_retrouve_le_zero_initial():
    result = clean_code_commune(pd.Series(["1001", "1001.0", "75056"]))
    assert result.tolist() == ["01001", "01001", "75056"]


def test_code_commune_corse_inchange():
    assert clean_code_commune(pd.Series(["2a004"])).tolist() == ["2A004"]


def test_departement_metropole_corse_outre_mer():
    codes = pd.Series(["01001", "2A004", "97411"])
    assert departement_from_code(codes).tolist() == ["01", "2A", "974"]


def test_nombres_au_format_francais():
    result = to_numeric_fr(pd.Series(["1 234,5", "69 140", "abc", None]))
    assert result.iloc[0] == 1234.5
    assert result.iloc[1] == 69140
    assert pd.isna(result.iloc[2])  # illisible → NaN, jamais 0
    assert pd.isna(result.iloc[3])
