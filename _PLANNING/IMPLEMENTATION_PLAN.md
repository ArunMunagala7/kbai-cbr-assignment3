# CBR Assignment 3 - Complete Implementation Plan

## Executive Summary
This document outlines a comprehensive step-by-step plan to implement a Case-Based Reasoning system for two datasets:
1. **Regression Task**: Energy Efficiency Dataset (predict heating load)
2. **Classification Task**: Car Evaluation Dataset (predict car grade)

---

## Part 1: Understanding the Datasets

### 1.1 Car Evaluation Dataset (Classification)
**File**: `car.data`, `car.names`
- **Total Instances**: 1,728
- **Attributes**: 6 categorical features
- **Features**:
  - `buying`: v-high, high, med, low
  - `maint`: v-high, high, med, low
  - `doors`: 2, 3, 4, 5-more
  - `persons`: 2, 4, more
  - `lug_boot`: small, med, big
  - `safety`: low, med, high
- **Target**: car acceptability (unacc: 70%, acc: 22%, good: 4%, v-good: 4%)

### 1.2 Energy Efficiency Dataset (Regression)
**File**: `ENB2012_data.xlsx`
- **Numerical features**: relative compactness, surface area, wall area, roof area, orientation, glazing area, glazing area distribution
- **Target**: Heating Load (continuous value)
- **Mix**: Numerical + categorical features

---

## Part 2: CBR System Architecture

### 2.1 Core CBR Components

#### A. Data Structures
```
Case: {
    features: dict,          # attribute names -> values
    solution: value/class,   # target label or regression value
    metadata: dict           # timestamps, etc.
}

CaseBase: List[Case]
Query: Case without solution
```

#### B. Main CBR Cycle Function
```python
def run_query(case_base, query):
    """
    Core CBR cycle:
    1. Retrieve: Find most similar case(s)
    2. Adapt: Modify solution based on differences
    3. Solve: Return adapted solution
    4. Retain: Add new case to case base
    """
    # Returns: [solution, updated_case_base]
```

---

## Part 3: Implementation Strategy

### 3.1 Phase 1: Data Loading & Preprocessing
**What to do**:
1. Parse car.data (CSV format)
2. Parse ENB2012_data.xlsx (Excel format)
3. Create standardized Case objects for each dataset
4. Implement train/test split (80/20)
5. Store case base as initial training set

**Key Decisions**:
- Use pandas for data loading
- Create separate data loader functions for each dataset
- Normalize/encode categorical data appropriately

---

### 3.2 Phase 2: Similarity Computation (Retrieval)

#### A. Feature-Level Similarity Functions

**For Classification (Car Dataset)**:
1. **Categorical Direct Match**: 
   - Same value = 1.0, Different = 0.0
   - Simple but effective for discrete attributes

2. **Ordinal Similarity** (where applicable):
   - `buying`, `maint`, `safety`, `lug_boot` have implicit ordering
   - Example: `buying: vhigh=4, high=3, med=2, low=1`
   - Similarity = 1 - |rank1 - rank2| / max_rank_diff

3. **Domain-Specific Hierarchies**:
   - Use known relationships from car.names structure
   - Example: doors have ordering (2 < 3 < 4 < 5more)

**For Regression (Energy Dataset)**:
1. **Numerical Distance**:
   - Euclidean distance: sqrt(sum((v1-v2)²))
   - Normalized Euclidean (after z-score normalization)

2. **Categorical Matching**:
   - Direct match for categorical features

#### B. Overall Similarity Computation

**Baseline (Untuned)**:
```
similarity = (sum of individual feature similarities) / number of features
All features weighted equally (weight = 1.0)
```

**Tuned**:
```
similarity = sum(weight_i * feature_similarity_i) / sum(weights)
Different weights per feature based on domain understanding
```

**Feature Weighting Strategy**:

For **Car Classification**:
- `safety`: 0.3 (most important for car quality)
- `persons`: 0.2 (capacity matters)
- `buying`: 0.2 (price is significant)
- `maint`: 0.1 (maintenance cost secondary)
- `lug_boot`: 0.1 (comfort feature)
- `doors`: 0.1 (less critical)

For **Energy Regression**:
- Identify most correlated features with heating load
- Weight features by correlation coefficient
- Normalize numerical features

---

### 3.3 Phase 3: Adaptation Strategy

#### A. Regression Adaptation (4+ Rules Required)

**Rule 1: Difference Scaling**
- Calculate feature differences between query and retrieved case
- Scale the retrieved solution by the magnitude of differences
- Formula: `adapted_solution = retrieved_solution * (1 + scaling_factor)`

**Rule 2: Linear Extrapolation**
- If query differs significantly from retrieved case
- Estimate a linear relationship: `solution_delta ≈ feature_delta * slope`
- Find slope from case base patterns

**Rule 3: Multi-Case Averaging**
- Retrieve top-k similar cases (e.g., k=3)
- Adapt each and average their solutions
- Gives more robust predictions

**Rule 4: Segment-Based Adaptation**
- Divide case base into segments (e.g., by energy level)
- Identify which segment query belongs to
- Apply segment-specific adaptation rules

**Rule 5 (Optional): Attribute-Specific Adaptation**
- Track which features changed most
- Apply different adaptation strategies based on which features matter

#### B. Classification Adaptation (2-4 Rules Required)

**Rule 1: Confidence-Based Threshold**
- Retrieve most similar case
- If similarity > threshold (e.g., 0.8), use its solution directly
- Else, classify as uncertain/borderline

**Rule 2: Multi-Case Voting**
- Retrieve top-k cases
- Use majority voting on their classes
- Weight votes by similarity

**Rule 3: Feature-Based Refinement**
- If query's safety is much better than retrieved case → upgrade class
- If query's price is much worse → downgrade class
- Apply domain-specific rules

**Rule 4: Confidence Scoring**
- Combine solutions from top-3 similar cases
- Higher confidence if all agree
- Penalize confidence if they disagree

---

### 3.4 Phase 4: Learning & Retention

**Storage Logic**:
- After solving query, add new case to case base
- For "non-learning" condition: disable this step
- For "tuned" condition: enable learning

---

## Part 4: Testing & Evaluation

### 4.1 Evaluation Conditions

**For Regression**:
1. **Condition 1: Untuned**
   - Baseline similarity (equal weights)
   - No adaptation
   - Learning enabled

2. **Condition 2: Tuned**
   - Weighted similarity features
   - Full adaptation (4+ rules)
   - Learning enabled

3. **Condition 3: Tuned Non-Learning**
   - Weighted similarity features
   - Full adaptation (4+ rules)
   - Learning disabled (case base frozen)

**For Classification**:
1. **Condition 1: Untuned**
   - Baseline similarity
   - No adaptation
   - Just return retrieved case's class

2. **Condition 2: Tuned Similarity**
   - Weighted similarity features
   - No adaptation

3. **Condition 3: Tuned with Adaptation**
   - Weighted similarity features
   - Rule-based adaptation (2-4 rules)

### 4.2 Metrics
- **Regression**: MAE (Mean Absolute Error) or RMSE (Root Mean Squared Error)
- **Classification**: Accuracy (%)
- Report results for each condition
- Compare to establish tuning effects

---

## Part 5: Code Structure

### Directory Layout
```
Assignment3_KBAI/
├── cbr_system.py          # Core CBR implementation
├── car_cbr.py             # Car classification system
├── energy_cbr.py          # Energy regression system
├── data_loader.py         # Data loading utilities
├── evaluation.py          # Evaluation metrics
├── main.py                # Main execution script
├── README.md              # Documentation
└── IMPLEMENTATION_PLAN.md # This file
```

### Key Implementation Order
1. **data_loader.py**: Load and parse both datasets
2. **cbr_system.py**: Core similarity, retrieval, adaptation logic
3. **car_cbr.py**: Instantiate CBR with car-specific knowledge
4. **energy_cbr.py**: Instantiate CBR with energy-specific knowledge
5. **evaluation.py**: Implement evaluation metrics
6. **main.py**: Run all 6 conditions and collect results

---

## Part 6: Detailed Implementation Checklist

### Phase 1: Data Loading
- [ ] Load car.data with correct attribute names
- [ ] Load ENB2012 Excel file
- [ ] Create Case objects for each instance
- [ ] Implement 80/20 train/test split with random seed
- [ ] Normalize numerical features (z-score or min-max)
- [ ] Encode categorical features appropriately

### Phase 2: Core CBR
- [ ] Implement feature similarity functions
- [ ] Implement weighted similarity computation
- [ ] Implement retrieval (find most similar case)
- [ ] Implement case storage/learning
- [ ] Create run_query function

### Phase 3: Adaptation
- [ ] Implement 4+ adaptation rules for regression
- [ ] Implement 2-4 adaptation rules for classification
- [ ] Create adaptation selection logic
- [ ] Test adaptation with sample cases

### Phase 4: Evaluation
- [ ] Implement cross-validation or train/test split
- [ ] Calculate MAE/RMSE for regression
- [ ] Calculate accuracy for classification
- [ ] Run all 6 test conditions
- [ ] Collect and tabulate results

### Phase 5: Documentation
- [ ] Write clear comments in code
- [ ] Document adaptation rules with rationale
- [ ] Create README.md with instructions
- [ ] Write PDF report with sections:
  - Introduction
  - Retrieval Strategy
  - Adaptation Strategy
  - Results
  - Conclusion

---

## Part 7: Expected Outcomes & Insights

### Key Insights to Look For

**Regression (Energy)**:
1. Will adaptation improve MAE/RMSE?
2. How much do feature weights matter?
3. Does learning improve over time?
4. Which adaptation rules work best?

**Classification (Car)**:
1. Can CBR with similarity alone achieve reasonable accuracy?
2. How much does adaptation help?
3. Are there cases that are hard to classify?

### Likely Challenges
1. **Cold Start Problem**: Initial case base might be small/unrepresentative
2. **Feature Weighting**: Hard to determine optimal weights
3. **Adaptation Effectiveness**: Overfitting to training cases
4. **Computational Cost**: With 1700+ cases, similarity computation could be slow

### Solutions
1. Use larger initial case base (don't shrink training set too much)
2. Use domain knowledge and correlation analysis
3. Test adaptation on held-out test set
4. Optimize similarity computation (vectorization)

---

## Timeline Recommendation

**Week 1** (by Feb 27):
- [ ] Phase 1: Complete data loading
- [ ] Phase 2: Implement basic similarity

**Week 2** (by Feb 28):
- [ ] Phase 3: Implement all adaptation rules
- [ ] Phase 4: Set up evaluation framework

**Before Deadline** (by March 1):
- [ ] Complete testing on all 6 conditions
- [ ] Write report
- [ ] Final submission

---

## Next Steps

1. **Confirm understanding** of both datasets
2. **Create basic file structure** (data_loader.py, cbr_system.py, etc.)
3. **Implement data loading** first
4. **Build core CBR** loop
5. **Add domain-specific knowledge** (similarity weights, adaptation rules)
6. **Evaluate comprehensively**
7. **Write report**

---

This plan ensures a systematic, well-tested implementation that demonstrates deep understanding of CBR principles while meeting all assignment requirements.
