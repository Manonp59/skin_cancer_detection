import streamlit as st
from PIL import Image,ImageDraw
from ultralytics import YOLO


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
    


    return annotated_image


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



def main():
    # Ajuster la largeur de la page
    st.set_page_config(layout="wide")
    
    st.title("YOLOv8 Skin Cancer Detection")

    # Afficher l'interface utilisateur pour télécharger une image
    uploaded_image = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])

    if uploaded_image is not None:
        
        col1, col2 = st.columns(2)
        
        # Afficher l'image originale
        col1.image(uploaded_image, caption="Original Image", use_column_width=True)

        # Effectuer la détection des objets et afficher l'image annotée
        # annotated_image = detect_objects(uploaded_image)
        # st.image(annotated_image, caption="Annotated Image", use_column_width=True)

        # Convertir l'image en format attendu par YOLOv8
        img = Image.open(uploaded_image).convert('RGB')
        results = model(img)
        col2.image(results[0].plot())
        
        label = label_image(uploaded_image)
        if label == 'maliganent':
            st.write('Malin')
        else : 
            st.write('Bénin')
    
        
    

if __name__ == '__main__':
    main()

