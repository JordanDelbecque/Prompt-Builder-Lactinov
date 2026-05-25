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
            st.markdown("### Portail
