import streamlit as st
import pandas as pd
import requests
import os

# 1. Configuration (Doit être la toute première ligne)
st.set_page_config(page_title="Studio Promess", page_icon="🥛", layout="wide")

# 2. Injection de la Charte Graphique (CSS)
st.markdown("""
    <style>
    /* Fond général en blanc */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Couleur des titres en Bleu Promess */
    h1, h2, h3 {
        color: #0085C5 !important;
    }
    
    /* --- DESIGN DES LISTES DÉROULANTES (SELECTBOX) --- */
    /* Force la bordure et le fond des listes en Bleu Promess */
    div[data-baseweb="select"] {
        border: 2px solid #0085C5 !important;
        border-radius: 6px !important;
        background-color: #FFFFFF !important;
    }
    
    /* Force le texte à l'intérieur des listes en Bleu Promess */
    div[data-baseweb="select"] div {
        color: #0085C5 !important;
        font-weight: 500 !important;
    }
    
    /* Force la petite flèche de droite à devenir Bleue */
    div[data-baseweb="select"] svg {
        fill: #0085C5 !important;
    }
    
    /* Libellés au-dessus des listes (ex: "Produit Officiel") */
    .stSelectbox label p {
        color: #333333 !important;
        font-weight: bold !important;
    }
    /* ------------------------------------------------- */

    /* Style du bouton de téléchargement (Bleu de base, Vert au survol) */
    .stDownloadButton > button {
        background-color: #0085C5 !important;
        color: #FFFFFF !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    .stDownloadButton > button:hover {
        background-color: #A8C96A !important;
        color: #FFFFFF !important;
    }
    
    /* Style du bouton de connexion */
    .stButton > button {
        background-color: #0085C5 !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    .stButton > button:hover {
        background-color: #A8C96A !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Le système de Sécurité
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
                st.markdown("<h1 style='text-align: left;'>Studio Promess</h1>", unsafe_allow_html=True)
                
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

# 4. L'application principale
if check_password():
    
    # En-tête avec Logo
    col_logo, col_titre = st.columns([1, 4])
    with col_logo:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=150)
    with col_titre:
        st.title("Studio Créatif IA")
        st.markdown("**Générez vos campagnes visuelles en respectant la charte produit.**")

    st.markdown("---")

    # Chargement des ingrédients
    @st.cache_data
    def load_data():
        fichiers = os.listdir()
        f_data = next((f for f in fichiers if "data" in f.lower() and f.endswith(".csv")), None)
        f_config = next((f for f in fichiers if "config" in f.lower() and f.endswith(".csv")), None)
        
        if not f_data or not f_config:
            st.error("🚨 Base de données introuvable.")
            st.stop()
            
        return pd.read_csv(f_data), pd.read_csv(f_config)

    df_data, df_config = load_data()

    # Mise en page
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🎛️ 1. Configuration du Shoot")
        
        produits = df_data['Produit'].dropna().unique()
        selected_produit = st.selectbox("📦 Produit Officiel", produits)
        
        angles = df_config['Angles'].dropna().unique()
        selected_angle = st.selectbox("📐 Angle Caméra", angles)
        
        ambiances = df_config['Ambiances'].dropna().unique()
        selected_ambiance = st.selectbox("🏡 Set Design (Ambiance)", ambiances)
        
        col_format = 'Formats/Ratios)' if 'Formats/Ratios)' in df_config.columns else 'Formats/Ratios'
        formats = df_config[col_format].dropna().unique()
        selected_format = st.selectbox("📱 Format de sortie", formats)
        
        styles = df_config['Styles Photo'].dropna().unique()
        selected_style = st.selectbox("🎨 Direction Artistique", styles)
        
        scenarios = df_config['Scénarios'].dropna().unique()
        selected_scenario = st.selectbox("🎬 Action / Scénario", scenarios)
        
        personnages = df_config['Personnages'].dropna().unique()
        selected_personnage = st.selectbox("👤 Casting", personnages)
        
        lumieres = df_config['Lumières'].dropna().unique()
        selected_lumiere = st.selectbox("💡 Éclairage Studio", lumieres)

    with col2:
        st.subheader("🖼️ 2. Asset Visuel")
        
        infos_produit = df_data[df_data['Produit'] == selected_produit].iloc[0]
        lien_image = infos_produit['Image FACE']
        
        if pd.notna(lien_image) and "http" in str(lien_image):
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                reponse = requests.get(lien_image, headers=headers)
                st.image(reponse.content, width=200)
                
                st.download_button(
                    label="⬇️ Télécharger l'Asset Officiel",
                    data=reponse.content,
                    file_name=f"ASSET_{selected_produit.replace(' ', '_')}.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )
            except:
                st.info("Aperçu non disponible (Sécurité Drive).")
        
        st.subheader("📝 3. Prompt Final")
        
        script_angle = df_config[df_config['Angles'] == selected_angle].iloc[0]['Scripts Angles']
        script_ambiance = df_config[df_config['Ambiances'] == selected_ambiance].iloc[0]['Script Ambiances']
        script_format = df_config[df_config[col_format] == selected_format].iloc[0]['Script Formats/Ratios']
        script_style = df_config[df_config['Styles Photo'] == selected_style].iloc[0]['Scripts Styles Photos']
        script_scenario = df_config[df_config['Scénarios'] == selected_scenario].iloc[0]['Scripts Scénarios']
        script_personnage = df_config[df_config['Personnages'] == selected_personnage].iloc[0]['Script Personnages']
        script_lumiere = df_config[df_config['Lumières'] == selected_lumiere].iloc[0]['Script Lumières']
        
        def clean(text):
            return str(text).strip() if pd.notna(text) and str(text).lower() != 'nan' else ""

        prompt_final = (
            f"Utilise l'image fournie comme base visuelle absolue. "
            f"Tu es un photographe publicitaire professionnel. "
            f"Contrainte stricte : Ne modifie en aucun cas le design, the forme ou les couleurs du produit.\n\n"
            f"Description : {clean(script_angle)}.\n"
            f"Ambiance : {clean(script_ambiance)}.\n"
            f"Scénario : {clean(script_scenario)}.\n"
            f"Personnage : {clean(script_personnage)}.\n"
            f"Lumière : {clean(script_lumiere)}.\n"
            f"Style : {clean(script_style)}.\n\n"
            f"Rendu : Photorealistic, 8k, highly detailed, sharp focus, commercial photography. "
            f"Format : {clean(script_format)}"
        )
        
        st.text_area(
            label="Copiez ce bloc de texte :",
            value=prompt_final,
            height=300
        )
