import pandas as pd

def compute_cet1_ratio_by_scenario(df, cet1_col, trea_col):
    """
    Calcule le ratio CET1 par scénario : CET1 / TREA

    Parameters:
    - df : DataFrame contenant la colonne 'Applied Scenario'
    - cet1_col : nom de la colonne CET1 capital
    - trea_col : nom de la colonne des expositions pondérées (TREA)

    Returns:
    - DataFrame avec CET1, TREA, et ratio CET1 (%) par scénario
    """
    grouped = df.groupby("Applied Scenario")[[cet1_col, trea_col]].sum()
    grouped["CET1 Ratio (%)"] = (grouped[cet1_col] / grouped[trea_col]) * 100
    return grouped


def summarize_by_scenario(df, numeric_cols):
    """
    Agrège les encours par scénario sur les colonnes numériques.

    Parameters:
    - df : DataFrame avec colonne 'Applied Scenario'
    - numeric_cols : colonnes à agréger

    Returns:
    - DataFrame résumant les encours par scénario
    """
    summary = df.groupby("Applied Scenario")[numeric_cols].sum()
    summary["Total Encours"] = summary.sum(axis=1)
    return summary.sort_values("Total Encours", ascending=False)

def summarize_by_poste(df, poste, dim3_col, numeric_cols):
    """
    Agrège les encours d’un poste spécifique (ex : Crédit immo) par scénario.

    Parameters:
    - df : DataFrame avec la colonne de poste (ex: Dim3)
    - poste : nom du poste à filtrer
    - dim3_col : nom de la colonne des postes (ex: Dim3)
    - numeric_cols : colonnes à agréger

    Returns:
    - DataFrame avec l’agrégation par scénario pour ce poste
    """
    # Filtrage du poste
    df_poste = df[df[dim3_col].astype(str).str.contains(poste, case=False, na=False)]
    agg_poste = df_poste.groupby("Applied Scenario")[numeric_cols].sum()
    agg_poste["Total Poste"] = agg_poste.sum(axis=1)
    return agg_poste

def compare_to_base(agg_df):
    """
    Compare chaque scénario à la base (en % de variation).

    Parameters:
    - agg_df : DataFrame avec index par scénario, contenant 'Total Poste'

    Returns:
    - DataFrame des écarts relatifs (en %), ou None si Base manquant
    """
    if "Base" not in agg_df.index:
        return None  # base manquante

    base_row = agg_df.loc["Base"]
    ecarts = agg_df.div(base_row) - 1
    ecarts["Variation % Total Poste"] = ecarts["Total Poste"] * 100
    return ecarts.drop(index="Base")

def top_5_variations(df, dim3_col, numeric_cols):
    """
    Calcule les 5 postes les plus impactés entre Base et Scénario appliqué.

    Parameters:
    - df : DataFrame combiné avec Base + Scénario
    - dim3_col : nom de la colonne des postes
    - numeric_cols : colonnes numériques

    Returns:
    - DataFrame avec les 5 plus grandes variations (en %)
    """
    base_df = df[df["Applied Scenario"] == "Base"]
    scenario_df = df[df["Applied Scenario"] != "Base"]

    # Agrégation par poste
    base_grouped = base_df.groupby(dim3_col)[numeric_cols].sum().sum(axis=1)
    scenario_grouped = scenario_df.groupby(dim3_col)[numeric_cols].sum().sum(axis=1)

    # Jointure pour comparaison
    joined = pd.concat([base_grouped, scenario_grouped], axis=1)
    joined.columns = ["Base", "Scenario"]
    joined.dropna(inplace=True)

    # Variation relative
    joined["Variation (%)"] = ((joined["Scenario"] - joined["Base"]) / joined["Base"]) * 100
    top5 = joined.reindex(joined["Variation (%)"].abs().sort_values(ascending=False).index).head(5)

    return top5.reset_index().rename(columns={dim3_col: "Poste"})
