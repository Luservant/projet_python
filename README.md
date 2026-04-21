# Inégalités territoriales d'accès aux équipements sportifs en France

Évaluation finale — *Python pour la data science*  
Auteurs : DELETANG Arthur, GOUALOU Maxence, SERVANT Lucas  
Chargé de TD : BEROVA Raya

---

## Objectif

Analyser les **inégalités territoriales d'accès aux équipements sportifs** à l'échelle des départements français, et déterminer dans quelle mesure ces inégalités reflètent des inégalités socio-économiques (revenu médian, taux de pauvreté, densité de population, ruralité).

---

## Structure du dépôt

```
.
├── main.ipynb             # Notebook principal (collecte, nettoyage, analyse, modélisation)
├── utils.py               # Fonctions utilitaires (moyenne pondérée)
├── requirements.txt       # Dépendances Python
├── cartographies_html/    # Cartes Folium interactives (format HTML)
└── README.md              # Documentation du projet
```

---

## Données

Toutes les données sont chargées automatiquement depuis le notebook via des APIs publiques — aucun téléchargement manuel n'est nécessaire.

| Source | Description | Méthode |
|---|---|---|
| [Ministère des Sports — Data ES](https://equipements.sports.gouv.fr) | Recensement national des équipements sportifs (~330 000 équipements géolocalisés) | API REST Opendatasoft |
| [INSEE via Data ES](https://equipements.sports.gouv.fr/explore/dataset/insee-2020-geoapi-2023) | Données socio-économiques communales issues du dispositif Filosofi 2020 (revenus, pauvreté, ruralité, superficie) | API REST Opendatasoft |
| [france-geojson (GitHub)](https://github.com/gregoiredavid/france-geojson) | Contours géographiques des départements basés sur les données IGN | Requête HTTP (GeoJSON) |

### Variables principales

| Variable | Description |
|---|---|
| `equip_10k` | Nombre d'équipements sportifs pour 10 000 habitants — variable cible construite à partir du RES et de la population INSEE |
| `revenu_median` | Revenu médian disponible par unité de consommation (€/an) — moyenne pondérée par la population des médianes communales Filosofi (`MED20`) |
| `taux_pauvrete` | Part de la population sous le seuil de pauvreté à 60% du revenu médian — moyenne pondérée par la population (`TP6020`) |
| `densite` | Densité de population (hab./km²) — calculée à partir de la population et de la superficie communales |
| `part_rural` | Part des communes rurales dans le département selon la grille de densité officielle INSEE 2020 (`TYPO_RURB_CRTE`) |

---

## Installation et utilisation

**1. Cloner le dépôt** — ouvrir un terminal et exécuter :

```bash
git clone https://github.com/Luservant/projet_python.git
```

**2. Installer les dépendances :**

```bash
pip install -r requirements.txt
```

**3. Lancer le notebook :**

Ouvrir `main.ipynb` et exécuter toutes les cellules dans l'ordre (ou directement *Run All*).  
Le notebook est entièrement reproductible : les données sont téléchargées automatiquement à chaque exécution.

---

## Contenu du notebook

| Section | Description |
|---|---|
| **1. Imports** | Chargement des librairies |
| **2. Collecte des données** | Récupération du RES via API REST, données INSEE communes, contours GeoJSON |
| **3. Nettoyage et fusion** | Exploration des valeurs manquantes, standardisation des codes département, suppression des doublons, agrégation commune → département, construction du DataFrame analytique |
| **4. Analyse descriptive** | Statistiques générales, distribution de la densité d'équipements, classement des départements, corrélations avec les variables socio-économiques, analyse par type d'équipement |
| **5. Visualisation cartographique** | Carte choroplèthe interactive, carte bivarée équipements × pauvreté, carte des types d'équipements dominants par département |
| **6. Modélisation** | Régression linéaire et Random Forest, analyse des résidus, validation croisée, optimisation des hyperparamètres, importance des variables |

---
## Visualisation des cartes

Les cartes interactives (Folium) peuvent parfois ne pas s'afficher directement dans l'aperçu statique de GitHub, ni sur le notebook. 

Si les cartes n'apparaissent pas dans le notebook :
1. **Option locale** : Vous pouvez consulter ou télécharger les fichiers interactifs directement dans le dossier [`cartographies_html/`](./cartographies_html/).
   * *Note : Pour les visualiser, téléchargez le fichier et ouvrez-le avec n'importe quel navigateur (Chrome, Firefox, etc.).*
---

## Principaux résultats

En moyenne, on compte **65 équipements sportifs pour 10 000 habitants** en France, avec de très fortes disparités : les Hautes-Alpes affichent un ratio de 265 contre 14 pour Paris.

La matrice de corrélation révèle que la **densité de population** est la variable la plus corrélée négativement avec la densité d'équipements (r ≈ −0.8), suivie de la **part rurale** (corrélation positive, r ≈ +0.7). Le taux de pauvreté et le revenu médian ont une influence plus modérée.

Le modèle **Random Forest** atteint un R² de **0.875** sur le jeu de test, contre 0.693 pour la régression linéaire, ce qui suggère des relations non linéaires importantes entre les variables territoriales et la densité d'équipements.

---

## Bibliographie

- INSEE - Données communes (2020)
- Ministère des Sports (2025). *Data ES — Recensement des équipements sportifs*. https://equipements.sports.gouv.fr
- INSEE. *Filosofi — Fichier localisé social et fiscal*. https://www.insee.fr/fr/metadonnees/source/serie/s1172
- Galiana, L. (2025). *Python pour la data science*. https://pythonds.linogaliana.fr
