# CBR Assignment 3 - Executive Summary & Start Guide

## What You Need to Build

A **Case-Based Reasoning (CBR) system** that solves two problems:

| Problem | Type | Task | Metric |
|---------|------|------|--------|
| **Car Evaluation** | Classification | Predict car quality (unacc/acc/good/v-good) | Accuracy % |
| **Energy Efficiency** | Regression | Predict building heating load (kWh) | MAE or RMSE |

---

## The CBR Concept in Simple Terms

Imagine you're a doctor. When a patient comes in with a problem:
1. **Retrieve**: Look up similar past patients in your medical record
2. **Adapt**: Adjust the treatment based on differences (medication adjustments, etc.)
3. **Solve**: Prescribe the adapted treatment
4. **Retain**: Add this new case to your records for future reference

**That's CBR!** We're doing this for cars and buildings instead of patients.

---

## Your 6 Required Tests

You must test your system under 6 different configurations and report results:

### For Car Classification (3 conditions):
1. **Basic** (no optimization) → Baseline accuracy
2. **Weighted similarities** (no adaptation) → Does weighting help?
3. **Weighted + Adaptation rules** → Best effort accuracy

### For Energy Regression (3 conditions):
1. **Basic** (no optimization, learning enabled) → Baseline error
2. **Weighted + Adaptation** (learning enabled) → Best effort error
3. **Weighted + Adaptation** (learning **disabled**) → Isolate learning effect

---

## Implementation Roadmap (What to Create)

### File Structure:
```
Project/
├── 📄 data_loader.py          (Load CSV/Excel files)
├── 📄 cbr_system.py           (Core similarity & retrieval)
├── 📄 car_cbr.py              (Car-specific system)
├── 📄 energy_cbr.py           (Energy-specific system)
├── 📄 evaluation.py           (Calculate errors/accuracy)
├── 📄 main.py                 (Run all 6 tests)
├── 📄 README.md               (How to run)
└── 📄 report.pdf              (Results & analysis)
```

### Core Components to Implement:

#### 1. **Data Loader** (data_loader.py)
```python
def load_car_data():
    # Parse car.data (CSV)
    # Return list of Case objects
    
def load_energy_data():
    # Parse ENB2012_data.xlsx
    # Return list of Case objects
```

#### 2. **Similarity Calculator** (cbr_system.py)
```python
def calculate_similarity(query_case, base_case, weights=None, tuned=False):
    # Compare all features
    # Apply weights if tuned=True
    # Return similarity score (0.0 to 1.0)
    
def retrieve_most_similar(query, case_base, weights=None):
    # Find case with highest similarity
    # Return the most similar case
```

#### 3. **Adaptation Engine** (car_cbr.py & energy_cbr.py)
```python
# For Regression: 4+ adaptation rules
def adapt_regression(retrieved_case, query_case):
    rule1_result = apply_difference_scaling(...)
    rule2_result = apply_linear_extrapolation(...)
    rule3_result = apply_multi_case_averaging(...)
    rule4_result = apply_segment_adaptation(...)
    return average([rule1_result, rule2_result, ...])

# For Classification: 2-4 adaptation rules
def adapt_classification(retrieved_case, query_case):
    rule1_result = apply_feature_refinement(...)
    rule2_result = apply_multi_case_voting(...)
    rule3_result = apply_confidence_threshold(...)
    return majority_vote([rule1_result, rule2_result, ...])
```

#### 4. **Core Run Function** (main CBR loop)
```python
def run_query(case_base, query, tuned=False, adapt=False, learning=True):
    """
    1. Retrieve: Find most similar case
    2. Adapt: Modify solution (if adapt=True)
    3. Solve: Return the (adapted) solution
    4. Retain: Add new case to base (if learning=True)
    """
    most_similar = retrieve_most_similar(query, case_base)
    
    if adapt:
        solution = adapt_solution(most_similar, query)
    else:
        solution = most_similar.solution
    
    if learning:
        case_base.add(query with solution)  # Learn!
    
    return solution, case_base
```

#### 5. **Evaluation** (evaluation.py)
```python
def calculate_mae(predictions, actuals):
    # Mean Absolute Error for regression
    
def calculate_rmse(predictions, actuals):
    # Root Mean Square Error for regression
    
def calculate_accuracy(predictions, actuals):
    # Percentage correct for classification
```

#### 6. **Main Test Runner** (main.py)
```python
def main():
    # Load data
    car_data = load_car_data()
    energy_data = load_energy_data()
    
    # Run 6 conditions
    results = {}
    
    # Regression conditions
    results['untuned'] = test_regression(energy_data, 
                                        tuned=False, 
                                        adapt=False, 
                                        learning=True)
    results['tuned'] = test_regression(energy_data, 
                                      tuned=True, 
                                      adapt=True, 
                                      learning=True)
    results['tuned_nolearn'] = test_regression(energy_data, 
                                             tuned=True, 
                                             adapt=True, 
                                             learning=False)
    
    # Classification conditions
    results['class_untuned'] = test_classification(car_data, 
                                                 tuned=False, 
                                                 adapt=False)
    results['class_tuned'] = test_classification(car_data, 
                                               tuned=True, 
                                               adapt=False)
    results['class_tuned_adapt'] = test_classification(car_data, 
                                                     tuned=True, 
                                                     adapt=True)
    
    # Print results table
    print_results(results)
```

---

## Key Decisions You Need to Make

### 1. Similarity Weights (For Tuned Conditions)

**Car Classification**:
- Which features matter most for predicting car quality?
- My suggestion:
  - `safety`: 0.30 (most critical)
  - `buying`: 0.20 (price important)
  - `persons`: 0.20 (capacity matters)
  - `maint`: 0.10
  - `lug_boot`: 0.10
  - `doors`: 0.10

**Energy Regression**:
- Which features correlate most with heating load?
- Calculate correlation coefficients with heating load
- Weight features by correlation strength

### 2. Adaptation Rules (Critical!)

**For Regression (Need 4+)**:
- **Rule 1**: Scale solution by difference magnitude
- **Rule 2**: Linear extrapolation from correlations
- **Rule 3**: Average top-3 similar cases
- **Rule 4**: Segment-specific adaptation (by load level)
- (Optional) **Rule 5**: Attribute-weighted scaling

**For Classification (Need 2-4)**:
- **Rule 1**: Feature-based class refinement (e.g., safety improves → upgrade)
- **Rule 2**: Multi-case voting (retrieve top-3, vote)
- **Rule 3**: Confidence threshold (only adapt if confident)
- (Optional) **Rule 4**: Weighted voting

### 3. Feature Comparison Method

**For Categorical (Car)**:
- Ordinal comparison: `buying (vhigh > high > med > low)`
- Direct match: `doors (2 vs 3 = different)`
- Hierarchical: Use car.names structure if helpful

**For Numerical (Energy)**:
- Normalize first! (z-score or min-max)
- Then use Euclidean distance or similar

---

## Step-by-Step Implementation Order

### Week 1:
1. ✅ Understand both datasets (done - see CONCRETE_EXAMPLES.md)
2. ⬜ Create data_loader.py (load both datasets)
3. ⬜ Create Case class (feature dict + solution)
4. ⬜ Test data loading works

### Week 1-2:
5. ⬜ Implement similarity_score() function
6. ⬜ Implement retrieve() function
7. ⬜ Test retrieval on sample cases

### Week 2:
8. ⬜ Implement adaptation rules for regression (4+)
9. ⬜ Implement adaptation rules for classification (2-4)
10. ⬜ Test adaptation improves accuracy

### Before Deadline:
11. ⬜ Run all 6 conditions
12. ⬜ Collect results in table
13. ⬜ Write README.md
14. ⬜ Write report.pdf
15. ⬜ Submit!

---

## What Success Looks Like

### Your System Should:
- ✓ Load data correctly
- ✓ Calculate similarity between cases
- ✓ Retrieve most similar case(s)
- ✓ Adapt solutions appropriately
- ✓ Store new cases when learning enabled
- ✓ Run without errors on all test cases
- ✓ Show measurable improvement from tuning

### Your Results Should Show:
- ✓ Tuned > Untuned (feature weights help!)
- ✓ With Adaptation > Without Adaptation (rules help!)
- ✓ Learning > No Learning (accumulation helps!)
- ✓ Clear explanation of why each helps

### Your Report Should Have:
- ✓ Clear explanation of similarity strategy
- ✓ List of all adaptation rules with justification
- ✓ Results table for all 6 conditions
- ✓ Discussion of what was surprising
- ✓ Challenges faced and solutions

---

## Quick Troubleshooting Guide

| Problem | Solution |
|---------|----------|
| Can't load data | Check file paths, use os.path.abspath() |
| Similarity always 0 or 1 | Check feature normalization and comparison logic |
| Adaptation makes accuracy worse | Review adaptation rule logic, test each rule separately |
| Learning doesn't help | Verify case_base.add() is actually happening |
| Results all same | Check that weights are being applied correctly |
| Can't run all 6 conditions | Verify each condition's parameters are correct |

---

## Critical Tips

🔴 **Must Do These**:
1. Normalize numerical features BEFORE similarity comparison
2. Set random seed for reproducibility
3. Apply weights in tuned conditions (not in baseline)
4. Add new cases to case base only when learning=True
5. Test adaptation rules separately before combining

🟡 **Should Consider**:
1. Use top-3 cases instead of just 1 for more robust predictions
2. Document why you chose each weight value
3. Test different weight combinations
4. Explain each adaptation rule in your code with comments

🟢 **Nice to Have**:
1. Visualize similarity distributions
2. Plot error trends over test cases
3. Compare adaptation rule effectiveness
4. Test different random seeds for consistency

---

## Resources You Already Have

- ✅ `IMPLEMENTATION_PLAN.md` - Detailed strategic plan
- ✅ `QUICK_REFERENCE.md` - Quick lookup guide
- ✅ `ARCHITECTURE_DIAGRAMS.md` - Visual system flow
- ✅ `CONCRETE_EXAMPLES.md` - Worked examples with real data
- ✅ `car.data` & `car.names` - Car dataset
- ✅ `ENB2012_data.xlsx` - Energy dataset

---

## Next Step: Ready to Code?

When you're ready to start implementing, let me know and I can help with:
1. Creating the data_loader.py template
2. Implementing similarity functions
3. Debugging any issues
4. Optimizing your code
5. Writing the final report

**Current Status**: 📋 Planning Complete ✓
**Next Status**: 💻 Implementation Ready

---

Good luck! You've got this! 🚀
