# CBR System Architecture & Flow Diagrams

## 1. High-Level CBR Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                    NEW QUERY ARRIVES                          │
│              (car attributes OR building data)                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  1. RETRIEVE PHASE         │
        │  Find most similar case    │
        │  from case base            │
        │  (Compare features)        │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  2. ADAPT PHASE            │
        │  Apply adaptation rules:   │
        │  - Modify retrieved        │
        │    solution based on       │
        │    differences             │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  3. SOLVE PHASE            │
        │  Return the adapted        │
        │  solution to user          │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  4. RETAIN PHASE           │
        │  (If learning enabled)     │
        │  Add new case to base      │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  UPDATED CASE BASE         │
        │  (ready for next query)    │
        └────────────────────────────┘
```

---

## 2. Similarity Computation Process

```
Query Case:  buying=low, maint=low, doors=4, persons=4, lug_boot=big, safety=high

Case in Base: buying=med, maint=low, doors=2, persons=2, lug_boot=med, safety=high

Step 1: Compare Each Feature
┌──────────┬──────────┬────────────┬──────────┬─────────────┐
│ Feature  │ Query    │ Case       │ Same?    │ Similarity  │
├──────────┼──────────┼────────────┼──────────┼─────────────┤
│ buying   │ low      │ med        │ NO       │ 0.5 (ordered)
│ maint    │ low      │ low        │ YES      │ 1.0         │
│ doors    │ 4        │ 2          │ NO       │ 0.67        │
│ persons  │ 4        │ 2          │ NO       │ 0.5         │
│ lug_boot │ big      │ med        │ NO       │ 0.67        │
│ safety   │ high     │ high       │ YES      │ 1.0         │
└──────────┴──────────┴────────────┴──────────┴─────────────┘

BASELINE (equal weights):
Similarity = (0.5 + 1.0 + 0.67 + 0.5 + 0.67 + 1.0) / 6 = 0.72

TUNED (weighted):
          (0.5×0.2 + 1.0×0.1 + 0.67×0.1 + 0.5×0.2 + 0.67×0.1 + 1.0×0.3)
Similarity = ─────────────────────────────────────────────────────────────
                             0.2 + 0.1 + 0.1 + 0.2 + 0.1 + 0.3
          = 0.79 (weights prioritize safety and buying price)
```

---

## 3. Adaptation Rules Flow (Regression Example)

```
Retrieved Case: heating_load = 25.5 kWh
Query differs from retrieved case by:
  - relative_compactness: -0.05 (query is less compact)
  - surface_area: +100 (query has more surface)
  - other features differ moderately

┌─────────────────────────────────┐
│    SELECT ADAPTATION RULE       │
└────────┬────────────────────────┘
         │
    ┌────┴─────────────────────────────────┐
    │                                        │
    ▼ (Rule 1)              ▼ (Rule 2)      ▼ (Rule 3)     ▼ (Rule 4)
Difference       Linear          Multi-Case     Segment
Scaling       Extrapolation      Averaging      Adaptation
    │             │               │              │
    ▼             ▼               ▼              ▼
Multiply by   Apply slope   Average top-3   Apply segment-
(1 + alpha)   adjustment    similar cases   specific rules
    │             │               │              │
    │             ▼               ▼              ▼
    │         Solution = 27.3  Solution = 26.1 Solution = 25.9
    │
    ▼
Adapted = 26.7

If using multiple rules:
Final = (26.7 + 27.3 + 26.1 + 25.9) / 4 = 26.5 kWh
```

---

## 4. Classification Adaptation Rules Flow

```
Retrieved Case: safety=high, buying=high → Class = "good"
Query Case: safety=high, buying=low (different on buying)

┌──────────────────────────────────┐
│  APPLY ADAPTATION RULES          │
└────────┬─────────────────────────┘
         │
    ┌────┴──────────────────────┐
    │                            │
    ▼ (Rule 1)       ▼ (Rule 2)  ▼ (Rule 3)
Multi-Case        Feature      Confidence
Voting          Refinement      Threshold
    │               │              │
    ▼               ▼              ▼
Retrieve 3       If safety       If similarity
top cases        improved        > 0.8:
Vote on         → upgrade class  Use directly
class:          If buying       Else:
case1=good      worsened        Downgrade
case2=acc       → downgrade     class
case3=good         class        
Result:                         
majority=good   Result=       Result=
               acc/good      good (uncertain)
    │               │              │
    └───────┬───────┴──────────────┘
            │
            ▼
        FINAL PREDICTION
        (Compare outputs from rules)
```

---

## 5. The 6 Test Conditions Explained

### Regression (Energy Efficiency)

```
┌─────────────────────────┐
│ CONDITION 1: UNTUNED    │
│ • Equal feature weights │
│ • No adaptation rules   │
│ • Learning enabled      │
│                         │
│ Just return retrieved   │
│ case's solution         │
└─────────────────────────┘

                ▼

┌──────────────────────────┐
│ CONDITION 2: TUNED       │
│ • Weighted features      │
│ • 4+ adaptation rules    │
│ • Learning enabled       │
│                          │
│ Best performance         │
│ (should be best)         │
└──────────────────────────┘

                ▼

┌────────────────────────────────┐
│ CONDITION 3: TUNED NO-LEARNING │
│ • Weighted features            │
│ • 4+ adaptation rules          │
│ • Learning DISABLED            │
│                                │
│ Isolate effect of learning     │
│ (compare to condition 2)       │
└────────────────────────────────┘
```

### Classification (Car Evaluation)

```
┌──────────────────────────┐
│ CONDITION 1: UNTUNED     │
│ • Equal weights          │
│ • No adaptation          │
│ • Return class directly  │
│                          │
│ Baseline accuracy        │
└──────────────────────────┘

                ▼

┌──────────────────────────┐
│ CONDITION 2: TUNED       │
│ • Weighted features      │
│ • No adaptation          │
│ • Return class directly  │
│                          │
│ Test if weights help     │
└──────────────────────────┘

                ▼

┌──────────────────────────────┐
│ CONDITION 3: TUNED+ADAPT     │
│ • Weighted features          │
│ • 2-4 adaptation rules       │
│ • Apply rules to improve     │
│                              │
│ Best effort for accuracy     │
└──────────────────────────────┘
```

---

## 6. Data Flow: From Raw Data to Results

```
┌──────────────────┐
│   Raw Data       │
│ car.data         │
│ ENB2012.xlsx     │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────┐
│ Data Loader Module       │
│ - Parse CSV/Excel        │
│ - Create Case objects    │
│ - Normalize features     │
│ - Train/Test split       │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Initial Case Base       │
│  (Training cases)        │
│  1381 cars / 500 buildings
└────────┬─────────────────┘
         │
    ┌────┴─────────────────┐
    │                      │
    ▼                      ▼
┌──────────────┐    ┌──────────────┐
│ Test Case 1  │... │ Test Case N  │
│ (No label)   │    │ (No label)   │
└────┬─────────┘    └────┬─────────┘
     │                   │
     │  run_query(cb, q) │
     └─────────┬─────────┘
               │
        ┌──────▼────────┐
        │  CBR System   │
        │ (Retrieve)    │
        │ (Adapt)       │
        │ (Solve)       │
        │ (Retain)      │
        └──────┬────────┘
               │
               ▼
        ┌──────────────┐
        │  Prediction  │
        │ (+ updated   │
        │  case base)  │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │ Evaluation   │
        │ Compare to   │
        │ actual label │
        │ (MAE/RMSE or │
        │  Accuracy%)  │
        └──────┬───────┘
               │
               ▼
        ┌─────────────────┐
        │  Results Table  │
        │  (6 conditions) │
        └─────────────────┘
```

---

## 7. Pseudo-Code for Main Run Loop

```python
def run_all_conditions():
    # Load data
    car_data = load_car_data()
    energy_data = load_energy_data()
    
    # Split into train/test
    car_train, car_test = split_data(car_data, 0.8)
    energy_train, energy_test = split_data(energy_data, 0.8)
    
    results = {}
    
    # --- REGRESSION CONDITIONS ---
    
    # Condition 1: Untuned Regression
    cb = car_train.copy()  # Initial case base
    results['regression_untuned'] = []
    for query in car_test:
        solution, cb = run_query(cb, query, 
                                tuned=False, 
                                adaptation=False, 
                                learning=True)
        results['regression_untuned'].append(evaluate(solution, query.actual))
    
    # Condition 2: Tuned Regression with Learning
    cb = energy_train.copy()
    results['regression_tuned'] = []
    for query in energy_test:
        solution, cb = run_query(cb, query, 
                                tuned=True,
                                adaptation=True, 
                                learning=True)
        results['regression_tuned'].append(evaluate(solution, query.actual))
    
    # Condition 3: Tuned Regression NO Learning
    cb = energy_train.copy()
    results['regression_tuned_nolearn'] = []
    for query in energy_test:
        solution, cb = run_query(cb, query, 
                                tuned=True, 
                                adaptation=True, 
                                learning=False)  # KEY: learning disabled
        results['regression_tuned_nolearn'].append(evaluate(solution, query.actual))
    
    # --- CLASSIFICATION CONDITIONS ---
    
    # Condition 4: Untuned Classification
    cb = car_train.copy()
    results['classification_untuned'] = []
    for query in car_test:
        prediction, cb = run_query(cb, query, 
                                  tuned=False, 
                                  adaptation=False)
        results['classification_untuned'].append(
            1 if prediction == query.actual else 0
        )
    
    # Condition 5: Tuned Classification (no adaptation)
    cb = car_train.copy()
    results['classification_tuned'] = []
    for query in car_test:
        prediction, cb = run_query(cb, query, 
                                  tuned=True, 
                                  adaptation=False)
        results['classification_tuned'].append(
            1 if prediction == query.actual else 0
        )
    
    # Condition 6: Tuned Classification with Adaptation
    cb = car_train.copy()
    results['classification_tuned_adapt'] = []
    for query in car_test:
        prediction, cb = run_query(cb, query, 
                                  tuned=True, 
                                  adaptation=True)
        results['classification_tuned_adapt'].append(
            1 if prediction == query.actual else 0
        )
    
    # Print results
    print_results_table(results)
    return results
```

---

## 8. Expected Results Pattern

```
REGRESSION (Energy Efficiency):
┌─────────────────────────┬──────────┐
│ Condition               │ MAE      │
├─────────────────────────┼──────────┤
│ 1. Untuned              │ ~5.2     │  ← Baseline (highest error)
│ 2. Tuned + Learning     │ ~3.8     │  ← Best (lowest error)
│ 3. Tuned + No Learning  │ ~4.1     │  ← In between (learning helps)
└─────────────────────────┴──────────┘

CLASSIFICATION (Car Evaluation):
┌──────────────────────────┬──────────┐
│ Condition                │ Accuracy │
├──────────────────────────┼──────────┤
│ 1. Untuned               │ ~72%     │  ← Baseline
│ 2. Tuned (no adaptation) │ ~76%     │  ← Weights help
│ 3. Tuned + Adaptation    │ ~78%     │  ← Best effort
└──────────────────────────┴──────────┘

Key Insight: Tuned > Untuned > No-Learning
This shows your customization is working!
```

---

This visual reference should help guide your implementation. Each diagram shows:
1. What happens at each step
2. How data flows through the system
3. What makes tuned different from untuned
4. How to test all 6 conditions

**Next: Ready to start coding?**
