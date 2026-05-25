import streamlit as st
import pandas as pd
import requests
import os

# 1. Configuration initiale
st.set_page_config(page_title="Studio Promess", page_icon="🥛", layout="wide")

# 2. CSS pour les boutons bleus et verts
st.markdown("""
    <style>
    .stButton > button { background-color: #0085C5 !important; color: #FFFFFF !important; border: none !important; }
    .stButton > button:hover { background-color: #A8C96A !important; }
    .stDownloadButton > button { background-color: #0085C5 !important; color: #FFFFFF !important; border: none !important; width: 100%; }
    .stDownloadButton > button:hover { background-color: #A8C96A !important; }
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
            st.markdown("<h1 style='color:#0085C5;'>Studio Promess</h1>", unsafe_allow_html=True)
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
    st.title("Studio Créatif IA")
    st.markdown("---")

    def load_data():
        fichiers = os.listdir()
        f_data = next((f for f in fichiers if "data" in f.lower() and f.endswith(".csv")), None)
        f_config = next((f for f in fichiers if "config" in f.lower() and f.endswith(".csv")), None)
        if not f_data or not f_config:
            st.error("🚨 Fichiers CSV introuvables.")
            st.stop()
        df_d = pd.read_csv(f_data).dropna(how='all')
        df_c = pd.read_csv(f_config).dropna(how='all')
        df_d.columns = [str(col).strip() for col in df_d.columns]
        df_c.columns = [str(col).strip() for col in df_c.columns]
        return df_d, df_c

    df_data, df_config = load_data()

    # Fonction pour extraire les options d'une catégorie
    def get_options(cat):
        return df_config[df_config['Categorie'] == cat]['Option'].unique().tolist()

    # Extraction des listes depuis le nouveau format
    produits = df_data['Produit'].dropna().unique().tolist() if 'Produit' in df_data.columns else []
    angles = get_options('Angles')
    ambiances = get_options('Ambiances')
    formats = get_options('Formats/Ratios')
    styles = get_options('Styles Photo')
    scenarios = get_options('Scénarios')
    personnages = get_options('Personnages')
    lumieres = get_options('Lumières')

    tab_studio, tab_guide = st.tabs(["📸 Studio Créatif", "📖 Guide d'utilisation"])

    with tab_studio:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🎛️ 1. Configuration")
            sel_prod = st.selectbox("Produit", produits)
            sel_angle = st.selectbox("Angle", angles)
            sel_amb = st.selectbox("Ambiance", ambiances)
            sel_form = st.selectbox("Format", formats)
            sel_style = st.selectbox("Style", styles)
            sel_scen = st.selectbox("Scénario", scenarios)
            sel_perso = st.selectbox("Casting", personnages)
            sel_lum = st.selectbox("Lumière", lumieres)

        with col2:
            st.subheader("🖼️ 2. Asset Visuel")
            if sel_prod:
                infos = df_data[df_data['Produit'] == sel_prod].iloc[0]
                colonnes_images = {"Face": "Image FACE", "Profil": "Image PROFIL", "Dessus": "Image DESSUS", "45°": " Image 45°"}
                col_c = colonnes_images.get(sel_angle, "Image FACE")
                if col_c in infos and pd.notna(infos[col_c]):
                    try:
                        session = requests.Session()
                        session.headers.update({'User-Agent': 'Mozilla/5.0'})
                        reponse = session.get(infos[col_c])
                        st.image(reponse.content, width=400)
                        st.download_button("⬇️ Télécharger l'Asset", data=reponse.content, file_name=f"{sel_prod}.jpg", mime="image/jpeg")
                    except:
                        st.warning("Impossible d'afficher l'image.")
            
            st.subheader("📝 3. Prompt Final")
            
            # Fonction pour récupérer le script selon la catégorie et l'option
            def get_s(cat, opt):
                match = df_config[(df_config['Categorie'] == cat) & (df_config['Option'] == opt)]
                return str(match.iloc[0]['Script']) if not match.empty else ""
            
            p_final = (f"Produit: {sel_prod}. "
                       f"Angle: {get_s('Angles', sel_angle)}. "
                       f"Ambiance: {get_s('Ambiances', sel_amb)}. "
                       f"Scénario: {get_s('Scénarios', sel_scen)}. "
                       f"Personnage: {get_s('Personnages', sel_perso)}. "
                       f"Lumière: {get_s('Lumières', sel_lum)}.")
            
            st.text_area("Prompt:", value=p_final, height=250)
            if st.button("💾 Sauvegarder"):
                st.session_state["historique"].insert(0, p_final)
                st.success("Sauvegardé !")
