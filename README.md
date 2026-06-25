# Press Freedom Analysis (2013–2021)

Exploratory analysis of global press freedom patterns using the [Reporters Without Borders (RSF) Press Freedom Index](https://rsf.org/en/index), covering 179 countries over nine years.

## Live Dashboard 

An interactive Streamlit dashboard is available for exploring:
- Global trends over time
- Country-level trajectories
- Regional comparisons
- Clustering results
- Statistical summaries

https://press-freedom-dashboard.streamlit.app/

![Dashboard](outputs/press_freedom_dashboard.png)

---

## Research questions

1. How has press freedom evolved globally between 2013 and 2021?
2. Are there statistically significant differences between world regions?
3. Which countries experienced the largest improvements or deteriorations?
4. Can countries be grouped into meaningful clusters based on press freedom patterns?

> **Note:** Higher RSF scores indicate *worse* press freedom. An increase represents deterioration, while a decrease represents improvement.

---

## Methods

- **Data acquisition:** Public API (Our World in Data)
- **Data cleaning:** pandas (type handling, missing values, validation)
- **Exploratory analysis:** distribution analysis, normality testing (D’Agostino K²)
- **Regional comparison:** Kruskal–Wallis test + effect size (ε²)
- **Time-series analysis:** global trends, year-to-year stability, country-level change
- **Clustering:** K-Means (k=4), StandardScaler, silhouette score evaluation
- **Visualization:** matplotlib, seaborn, Plotly Express

---

## Key findings

- **Country rankings are highly stable over time** (year-to-year correlation ≈ 0.99), with gradual rather than abrupt changes.
- **Strong regional differences exist**, with statistically significant variation between world regions (ε² = 0.478).
- Northern and Western Europe consistently show the lowest (best) press freedom scores, while parts of Africa, the Middle East, and Asia show the highest (worst).
- **Four distinct country profiles emerge** from clustering, ranging from stable free environments to severely constrained systems, including a group showing long-term improvement.
- Overall, press freedom changes are **slow-moving and structurally persistent** rather than volatile year-to-year shifts.

---

## Why this matters

This project demonstrates how statistical analysis and machine learning can be used to uncover structural patterns in global institutional indicators, highlighting long-term regional disparities and stability in governance-related metrics.

---

## Project structure


```
press-freedom-analysis/
│
├── data/
│   └── clean_press_freedom.csv 
│
├── outputs/
│   ├── country_features.csv       
│   └── press_freedom_dashboard.png  
│
├── notebooks/
│   └── press_freedom_analysis.ipynb 
│
├── app/
│   └── streamlit_app.py 
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Reproducing the analysis

**Requirements:** Python 3.9+

```bash
git clone https://github.com/lant96/press-freedom-analysis.git
cd press-freedom-analysis
pip install -r requirements.txt
jupyter notebook notebooks/press_freedom_analysis.ipynb
```

The notebook fetches data directly from the Our World in Data API on first run — no manual download needed.

To run the interactive dashboard locally:
```bash
streamlit run app/streamlit_app.py
```

---

## Requirements

See [`requirements.txt`](requirements.txt). Core dependencies:

- `pandas`, `numpy`
- `matplotlib`, `seaborn`, `plotly`
- `scipy`, `scikit-learn`
- `country_converter`

---

## Data source

Reporters Without Borders — *Press Freedom Index*, via [Our World in Data](https://ourworldindata.org/press-freedom).

The index is a composite expert-based metric. Results reflect associations rather than causal mechanisms, and changes in score do not necessarily indicate changes in underlying media conditions alone.

---

## Limitations

- Limited to 2013–2021
- No external covariates (GDP, democracy indices)
- Regional grouping is simplified (UN macro-regions)
- Index methodology may vary over time, affecting strict comparability
---

## License

MIT