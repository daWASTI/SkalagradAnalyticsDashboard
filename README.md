# Skalagrad Analytics Dashboard

Analytics project for exploring player activity, rating behavior, matchmaking quality, and gameplay patterns in [Skalagrad](https://skalagrad.com)

## Overview

Quantifies aspects of the game often discussed qualitatively:

- Rating system convergence  
- Match fairness  
- Player stats across MMR bands  
- Playstyle patterns  
- Features for matchmaking improvement  

## Metrics

**Overview**: matches played, active players, user growth  
**Rating**: rating convergence, smoothed trends, TrueSkill comparison  
**Matchmaking**: match quality convergence, activity vs balance, benchmark for ideal matches  
**Player**: score, kills, assists vs MMR, close vs decisive matches  
**Team (planned)**: snowball effects, weapon combos, synergy, queue relationships  
**Feature Analysis (planned)**: 1vX potential, survivability, aggression, versatility, synergy  
**Playstyle Clusters (planned)**: player clustering, meta-clustering, evolution, t-SNE  
**Match Prediction (planned)**: outcome prediction via ensemble models  
**Live / Cached Data (planned)**: fast-loading cached analytics, near-live refreshes  

## Implementation Status

- **Implemented**: Dash app shell, MySQL preprocessing, overview/rating/matchmaking/player charts, custom Plotly theme  
- **Partial**: modular tabs, central preprocessing, cached data, reusable plotting/layout helpers  
- **Placeholder**: team metrics, feature analysis, playstyle clusters, match prediction  

## Tech Stack

Python, Dash, Plotly, Pandas, NumPy, SciPy, Statsmodels, SQLAlchemy, MySQL  

## Project Structure

```text
src/
  dashboard/
    app.py
    style.py
    assets/
    components/
  preprocessing/
  utils/
  ```
- `app.py` – dashboard entrypoint  
- `components/` – tab layouts & charts  
- `preprocessing/` – data preparation  
- `assets/` – styling & branding  

## Roadmap

- Wire full tab structure  
- Replace placeholders with real analyses  
- Expand player metrics (weapon/KDA)  
- Add team & synergy features  
- Build feature layer for clustering  
- Explore playstyle clusters  
- Prototype match prediction  
- Support live-refresh where relevant  
