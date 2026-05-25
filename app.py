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

    # Extraction des listes (Sécurisé)
    produits = df_data['Produit'].dropna().unique().tolist() if 'Produit' in df_data.columns else []
    angles = df_config['Angles'].dropna().unique().tolist() if 'Angles' in df_config.columns else []
    ambiances = df_config['Ambiances'].dropna().unique().tolist() if 'Ambiances' in df_config.columns else []
    formats = df_config['Formats/Ratios'].dropna().unique().tolist() if 'Formats/Ratios' in df_config.columns else []
    styles = df_config['Styles Photo'].dropna().unique().tolist() if 'Styles Photo' in df_config.columns else []
    scenarios = df_config['Scénarios'].dropna().unique().tolist() if 'Scénarios' in df_config.columns else []
    personnages = df_config['Personnages'].dropna().unique().tolist() if 'Personnages' in df_config.columns else []
    lumieres = df_config['Lumières'].dropna().unique().tolist() if 'Lumières' in df_config.columns else []

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
            # Logique d'affichage image (simplifiée)
            if sel_prod:
                infos = df_data[df_data['Produit'] == sel_prod].iloc[0]
                m_img = {"Face": "Image FACE", "Profil": "Image PROFIL", "Dessus": "Image DESSUS", "45°": "Image 45°"}
                col_c = m_img.get(sel_angle, "Image FACE")
                if col_c in infos:
                    st.image(infos[col_c], width=200)
            
            st.subheader("📝 3. Prompt Final")
            def get_s(df, col_s, val_s, col_r):
                m = df[df[col_s] == val_s]
                return str(m.iloc[0][col_r]) if not m.empty else ""
            
            p_final = f"Produit: {sel_prod}. Angle: {get_s(df_config, 'Angles', sel_angle, 'Scripts Angles')}. Ambiance: {get_s(df_config, 'Ambiances', sel_amb, 'Script Ambiances')}. Scénario: {get_s(df_config, 'Scénarios', sel_scen, 'Scripts Scénarios')}. Lumière: {get_s(df_config, 'Lumières', sel_lum, 'Script Lumières')}."
            st.text_area("Prompt:", value=p_final, height=250)
