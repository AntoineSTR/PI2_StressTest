# 💼 ALM Stress Testing App — Projet PI² ESILV

Cette application permet de simuler et analyser des **stress tests bancaires** appliqués aux données ALM, en s’appuyant sur des scénarios personnalisés ou officiels (EBA 2023).

---

## 🎯 Objectif

> Offrir une plateforme professionnelle pour visualiser l’impact de chocs macroéconomiques (taux, spreads, volumes...) sur les postes du bilan bancaire.

---

## ⚙️ Fonctionnalités

- 📁 Import de données ALM (`Base.xlsx`)
- 📊 Choix du scénario de stress :
  - Scénario personnalisé
  - Scénario prédéfini (`vecteurs_stress.csv`)
  - Scénario officiel EBA 2023 (`scenarios_eba.csv`)
- 🧠 Application automatique des chocs sur :
  - Taux d’intérêt
  - Spread de crédit
  - Volume
  - Durée
- 🔍 Analyse ciblée par poste du bilan (`Dim3`)
- 📉 Comparaison avant / après stress
- 📌 Top 5 des postes les plus impactés
- 🧮 Calcul automatique du ratio **CET1 / TREA**
- 📈 Graphiques interactifs (Plotly)
- 📥 Export Excel des résultats

---

## 🏁 Lancer l’application en ligne

**Lien Internet** : https://cryptodashboard-3bmggrrnlvk2tyyqpya3ny.streamlit.app/

---

## 🏁 Lancer l’application localement

### 1. Cloner le repo

```bash
git clone https://github.com/AntoineSTR/PI2_StressTest.git
cd PI2_StressTest
