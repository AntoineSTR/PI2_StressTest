import pandas as pd

def apply_stress(df, stress_row, numeric_cols):
    """
    Applique les chocs d’un scénario à un DataFrame ALM sur les colonnes numériques spécifiées.

    Parameters:
    - df : DataFrame source (avec colonnes comme 'Dim3', 'INDEX', etc.)
    - stress_row : ligne du scénario contenant les paramètres de choc
    - numeric_cols : liste des colonnes numériques à impacter

    Returns:
    - df_copy : DataFrame avec les stress appliqués
    """
    # Récupération des paramètres du scénario
    target = str(stress_row["Target Column"])
    taux = stress_row.get("Taux Shock (%)", 0) / 100       # En pourcentage
    spread = stress_row.get("Spread Shock (bps)", 0) / 10000  # En pourcentage aussi
    volume = stress_row.get("Volume Shock (%)", 0) / 100
    duree = stress_row.get("Durée Shock (%)", 0) / 100

    # Copie de sécurité du DataFrame original
    df_copy = df.copy()

    # === Création du masque pour identifier les lignes à impacter ===
    mask = pd.Series(False, index=df.index)

    if "Dim3" in df.columns:
        mask |= df["Dim3"].astype(str).str.lower().str.contains(target.lower(), na=False)

    if "INDEX" in df.columns and "tla" in target.lower():
        mask |= df["INDEX"].astype(str).str.lower().str.contains("tla", na=False)

    if target.lower() == "all":
        mask = pd.Series(True, index=df.index)

    # === Application vectorisée des stress ===
    # Facteur de stress commun (taux + spread + volume)
    total_shock_factor = 1 + taux + spread + volume

    # Application du facteur de stress sur toutes les colonnes numériques
    df_copy.loc[mask, numeric_cols] = df_copy.loc[mask, numeric_cols].astype(float) * total_shock_factor

    # === Application du choc de durée, s’il existe ===
    if duree != 0:
        # Pondération progressive sur les buckets : plus c’est tard, plus c’est impacté
        weights = [(1 + duree) ** (i / len(numeric_cols)) for i in range(len(numeric_cols))]
        df_copy.loc[mask, numeric_cols] = df_copy.loc[mask, numeric_cols].multiply(weights, axis=1)

    return df_copy
