"""Tableau de bord Streamlit — point de départ.

Lancement : streamlit run app/app.py
Principe : chaque écran répond à une question de la note de cadrage, affiche sa source,
signale les données manquantes et reste lisible sans la couleur.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from observatoire.config import OUTPUT_CSV  # noqa: E402

st.set_page_config(page_title="Observatoire décisionnel", layout="wide")

# Une seule couleur d'accent, contrastée ; la couleur ne porte jamais seule l'information.
ACCENT = "#1F4E79"
SOURCE_LABEL = "Source : [producteur, jeu de données], consulté le [AAAA-MM-JJ]. Traitements : voir le dépôt."


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype={"code_commune": str, "departement": str})


st.title("Observatoire décisionnel")
st.caption("[Problématique en une phrase, reprise de la note de cadrage]")

if not OUTPUT_CSV.exists():
    st.error(
        "Aucune donnée préparée. Lancez d'abord le pipeline : "
        "`python -m observatoire.pipeline --sample` (échantillon) ou `python -m observatoire.pipeline`."
    )
    st.stop()

df = load_data(OUTPUT_CSV)

# --- Filtres -----------------------------------------------------------------
with st.sidebar:
    st.header("Filtres")
    departements = sorted(df["departement"].dropna().unique())
    choix_dep = st.multiselect("Départements", departements, default=departements)
    annees = sorted(df["annee"].dropna().astype(int).unique())
    choix_annee = st.selectbox("Année", annees, index=len(annees) - 1)

vue = df[df["departement"].isin(choix_dep) & (df["annee"] == choix_annee)]

if vue.empty:
    st.warning("Aucune commune ne correspond à ces filtres. Élargissez la sélection de départements.")
    st.stop()

# --- Indicateurs clés ------------------------------------------------------------
manquants = int(vue["indicateur"].isna().sum())
c1, c2, c3 = st.columns(3)
c1.metric("Communes affichées", len(vue))
c2.metric("Indicateur médian", f"{vue['indicateur'].median():.1f}")
c3.metric("Valeurs manquantes", manquants)
if manquants:
    st.info(
        f"{manquants} commune(s) sans valeur pour l'indicateur : elles n'apparaissent pas dans le "
        "classement ci-dessous, mais restent listées dans le tableau détaillé."
    )

# --- Classement ----------------------------------------------------------------
st.subheader(f"Communes classées par indicateur — {choix_annee}")
classement = vue.dropna(subset=["indicateur"]).sort_values("indicateur", ascending=True)
fig = px.bar(
    classement,
    x="indicateur",
    y="nom_commune",
    orientation="h",
    text="indicateur",
    labels={"indicateur": "Indicateur [unité]", "nom_commune": ""},
    color_discrete_sequence=[ACCENT],
)
fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
fig.update_layout(height=max(300, 40 * len(classement)), margin=dict(l=0, r=40, t=10, b=0))
mediane = classement["indicateur"].median()
fig.add_vline(x=mediane, line_dash="dash", line_color="#555555")
fig.add_annotation(x=mediane, y=1.02, yref="paper", text=f"Médiane : {mediane:.1f}", showarrow=False)
st.plotly_chart(fig, width="stretch")
st.caption(SOURCE_LABEL)

# --- Limites ------------------------------------------------------------------
with st.expander("Ce que ce tableau de bord ne permet pas de conclure"):
    st.markdown("- [Limite 1, reprise du hors-périmètre de la note de cadrage]\n- [Limite 2]")

with st.expander("Données détaillées"):
    st.dataframe(vue, width="stretch", hide_index=True)
    st.download_button("Télécharger la sélection (CSV)", vue.to_csv(index=False).encode("utf-8"), "selection.csv")
