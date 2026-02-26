# CBR Assignment 3 - Concrete Examples & Decision Guide

## Example 1: How Retrieval Works (Car Classification)

### Scenario: New Query Car

```
QUERY CAR (trying to classify):
  - buying: low
  - maint: low  
  - doors: 4
  - persons: 4
  - lug_boot: big
  - safety: high
```

### Case Base has 1,728 cars. Let's look at how we find the most similar:

#### Car A in Case Base:
```
  - buying: low      (MATCH: similarity = 1.0)
  - maint: low       (MATCH: similarity = 1.0)
  - doors: 4         (MATCH: similarity = 1.0)
  - persons: 4       (MATCH: similarity = 1.0)
  - lug_boot: big    (MATCH: similarity = 1.0)
  - safety: high     (MATCH: similarity = 1.0)
  
OVERALL BASELINE SIMILARITY: 6/6 = 1.00 (PERFECT MATCH!)
PREDICTION FOR THIS CASE: v-good (if this case was v-good)
```

#### Car B in Case Base:
```
  - buying: low      (MATCH: similarity = 1.0)
  - maint: medium    (DIFFERENT: similarity = 0.5 if ordinal, 0.0 if not)
  - doors: 4         (MATCH: similarity = 1.0)
  - persons: 2       (DIFFERENT: similarity = 0.5)
  - lug_boot: med    (DIFFERENT: similarity = 0.67)
  - safety: high     (MATCH: similarity = 1.0)
  
OVERALL BASELINE SIMILARITY: (1+0.5+1+0.5+0.67+1) / 6 = 0.78
PREDICTION FOR THIS CASE: good (if this case was good)
```

#### Car C in Case Base:
```
  - buying: vhigh    (OPPOSITE: similarity = 0.0)
  - maint: vhigh     (OPPOSITE: similarity = 0.0)
  - doors: 2         (DIFFERENT: similarity = 0.5)
  - persons: 2       (DIFFERENT: similarity = 0.5)
  - lug_boot: small  (DIFFERENT: similarity = 0.33)
  - safety: low      (DIFFERENT: similarity = 0.0)
  
OVERALL BASELINE SIMILARITY: (0+0+0.5+0.5+0.33+0) / 6 = 0.22
PREDICTION FOR THIS CASE: unacc (if this case was unacc) - NOT SIMILAR
```

### Retriever Decision:
```
Winner: Car A (similarity = 1.00)
Prediction: v-good (assuming Car A was labeled v-good)

With Learning: Add query car + its actual label to case base
Next query might match to this car too!
```

### With TUNED Similarity (Weighted):

Assume we weight as:
```
  safety: 0.30 (most important)
  buying: 0.20 (price matters)
  persons: 0.20 (capacity matters)
  maint: 0.10
  lug_boot: 0.10
  doors: 0.10
  ───────────────
  Total: 1.00
```

For Car B with tuned similarity:
```
safety×1.0×0.30 = 0.30
buying×1.0×0.20 = 0.20
doors×1.0×0.10 = 0.10
persons×0.5×0.20 = 0.10
lug_boot×0.67×0.10 = 0.067
maint×0.5×0.10 = 0.05
───────────────────────────
TOTAL WEIGHTED = 0.817 (higher than baseline 0.78!)

Because safety and buying matched perfectly (weighted heavily)
```

---

## Example 2: Adaptation for Regression (Energy Efficiency)

### Scenario: Predicting Heating Load

#### Retrieved Case from Case Base:
```
Features:
  relative_compactness: 0.61
  surface_area: 514.5 m²
  wall_area: 318.0 m²
  roof_area: 122.62 m²
  orientation: 2
  glazing_area: 0
  glazing_area_distribution: 0
  
KNOWN SOLUTION: heating_load = 15.27 kWh
```

#### New Query (to be solved):
```
Features:
  relative_compactness: 0.66 (DIFFERS by +0.05)
  surface_area: 594.5 m²   (DIFFERS by +80 m²)
  wall_area: 346.0 m²      (DIFFERS by +28 m²)
  roof_area: 114.5 m²      (DIFFERS by -8.12 m²)
  orientation: 2           (SAME)
  glazing_area: 10         (DIFFERS by +10)
  glazing_area_distribution: 0 (SAME)
```

### Without Adaptation (Untuned):
```
PREDICTION: heating_load = 15.27 kWh (same as retrieved case)
❌ WRONG! Query is different enough to expect different heating load
```

### With Adaptation (Tuned):

#### Adaptation Rule 1: Difference Scaling
```
Magnitude of differences:
- relative_compactness: +0.05 (small increase in compactness)
- surface_area: +80 m² (10% larger)
- glazing_area: +10 (more windows = more heat loss!)

Score: larger surface + more glazing = higher heating load
Expected: ~20% increase

Adapted prediction = 15.27 × 1.20 = 18.32 kWh
```

#### Adaptation Rule 2: Linear Extrapolation
```
From historical patterns in case base:
- Each 100 m² increase in surface → ~2.5 kWh increase in heating
- Each 5 units of glazing → ~1.8 kWh increase

Query's changes:
- Surface +80 m² → +2.0 kWh
- Glazing +10 → +3.6 kWh
- Total adjustment: +5.6 kWh

Adapted prediction = 15.27 + 5.6 = 20.87 kWh
```

#### Adaptation Rule 3: Multi-Case Averaging
```
Retrieve top-3 similar cases:
  Case A (similarity 0.92): predict 18.5 kWh
  Case B (similarity 0.88): predict 19.8 kWh
  Case C (similarity 0.84): predict 17.3 kWh

Weighted average: (18.5×0.92 + 19.8×0.88 + 17.3×0.84) / (0.92+0.88+0.84)
               = (17.02 + 17.42 + 14.53) / 2.64
               = 18.59 kWh
```

#### Adaptation Rule 4: Segment-Based Adaptation
```
Case base segmented by heating load ranges:
  Low (< 10 kWh): 200 cases
  Medium (10-20 kWh): 400 cases  ← Retrieved case in this segment
  High (20-30 kWh): 300 cases
  Very High (> 30 kWh): 100 cases

Query characteristics → similar to "Medium" segment cases
Apply medium-segment-specific adaptation
Prediction: 19.2 kWh
```

### Final Adapted Prediction:
```
If combining all rules:
Average = (18.32 + 20.87 + 18.59 + 19.2) / 4 = 19.25 kWh

Actual value: 21.5 kWh
Error: |21.5 - 19.25| = 2.25 kWh (better than 21.5 - 15.27 = 6.23 kWh!)
✓ Adaptation helped!
```

---

## Example 3: Classification Adaptation

### Scenario: Car Classification

#### Retrieved Case:
```
buying: high
maint: high
doors: 2
persons: 2
lug_boot: small
safety: high
Class: good (retrieved prediction)
```

#### Query (different from retrieved):
```
buying: med     ← BETTER than retrieved (lower price)
maint: high     ← SAME
doors: 2        ← SAME
persons: 2      ← SAME
lug_boot: small ← SAME
safety: high    ← SAME
```

### Without Adaptation:
```
Just return: good
```

### With Adaptation Rules:

#### Rule 1: Feature-Based Refinement
```
Query vs Retrieved difference:
  buying changed from high → med (IMPROVED / cheaper)
  
Domain rule: "If buying price improves (cheaper), upgrade class quality"
Improvement magnitude: 1 level

Adapted prediction: good → v-good (upgrade by one class)
```

#### Rule 2: Multi-Case Voting
```
Retrieve top-3 similar cases:
  Case 1: v-good (similarity 0.91)
  Case 2: good (similarity 0.88)
  Case 3: v-good (similarity 0.85)
  
Vote: v-good (2 votes) beats good (1 vote)
Adapted prediction: v-good
```

#### Rule 3: Confidence Threshold
```
If all top-3 cases vote the same AND similarity > 0.85:
  Use that class with confidence
  
Here: Cases 1 & 3 agree (v-good) but similarity > 0.85 ✓
High confidence in v-good

If there was disagreement (e.g., 2 for v-good, 1 for good):
  Downgrade confidence
  Stick with more conservative prediction (good)
```

### Final Prediction:
```
Using Rule 1: v-good
Using Rule 2: v-good  
Using Rule 3: v-good (high confidence)

FINAL: v-good
Actual: v-good ✓ CORRECT!
```

---

## Example 4: The 6 Test Conditions in Action

### Setup:
- Car dataset: 1381 training cases, 347 test cases
- Energy dataset: split similar way

### Condition 1: Regression Untuned

```python
for test_case in regression_test_set:
    # Use equal weights (all 1.0)
    # No adaptation (return exact solution from retrieved case)
    # Learning enabled
    
    best_case = find_most_similar(test_case, case_base, 
                                 weights=[1,1,1,1,1,1,1])
    prediction = best_case.heating_load
    error = abs(prediction - test_case.actual)
    case_base.add(test_case)  # Learn
    
errors['untuned'].append(error)

Result: MAE = 5.2 kWh (baseline)
```

### Condition 2: Regression Tuned with Learning

```python
for test_case in regression_test_set:
    # Use optimized weights [1.2, 0.9, 1.1, 0.8, 1.3, 0.7]
    # 4+ adaptation rules enabled
    # Learning enabled
    
    best_cases = find_top_3_similar(test_case, case_base,
                                    weights=[1.2, 0.9, ...])
    
    pred1 = adapt_rule1(best_cases[0])  # Difference scaling
    pred2 = adapt_rule2(best_cases[0])  # Linear extrapolation
    pred3 = adapt_rule3(best_cases)     # Multi-case average
    pred4 = adapt_rule4(best_cases[0])  # Segment-based
    
    prediction = (pred1 + pred2 + pred3 + pred4) / 4
    error = abs(prediction - test_case.actual)
    case_base.add(test_case)  # Learn
    
errors['tuned_learn'].append(error)

Result: MAE = 3.8 kWh (better!)
```

### Condition 3: Regression Tuned No-Learning

```python
for test_case in regression_test_set:
    # Same as Condition 2, but...
    # Learning DISABLED - case base stays the same
    
    best_cases = find_top_3_similar(test_case, case_base,
                                    weights=[1.2, 0.9, ...])
    pred1 = adapt_rule1(best_cases[0])
    pred2 = adapt_rule2(best_cases[0])
    pred3 = adapt_rule3(best_cases)
    pred4 = adapt_rule4(best_cases[0])
    
    prediction = (pred1 + pred2 + pred3 + pred4) / 4
    error = abs(prediction - test_case.actual)
    # case_base.add(test_case)  ← SKIP THIS! No learning
    
errors['tuned_nolearn'].append(error)

Result: MAE = 4.1 kWh (worse than learning, but still better than untuned)
Shows: Learning provides ~0.3 kWh improvement
```

### Results Table:
```
┌─────────────────────────────┬────────┐
│ Condition                   │ MAE    │
├─────────────────────────────┼────────┤
│ 1. Untuned                  │ 5.2    │ ← No weights, no adapt
│ 2. Tuned + Learning         │ 3.8    │ ← Best: 36% improvement!
│ 3. Tuned + No Learning      │ 4.1    │ ← Shows learning value
└─────────────────────────────┴────────┘

Key findings:
- Tuning weights helps: 5.2 → 4.1 (feature weights matter)
- Adaptation helps: ~0.3 kWh improvement (rules matter)
- Learning helps: 4.1 → 3.8 (case base accumulation matters)
```

---

## Checklist: What to Verify Before Submitting

### Code Quality
- [ ] All code well-commented, especially adaptation rules
- [ ] Clear function names and variable names
- [ ] No hard-coded paths (use relative paths or parameters)
- [ ] Error handling for edge cases
- [ ] Reproducible results (set random seeds)

### Functionality
- [ ] `run_query(cb, query)` returns [solution, updated_cb]
- [ ] Baseline similarity implemented
- [ ] Tuned similarity with weights implemented
- [ ] 4+ adaptation rules for regression
- [ ] 2-4 adaptation rules for classification
- [ ] Learning works (new cases added to base)
- [ ] Non-learning works (new cases NOT added)

### Testing
- [ ] All 6 conditions run successfully
- [ ] Results table printed clearly
- [ ] Error metrics calculated correctly
- [ ] Tested on full test set (not just first few cases)
- [ ] Reproducible (same seed = same results)

### Documentation
- [ ] README.md with clear instructions
- [ ] Explanation of feature weights (why weights chosen?)
- [ ] Explanation of each adaptation rule
- [ ] PDF report with all required sections
- [ ] Results tables with error metrics
- [ ] Discussion of tuning effects

### Report Contents (Per Dataset)
- [ ] **Introduction**: What problem are we solving?
- [ ] **Retrieval Strategy**: 
  - How do you measure similarity?
  - What distance metric?
  - What are your weights and why?
- [ ] **Adaptation Strategy**:
  - List each rule (4+ for regression, 2-4 for classification)
  - Explain why each rule helps
  - Show pseudocode or formula
- [ ] **Results**:
  - Table with all 3 conditions (regression) or 3 conditions (classification)
  - Show error metrics (MAE/RMSE for regression, accuracy for classification)
  - Compare conditions
- [ ] **Conclusion**:
  - Did tuning help?
  - Did adaptation help?
  - Were results expected?
  - What was surprising?
  - Challenges faced

---

## Quick Decision Tree: Am I on the Right Track?

```
Q1: Can I load both datasets? YES ✓ / NO ✗
  └─NO: Fix data_loader.py

Q2: Can I calculate similarity between two cases? YES ✓ / NO ✗
  └─NO: Implement similarity_score(case1, case2)

Q3: Can I retrieve the most similar case? YES ✓ / NO ✗
  └─NO: Implement retrieve(query, case_base)

Q4: Can I adapt solution based on differences? YES ✓ / NO ✗
  └─NO: Implement adapt_solution(retrieved_case, query)

Q5: Can I run all 6 conditions without errors? YES ✓ / NO ✗
  └─NO: Debug condition setup

Q6: Do tuned conditions perform better than untuned? YES ✓ / NO ✗
  └─NO: Reconsider your weights and adaptation rules

Q7: Can I write a clear report explaining everything? YES ✓ / NO ✗
  └─NO: Reference sections above
  
If all YES ✓: You're ready to submit!
```

---

## Common Pitfalls to Avoid

❌ **Pitfall 1**: Comparing nominal (categorical) features as numbers
- Car's "doors" field: 2, 3, 4, 5more
- Don't do: |2-3| = 1 (wrong for 5more)
- Do: Direct match (1.0 if same, 0.0 if different) OR ordinal similarity

❌ **Pitfall 2**: Not normalizing numerical features
- Building surface area: 300-1000 m²
- Compactness: 0.6-0.98
- Different scales! Use z-score or min-max normalization

❌ **Pitfall 3**: Forgetting to update case base when learning enabled
- Easy to forget: `case_base.add(solved_case)`
- Impact: No learning effect (condition 2 same as condition 3)

❌ **Pitfall 4**: Adaptation rules that always degrade accuracy
- Test your rules on the test set during development
- If accuracy goes down, reconsider the rule

❌ **Pitfall 5**: Returning wrong types
- Classification should return class label (string)
- Regression should return numerical value (float)
- Check your types!

❌ **Pitfall 6**: Not discussing effects in report
- Just showing numbers isn't enough
- Explain: Why did tuning help? How much? Was it expected?

---

These examples should give you concrete guidance for implementing each component!
