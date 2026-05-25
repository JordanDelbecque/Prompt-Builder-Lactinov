import streamlit as st
import pandas as pd
import requests
import os
import random

# 1. Configuration initiale
st.set_page_config(page_title="Studio Promess", page_icon="🥛", layout="wide")

# 2. CSS pour les boutons bleus et verts
st.markdown("""
    <style>
    .stButton > button {
        background-color: #0085C5 !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    .stButton > button:hover {
        background-color: #A8C96A !important;
    }
    .stDownloadButton > button {
        background-color: #0085C5 !important;
        color: #FFFFFF !important;
        border: none !important;
        width: 100%;
    }
    .stDownloadButton > button:hover {
        background-color: #A8C96A !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Initialisation de l'historique
if "historique" not in st.session_state:
    st.session_state["historique"] = []

# 4. Le système de Sécurité
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if os.path.exists("logo.png"):
                st.image("logo.png", width=250)
            else:
                st.markdown("<h1>Studio Promess</h1>", unsafe_allow_html=True)
            st.markdown("### Portail Sécurisé")
            pwd = st.text_input("Code d'accès collaborateur :", type="password")
            if st.button("Se connecter"):
                if pwd == "PROMESS2026":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("Code incorrect.")
        return False
    return True

# 5. L'application principale
if check_password():
    
    # En-tête
    col_logo, col_titre = st.columns([1, 4])
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=150)
    with col_titre:
        st.title("Studio Créatif IA")
        st.markdown("**Générez vos campagnes visuelles en respectant la charte produit.**")

    st.markdown("---")

    # Chargement des données
    def load_data():
        fichiers = os.listdir()
        f_data = next((f for f in fichiers if "data" in f.lower() and f.endswith(".csv")), None)
        f_config = next((f for f in fichiers if "config" in f.lower() and f.endswith(".csv")), None)
        
        if not f_data or not f_config:
            st.error("🚨 Base de données introuvable. Veuillez vérifier que DATA.csv et CONFIG.csv sont présents.")
            st.stop()
            
        df_d = pd.read_csv(f_data)
        df_c = pd.read_csv(f_config)
        
        df_d.columns = [str(col).strip() for col in df_d.columns]
        df_c.columns = [str(col).strip() for col in df_c.columns]
        
        return df_d, df_c

    df_data, df_config = load_data()

    produits = df_data['Produit'].dropna().unique().tolist() if 'Produit' in df_data.columns else ["Erreur"]
    
    col_angles = 'Angles' if 'Angles' in df_config.columns else (df_config.columns[4] if len(df_config.columns) > 4 else 'Angles')
    angles = df_config[col_angles].dropna().unique().tolist() if col_angles in df_config.columns else []
    
    ambiances = df_config['Ambiances'].dropna().unique().tolist() if 'Ambiances' in df_config.columns else []
    
    col_format = 'Formats/Ratios)' if 'Formats/Ratios)' in df_config.columns else 'Formats/Ratios'
    formats = df_config[col_format].dropna().unique().tolist() if col_format in df_config.columns else []
    
    styles = df_config['Styles Photo'].dropna().unique().tolist() if 'Styles Photo' in df_config.columns else []
    scenarios = df_config['Scénarios'].dropna().unique().tolist() if 'Scénarios' in df_config.columns else []
    personnages = df_config['Personnages'].dropna().unique().tolist() if 'Personnages' in df_config.columns else []
    lumieres = df_config['Lumières'].dropna().unique().tolist() if 'Lumières' in df_config.columns else []

    def randomizer():
        if produits and "Erreur" not in produits[0]: st.session_state['sel_produit'] = random.choice(produits)
        if angles: st.session_state['sel_angle'] = random.choice(angles)
        if ambiances: st.session_state['sel_ambiance'] = random.choice(ambiances)
        if formats: st.session_state['sel_format'] = random.choice(formats)
        if styles: st.session_state['sel_style'] = random.choice(styles)
        if scenarios: st.session_state['sel_scenario'] = random.choice(scenarios)
        if personnages: st.session_state['sel_personnage'] = random.choice(personnages)
        if lumieres: st.session_state['sel_lumiere'] = random.choice(lumieres)

    tab_studio, tab_guide = st.tabs(["📸 Studio Créatif", "📖 Guide d'utilisation"])

    with tab_guide:
        st.subheader("Comment utiliser le Studio ?")
        st.markdown("""
        **Étape 1 : Configurer le Shoot**
        * Allez dans l'onglet *Studio Créatif*.
        * Utilisez les menus déroulants pour choisir votre produit et l'ambiance désirée.
        
        **Étape 2 : Récupérer les éléments**
        * Cliquez sur le bouton bleu **⬇️ Télécharger l'Asset Officiel** pour sauvegarder l'image du produit.
        * Copiez l'intégralité du texte généré dans la boîte *Prompt Final*.
        
        **Étape 3 : Générer l'image**
        * Ouvrez votre outil IA (Google Flow, Midjourney, etc.).
        * Importez l'image que vous venez de télécharger.
        * Collez le texte juste en dessous de l'image et validez !
        """)

    with tab_studio:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("🎛️ 1. Configuration du Shoot")
            st.button("🎲 Surprends-moi !", on_click=randomizer)
            
            selected_produit = st.selectbox("📦 Produit Officiel", produits, key="sel_produit")
            selected_angle = st.selectbox("📐 Angle Caméra", angles, key="sel_angle") if angles else None
            selected_ambiance = st.selectbox("🏡 Set Design (Ambiance)", ambiances, key="sel_ambiance") if ambiances else None
            selected_format = st.selectbox("📱 Format de sortie", formats, key="sel_format") if formats else None
            selected_style = st.selectbox("🎨 Direction Artistique", styles, key="sel_style") if styles else None
            selected_scenario = st.selectbox("🎬 Action / Scénario", scenarios, key="sel_scenario") if scenarios else None
            selected_personnage = st.selectbox("👤 Casting", personnages, key="sel_personnage") if personnages else None
            selected_lumiere = st.selectbox("💡 Éclairage Studio", lumieres, key="sel_lumiere") if lumieres else None

        with col2:
            st.subheader("🖼️ 2. Asset Visuel")
            
            if selected_produit and "Erreur" not in selected_produit:
                infos_produit = df_data[df_data['Produit'] == selected_produit].iloc[0]
                
                colonnes_images = {
                    "Face": "Image FACE",
                    "Profil": "Image PROFIL",
                    "Dessus": "Image DESSUS",
                    "45°": "Image 45°"
                }
                
                colonne_cible = colonnes_images.get(selected_angle, "Image FACE")
                
                if colonne_cible in df_data.columns:
                    lien_image = infos_produit[colonne_cible]
                else:
                    lien
