import streamlit as st
import pandas as pd
import requests

# Configuration de la page (on utilise tout l'écran)
st.set_page_config(page_title="Studio Promess", layout="wide")
st.title("📸 Studio Créatif Promess")
st.write("Générez vos prompts parfaits en quelques clics.")

# Chargement des ingrédients (tes fichiers CSV)
@st.cache_data
def load_data():
    df_data = pd.read_csv("DATA.csv")
    df_config = pd.read_csv("CONFIG.csv")
    return df_data, df_config

df_data, df_config = load_data()

# Séparation de l'écran en deux colonnes égales
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎛️ 1. Paramètres du Prompt")
    
    # 1. Choix du produit (depuis DATA.csv)
    produits = df_data['Produit'].dropna().unique()
    selected_produit = st.selectbox("📦 Choix du Produit", produits)
    
    # 2. Choix de l'Angle
    angles = df_config['Angles'].dropna().unique()
    selected_angle = st.selectbox("📐 Angle de vue", angles)
    
    # 3. Choix de l'Ambiance
    ambiances = df_config['Ambiances'].dropna().unique()
    selected_ambiance = st.selectbox("🏡 Ambiance", ambiances)
    
    # 4. Choix du Format (on gère la petite parenthèse du fichier d'origine)
    col_format = 'Formats/Ratios)' if 'Formats/Ratios)' in df_config.columns else 'Formats/Ratios'
    formats = df_config[col_format].dropna().unique()
    selected_format = st.selectbox("📐 Format (Ratio)", formats)
    
    # 5. Choix du Style Photo
    styles = df_config['Styles Photo'].dropna().unique()
    selected_style = st.selectbox("🎨 Style Photo", styles)
    
    # 6. Choix du Scénario
    scenarios = df_config['Scénarios'].dropna().unique()
    selected_scenario = st.selectbox("🎬 Scénario", scenarios)
    
    # 7. Choix du Personnage
    personnages = df_config['Personnages'].dropna().unique()
    selected_personnage = st.selectbox("👤 Personnage", personnages)
    
    # 8. Choix de la Lumière
    lumieres = df_config['Lumières'].dropna().unique()
    selected_lumiere = st.selectbox("💡 Éclairage / Lumière", lumieres)

with col2:
    st.subheader("🖼 Honoraires & Aperçu")
    
    # Recherche de l'image correspondante dans DATA.csv
    infos_produit = df_data[df_data['Produit'] == selected_produit].iloc[0]
    lien_image = infos_produit['Image FACE']
    
    # Affichage de la photo du produit
    if pd.notna(lien_image) and "http" in str(lien_image):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            reponse = requests.get(lien_image, headers=headers)
            st.image(reponse.content, width=200, caption=f"Aperçu de face : {selected_produit}")
        except:
            st.info(f"🔗 [Lien de l'image source]({lien_image})")
    else:
        st.warning("Aucune image de face trouvée pour ce produit.")

    st.subheader("📝 3. Prompt Final à copier")
    
    # Extraction de chaque petit bout de texte correspondant aux choix
    script_angle = df_config[df_config['Angles'] == selected_angle].iloc[0]['Scripts Angles']
    script_ambiance = df_config[df_config['Ambiances'] == selected_ambiance].iloc[0]['Script Ambiances']
    script_format = df_config[df_config[col_format] == selected_format].iloc[0]['Script Formats/Ratios']
    script_style = df_config[df_config['Styles Photo'] == selected_style].iloc[0]['Scripts Styles Photos']
    script_scenario = df_config[df_config['Scénarios'] == selected_scenario].iloc[0]['Scripts Scénarios']
    script_personnage = df_config[df_config['Personnages'] == selected_personnage].iloc[0]['Script Personnages']
    script_lumiere = df_config[df_config['Lumières'] == selected_lumiere].iloc[0]['Script Lumières']
    
    # Petite fonction magique pour nettoyer les textes vides (nan)
    def clean(text):
        return str(text).strip() if pd.notna(text) and str(text).lower() != 'nan' else ""

    # Construction du gros prompt final articulé
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
    
    # LA CORRECTION VISUELLE : Une grande boîte qui montre tout le texte d'un coup !
    st.text_area(
        label="Sélectionne tout le texte ci-dessous pour ton IA (Gemini / Flow / Midjourney) :",
        value=prompt_final,
        height=380 # Grande hauteur pour éviter la barre de défilement pénible
    )
