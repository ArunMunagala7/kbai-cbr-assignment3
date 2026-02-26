# CBR Assignment 3 - Quick Reference Guide

## What You Need to Do (Summary)

### 1. Build a Case-Based Reasoning System
You're implementing a problem-solving system that learns from past examples (cases) and reuses them to solve new problems.

### 2. Two Separate Systems

#### System A: Car Classification
- **Task**: Given car attributes (price, maintenance cost, doors, capacity, trunk size, safety), predict if the car is: unacc, acc, good, or v-good
- **Data**: 1,728 cars with 6 categorical features
- **Evaluation**: Accuracy percentage

#### System B: Energy Efficiency Regression  
- **Task**: Given building attributes, predict heating load (a number)
- **Data**: Building data with numerical and categorical features
- **Evaluation**: MAE or RMSE (error metric)

---

## Core CBR Concept (The 4-Step Cycle)

```
1. RETRIEVE: Find the most similar past case
2. ADAPT: Modify the past solution based on differences
3. SOLVE: Return the adapted solution
4. RETAIN: Store this new case for future use
```

### How Similarity Works
- Compare each feature between query and cases
- Calculate how different they are
- Average these differences (weighted)
- More similar = higher similarity score

### What Adaptation Does
- The past case may not be perfect for your query
- Rules help adjust the solution based on differences
- Example: If new car is cheaper than retrieved car, maybe upgrade its class

---

## What You Must Implement

### Test 6 Different Configurations:

| # | Task | Setup | Learning | Expected Result |
|---|------|-------|----------|-----------------|
| 1 | Regression | Basic (equal weights, no adaptation) | Yes | Baseline accuracy |
| 2 | Regression | Tuned (weighted features + adaptation) | Yes | Better accuracy |
| 3 | Regression | Tuned (weighted features + adaptation) | No | Compare effect of learning |
| 4 | Classification | Basic (equal weights, no adaptation) | N/A | Baseline accuracy |
| 5 | Classification | Tuned (weighted features, no adaptation) | N/A | See if weights help |
| 6 | Classification | Tuned with adaptation (weighted + rules) | N/A | Best attempt |

---

## Key Implementation Components

### 1. Similarity Computation
**Baseline** (untuned):
```
All features weighted equally
Direct comparison for categorical features
```

**Tuned**:
```
Weighted features based on importance
Car: safety (30%) > price (20%) > capacity (20%) > ...
Energy: features weighted by correlation with heating load
```

### 2. Adaptation Rules

**For Regression (need 4+)**:
1. Scale solution by magnitude of feature differences
2. Linear extrapolation from retrieved case
3. Average solutions from multiple retrieved cases
4. Segment-based adaptation (group similar cases)
5. Attribute-specific scaling (different rules for different features)

**For Classification (need 2-4)**:
1. Multi-case voting (retrieve 3 cases, vote on class)
2. Feature-based refinement (if safety improves, upgrade class)
3. Confidence thresholding (only adapt if confident)
4. Weighted voting by similarity

### 3. Learning
- After solving each query: add the new case to case base
- For "non-learning" condition: skip this step
- Later queries can use cases from earlier queries

---

## Implementation Strategy

### File Structure to Create:
```
data_loader.py       → Load and parse CSV/Excel files
cbr_system.py        → Core similarity, retrieval, adaptation
car_cbr.py           → Car-specific system instance
energy_cbr.py        → Energy-specific system instance
evaluation.py        → Calculate MAE/RMSE/Accuracy
main.py              → Run all 6 test configurations
README.md            → Instructions to run code
report.pdf           → Final results and analysis
```

### Step-by-Step Implementation Order:
1. Load data and create Case objects
2. Implement basic similarity function
3. Implement retriever (find most similar case)
4. Test retrieval works correctly
5. Add adaptation rules
6. Run evaluation on all 6 conditions
7. Analyze results
8. Write report

---

## What to Include in Final Report

### For Each Dataset:

**1. Introduction**
- Brief description of the problem
- What we're trying to predict

**2. Retrieval Strategy**
- How you measure similarity
- Which features you weighted and why
- Your distance metric

**3. Adaptation Strategy**
- Your 4+ adaptation rules for regression (or 2-4 for classification)
- Why you chose each rule
- How they work

**4. Results**
- Table with results for all 3 conditions (regression) or 3 conditions (classification)
- Error metrics or accuracy percentages
- Compare untuned vs tuned
- Discuss effects of learning vs non-learning

**5. Conclusion**
- What worked? What didn't?
- Were results expected?
- Most interesting findings
- Challenges you faced

---

## Success Criteria

✓ Core CBR loop implemented (retrieve → adapt → solve → retain)
✓ Two separate systems (one for classification, one for regression)
✓ 4+ adaptation rules for regression
✓ 2-4 adaptation rules for classification
✓ Baseline and tuned similarity measures
✓ All 6 test conditions evaluated
✓ Clear documentation and report

---

## Key Insights to Discover

1. **Does similarity weighting help?** Compare tuned vs untuned
2. **Does adaptation work?** Compare with/without adaptation
3. **Does learning help?** Compare learning vs non-learning
4. **Which rules matter most?** Test different rule combinations
5. **What's the baseline accuracy?** Know what you're improving from

---

## Detailed Plan Document

A complete step-by-step plan has been saved to: `IMPLEMENTATION_PLAN.md`

This includes:
- Detailed dataset descriptions
- All adaptation rules with formulas
- Feature weighting strategies
- Evaluation methodology
- Code structure recommendations
- Timeline and checklist

---

**Ready to start implementing?** Let me know if you'd like help with:
- Data loading code
- CBR core functions
- Adaptation rule design
- Running tests
- Writing the report
