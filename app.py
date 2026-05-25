import streamlit as st
import pandas as pd
import requests
import os

# Configuration de la page
st.set_page_config(page_title="Studio Promess", layout="wide")
st.title("📸 Studio Créatif Promess")
st.write("Générez vos prompts parfaits en quelques clics.")

# Chargement intelligent des ingrédients (Insensible aux majuscules)
@st.cache_data
def load_data():
    fichiers_presents = os.listdir()
    
    # Le robot cherche n'importe quel fichier contenant "data" ou "config"
    fichier_data = next((f for f in fichiers_presents if "data" in f.lower() and f.endswith(".csv")), None)
    fichier_config = next((f for f in fichiers_presents if "config" in f.lower() and f.endswith(".csv")), None)
    
    # Sécurité : Si le robot ne trouve rien, il nous dit ce qu'il voit
    if not fichier_data or not fichier_config:
        st.error(f"🚨 Fichiers CSV introuvables ! Voici les fichiers que le robot voit dans ton dossier : {fichiers_presents}")
        st.stop()
        
    df_data = pd.read_csv(fichier_data)
    df_config = pd.read_csv(fichier_config)
    return df_data, df_config

df_data, df_config = load_data()

# Séparation de l'écran en deux colonnes égales
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎛️ 1. Paramètres du Prompt")
    
    # Menus déroulants
    produits = df_data['Produit'].dropna().unique()
    selected_produit = st.selectbox("📦 Choix du Produit", produits)
    
    angles = df_config['Angles'].dropna().unique()
    selected_angle = st.selectbox("📐 Angle de vue", angles)
    
    ambiances = df_config['Ambiances'].dropna().unique()
    selected_ambiance = st.selectbox("🏡 Ambiance", ambiances)
    
    col_format = 'Formats/Ratios)' if 'Formats/Ratios)' in df_config.columns else 'Formats/Ratios'
    formats = df_config[col_format].dropna().unique()
    selected_format = st.selectbox("📐 Format (Ratio)", formats)
    
    styles = df_config['Styles Photo'].dropna().unique()
    selected_style = st.selectbox("🎨 Style Photo", styles)
    
    scenarios = df_config['Scénarios'].dropna().unique()
    selected_scenario = st.selectbox("🎬 Scénario", scenarios)
    
    personnages = df_config['Personnages'].dropna().unique()
    selected_personnage = st.selectbox("👤 Personnage", personnages)
    
    lumieres = df_config['Lumières'].dropna().unique()
    selected_lumiere = st.selectbox("💡 Éclairage / Lumière", lumieres)

with col2:
    st.subheader("🖼️ Aperçu du Produit")
    
    infos_produit = df_data[df_data['Produit'] == selected_produit].iloc[0]
    lien_image = infos_produit['Image FACE']
    
    if pd.notna(lien_image) and "http" in str(lien_image):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            reponse = requests.get(lien_image, headers=headers)
            st.image(reponse.content, width=200)
        except:
            st.info(f"🔗 [Lien de l'image source]({lien_image})")
    else:
        st.warning("Aucune image de face trouvée pour ce produit.")

    st.subheader("📝 3. Prompt Final à copier")
    
    # Extraction des scripts
    script_angle = df_config[df_config['Angles'] == selected_angle].iloc[0]['Scripts Angles']
    script_ambiance = df_config[df_config['Ambiances'] == selected_ambiance].iloc[0]['Script Ambiances']
    script_format = df_config[df_config[col_format] == selected_format].iloc[0]['Script Formats/Ratios']
    script_style = df_config[df_config['Styles Photo'] == selected_style].iloc[0]['Scripts Styles Photos']
    script_scenario = df_config[df_config['Scénarios'] == selected_scenario].iloc[0]['Scripts Scénarios']
    script_personnage = df_config[df_config['Personnages'] == selected_personnage].iloc[0]['Script Personnages']
    script_lumiere = df_config[df_config['Lumières'] == selected_lumiere].iloc[0]['Script Lumières']
    
    # Nettoyage des textes vides
    def clean(text):
        return str(text).strip() if pd.notna(text) and str(text).lower() != 'nan' else ""

    prompt_final = (
        f"Utilise l'image {lien_image} comme base visuelle absolue. "
        f"Tu es un photographe publicitaire professionnel. "
        f"Contrainte stricte : Ne modifie en aucun cas le design, la forme ou les couleurs du produit sur l'image.\n\n"
        f"Description technique : {clean(script_angle)}.\n"
        f"Ambiance : {clean(script_ambiance)}.\n"
        f"Scénario : {clean(script_scenario)}.\n"
        f"Personnage : {clean(script_personnage)}.\n"
        f"Lumière : {clean(script_lumiere)}.\n"
        f"Style visuel : {clean(script_style)}.\n\n"
        f"Rendu : Photorealistic, 8k, highly detailed, sharp focus, professional post-processing. "
        f"Format : {clean(script_format)}"
    )
    
    # La grande zone de texte lisible d'un coup
    st.text_area(
        label="Sélectionne tout le texte ci-dessous pour ton IA :",
        value=prompt_final,
        height=380
    )
