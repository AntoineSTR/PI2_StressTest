import pandas as pd
import pycountry

def get_eba_map_data(csv_path):
    """
    Prépare les données de scénarios EBA pour affichage sur carte.

    Returns:
    - df : DataFrame avec colonne 'iso_alpha' (code pays 3 lettres) + intensité de choc
    """
    df = pd.read_csv(csv_path)
    df["iso_alpha"] = df["Zone"].apply(lambda x: get_country_code(x))
    return df

def get_country_code(name):
    """
    Convertit le nom d’un pays (France, Germany, etc.) en code ISO alpha-3 pour Plotly.
    """
    try:
        return pycountry.countries.lookup(name).alpha_3
    except:
        return None

def load_eba_scenarios(csv_path):
    """
    Charge le fichier des scénarios EBA et retourne la liste des zones disponibles.
    """
    df = pd.read_csv(csv_path)
    return df

def get_stress_vector_for_zone(df, zone_name):
    """
    Retourne le vecteur de stress EBA sous forme de Series pour une zone donnée.

    Parameters:
    - df : DataFrame contenant les scénarios
    - zone_name : nom exact de la zone à récupérer (ex: 'France', 'Euro Area')

    Returns:
    - pd.Series compatible avec apply_stress()
    """
    row = df[df["Zone"] == zone_name].iloc[0]
    return pd.Series({
        "Scenario Name": f"EBA_Adverse_2023_{zone_name}",
        "Target Column": "ALL",
        "Taux Shock (%)": row["Taux Shock (%)"],
        "Spread Shock (bps)": row["Spread Shock (bps)"],
        "Volume Shock (%)": row["Volume Shock (%)"],
        "Durée Shock (%)": row["Durée Shock (%)"]
    })
