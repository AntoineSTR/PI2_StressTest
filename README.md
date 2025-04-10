# 💼 ALM Stress Testing App – Projet PI² ESILV

[![Streamlit App](https://img.shields.io/badge/🚀%20Streamlit-Live%20App-orange?logo=streamlit)](https://cryptodashboard-3bmggrrnlvk2tyyqpya3ny.streamlit.app)
[![GitHub Stars](https://img.shields.io/github/stars/AntoineSTR/PI2_StressTest?style=social)](https://github.com/AntoineSTR/PI2_StressTest)


Bienvenue sur l'application de **Stress Testing ALM** bancaire, développée dans le cadre du projet PI² de 4ᵉ année à l'ESILV (Majeure Ingénierie Financière).

L’objectif est de permettre une **analyse professionnelle** de scénarios macroéconomiques (type EBA/BCE), appliqués aux postes du bilan d'une banque, avec des résultats visuels, pédagogiques et exploitables.

---

## 🚀 Démo en ligne 

🌍 [Lien vers l'application en ligne](https://cryptodashboard-3bmggrrnlvk2tyyqpya3ny.streamlit.app/)

Etape : 
- Télécharger les fichiers disponibles dans la barre de gauche
- Choisir la catégorie de stress voulue
- Observer les résultats

---

## 📊 Fonctionnalités principales

| Fonctionnalité | Description |
|----------------|-------------|
| 📁 Import | Chargement de fichiers Excel (`Base.xlsx`) et CSV (`vecteurs_stress.csv`) + (`scenarios_eba.csv`) |
| 🌍 Scénarios EBA | Choix d’un pays de la zone euro → application automatique des chocs |
| 🗺️ Carte interactive | Carte de l’Europe montrant l’intensité des chocs par pays |
| 🛠️ Scénario personnalisé | Création manuelle d’un scénario avec sliders |
| 📉 Visualisation | Graphiques Plotly (encours total, répartition temporelle, ratio CET1) |
| 🧠 CET1 Ratio | Calcul automatique CET1 / TREA par scénario |
| 📌 Top variations | Affichage des postes les plus impactés |
| 📥 Export Excel | Téléchargement des résultats d’analyse |

---

## 🧰 Utilisation locale

### 1. Cloner le dépôt

```bash
git clone https://github.com/TON-UTILISATEUR/ton-repo.git
cd ton-repo
pip install -r requirements.txt
streamlit run app.py
```
L’interface s’ouvrira dans votre navigateur, prête à l’emploi.

---

## 📁 Arborescence du projet

```
.
├── app.py                        # Application principale
├── requirements.txt             # Dépendances Python
├── scenarios_eba.csv            # Scénarios EBA officiels
├── sample_data/
│   ├── Base.xlsx                # Données ALM d’exemple
│   └── vecteurs_stress.csv     # Scénarios personnalisés
├── modules/
│   ├── analyzer.py              # Fonctions d’analyse
│   ├── stress_engine.py         # Application des chocs
│   ├── ui_utils.py              # UI et nettoyage
│   └── eba_loader.py            # Chargement des scénarios EBA
```

---

## 🧠 Concepts abordés
- Stress testing ALM
- Chocs macroéconomiques (EBA)
- Ratio de solvabilité CET1
- Simulation d’impacts sur le bilan
- Interface no-code avec Streamlit
- Visualisation financière interactive (Plotly)
- Application pédagogique, proche du monde bancaire réel

## 👨‍🎓 Réalisation 
ESILV – Majeure Ingénierie Financière
Projet PI² A4 – Avril 2025