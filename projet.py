"""
Carte interactive des infrastructures sportives en France
Données : data-es-equipement.csv (Recensement des Équipements Sportifs)
Dépendances : pip install folium pandas
"""

import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap

# ─────────────────────────────────────────
# 1. CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────

CSV_PATH = "data-es-equipement.csv"  # Adaptez le chemin si nécessaire
SEP = ";"

print("Chargement des données...")
df = pd.read_csv(CSV_PATH, sep=",", encoding="utf-8", low_memory=False)
print(f"✓ {len(df)} équipements chargés")


# ─────────────────────────────────────────
# 2. NETTOYAGE ET PRÉPARATION
# ─────────────────────────────────────────

COL_LAT     = "coordonnees_y"
COL_LON     = "coordonnees_x"
COL_NOM     = "nom"
COL_TYPE    = "type"
COL_FAMILLE = "famille"
COL_COMMUNE = "commune"
COL_NATURE  = "nature"

# Conversion en numérique
df[COL_LAT] = pd.to_numeric(df[COL_LAT], errors="coerce")
df[COL_LON] = pd.to_numeric(df[COL_LON], errors="coerce")
df = df.dropna(subset=[COL_LAT, COL_LON])

# Filtrage géographique : France métropolitaine + DOM
df = df[
    (df[COL_LAT].between(-21.5, 51.2)) &
    (df[COL_LON].between(-63.2, 55.9))
]

print(f"✓ {len(df)} équipements avec coordonnées valides")


# ─────────────────────────────────────────
# 3. PALETTE DE COULEURS PAR FAMILLE
# ─────────────────────────────────────────

COULEURS = {
    "football":     "green",
    "natation":     "darkblue",
    "tennis":       "orange",
    "gymnase":      "blue",
    "athlétisme":   "red",
    "basket":       "darkred",
    "rugby":        "darkgreen",
    "golf":         "lightgreen",
    "équitation":   "beige",
    "cyclisme":     "purple",
    "arts martiaux":"cadetblue",
    "tir":          "black",
}
COULEUR_DEFAUT = "gray"

def couleur_pour(famille):
    if pd.isna(famille):
        return COULEUR_DEFAUT
    famille_lower = str(famille).lower()
    for cle, couleur in COULEURS.items():
        if cle in famille_lower:
            return couleur
    return COULEUR_DEFAUT


# ─────────────────────────────────────────
# 4. CRÉATION DE LA CARTE
# ─────────────────────────────────────────

print("Création de la carte...")

carte = folium.Map(
    location=[46.5, 2.5],
    zoom_start=6,
    tiles="CartoDB positron",
)

# Titre
titre_html = """
<div style="position: fixed; top: 15px; left: 50%; transform: translateX(-50%);
     z-index: 1000; background: white; padding: 10px 20px;
     border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.3);
     font-family: Arial; font-size: 16px; font-weight: bold; color: #333;">
    🏟️ Infrastructures sportives en France
</div>
"""
carte.get_root().html.add_child(folium.Element(titre_html))


# ─────────────────────────────────────────
# 5. COUCHE 1 : MARQUEURS CLUSTERISÉS
# ─────────────────────────────────────────

cluster = MarkerCluster(name="Équipements (marqueurs)", show=True)

# Échantillonnage pour les performances si trop de points
SAMPLE = 50_000
df_sample = df.sample(min(SAMPLE, len(df)), random_state=42) if len(df) > SAMPLE else df

for _, row in df_sample.iterrows():
    nom     = row.get(COL_NOM, "Inconnu")
    type_eq = row.get(COL_TYPE, "")
    famille = row.get(COL_FAMILLE, "")
    commune = row.get(COL_COMMUNE, "")
    nature  = row.get(COL_NATURE, "")
    couleur = couleur_pour(famille)

    popup_html = f"""
    <div style="font-family: Arial; min-width: 180px;">
        <b style="font-size:13px;">{nom}</b><br>
        <span style="color:#555;">🏅 {type_eq}</span><br>
        <span style="color:#555;">📂 {famille}</span><br>
        <span style="color:#555;">📍 {commune}</span><br>
        <span style="color:#555;">🌿 {nature}</span>
    </div>
    """

    folium.CircleMarker(
        location=[row[COL_LAT], row[COL_LON]],
        radius=5,
        color=couleur,
        fill=True,
        fill_color=couleur,
        fill_opacity=0.7,
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=str(nom),
    ).add_to(cluster)

cluster.add_to(carte)


# ─────────────────────────────────────────
# 6. COUCHE 2 : CARTE DE CHALEUR
# ─────────────────────────────────────────

coords_heatmap = df[[COL_LAT, COL_LON]].dropna().values.tolist()

HeatMap(
    coords_heatmap,
    name="Densité (heatmap)",
    radius=8,
    blur=10,
    min_opacity=0.3,
    show=False,
).add_to(carte)


# ─────────────────────────────────────────
# 7. CONTRÔLE DES COUCHES + LÉGENDE
# ─────────────────────────────────────────

folium.LayerControl(position="topright", collapsed=False).add_to(carte)

legende_html = """
<div style="position: fixed; bottom: 30px; left: 15px; z-index: 1000;
     background: white; padding: 12px 16px; border-radius: 8px;
     box-shadow: 0 2px 6px rgba(0,0,0,0.3); font-family: Arial; font-size: 12px;">
    <b>Légende</b><br>
    <span style="color:green;">●</span> Football<br>
    <span style="color:darkblue;">●</span> Natation<br>
    <span style="color:orange;">●</span> Tennis<br>
    <span style="color:blue;">●</span> Gymnase<br>
    <span style="color:red;">●</span> Athlétisme<br>
    <span style="color:darkred;">●</span> Basket<br>
    <span style="color:darkgreen;">●</span> Rugby<br>
    <span style="color:purple;">●</span> Cyclisme<br>
    <span style="color:gray;">●</span> Autre<br>
</div>
"""
carte.get_root().html.add_child(folium.Element(legende_html))


# ─────────────────────────────────────────
# 8. SAUVEGARDE
# ─────────────────────────────────────────

OUTPUT = "carte_sports.html"
carte.save(OUTPUT)
print(f"\n✅ Carte sauvegardée : {OUTPUT}")
print("   Ouvrez ce fichier dans votre navigateur.")