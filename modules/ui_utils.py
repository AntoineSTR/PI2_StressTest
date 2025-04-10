import streamlit as st
import pandas as pd

def show_intro():
    """
    Affiche l’introduction et les instructions de l’application Streamlit.
    """
    st.title("💼 Plateforme de Stress Testing ALM")
    st.markdown("""
    Cette application permet de :
    - Importer des **données ALM** (Base.xlsx)
    - Appliquer des **scénarios de stress** (taux, spread, volume, durée)
    - Visualiser les **résultats par scénario ou par poste**
    - Comparer les impacts avec la situation de base
    - Exporter les analyses en **Excel**

    👉 Laissez-vous guider étape par étape dans la **sidebar** à gauche.
    """)

def load_and_clean_data(data_file):
    """
    Charge le fichier Excel ALM, nettoie les colonnes, extrait les colonnes utiles.

    Parameters:
    - data_file : fichier uploadé par l’utilisateur (xlsx)

    Returns:
    - df : DataFrame nettoyé
    - numeric_cols : liste des colonnes numériques à analyser
    - dim3_col : colonne représentant les postes du bilan
    - scenario_col : colonne identifiant les scénarios
    """
    try:
        raw_df = pd.read_excel(data_file, skiprows=2)
        df = raw_df.iloc[1:].copy()
        new_header = raw_df.iloc[0]

        # Renommage intelligent
        df.columns = [
            f"{col}_{i}" if list(new_header).count(col) > 1 else str(col)
            for i, col in enumerate(new_header)
        ]
        df.reset_index(drop=True, inplace=True)

        # Suppression des lignes sans scénario
        scenario_col = [col for col in df.columns if "Scenario id" in col][0]
        df = df[df[scenario_col].notna()]
        df.dropna(axis=1, how="all", inplace=True)

        # Détection des colonnes numériques
        numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
        if scenario_col in numeric_cols:
            numeric_cols.remove(scenario_col)

        # Détection automatique de la colonne des postes
        dim3_col = [col for col in df.columns if "Dim3" in col][0]

        st.success("✅ Fichier ALM chargé et préparé avec succès.")
        return df, numeric_cols, dim3_col, scenario_col

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données : {e}")
        return None, [], "", ""
