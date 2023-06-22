import streamlit as st
from PIL import Image,ImageDraw
from ultralytics import YOLO
import pandas as pd
import os
import random
import string

model = YOLO('best2.pt')

def detect_objects(image):
    # Convertir l'image en format attendu par YOLOv8
    img = Image.open(image).convert('RGB')

    # Effectuer la détection des objets
    results = model(img)

    # Obtenir les coordonnées des boîtes englobantes et les classes prédites
    boxes = results[0].boxes.xyxy[0].cpu().numpy()
    labels = results[0].names

    # Obtenir le label à partir du tenseur cls
    label_id = int(results[0].boxes.cls[0])  # Récupère la valeur du tenseur cls
    label = labels[label_id]  # Obtient le label correspondant à l'indice de classe prédite

    # Annoter l'image avec les boîtes englobantes
    annotated_image = img.copy()
    draw = ImageDraw.Draw(annotated_image)
    x_min, y_min, x_max, y_max = boxes[:4]
    draw.rectangle([(x_min, y_min), (x_max, y_max)], outline='red')
    draw.text((x_min, y_min), label, fill='red')
    


    return annotated_image, label


def label_image(image):
    # Convertir l'image en format attendu par YOLOv8
    img = Image.open(image).convert('RGB')

    # Effectuer la détection des objets
    results = model(img)

    # Obtenir les coordonnées des boîtes englobantes et les classes prédites
    boxes = results[0].boxes.xyxy[0].cpu().numpy()
    labels = results[0].names

    # Obtenir le label à partir du tenseur cls
    label_id = int(results[0].boxes.cls[0])  # Récupère la valeur du tenseur cls
    label = labels[label_id]  # Obtient le label correspondant à l'indice de classe prédite
    
    return label 

def save_prediction(date, patient_name, prediction,annotated_image):
    
    # Générer un ID unique pour la prédiction
    prediction_id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
    
    data = {'Date': [date],
            'Patient Name': [patient_name],
            'Prediction': [prediction],
            'Prediction ID': [prediction_id]}
    
    df = pd.DataFrame(data)
    
    # Charger le fichier CSV existant ou créer un nouveau fichier s'il n'existe pas
    try:
        df_existing = pd.read_csv('predictions.csv')
        df = pd.concat([df_existing, df], ignore_index=True)
    except FileNotFoundError:
        pass
    
    # Enregistrer les prédictions dans le fichier CSV
    df.to_csv('predictions.csv', index=False)
    
    # Convertir le tableau NumPy en image PIL
    annotated_image_pil = Image.fromarray(annotated_image)

    # Enregistrer l'image annotée
    annotated_image_pil.save(f'annotated_images/{patient_name}_{date}_{prediction_id}.jpg')

def search_predictions(patient_name):
    try:
        df = pd.read_csv('predictions.csv')
        filtered_df = df[(df['Patient Name'] == patient_name)]
        return filtered_df
    except FileNotFoundError:
        return pd.DataFrame()

def get_patient_names():
    try:
        df = pd.read_csv('predictions.csv')
        return df['Patient Name'].unique().tolist()
    except FileNotFoundError:
        return []

def make_predictions():
    label = None
    annotated_image = None

    # Afficher l'interface utilisateur pour télécharger une image
    uploaded_image = st.file_uploader("Charger une image", type=['jpg', 'jpeg', 'png'],key="uploader")

    if uploaded_image is not None:
        
        col1, col2 = st.columns(2)
        
        # Afficher l'image originale
        col1.image(uploaded_image, caption="Image originale", use_column_width=True)

        # Effectuer la détection des objets et afficher l'image annotée
        # annotated_image = detect_objects(uploaded_image)
        # st.image(annotated_image, caption="Annotated Image", use_column_width=True)

        # Convertir l'image en format attendu par YOLOv8
        img = Image.open(uploaded_image).convert('RGB')
        results = model(img)
        annotated_image = results[0].plot()
        col2.image(annotated_image, caption="Image annotée", use_column_width=True)
        
        # Ajouter du style CSS à l'aide de balises HTML et de la fonction st.markdown
        st.markdown("""
            <style>
                h2 {
                   color: blue;
                   text-align: center;
             }
                .bad {
                    color:red;
                    text-align:center;
                }
                
                .good {
                    color:green;
                    text-align:center;
                }
                
            </style>
    """, unsafe_allow_html=True)

        # Utiliser la balise h2 avec le style appliqué
        st.markdown('<h2>Résultat</h2>', unsafe_allow_html=True)
        label = label_image(uploaded_image)
        if label == 'maliganent':
            st.write('<h3 class="bad">Malin</h3>',unsafe_allow_html=True)
        else : 
            st.write('<h3 class="good">Bénin</h3>', unsafe_allow_html=True)

    
    return annotated_image, label

def enregistrement():
    annotated_image,label = make_predictions()
    # Formulaire pour saisir la date, le nom du patient et la prédiction
    st.write('<h3>Enregistrer vos résultats</h3>', unsafe_allow_html=True)
    date = st.date_input("Date")   
    nom = st.text_input("Nom")   

    
    
    # Bouton pour enregistrer la prédiction
    if st.button("Enregistrer"):
        save_prediction(date, nom, label,annotated_image)
        st.success("Prédiction enregistrée avec succès!")
        
def view_predictions():
    st.title("Historique")

    # Récupérer la liste des noms des patients
    patient_names = get_patient_names()
    patient_name = st.selectbox("Nom du patient", patient_names)

    if st.button("Rechercher"):
        results = search_predictions(patient_name)

        if not results.empty:
            st.write("Résultats pour", patient_name)

            # Créer un tableau pour afficher les résultats
            table_data = {
                "Date": results["Date"],
                "Patient Name": results["Patient Name"],
                "Prediction": results["Prediction"]
            }

            # Afficher le tableau des résultats
            st.table(pd.DataFrame(table_data))
            
            # Parcourir chaque prédiction
            for index, row in results.iterrows():
                date = row['Date']
                prediction_id = row['Prediction ID']

                # Construire le chemin de l'image en utilisant l'ID de prédiction
                image_path = f"annotated_images/{patient_name}_{date}_{prediction_id}.jpg"

                # Vérifier si l'image existe avant de l'afficher
                if os.path.exists(image_path):
                    annotated_image = Image.open(image_path)
                    st.image(annotated_image, caption=f"Image annotée pour {patient_name} - {date}",
                             use_column_width=True)
                else:
                    st.write(f"Aucune image trouvée pour la prédiction {prediction_id}")
        else:
            st.write("Aucun résultat trouvé pour", patient_name)


def main():
    st.title("Détection cancer de la peau")

    # Création des onglets
    tabs = ["Analyse photo", "Historique"]
    selected_tab = st.selectbox("Sélectionner un onglet", tabs)

    if selected_tab == "Analyse photo":
        enregistrement()
    elif selected_tab == "Historique":
        view_predictions()
    

if __name__ == '__main__':
    main()

