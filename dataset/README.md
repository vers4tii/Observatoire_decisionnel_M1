# Observatoire décisionnel — [titre de votre observatoire]

> PRJ450 · Projet IA — Visualisation de données avancée · M1 Mastère Expert IT · École 89
> Binôme : [Nom Prénom] · [Nom Prénom]

**Problématique** : [une phrase interrogative, reprise de `docs/note_cadrage.md`]
**Public cible** : [persona en une ligne]
**Décision éclairée** : [ce que le public fera du résultat, et quand]

---

## Structure du dépôt

```
.
├── README.md                 ← vous êtes ici (présentation + guide de reproduction)
├── DECISIONS.md              ← journal des décisions (règle de preuve)
├── AI_USAGE.md               ← déclaration de l'usage d'IA générative
├── sources.yaml              ← provenance, licence et date d'accès de chaque source
├── requirements.txt
├── Makefile                  ← raccourcis : install, data, test, app
├── docs/
│   ├── note_cadrage.md       ← livrable 1
│   ├── data_card.md          ← livrable 2
│   ├── dictionnaire.md       ← livrable 2
│   └── revue_croisee.md      ← grilles de revue reçues
├── data/
│   ├── raw/                  ← données brutes téléchargées (non versionnées)
│   ├── processed/            ← sorties du pipeline (non versionnées)
│   └── sample/               ← petit échantillon versionné pour les tests et la démo
├── src/observatoire/
│   ├── collect.py            ← téléchargement depuis sources.yaml
│   ├── clean.py              ← nettoyage et typage
│   ├── quality.py            ← contrôles qualité
│   └── pipeline.py           ← enchaîne collecte → nettoyage → contrôles → export
├── app/
│   └── app.py                ← tableau de bord Streamlit
└── tests/                    ← tests automatiques (pytest)
```

## Guide de reproduction

Prérequis : Python 3.11 ou plus récent, Git.

```bash
# 1. Cloner et créer l'environnement
git clone [URL du dépôt] && cd [dossier]
python -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -r requirements.txt
export PYTHONPATH=src              # Windows PowerShell : $env:PYTHONPATH="src"

# 2. Lancer le pipeline sur l'échantillon (sans réseau)
python -m observatoire.pipeline --sample

# 3. Lancer le pipeline sur les vraies données (télécharge les sources de sources.yaml)
python -m observatoire.pipeline

# 4. Vérifier
python -m pytest

# 5. Ouvrir le tableau de bord
streamlit run app/app.py
```

Avec `make` : `make install`, `make sample`, `make data`, `make test`, `make app`.

`make` positionne `PYTHONPATH` tout seul.

Chaque chiffre présenté en soutenance doit pouvoir être régénéré par ces commandes.

## Livrables et jalons

| Jalon | Séance | Attendu | Où dans le dépôt | Fait |
| --- | --- | --- | --- | --- |
| Preuve S1 | S1 | Note de cadrage v0, premier commit de chaque membre | `docs/note_cadrage.md` | [ ] |
| J1 | S2 | Problématique, sources, test de faisabilité | `docs/note_cadrage.md`, `sources.yaml`, `docs/data_card.md` | [ ] |
| J2 | S4 | Données propres, contrôles, premières mesures | `src/`, `tests/`, `data/processed/` | [ ] |
| J3 | S6 | Choix visuels, prototype interactif | `app/` | [ ] |
| J4 | S8 | Test utilisateur, accessibilité, limites | `docs/`, `DECISIONS.md` | [ ] |
| Final | S10 | Observatoire publié, rapport 8–12 p., soutenance 12 min | tout le dépôt | [ ] |

## Sources et licences

Voir `sources.yaml` et `docs/data_card.md`. Bibliothèques : voir `requirements.txt`.

## Contributions

| Membre | Principales contributions |
| --- | --- |
| [Nom] | [à compléter au fil du projet] |
| [Nom] | [à compléter au fil du projet] |
