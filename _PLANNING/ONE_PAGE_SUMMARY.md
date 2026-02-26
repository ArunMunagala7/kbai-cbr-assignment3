# CBR Assignment 3 - One-Page Quick Reference

## TL;DR: What You're Building

A **Case-Based Reasoning (CBR) System** that:
1. Learns from past examples (cases)
2. Finds the most similar case to a new problem
3. Adapts the past solution to fit the new problem
4. Stores the solution for future use

**Two applications**:
- **Cars**: Given car features → predict acceptability grade
- **Buildings**: Given building features → predict heating load

---

## The 4-Step CBR Loop (Repeat for Each Query)

```
┌──────────────────────────────────────────────────────────────┐
│  NEW PROBLEM ARRIVES                                          │
└────────────────────────┬─────────────────────────────────────┘
                         ▼
        ╔════════════════════════════════════╗
        ║ 1. RETRIEVE                        ║
        ║ Find most similar past case        ║
        ║ Similarity = how much alike        ║
        ╚════════════┬═══════════════════════╝
                     ▼
        ╔════════════════════════════════════╗
        ║ 2. ADAPT                           ║
        ║ Modify solution based on           ║
        ║ differences between old & new      ║
        ╚════════════┬═══════════════════════╝
                     ▼
        ╔════════════════════════════════════╗
        ║ 3. SOLVE                           ║
        ║ Return the (adapted) solution      ║
        ╚════════════┬═══════════════════════╝
                     ▼
        ╔════════════════════════════════════╗
        ║ 4. RETAIN                          ║
        ║ Learn: add new case to database    ║
        ║ (if learning enabled)              ║
        ╚════════════┬═══════════════════════╝
                     ▼
        ┌────────────────────────────────────┐
        │ SOLUTION RETURNED + CASE BASE       │
        │ UPDATED FOR NEXT QUERY              │
        └────────────────────────────────────┘
```

---

## What You Must Implement

### Core Functions:
```python
# Main function
run_query(case_base, query, tuned=False, adapt=False, learning=True)
  → Returns: [solution, updated_case_base]

# Retrieval
retrieve_most_similar(query, case_base, weights)
  → Returns: most_similar_case

# Adaptation (4+ rules for regression, 2-4 for classification)
adapt_solution(retrieved_case, query_case)
  → Returns: adapted_solution
```

### Two Separate Systems:
1. **car_cbr.py** - For classification (car acceptability)
2. **energy_cbr.py** - For regression (heating load)

---

## The 6 Tests You Must Run

```
REGRESSION (Energy Efficiency)           CLASSIFICATION (Cars)
─────────────────────────────────        ──────────────────────────
Test 1: Basic                             Test 4: Basic
  - No weights                              - No weights
  - No adaptation                           - No adaptation
  - Learning: ON                            
  ▶ Baseline error                        ▶ Baseline accuracy
                                            
Test 2: Tuned                             Test 5: Tuned (no adapt)
  - Weighted features                       - Weighted features
  - 4+ adaptation rules                    - No adaptation
  - Learning: ON                            
  ▶ Best effort                           ▶ Weight test
                                            
Test 3: Tuned (no learn)                  Test 6: Tuned+Adapt
  - Weighted features                       - Weighted features
  - 4+ adaptation rules                    - 2-4 adaptation rules
  - Learning: OFF                           
  ▶ Learning effect test                  ▶ Best effort
```

**Goal**: Show that Tuned > Untuned & Learning helps

---

## Feature Weighting (Tuned Conditions)

### For Cars (Classification):
```
safety:      0.30  (safest cars rated better)
buying:      0.20  (price matters)
persons:     0.20  (capacity matters)
maint:       0.10  (maintenance cost)
lug_boot:    0.10  (trunk size)
doors:       0.10  (number of doors)
─────────────────
Total:       1.00
```

### For Energy (Regression):
```
Calculate correlation of each feature with heating load
Weight by correlation magnitude
Example:
surface_area:        0.25  (high correlation)
relative_compactness: 0.20
glazing_area:        0.18
wall_area:           0.15
roof_area:           0.12
... (others):        0.10
```

---

## Adaptation Rules (Examples)

### Regression (Need 4+):
```
Rule 1: Scale by difference magnitude
  If surfaces differ 10% → scale solution by 10%

Rule 2: Linear extrapolation
  Each 100m² more surface → +2.5 kWh heating

Rule 3: Average top-3 similar cases
  Get top 3 most similar, adapt each, average results

Rule 4: Segment-based
  Group cases by heating level, apply segment rules
```

### Classification (Need 2-4):
```
Rule 1: Feature refinement
  If safety improved → upgrade class by 1 level

Rule 2: Multi-case voting
  Get top 3, vote on class, use majority

Rule 3: Confidence threshold
  If similarity > 0.8 AND all cases agree → high confidence

Rule 4: Weighted voting
  Weight votes by similarity scores
```

---

## Your Code Structure

```python
# data_loader.py
load_car_data() → List[Case]
load_energy_data() → List[Case]

# cbr_system.py (CORE)
similarity_score(case1, case2, weights)
retrieve_most_similar(query, case_base)
run_query(case_base, query, tuned, adapt, learning)

# car_cbr.py (CAR-SPECIFIC)
car_weights = [...]  # feature weights
car_rules = [...]    # adaptation rules
cbr_car = CBRSystem(weights=car_weights, rules=car_rules)

# energy_cbr.py (ENERGY-SPECIFIC)
energy_weights = [...]
energy_rules = [...]
cbr_energy = CBRSystem(weights=energy_weights, rules=energy_rules)

# evaluation.py
calculate_mae(predictions, actuals)
calculate_accuracy(predictions, actuals)

# main.py
for each of 6 conditions:
  test_system()
  record results
  print results table
```

---

## Expected Results

### Regression:
```
Condition              Error (MAE)
────────────────────────────────
1. Untuned             5.2 kWh      ← Baseline (worst)
2. Tuned + Learn       3.8 kWh      ← Best
3. Tuned + No Learn    4.1 kWh      ← In between

Insights:
- Tuning helps: 36% improvement
- Learning helps: 0.3 kWh additional improvement
```

### Classification:
```
Condition              Accuracy
─────────────────────────────────
1. Untuned             72%         ← Baseline
2. Tuned (no adapt)    76%         ← Weights help
3. Tuned + Adapt       78%         ← Best effort

Insights:
- Weights help: 4% improvement
- Adaptation helps: 2% improvement
```

---

## Submission Checklist

### Code Files:
- [ ] data_loader.py (loads both datasets)
- [ ] cbr_system.py (core CBR logic)
- [ ] car_cbr.py (car classification)
- [ ] energy_cbr.py (energy regression)
- [ ] evaluation.py (metrics)
- [ ] main.py (runs all 6 tests)

### Documentation:
- [ ] README.md (how to run)
- [ ] Comments in code explaining adaptation rules
- [ ] docstrings for all functions

### Report (PDF):
For EACH dataset (cars & energy):
- [ ] Introduction (what problem?)
- [ ] Retrieval Strategy (how similar? what weights? why?)
- [ ] Adaptation Strategy (what rules? why each helps?)
- [ ] Results (table with all conditions, metrics, comparison)
- [ ] Conclusion (what worked? surprises? challenges?)

### Code Quality:
- [ ] No hard-coded paths
- [ ] Consistent variable naming
- [ ] Error handling
- [ ] Reproducible (set seed)

---

## Implementation Timeline

| Week | Task |
|------|------|
| By Feb 27 | Load both datasets ✓ |
| By Feb 27 | Implement similarity functions ✓ |
| By Feb 28 | Implement retrieval ✓ |
| By Feb 28 | Implement adaptation rules ✓ |
| By Feb 28 | Run all 6 tests ✓ |
| By Feb 28 | Write README ✓ |
| By Mar 1  | Write report ✓ |
| By Mar 1  | **SUBMIT** |

---

## Key Success Factors

✅ **Must Have**:
- Core CBR loop (retrieve → adapt → solve → retain)
- 4+ adaptation rules for regression
- 2-4 adaptation rules for classification
- Baseline + tuned similarity measures
- All 6 test conditions passing
- Clear documentation

✅ **Should Have**:
- Tuned conditions better than untuned
- Learning effect demonstrated
- Clear explanation of feature weights
- Discussion of results in report

✅ **Nice to Have**:
- Optimized similarity computation
- Analysis of which rules work best
- Visualization of results
- Discussion of computational efficiency

---

## Red Flags (Avoid These)

❌ Not normalizing numerical features
❌ Comparing categorical features as numbers
❌ Forgetting to add cases when learning enabled
❌ Adaptation rules that don't improve accuracy
❌ Same results for all conditions
❌ Missing documentation in code
❌ No explanation of weights/rules in report
❌ Results table without analysis

---

## Questions to Answer in Your Report

**For each dataset**:
1. What features did you weight most? Why?
2. Describe your 4+ (or 2-4) adaptation rules
3. Did tuning improve results? By how much?
4. Did learning help? Evidence?
5. Were results as expected? Any surprises?
6. What was most challenging?
7. What did you learn about CBR?

---

## Files You Already Have

✅ `car.data` - 1,728 cars with 6 features
✅ `car.names` - Feature descriptions
✅ `ENB2012_data.xlsx` - Building data

## Files You Need to Create

⬜ `data_loader.py`
⬜ `cbr_system.py`
⬜ `car_cbr.py`
⬜ `energy_cbr.py`
⬜ `evaluation.py`
⬜ `main.py`
⬜ `README.md`
⬜ `report.pdf`

---

## Start Here

1. **Read** IMPLEMENTATION_PLAN.md (strategic overview)
2. **Review** CONCRETE_EXAMPLES.md (worked examples)
3. **Reference** ARCHITECTURE_DIAGRAMS.md (system flow)
4. **Code** data_loader.py first
5. **Test** with sample cases
6. **Implement** similarity & retrieval
7. **Add** adaptation rules
8. **Evaluate** all 6 conditions
9. **Write** report

---

**You've got this!** 🚀

All the planning is done. Time to code!
