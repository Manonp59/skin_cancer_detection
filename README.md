# Détection de Cancer de la Peau

Bienvenue dans le projet de détection de cancer de la peau ! Cette application utilise Streamlit pour fournir une interface permettant de détecter le cancer de la peau à partir d'images dermatologiques.

## Description

La détection précoce du cancer de la peau est cruciale pour assurer un traitement efficace. Cette application utilise un modèle de détection basé sur l'algorithme YOLO (You Only Look Once) pour identifier si les mélanomes sont bégnins ou malins.

## Fonctionnalités

- Chargement et affichage d'images dermatologiques
- Détection des lésions cutanées à l'aide de l'algorithme YOLO
- Affichage des résultats de détection avec des cadres autour des lésions

## Prérequis

- Python 3.11
- Bibliothèques Python : Streamlit, PIL, ultralytics, pandas, etc. (voir le fichier `requirements.txt` pour la liste complète des dépendances)

## Installation

1. Clonez ce dépôt sur votre machine locale :

git clone https://github.com/Manonp59/skin_cancer_detection.git

2. Accédez au répertoire du projet :

cd skin_cancer_detection

3. Installez les dépendances nécessaires :

pip install -r requirements.txt

4. Lancez l'application Streamlit :

streamlit run streamlit.py

## Licence

Ce projet est distribué sous la licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.
