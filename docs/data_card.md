# Data card

> Une section par source, plus une section pour le jeu de données final (après jointure).
> À commencer en S2, à tenir à jour jusqu'au rendu.

## Source : [nom] (`source_1` dans sources.yaml)

| Champ | Valeur |
| --- | --- |
| Producteur | |
| Lien | |
| Licence | |
| Date d'accès | |
| Fréquence de mise à jour | |
| Maille | |
| Période couverte | |
| Nombre de lignes / colonnes (brut) | |
| Clé de jointure | |

**Comment les données sont produites** : [déclaratif, administratif, capteur, enquête…]

**Qualité constatée** : [valeurs manquantes, doublons, valeurs aberrantes, changements de définition, codes géographiques obsolètes ; chiffres issus de `quality.py`]

**Biais connus** : [qui est sous-représenté, qui manque]

**Usages à éviter** : [ce que ces données ne permettent pas de dire]

## Jeu de données final

| Champ | Valeur |
| --- | --- |
| Fichier | `data/processed/observatoire.csv` |
| Lignes / colonnes | |
| Lignes perdues à la jointure | [nombre et part ; pourquoi] |
| Valeurs manquantes par colonne | [voir rapport qualité] |

**Traitements appliqués** : [renvoi aux fonctions de `src/observatoire/clean.py` et aux décisions D-XXX]
