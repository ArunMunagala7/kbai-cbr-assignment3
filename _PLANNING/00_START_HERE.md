# CBR Assignment 3 - COMPLETE REPORT OVERVIEW

## Your Complete Planning & Implementation Strategy

This is your comprehensive guide to solving the Case-Based Reasoning assignment. All documents have been created and organized for you.

---

## 📚 What You've Received

### Planning Documents Created:
1. **PLANNING_GUIDE.md** - How to use all the documentation
2. **ONE_PAGE_SUMMARY.md** - Quick reference (keep on desk!)
3. **EXECUTIVE_SUMMARY.md** - Overview & roadmap
4. **QUICK_REFERENCE.md** - CBR concept summary
5. **ARCHITECTURE_DIAGRAMS.md** - Visual system design
6. **CONCRETE_EXAMPLES.md** - Worked examples with real data
7. **IMPLEMENTATION_PLAN.md** - Detailed strategic plan

### Data Files (Already Provided):
- `car.data` - 1,728 car evaluation cases
- `car.names` - Car feature descriptions
- `ENB2012_data.xlsx` - Building energy efficiency data

---

## 🎯 The Assignment in 60 Seconds

You must build a **Case-Based Reasoning system** for two different tasks:

### Task 1: Car Classification
- **Data**: 1,728 cars with 6 features
- **Goal**: Predict car quality (unacc/acc/good/v-good)
- **Metric**: Accuracy percentage
- **Test Conditions**: 3 (untuned, tuned, tuned+adapt)

### Task 2: Energy Regression
- **Data**: Building data with multiple features
- **Goal**: Predict heating load (continuous value in kWh)
- **Metric**: MAE or RMSE error
- **Test Conditions**: 3 (untuned, tuned, tuned+learn vs no-learn)

### Total Test Conditions: **6**

---

## 🔑 Key Concepts

### What is CBR?
A problem-solving approach that:
1. **Retrieves** similar past cases
2. **Adapts** the past solution to fit the new problem
3. **Solves** the current problem
4. **Retains** the new solution for future use

### Why it works:
- Reuses domain knowledge from past cases
- Faster than building complex models from scratch
- Natural way humans solve problems

### Your Job:
Implement this 4-step cycle and test it under 6 different conditions

---

## 🏗️ System Architecture (What to Build)

```
┌─────────────────────────────────────────────────────┐
│                    MAIN.PY                          │
│  (Orchestrates tests for both datasets)             │
└────────┬──────────────┬────────────────────────────┘
         │              │
    ┌────▼──────────┐  ┌▼──────────────┐
    │  CAR_CBR.PY   │  │  ENERGY_CBR.PY│
    │ Classification│  │  Regression   │
    └────┬──────────┘  └┬──────────────┘
         │              │
    ┌────▼──────────────▼──────────┐
    │  CBR_SYSTEM.PY (CORE)        │
    │  - similarity_score()        │
    │  - retrieve()                │
    │  - adapt_solution()          │
    │  - run_query()               │
    └────┬───────────────────────┬─┘
         │                       │
    ┌────▼────────┐      ┌──────▼────────┐
    │DATA_LOADER  │      │EVALUATION.PY  │
    │parse CSV/XL │      │calc MAE/Acc   │
    └─────────────┘      └───────────────┘
```

### Files to Create:
1. **data_loader.py** - Load both datasets
2. **cbr_system.py** - Core similarity & retrieval (shared)
3. **car_cbr.py** - Car-specific setup
4. **energy_cbr.py** - Energy-specific setup
5. **evaluation.py** - Calculate metrics
6. **main.py** - Run all 6 tests

---

## 📊 The 6 Required Tests

### Regression (Energy Efficiency):

| Test | Weights | Adaptation | Learning | Purpose |
|------|---------|------------|----------|---------|
| 1 | Equal | None | ON | Baseline |
| 2 | Tuned | 4+ rules | ON | Best effort |
| 3 | Tuned | 4+ rules | OFF | Isolate learning |

**Key Insight**: Test 2 vs 3 shows learning impact

### Classification (Cars):

| Test | Weights | Adaptation | Purpose |
|------|---------|------------|---------|
| 4 | Equal | None | Baseline |
| 5 | Tuned | None | Weight impact |
| 6 | Tuned | 2-4 rules | Best effort |

**Key Insight**: Test 5 vs 6 shows adaptation impact

### Expected Results:
```
Regression:
  Test 1 (untuned): MAE ≈ 5.2 kWh
  Test 2 (tuned):   MAE ≈ 3.8 kWh  ← 27% improvement
  Test 3 (no-learn): MAE ≈ 4.1 kWh ← Learning adds 0.3 kWh

Classification:
  Test 4 (untuned): 72% accuracy
  Test 5 (tuned):   76% accuracy    ← Weights help
  Test 6 (adapted): 78% accuracy    ← Adaptation helps
```

---

## 💻 Implementation Steps

### Step 1: Data Loading (Day 1 afternoon)
```python
def load_car_data():
    # Parse car.data (CSV)
    # Create Case(features={...}, solution=class)
    
def load_energy_data():
    # Parse ENB2012_data.xlsx (Excel)
    # Create Case(features={...}, solution=heating_load)
    
# Test: print sample cases
```

### Step 2: Similarity Computation (Day 2 morning)
```python
def feature_similarity(val1, val2, feature_type):
    # For categorical: direct match or ordinal
    # For numerical: normalized distance
    
def calculate_similarity(case1, case2, weights=None):
    # Average feature similarities
    # Apply weights if provided
    # Return 0.0 to 1.0
    
# Test: similarity should be higher for similar cases
```

### Step 3: Retrieval (Day 2 afternoon)
```python
def retrieve_most_similar(query, case_base, weights=None):
    similarities = [calculate_similarity(query, case, weights)
                    for case in case_base]
    return case_base[argmax(similarities)]
    
# Test: retrieve and verify it's actually most similar
```

### Step 4: Adaptation (Day 3)
```python
# For Regression (4+ rules):
def adapt_regression(retrieved, query):
    rule1 = difference_scaling(retrieved, query)
    rule2 = linear_extrapolation(retrieved, query)
    rule3 = multi_case_averaging(case_base, query)
    rule4 = segment_adaptation(retrieved, query)
    return average([rule1, rule2, rule3, rule4])

# For Classification (2-4 rules):
def adapt_classification(retrieved, query):
    rule1 = feature_refinement(retrieved, query)
    rule2 = multi_case_voting(case_base, query)
    rule3 = confidence_threshold(case_base, query)
    return majority_vote([rule1, rule2, rule3])
    
# Test: adaptation should improve accuracy
```

### Step 5: Core Loop (Day 3)
```python
def run_query(case_base, query, tuned=False, 
              adapt=False, learning=True):
    # 1. RETRIEVE
    weights = tuned_weights if tuned else equal_weights
    similar = retrieve_most_similar(query, case_base, weights)
    
    # 2. ADAPT
    if adapt:
        solution = adapt_solution(similar, query)
    else:
        solution = similar.solution
    
    # 3. SOLVE
    # solution already obtained
    
    # 4. RETAIN
    if learning:
        new_case = Case(features=query, solution=solution)
        case_base.append(new_case)
    
    return solution, case_base
    
# Test: runs without errors
```

### Step 6: Evaluation (Day 4 morning)
```python
def evaluate_regression(predictions, actuals):
    mae = sum(abs(p - a) for p, a in zip(...)) / len(...)
    rmse = sqrt(sum((p - a)**2 for ...) / len(...))
    return mae, rmse
    
def evaluate_classification(predictions, actuals):
    correct = sum(p == a for p, a in zip(...))
    accuracy = correct / len(actuals)
    return accuracy
    
# Test: metrics calculated correctly
```

### Step 7: Run All Tests (Day 4)
```python
def main():
    # Load data
    car_data = load_car_data()
    energy_data = load_energy_data()
    
    # Run 6 conditions
    results = {}
    
    # Regression condition 1: untuned
    cb = energy_data[:1000]  # training set
    test = energy_data[1000:]  # test set
    predictions = []
    for query in test:
        pred, cb = run_query(cb, query, tuned=False, 
                           adapt=False, learning=True)
        predictions.append(pred)
    results['regression_untuned'] = evaluate_regression(...)
    
    # ... repeat for other 5 conditions ...
    
    # Print results table
    for condition, metrics in results.items():
        print(f"{condition}: {metrics}")
```

### Step 8: Documentation (Day 5)
```python
# Write README.md with:
# - How to install dependencies
# - How to run: python main.py
# - What output to expect

# Write report.pdf with:
# - Introduction (both datasets)
# - Retrieval Strategy (similarity, weights)
# - Adaptation Strategy (all rules + rationale)
# - Results (table + analysis)
# - Conclusion (findings, surprises)
```

---

## 📋 Feature Weighting Strategy

### For Cars (My Suggestion):
```python
car_weights = {
    'safety': 0.30,      # Most critical for quality
    'buying': 0.20,      # Price significantly impacts rating
    'persons': 0.20,     # Capacity is important
    'maint': 0.10,       # Maintenance cost
    'lug_boot': 0.10,    # Trunk size (comfort)
    'doors': 0.10        # Door count (least critical)
}
```

### For Energy (My Suggestion):
```python
# Calculate correlation of each feature with heating_load
# Example (you'll calculate exact values):
energy_weights = {
    'surface_area': 0.25,           # Highly correlated
    'relative_compactness': 0.20,
    'glazing_area': 0.18,
    'wall_area': 0.15,
    'roof_area': 0.12,
    'orientation': 0.06,
    'glazing_area_distribution': 0.04
}

# Normalize so sum = 1.0
```

---

## 🧠 Adaptation Rules (Examples)

### Regression Rules (Need 4+):

**Rule 1: Difference Scaling**
```
Idea: If features differ significantly, scale solution accordingly
Example: If query surface is 10% larger → solution might be 10% higher
Formula: adapted = retrieved * (1 + alpha * magnitude_of_difference)
```

**Rule 2: Linear Extrapolation**
```
Idea: Learn relationships from case base
Example: Each 100m² more surface → 2.5 kWh more heating
Formula: adapted = retrieved + sum(feature_delta * learned_slope)
```

**Rule 3: Multi-Case Averaging**
```
Idea: Get more robust predictions by averaging
Steps:
  1. Retrieve top-3 similar cases
  2. Adapt each one
  3. Average the results
Formula: adapted = mean(adapt(case1), adapt(case2), adapt(case3))
```

**Rule 4: Segment-Based Adaptation**
```
Idea: Different rules for different parts of solution space
Steps:
  1. Group cases by solution level (low/medium/high heating)
  2. Identify which segment query belongs to
  3. Apply segment-specific adaptation
Formula: adapted = segment_specific_adapt(retrieved, query)
```

### Classification Rules (Need 2-4):

**Rule 1: Feature Refinement**
```
Idea: Adjust class based on feature improvements
Example:
  If safety improved → upgrade class by 1 level
  If price worsened → downgrade class by 1 level
Formula: adapted_class = base_class + adjustments
```

**Rule 2: Multi-Case Voting**
```
Idea: Democracy - let multiple cases vote
Steps:
  1. Retrieve top-3 similar cases
  2. Adapt each one
  3. Vote on class (majority wins)
Formula: adapted_class = mode([adapt(c1), adapt(c2), adapt(c3)])
```

**Rule 3: Confidence Threshold**
```
Idea: Only adapt if confident in prediction
Steps:
  1. Get top-3 cases
  2. If all vote same AND similarity > threshold → adapt
  3. Else use conservative prediction
Formula: if unanimous and high_similarity: aggressive_adaptation
         else: conservative_prediction
```

---

## 📝 What Goes in Your Report

### For Each Dataset (Cars & Energy):

#### 1. Introduction
- What problem are we solving?
- Why is it important?
- What's the dataset size/composition?

#### 2. Retrieval Strategy
```
Must include:
- How do you measure similarity? (formula)
- What distance metric? (Euclidean, Manhattan, etc.)
- How are features compared? (ordinal, direct match, etc.)
- What weights did you choose? (and why?)
- Example: "Safety is weighted 0.30 because it's most 
  important for car quality based on domain knowledge"
```

#### 3. Adaptation Strategy
```
Must include for REGRESSION:
- List all 4+ adaptation rules
- For each rule:
  - Name and purpose
  - Formula or pseudocode
  - Why you chose it
  - How it helps

Must include for CLASSIFICATION:
- List all 2-4 adaptation rules
- For each rule:
  - Name and purpose
  - How it works (steps)
  - Why you chose it
- Rationale: "These rules target the most common 
  classification errors"
```

#### 4. Results
```
Must include:
- Table showing all test conditions
- Error metrics (MAE/RMSE for regression)
- Accuracy percentages (for classification)
- Analysis of differences:
  - Did tuning help? By how much?
  - Did adaptation help? By how much?
  - Did learning help (regression only)? By how much?
- Example insights:
  "Tuning improved accuracy by 4%, showing that 
   feature weights matter for this dataset"
```

#### 5. Conclusion
```
Must include:
- Summary of findings
- Were results as expected?
- Any surprising results? Explain!
- What was most challenging?
- What did you learn about CBR?
```

---

## 🚀 Quick Start Checklist

- [ ] Read **ONE_PAGE_SUMMARY.md** (10 min)
- [ ] Read **CONCRETE_EXAMPLES.md** (20 min)
- [ ] Create **data_loader.py** and test it
- [ ] Create **cbr_system.py** with similarity/retrieval
- [ ] Create **car_cbr.py** and **energy_cbr.py**
- [ ] Create **evaluation.py**
- [ ] Create **main.py** and run all 6 tests
- [ ] Verify tuned > untuned
- [ ] Write **README.md**
- [ ] Write **report.pdf**
- [ ] SUBMIT!

---

## ⏰ Timeline (4 Days to Deadline)

**Day 1 (Feb 27)**:
- Morning: Read planning docs (90 min)
- Afternoon: Set up project, create data_loader.py
- Evening: Test data loading works

**Days 2-3 (Feb 27-28)**:
- Day 2: Implement similarity & retrieval
- Day 3 morning: Implement adaptation rules
- Day 3 afternoon: Run all 6 tests

**Day 4 (Feb 28)**:
- Morning: Verify results, fix bugs
- Afternoon: Write README.md & report.pdf

**Day 5 (Mar 1)**:
- Before 11:59 PM: SUBMIT on Canvas!

---

## 🎓 Learning Outcomes

After completing this assignment, you will understand:
✅ How Case-Based Reasoning works
✅ The CBR cycle (retrieve → adapt → solve → retain)
✅ How to measure similarity between cases
✅ How to design effective adaptation rules
✅ How to evaluate CBR system performance
✅ The importance of knowledge containers in AI systems
✅ Practical implementation challenges in CBR

---

## 📚 Document Reference Index

| Topic | Primary Source | Backup |
|-------|---|---|
| "What am I building?" | ONE_PAGE_SUMMARY.md | EXECUTIVE_SUMMARY.md |
| "How does similarity work?" | CONCRETE_EXAMPLES.md | ARCHITECTURE_DIAGRAMS.md |
| "What adaptation rules?" | IMPLEMENTATION_PLAN.md | CONCRETE_EXAMPLES.md |
| "How do I implement this?" | ARCHITECTURE_DIAGRAMS.md | IMPLEMENTATION_PLAN.md |
| "What's my timeline?" | ONE_PAGE_SUMMARY.md | EXECUTIVE_SUMMARY.md |
| "How do I structure the code?" | IMPLEMENTATION_PLAN.md | ARCHITECTURE_DIAGRAMS.md |
| "What should my report say?" | EXECUTIVE_SUMMARY.md | IMPLEMENTATION_PLAN.md |
| "Show me an example!" | CONCRETE_EXAMPLES.md | - |
| "I'm stuck, what now?" | CONCRETE_EXAMPLES.md | PLANNING_GUIDE.md |

---

## ✨ Final Thoughts

This is **not** a small assignment, but it's **completely doable** with good planning.

You have:
- ✅ 7 comprehensive planning documents
- ✅ Both datasets ready to use
- ✅ Clear implementation strategy
- ✅ Worked examples with real numbers
- ✅ Detailed checklist to follow

**What you need to do**:
1. Read the planning docs (not all at once - skim first)
2. Start coding **data_loader.py**
3. Build each component step-by-step
4. Test as you go
5. Run the 6 tests
6. Write the report
7. Submit!

**Key to success**:
- Start early (don't wait until Mar 1)
- Test each component as you build it
- Reference the planning docs when stuck
- Make sure tuned > untuned (if not, reconsider your approach)

---

## 🎉 You're Ready!

You now have everything you need to implement a successful CBR system.

**Next step**: Start reading **ONE_PAGE_SUMMARY.md** and **CONCRETE_EXAMPLES.md**, then begin coding.

**Questions?** Reference the planning documents - they're comprehensive!

**Stuck?** Check **CONCRETE_EXAMPLES.md** for worked examples.

**Good luck! 🚀**

---

*Complete planning provided by AI Assistant*
*Assignment due: March 1, 2026, 11:59 PM*
*Current date: February 26, 2026*
*Days remaining: 4*
