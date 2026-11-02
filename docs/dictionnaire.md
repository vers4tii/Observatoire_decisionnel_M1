# Dictionnaire des variables

Une ligne par colonne du jeu de données final (`data/processed/observatoire.csv`).

| Variable | Description | Type | Unité | Valeurs possibles / plage | Source | Traitement appliqué |
| --- | --- | --- | --- | --- | --- | --- |
| code_commune | Code officiel géographique INSEE de la commune | texte (5 caractères) | — | ex. 92002 | source_1 | complété à 5 caractères |
| nom_commune | Nom de la commune | texte | — | | source_1 | espaces retirés |
| departement | Code du département | texte | — | ex. 92, 2A | dérivé | 2 premiers caractères du code commune (3 pour l'outre-mer) |
| annee | Année d'observation | entier | année | | source_1 | |
| population | Population | entier | habitants | ≥ 0 | source_2 | |
| indicateur | [à définir] | décimal | [unité] | [plage attendue] | [source] | [traitement] |
