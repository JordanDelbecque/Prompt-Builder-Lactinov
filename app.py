import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Studio Promess", layout="wide")
st.title("📸 Studio Créatif Promess")
st.write("Générez vos prompts parfaits en quelques clics.")

# Chargement des ingrédients (tes fichiers CSV)
@st.cache_data
def load_data():
    df_data = pd.read_csv("data.csv")
    df_config = pd.read_csv("config.csv")
    return df_data, df_config

df_data, df_config = load_data()

# Séparation de l'écran en deux colonnes
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎛️ 1. Paramètres")
    # Création des menus déroulants
    produits = df_data['Produit'].dropna().unique()
    selected_produit = st.selectbox("Choix du Produit", produits)
    
    ambiances = df_config['Ambiances'].dropna().unique()
    selected_ambiance = st.selectbox("Ambiance", ambiances)

with col2:
    st.subheader("🖼️ 2. Aperçu du Produit")
    # Recherche de l'image correspondante dans data.csv
    infos_produit = df_data[df_data['Produit'] == selected_produit].iloc[0]
    lien_image = infos_produit['Image FACE']
    
    if pd.notna(lien_image) and "http" in str(lien_image):
        st.image(lien_image, width=250)
    else:
        st.warning("Aucune image de face trouvée pour ce produit.")

    st.subheader("📝 3. Prompt Final à copier")
    # Recherche du script d'ambiance dans config.csv
    infos_ambiance = df_config[df_config['Ambiances'] == selected_ambiance].iloc[0]
    script_ambiance = infos_ambiance['Script Ambiances']
    
    # Création de la phrase magique
    prompt_final = f"Utilise l'image fournie en pièce jointe comme base visuelle absolue. Tu es un photographe publicitaire professionnel. Contrainte stricte : Ne modifie en aucun cas le design, la forme ou les couleurs du produit sur l'image. Ambiance : {script_ambiance}."
    
    st.code(prompt_final, language="text")
