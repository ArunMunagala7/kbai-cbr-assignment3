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

**Step 1** – Activate the virtual environment (first time or new terminal):
```bash
source .venv/bin/activate
```

**Step 2** – Install dependencies (only needed once):
```bash
pip install -r requirements.txt
```

**Step 3** – Run the full evaluation (all 6 conditions):
```bash
python main.py
```

This will:
- Load both datasets
- Run all classification and regression conditions
- Print per-condition metrics
- Print a summary table and key findings

---

## Workflow (What Happens End-to-End)

1. **Load data** (`data_loader.py`)
	- Reads `car.data` and `ENB2012_data.xlsx`
	- Builds `Case` objects
	- Normalizes energy features (z-score)
	- Splits into train/test (80/20)

2. **Initialize systems** (`car_cbr.py`, `energy_cbr.py`)
	- Sets feature types (categorical vs numerical)
	- Sets baseline and tuned weights
	- Builds the initial case base (training set)

3. **Run six conditions** (`main.py`)
	- **Cars**: baseline, tuned, tuned+adaptation
	- **Energy**: baseline (learn), tuned+adapt (learn), tuned+adapt (no learn)

4. **Retrieve + Adapt** (`cbr_system.py`, domain files)
	- **Retrieve**: find most similar case(s)
	- **Adapt**: apply rules in `car_cbr.py` or `energy_cbr.py`
	- **Retain**: add new case when learning is enabled

5. **Evaluate** (`evaluation.py`)
	- Accuracy for classification
	- MAE/RMSE for regression

---

## Code Flow (How the Modules Interact)

```
main.py
  ├─ load_car_system_data() / load_energy_system_data()  [data_loader.py]
  ├─ CarCBRSystem / EnergyCBRSystem                      [car_cbr.py / energy_cbr.py]
  ├─ retrieve_most_similar()                             [cbr_system.py]
  ├─ adapt_classification() / adapt_regression()         [car_cbr.py / energy_cbr.py]
  └─ calculate_accuracy/mae/rmse                         [evaluation.py]
```

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

This project was completed equally by:

- **Arun Munagala**
- **Niloy Deb Roy Mishu**
- **Aditya Pise**

All three members contributed equally to the design and implementation of the CBR system, running and analyzing the 6 test conditions, and writing the README and PDF report.

Each member agrees that the amount of effort contributed by each member was equivalent.

---

## Reproducibility

Train/test split uses a fixed random seed (42) for reproducibility.

---

If you want me to generate the PDF report template or finalize team contribution text, just ask.
