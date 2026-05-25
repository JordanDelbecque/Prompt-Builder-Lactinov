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

# 3. Initialisation de l'historique dans la mémoire
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

    # Chargement des données (SANS CACHE : MISE À JOUR INSTANTANÉE)
    # Chargement des données (MODE DÉTECTIVE)
    def load_data():
        fichiers = os.listdir() # L'application regarde tous les fichiers autour d'elle
        
        # Recherche ultra-tolérante (ignore les majuscules/minuscules)
        f_data = next((f for f in fichiers if "data" in f.lower() and ".csv" in f.lower()), None)
        f_config = next((f for f in fichiers if "config" in f.lower() and ".csv" in f.lower()), None)
        
        if not f_data or not f_config:
            # Si ça plante, ça va afficher à l'écran TOUS les fichiers trouvés !
            st.error(f"🚨 Fichiers introuvables. Voici ce que l'application voit dans le dossier : {', '.join(fichiers)}")
            st.stop()
            
        return pd.read_csv(f_data), pd.read_csv(f_config)

    # Nettoyage des colonnes (enlève les espaces invisibles)
    df_data.columns = df_data.columns.str.strip()
    df_config.columns = df_config.columns.str.strip()

    # Extraction des listes de choix
    produits = df_data['Produit'].dropna().unique().tolist()
    
    # Sécurité au cas où la colonne Angles s'appelle autrement avec un espace
    col_angles = 'Angles' if 'Angles' in df_config.columns else df_config.columns[4]
    angles = df_config[col_angles].dropna().unique().tolist()
    
    ambiances = df_config['Ambiances'].dropna().unique().tolist()
    col_format = 'Formats/Ratios)' if 'Formats/Ratios)' in df_config.columns else 'Formats/Ratios'
    formats = df_config[col_format].dropna().unique().tolist()
    styles = df_config['Styles Photo'].dropna().unique().tolist()
    scenarios = df_config['Scénarios'].dropna().unique().tolist()
    personnages = df_config['Personnages'].dropna().unique().tolist()
    lumieres = df_config['Lumières'].dropna().unique().tolist()

    # Fonction pour le bouton "Surprends-moi"
    def randomizer():
        st.session_state['sel_produit'] = random.choice(produits)
        st.session_state['sel_angle'] = random.choice(angles)
        st.session_state['sel_ambiance'] = random.choice(ambiances)
        st.session_state['sel_format'] = random.choice(formats)
        st.session_state['sel_style'] = random.choice(styles)
        st.session_state['sel_scenario'] = random.choice(scenarios)
        st.session_state['sel_personnage'] = random.choice(personnages)
        st.session_state['sel_lumiere'] = random.choice(lumieres)

    # CREATION DES ONGLETS
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
            selected_angle = st.selectbox("📐 Angle Caméra", angles, key="sel_angle")
            selected_ambiance = st.selectbox("🏡 Set Design (Ambiance)", ambiances, key="sel_ambiance")
            selected_format = st.selectbox("📱 Format de sortie", formats, key="sel_format")
            selected_style = st.selectbox("🎨 Direction Artistique", styles, key="sel_style")
            selected_scenario = st.selectbox("🎬 Action / Scénario", scenarios, key="sel_scenario")
            selected_personnage = st.selectbox("👤 Casting", personnages, key="sel_personnage")
            selected_lumiere = st.selectbox("💡 Éclairage Studio", lumieres, key="sel_lumiere")

        with col2:
            st.subheader("🖼️ 2. Asset Visuel")
            
            infos_produit = df_data[df_data['Produit'] == selected_produit].iloc[0]
            
            # --- LE NOUVEAU TRADUCTEUR MAGIQUE ---
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
                lien_image = infos_produit['Image FACE']
                
            if pd.notna(lien_image) and "http" in str(lien_image):
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    reponse = requests.get(lien_image, headers=headers)
                    st.image(reponse.content, width=200)
                    
                    st.download_button(
                        label=f"⬇️ Télécharger la vue {selected_angle}",
                        data=reponse.content,
                        file_name=f"ASSET_{selected_produit.replace(' ', '_')}_{selected_angle}.jpg",
                        mime="image/jpeg"
                    )
                except:
                    st.info("Aperçu bloqué par Google Drive.")
            else:
                st.warning(f"Aucune image trouvée pour l'angle {selected_angle}")
            
            st.subheader("📝 3. Prompt Final")
            
            # Récupération sécurisée des scripts
            script_angle = df_config[df_config[col_angles] == selected_angle].iloc[0]['Scripts Angles'] if 'Scripts Angles' in df_config.columns else ""
            script_ambiance = df_config[df_config['Ambiances'] == selected_ambiance].iloc[0]['Script Ambiances'] if 'Script Ambiances' in df_config.columns else ""
            script_format = df_config[df_config[col_format] == selected_format].iloc[0]['Script Formats/Ratios'] if 'Script Formats/Ratios' in df_config.columns else ""
            script_style = df_config[df_config['Styles Photo'] == selected_style].iloc[0]['Scripts Styles Photos'] if 'Scripts Styles Photos' in df_config.columns else ""
            script_scenario = df_config[df_config['Scénarios'] == selected_scenario].iloc[0]['Scripts Scénarios'] if 'Scripts Scénarios' in df_config.columns else ""
            script_personnage = df_config[df_config['Personnages'] == selected_personnage].iloc[0]['Script Personnages'] if 'Script Personnages' in df_config.columns else ""
            script_lumiere = df_config[df_config['Lumières'] == selected_lumiere].iloc[0]['Script Lumières'] if 'Script Lumières' in df_config.columns else ""
            
            def clean(text):
                return str(text).strip() if pd.notna(text) and str(text).lower() != 'nan' else ""

            prompt_final = (
                f"Utilise l'image fournie comme base visuelle absolue. Tu es un photographe publicitaire professionnel. "
                f"Contrainte stricte : Ne modifie en aucun cas le design, la forme ou les couleurs du produit.\n\n"
                f"Description : {clean(script_angle)}.\n"
                f"Ambiance : {clean(script_ambiance)}.\n"
                f"Scénario : {clean(script_scenario)}.\n"
                f"Personnage : {clean(script_personnage)}.\n"
                f"Lumière : {clean(script_lumiere)}.\n"
                f"Style : {clean(script_style)}.\n\n"
                f"Rendu : Photorealistic, 8k, highly detailed, sharp focus, commercial photography. "
                f"Format : {clean(script_format)}"
            )
            
            st.text_area("Copiez ce bloc de texte :", value=prompt_final, height=250)
            
            if st.button("💾 Sauvegarder ce prompt dans l'historique"):
                if prompt_final not in st.session_state["historique"]:
                    st.session_state["historique"].insert(0, prompt_final)
                    st.success("Prompt sauvegardé en bas de la page !")

        if len(st.session_state["historique"]) > 0:
            st.markdown("---")
            st.subheader("🕰️ Historique de votre session")
            
            for i, prompt_sauvegarde in enumerate(st.session_state["historique"][:3]):
                st.text_area(f"Sauvegarde #{len(st.session_state['historique']) - i}", value=prompt_sauvegarde, height=100, key=f"hist_{i}")
