import pandas as pd

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
