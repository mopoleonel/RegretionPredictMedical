import streamlit as st
import pickle
import time
import  sklearn 
import numpy as np
from streamlit_extras.stylable_container import stylable_container

# --- Configuration de la Page ---
st.set_page_config(page_title="💰 Prédictions de Charges Médicales", page_icon="⚕️", layout='centered')

# --- Thème de Couleur Adapté (Santé/Finance) ---
primary_color = "#2E7D32"  # Vert foncé (santé, croissance financière)
secondary_color = "#1976D2"  # Bleu (confiance, professionnalisme)
background_color = "#F5F5F5"  # Gris clair (neutre, lisible)
text_color = "#212121"  # Noir foncé (lisibilité)
accent_color = "#FFC107"  # Jaune ambre (attention, résultats)
card_bg_color = "white"
border_radius = "0.5rem"
box_shadow = "0 0.125rem 0.25rem rgba(0, 0, 0, 0.075)"

# --- Styles CSS Personnalisés ---
st.markdown(
    f"""
    <style>
        body, .stApp {{
            color: {text_color};
            background-color: {background_color};
        }}
        .main {{
            background-color: {background_color};
            padding: 2rem;
        }}
        h1 {{
            color: {primary_color};
            text-align: center;
            margin-bottom: 2.5rem;
        }}
        h2 {{
            color: {secondary_color};
            margin-top: 2rem;
            border-bottom: 2px solid {secondary_color};
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }}
        .st-slider > div > div > div > div {{
            background-color: {card_bg_color};
            border: 1px solid #ced4da;
            border-radius: {border_radius};
            color: {text_color};
            padding: 0.5rem 1rem;
            font-size: 1rem;
            box-shadow: {box_shadow};
        }}
        .st-number-input > div > div > input {{
            background-color: {card_bg_color};
            border: 1px solid #ced4da;
            border-radius: {border_radius};
            color: {text_color};
            padding: 0.5rem;
            font-size: 1rem;
            box-shadow: {box_shadow};
        }}
        .st-selectbox > div > div > div > div {{
            background-color: {card_bg_color};
            border: 1px solid #ced4da;
            border-radius: {border_radius};
            color: {text_color};
            padding: 0.5rem 1rem;
            font-size: 1rem;
            box-shadow: {box_shadow};
        }}
        .st-button > button {{
            background-color: {secondary_color};
            color: white;
            border: none;
            border-radius: {border_radius};
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            box-shadow: {box_shadow};
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}
        .st-button > button:hover {{
            background-color: #1565C0;
        }}
        .st-success {{
            color: {primary_color};
            font-weight: bold;
            margin-top: 1rem;
        }}
        .st-spinner > div {{
            border-color: {primary_color};
            border-top-color: transparent;
        }}
        .st-markdown p, .st-markdown li {{
            color: {text_color};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Conteneur Principal ---
with stylable_container(key="main_container", css_styles=f"""
    padding: 2rem;
    border-radius: {border_radius};
    background-color: {background_color};
    box-shadow: {box_shadow};
"""):
    # --- Titre et Introduction ---
    st.title('⚕️ Prédictions des Charges Médicales')
    st.markdown('Veuillez renseigner les informations ci-dessous pour estimer les charges médicales.')

    # --- Chargement du Modèle avec Animation ---
    with st.spinner('Chargement du modèle...'):
        time.sleep(1)
        try:
            with open("reg.pkl", "rb") as file:
                model = pickle.load(file)
        except FileNotFoundError:
            st.error("Le fichier du modèle 'reg.pkl' n'a pas été trouvé.")
            st.stop()
        except Exception as e:
            st.error(f"Une erreur s'est produite lors du chargement du modèle : {e}")
            st.stop()

    st.subheader("Informations Patient")

    # --- Entrées Utilisateur en Colonnes ---
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider('Âge', 18, 100, 25)
        bmi = st.number_input('Indice de Masse Corporelle (BMI)', 10.0, 50.0, 25.0)
        smoker = st.selectbox("Fumeur ?", ['Non', 'Oui'])

    with col2:
        sex = st.selectbox('Sexe', ('Homme', 'Femme'))
        children = st.slider("Nombre d'enfants", 0, 5, 1)
        region = st.selectbox('Région', ['southwest', 'southeast', 'northeast', 'northwest'])

    # --- Encodage des Données ---
    sex_encoded = 1 if sex == 'Homme' else 0
    smoker_encoded = 1 if smoker == 'Oui' else 0
    region_dict = {'southwest': 0.2430, 'southeast': 0.2722, 'northeast': 0.2423, 'northwest': 0.2722}
    region_encoded = region_dict[region]

    # --- Préparation des Données pour la Prédiction ---
    input_data = [[age, sex_encoded, bmi, children, smoker_encoded, region_encoded]]
    prediction_placeholder = st.empty()

    # --- Bouton de Prédiction ---
    if st.button('Estimer les Charges Médicales'):
        with st.spinner('Calcul en cours...'):
            result = model.predict(input_data)[0]
            time.sleep(1)
        prediction_placeholder.success('✅ Prédiction Réussie !')
        prediction_placeholder.markdown(f"<h2 style='color:{accent_color};'>Les charges médicales estimées sont : <span style='font-weight: bold;'>{result:,.2f} USD</span></h2>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Application développée avec Streamlit.")