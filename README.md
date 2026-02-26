# CBR Assignment 3 – Case-Based Reasoning System

This project implements a Case-Based Reasoning (CBR) system for:
- **Classification**: Car Evaluation dataset
- **Regression**: Energy Efficiency dataset (predicting heating load)

It runs **6 evaluation conditions** (3 classification + 3 regression) as required by the assignment.

---

## Project Structure

```
Assignment3_KBAI/
├── main.py              # Runs all 6 test conditions
├── data_loader.py       # Loads datasets, normalizes, splits train/test
├── cbr_system.py        # Core similarity + retrieval + run_query
├── car_cbr.py           # Car classification system (weights + adaptation)
├── energy_cbr.py        # Energy regression system (weights + adaptation)
├── evaluation.py        # MAE/RMSE/Accuracy metrics
├── car.data             # Car Evaluation dataset
├── car.names            # Car dataset description
├── ENB2012_data.xlsx    # Energy Efficiency dataset
└── _PLANNING/           # Planning documents
```

---

## Requirements

- Python **3.11+** recommended
- Packages: `pandas`, `numpy`, `openpyxl`

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

---

## How to Run

Run the full evaluation (all 6 conditions):

```bash
python3 main.py
```

This will:
- Load both datasets
- Run all classification and regression conditions
- Print per-condition metrics
- Print a summary table and key findings

---

## How to Test Components (Optional)

You can run each module directly to sanity-check behavior:

```bash
python3 data_loader.py
python3 cbr_system.py
python3 car_cbr.py
python3 energy_cbr.py
python3 evaluation.py
```

---

## Output Explanation

### Classification (Car Evaluation)
- **Untuned**: baseline similarity (equal weights), no adaptation
- **Tuned**: weighted similarity, no adaptation
- **Tuned + Adaptation**: weighted similarity + rule-based adaptation

Metric: **Accuracy (%)**

### Regression (Energy Efficiency)
- **Untuned**: baseline similarity, no adaptation, learning ON
- **Tuned + Adaptation (Learning ON)**
- **Tuned + Adaptation (Learning OFF)**

Metrics: **MAE** and **RMSE**

---

## Notes

- Energy features are normalized (z-score) in `data_loader.py`.
- Tuned weights for energy are **computed from feature correlations** in `energy_cbr.py`.
- Adaptation rules are implemented in `car_cbr.py` and `energy_cbr.py`.

---

## Team Contribution

(Replace this section with your group’s division of labor)

- Member 1: Implementation + experiments
- Member 2: Report writing + analysis
- Member 3: Adaptation strategy + testing

---

## Reproducibility

Train/test split uses a fixed random seed (42) for reproducibility.

---

If you want me to generate the PDF report template or finalize team contribution text, just ask.
