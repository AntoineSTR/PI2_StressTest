import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px

from modules.stress_engine import apply_stress
from modules.analyzer import (
    summarize_by_scenario,
    summarize_by_poste,
    compare_to_base,
    top_5_variations,
    compute_cet1_ratio_by_scenario
)
from modules.ui_utils import show_intro, load_and_clean_data
from modules.eba_loader import load_eba_scenarios, get_stress_vector_for_zone, get_eba_map_data

st.set_page_config(page_title="💼 ALM Stress Testing", layout="wide")

# === Introduction
show_intro()

# === Fichiers d’entrée
st.sidebar.header("📂 Données à importer")
data_file = st.sidebar.file_uploader("1. Données ALM - Base.xlsx", type=["xlsx"])
stress_file = st.sidebar.file_uploader("2. Vecteurs de stress - vecteurs_stress.csv", type=["csv"])

# === Fichiers d'exemple
st.sidebar.markdown("📥 **Fichiers d’exemple à télécharger**")
try:
    with open("Base.xlsx", "rb") as f_base:
        st.sidebar.download_button("⬇️ Télécharger Base.xlsx", f_base, file_name="Base.xlsx")
    with open("vecteurs_stress.csv", "rb") as f_vec:
        st.sidebar.download_button("⬇️ Télécharger vecteurs_stress.csv", f_vec, file_name="vecteurs_stress.csv")
    with open("scenarios_eba.csv", "rb") as f_vec:
        st.sidebar.download_button("⬇️ Télécharger vecteurs_stress.csv", f_vec, file_name="scenarios_eba.csv")
except FileNotFoundError:
    st.sidebar.warning("❗ Fichiers d’exemple introuvables.")

# === Données par défaut si aucun fichier n’est chargé
if not data_file:
    st.info("📎 Données non chargées, fichier exemple utilisé.")
    data_file = "Base.xlsx"

if not stress_file:
    st.info("📎 Vecteurs non chargés, fichier exemple utilisé.")
    stress_file = "vecteurs_stress.csv"

# === Chargement des données
df, numeric_cols, dim3_col, scenario_col = load_and_clean_data(data_file)
stress_vectors = pd.read_csv(stress_file)

# === Sélection du scénario
st.sidebar.header("⚙️ Scénario de stress")
scenario_mode = st.sidebar.radio(
    "3. Mode de scénario",
    ["📄 Scénario personnalisé", "📁 Depuis vecteurs_stress.csv", "🌍 Scénario EBA par zone géographique"]
)

if scenario_mode == "📄 Scénario personnalisé":
    st.sidebar.subheader("🛠️ Paramètres du scénario personnalisé")
    selected_scenario = st.sidebar.text_input("Nom du scénario", "Scénario personnalisé")
    target = st.sidebar.text_input("Cible (ex: TLA, Crédit immobilier, ALL)", "ALL")
    taux = st.sidebar.slider("📉 Choc sur les taux (%)", -500, 500, 100)
    spread = st.sidebar.slider("📊 Choc sur les spreads (bps)", -500, 500, 0,
                               help="1 bps = 0,01% — utilisé pour mesurer les écarts de taux.")
    volume = st.sidebar.slider("📦 Choc sur le volume (%)", -100, 100, 0)
    duree = st.sidebar.slider("⏳ Choc sur la durée (%)", -100, 100, 0)

    stress_row = pd.Series({
        "Scenario Name": selected_scenario,
        "Target Column": target,
        "Taux Shock (%)": taux,
        "Spread Shock (bps)": spread,
        "Volume Shock (%)": volume,
        "Durée Shock (%)": duree
    })
    st.sidebar.success("✅ Scénario personnalisé prêt à être appliqué !")

elif scenario_mode == "📁 Depuis vecteurs_stress.csv":
    if "Scenario Name" not in stress_vectors.columns:
        st.sidebar.error("❌ Le fichier vecteurs_stress.csv ne contient pas la colonne 'Scenario Name'.")
    else:
        scenario_names = stress_vectors["Scenario Name"].dropna().tolist()
        selected_scenario = st.sidebar.selectbox("Choisissez un scénario prédéfini :", scenario_names)
        stress_row = stress_vectors[stress_vectors["Scenario Name"] == selected_scenario].iloc[0]
        st.sidebar.info(f"✅ Scénario sélectionné : {selected_scenario}")

elif scenario_mode == "🌍 Scénario EBA par zone géographique":
    try:
        eba_df = load_eba_scenarios("scenarios_eba.csv")
        selected_zone = st.sidebar.selectbox("Zone géographique EBA :", eba_df["Zone"].tolist())
        stress_row = get_stress_vector_for_zone(eba_df, selected_zone)
        selected_scenario = stress_row["Scenario Name"]
        st.sidebar.success(f"✅ Scénario appliqué : {selected_scenario}")
    except Exception as e:
        st.sidebar.error(f"❌ Erreur de chargement du scénario EBA : {e}")

# === Application du stress
stressed_df = apply_stress(df, stress_row, numeric_cols)
stressed_df["Applied Scenario"] = selected_scenario
df["Applied Scenario"] = "Base"
df_all = pd.concat([df, stressed_df], ignore_index=True)

# === Résumés
st.subheader("📊 Résumé des encours par scénario")
summary = summarize_by_scenario(df_all, numeric_cols)
st.dataframe(summary.style.format("{:,.0f}"))

# === Analyse ciblée
st.sidebar.header("🔍 Analyse ciblée")
postes = df[dim3_col].dropna().unique().tolist()
selected_poste = st.sidebar.selectbox("Choisissez un poste du bilan", postes)

st.subheader(f"🏦 Analyse ciblée : **{selected_poste}**")
agg_poste = summarize_by_poste(df_all, selected_poste, dim3_col, numeric_cols)
st.dataframe(agg_poste.style.format("{:,.0f}"))

# === Top 5 variations
st.subheader("📌 Top 5 variations (%) des postes impactés")
top_var = top_5_variations(df_all, dim3_col, numeric_cols)
if "Variation (%)" in top_var.columns:
    st.dataframe(top_var.style.format({"Variation (%)": "{:+.2f}%"}))
else:
    st.dataframe(top_var)

# === Comparaison avec Base
st.subheader("📉 Comparaison avec la base (%)")
ecarts = compare_to_base(agg_poste)
if ecarts is not None:
    st.dataframe(ecarts.style.format("{:+.2f}%"))
else:
    st.warning("⚠️ Scénario 'Base' manquant pour la comparaison.")

# === Graphique 1 : Encours total
st.subheader("📈 Évolution de l'encours total du poste")
fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=agg_poste.index,
    y=agg_poste["Total Poste"],
    marker_color='steelblue',
    name="Encours total"
))
fig1.update_layout(
    title=f"Encours total du poste '{selected_poste}'",
    xaxis_title="Scénario",
    yaxis_title="Montant (€)",
    template="plotly_white"
)
st.plotly_chart(fig1, use_container_width=True)

# === Carte interactive EBA
if scenario_mode == "🌍 Scénario EBA par zone géographique":
    st.subheader("🗺️ Carte interactive des scénarios EBA")
    map_data = get_eba_map_data("scenarios_eba.csv")
    fig_map = px.choropleth(
        map_data,
        locations="iso_alpha",
        color="Taux Shock (%)",
        hover_name="Zone",
        color_continuous_scale="Reds",
        title="Chocs sur les taux (%) par pays (EBA)"
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map, use_container_width=True)

# === Graphique 2 : Répartition temporelle
st.subheader("⏱️ Répartition des encours dans le temps")
scenario_to_plot = st.selectbox("Sélectionnez un scénario :", agg_poste.index.tolist())
buckets = [col for col in agg_poste.columns if col not in ["Total Poste"]]
values = agg_poste.loc[scenario_to_plot, buckets]
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=buckets,
    y=values,
    mode='lines+markers',
    name=scenario_to_plot,
    line=dict(color='orangered')
))
fig2.update_layout(
    title=f"Répartition temporelle – {scenario_to_plot}",
    xaxis_title="Bucket",
    yaxis_title="Montant (€)",
    template="plotly_white"
)
st.plotly_chart(fig2, use_container_width=True)

# === Analyse CET1 Ratio
st.subheader("🧮 Ratio de solvabilité CET1 (%)")
possible_cet1_cols = [col for col in df.columns if "CET1" in col]
possible_trea_cols = [col for col in df.columns if "Total Risk" in col or "TREA" in col]

if possible_cet1_cols and possible_trea_cols:
    cet1_col = st.selectbox("Colonne CET1 :", possible_cet1_cols)
    trea_col = st.selectbox("Colonne des expositions pondérées (TREA) :", possible_trea_cols)

    cet1_df = compute_cet1_ratio_by_scenario(df_all, cet1_col, trea_col)
    st.dataframe(cet1_df.style.format({
        cet1_col: "{:,.0f} €",
        trea_col: "{:,.0f} €",
        "CET1 Ratio (%)": "{:.2f} %"
    }))

    fig_cet1 = go.Figure()
    fig_cet1.add_trace(go.Bar(
        x=cet1_df.index,
        y=cet1_df["CET1 Ratio (%)"],
        marker_color='seagreen',
        name="Ratio CET1"
    ))
    fig_cet1.update_layout(
        title="📉 Ratio de solvabilité CET1 (%) par scénario",
        xaxis_title="Scénario",
        yaxis_title="CET1 Ratio (%)",
        template="plotly_white"
    )
    st.plotly_chart(fig_cet1, use_container_width=True)
else:
    st.warning("❗ Aucune colonne CET1 ou TREA détectée automatiquement dans les données.")

# === Export Excel
with st.expander("⬇️ Exporter les résultats Excel"):
    os.makedirs("output", exist_ok=True)
    output = agg_poste.reset_index()
    output.to_excel("output/analyse_poste.xlsx", index=False)
    with open("output/analyse_poste.xlsx", "rb") as f:
        st.download_button(
            label="📥 Télécharger l’analyse ciblée",
            data=f,
            file_name="analyse_poste.xlsx"
        )
