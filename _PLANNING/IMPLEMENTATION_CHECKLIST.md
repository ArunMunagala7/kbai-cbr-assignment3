# CBR Assignment 3 - Implementation Checklist

Use this document to track your progress. Check off items as you complete them.

---

## 📅 Timeline & Milestones

```
┌─────────────────────────────────────────────────────┐
│ DAY 1 (Feb 27): PLANNING & SETUP                   │
│ ✓ Read planning documents                          │
│ ✓ Understand assignment requirements               │
│ ✓ Create project structure                         │
└─────────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────────┐
│ DAY 2-3: CORE IMPLEMENTATION                       │
│ ✓ Data loading                                     │
│ ✓ Similarity computation                           │
│ ✓ Retrieval logic                                  │
│ ✓ Adaptation rules                                 │
└─────────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────────┐
│ DAY 4: TESTING & EVALUATION                        │
│ ✓ Run all 6 test conditions                        │
│ ✓ Verify results make sense                        │
│ ✓ Fix any bugs                                     │
└─────────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────────┐
│ DAY 5 (Mar 1): DOCUMENTATION & SUBMISSION          │
│ ✓ Write README.md                                  │
│ ✓ Write report.pdf                                 │
│ ✓ SUBMIT by 11:59 PM                               │
└─────────────────────────────────────────────────────┘
```

---

## ✅ PHASE 1: Understanding & Planning

**Expected Duration**: 90 minutes (or quick-skim 20 min)

### Reading Planning Documents:
- [ ] Read **00_START_HERE.md** (15 min) - Complete overview
- [ ] Read **ONE_PAGE_SUMMARY.md** (5 min) - Quick reference
- [ ] Read **CONCRETE_EXAMPLES.md** (20 min) - Worked examples
- [ ] Skim **ARCHITECTURE_DIAGRAMS.md** (10 min) - Visual design
- [ ] (Optional) Read **IMPLEMENTATION_PLAN.md** (20 min) - Detailed strategy

### Understanding Requirements:
- [ ] Understand 4-step CBR cycle (retrieve → adapt → solve → retain)
- [ ] Understand the 6 test conditions
- [ ] Understand expected results pattern
- [ ] Understand what goes in final report

### Datasets:
- [ ] Examined car.data (1,728 cars, 6 features)
- [ ] Examined car.names (feature descriptions)
- [ ] Examined ENB2012_data.xlsx (building data)
- [ ] Understand classification task (car evaluation)
- [ ] Understand regression task (heating load)

---

## ✅ PHASE 2: Project Setup

**Expected Duration**: 30 minutes

### Create File Structure:
- [ ] Create **data_loader.py** (empty file, ready to code)
- [ ] Create **cbr_system.py** (empty file)
- [ ] Create **car_cbr.py** (empty file)
- [ ] Create **energy_cbr.py** (empty file)
- [ ] Create **evaluation.py** (empty file)
- [ ] Create **main.py** (empty file)

### Initialize Version Control (Optional):
- [ ] Initialize git repository
- [ ] Create .gitignore

### Dependencies:
- [ ] Plan which libraries to use (pandas, numpy, etc.)
- [ ] Document dependencies in requirements.txt

---

## ✅ PHASE 3: Data Loading

**Expected Duration**: 2-3 hours

### Implement data_loader.py:
- [ ] Create `Case` class or namedtuple
  - [ ] Has `features` (dict)
  - [ ] Has `solution` (value for regression, class for classification)
- [ ] Implement `load_car_data()`
  - [ ] Read car.data CSV
  - [ ] Parse all 6 features
  - [ ] Create Case objects for each row
  - [ ] Return list of Cases
  - [ ] Test: print first 5 cases
- [ ] Implement `load_energy_data()`
  - [ ] Read ENB2012_data.xlsx
  - [ ] Parse all features
  - [ ] Create Case objects
  - [ ] Return list of Cases
  - [ ] Test: print first 5 cases

### Data Preprocessing:
- [ ] Implement feature normalization
  - [ ] Z-score normalization for numerical features
  - [ ] Encoding for categorical features (if needed)
- [ ] Implement train/test split
  - [ ] 80/20 split for both datasets
  - [ ] Set random seed for reproducibility
- [ ] Test: Verify data is loaded correctly
  - [ ] Print sample cases
  - [ ] Verify feature ranges
  - [ ] Verify target values

### Testing:
- [ ] Test loading car data: verify 1,728 cases
- [ ] Test loading energy data: verify correct number
- [ ] Test Case objects are created correctly
- [ ] Test data splits work correctly

---

## ✅ PHASE 4: Similarity & Retrieval

**Expected Duration**: 3-4 hours

### Implement cbr_system.py:

#### Similarity Functions:
- [ ] Implement `categorical_similarity(val1, val2)`
  - [ ] Direct match: same = 1.0, different = 0.0
  - [ ] OR ordinal: use hierarchy if applicable
- [ ] Implement `numerical_similarity(val1, val2)`
  - [ ] Normalize values if needed
  - [ ] Calculate distance
  - [ ] Convert to similarity (0-1 scale)
- [ ] Implement `feature_similarity(val1, val2, feature_type)`
  - [ ] Dispatch to appropriate function based on type
  - [ ] Return 0-1 similarity score

#### Overall Similarity:
- [ ] Implement `calculate_similarity(case1, case2, weights=None)`
  - [ ] For each feature: calculate feature similarity
  - [ ] If weights provided: apply weighted average
  - [ ] Else: simple average (baseline)
  - [ ] Return 0-1 similarity score
  - [ ] Test: cases identical → similarity = 1.0
  - [ ] Test: cases very different → similarity ≈ 0.0

#### Retrieval:
- [ ] Implement `retrieve_most_similar(query, case_base, weights=None)`
  - [ ] Calculate similarity to all cases
  - [ ] Find case with max similarity
  - [ ] Return that case
  - [ ] Test: retrieve case should be most similar

#### Testing:
- [ ] Test similarity is between 0 and 1
- [ ] Test identical cases have similarity 1.0
- [ ] Test very different cases have low similarity
- [ ] Test retrieval returns most similar case
- [ ] Test weighted similarities differ from unweighted
- [ ] Test with sample car data
- [ ] Test with sample energy data

---

## ✅ PHASE 5: Adaptation Rules

**Expected Duration**: 3-4 hours

### For Regression (energy_cbr.py):

#### Rule 1: Difference Scaling
- [ ] Implement difference calculation
- [ ] Implement scaling formula
- [ ] Test with sample cases

#### Rule 2: Linear Extrapolation
- [ ] Calculate feature deltas
- [ ] Learn slopes from case base patterns
- [ ] Apply extrapolation
- [ ] Test with sample cases

#### Rule 3: Multi-Case Averaging
- [ ] Implement retrieval of top-k cases
- [ ] Adapt each case
- [ ] Average results
- [ ] Test with sample cases

#### Rule 4: Segment-Based Adaptation
- [ ] Identify segments in case base
- [ ] Classify query into segment
- [ ] Apply segment-specific rules
- [ ] Test with sample cases

#### Rule 5 (Optional): Additional Rules
- [ ] Implement attribute-weighted scaling
- [ ] OR feature-importance adaptation
- [ ] Test with sample cases

#### Core Adaptation:
- [ ] Implement `adapt_regression(retrieved_case, query_case)`
  - [ ] Call all 4+ rules
  - [ ] Combine results (average)
  - [ ] Return adapted solution
  - [ ] Test: adaptation should improve accuracy

### For Classification (car_cbr.py):

#### Rule 1: Feature Refinement
- [ ] Identify feature improvements/deteriorations
- [ ] Map to class adjustments
- [ ] Apply adjustments
- [ ] Test with sample cases

#### Rule 2: Multi-Case Voting
- [ ] Retrieve top-3 cases
- [ ] Adapt each one
- [ ] Vote on class
- [ ] Return majority class
- [ ] Test: voting should give reasonable results

#### Rule 3: Confidence Threshold
- [ ] Calculate confidence from similarity/agreement
- [ ] Apply different strategies based on confidence
- [ ] Test with sample cases

#### Rule 4 (Optional): Weighted Voting
- [ ] Weight votes by similarity
- [ ] Return weighted majority
- [ ] Test with sample cases

#### Core Adaptation:
- [ ] Implement `adapt_classification(retrieved_case, query_case)`
  - [ ] Call 2-4 rules
  - [ ] Combine results (majority vote)
  - [ ] Return adapted class
  - [ ] Test: adaptation should improve accuracy

### Testing Adaptation:
- [ ] Test each rule individually
- [ ] Test combined adaptation
- [ ] Verify adaptation improves on baseline
- [ ] Verify results are reasonable

---

## ✅ PHASE 6: Core CBR Loop

**Expected Duration**: 1-2 hours

### Implement run_query():
- [ ] Create `run_query(case_base, query, tuned=False, adapt=False, learning=True)`
  - [ ] **Retrieve**: Find most similar case
    - [ ] Use tuned weights if tuned=True
    - [ ] Use equal weights if tuned=False
  - [ ] **Adapt**: Modify solution
    - [ ] Call adapt_solution() if adapt=True
    - [ ] Return retrieved solution if adapt=False
  - [ ] **Solve**: Return the solution
  - [ ] **Retain**: Add to case base if learning=True
    - [ ] Create new Case with query + solution
    - [ ] Append to case_base if learning=True
    - [ ] Skip if learning=False
  - [ ] Return: [solution, updated_case_base]

### Testing:
- [ ] Test returns solution
- [ ] Test returns updated case base
- [ ] Test learning adds cases (when enabled)
- [ ] Test learning doesn't add cases (when disabled)
- [ ] Test with tuned=True/False
- [ ] Test with adapt=True/False

---

## ✅ PHASE 7: Evaluation

**Expected Duration**: 1-2 hours

### Implement evaluation.py:

#### Regression Metrics:
- [ ] Implement `calculate_mae(predictions, actuals)`
  - [ ] MAE = mean(abs(prediction - actual))
- [ ] Implement `calculate_rmse(predictions, actuals)`
  - [ ] RMSE = sqrt(mean((prediction - actual)²))

#### Classification Metrics:
- [ ] Implement `calculate_accuracy(predictions, actuals)`
  - [ ] Accuracy = count(correct) / total
  - [ ] Return as percentage (0-100)

### Testing:
- [ ] Test metrics with sample predictions
- [ ] Verify metrics are in reasonable ranges

---

## ✅ PHASE 8: Run All Tests

**Expected Duration**: 2-3 hours

### Implement main.py:

#### Test Setup:
- [ ] Load car data
- [ ] Load energy data
- [ ] Split into train/test (80/20)

#### Regression Tests (3 conditions):
- [ ] **Test 1: Regression Untuned**
  - [ ] tuned=False, adapt=False, learning=True
  - [ ] Run on energy test set
  - [ ] Calculate MAE/RMSE
  - [ ] Record results

- [ ] **Test 2: Regression Tuned**
  - [ ] tuned=True, adapt=True, learning=True
  - [ ] Run on energy test set
  - [ ] Calculate MAE/RMSE
  - [ ] Record results

- [ ] **Test 3: Regression Tuned No-Learning**
  - [ ] tuned=True, adapt=True, learning=False
  - [ ] Run on energy test set
  - [ ] Calculate MAE/RMSE
  - [ ] Record results

#### Classification Tests (3 conditions):
- [ ] **Test 4: Classification Untuned**
  - [ ] tuned=False, adapt=False
  - [ ] Run on car test set
  - [ ] Calculate accuracy
  - [ ] Record results

- [ ] **Test 5: Classification Tuned**
  - [ ] tuned=True, adapt=False
  - [ ] Run on car test set
  - [ ] Calculate accuracy
  - [ ] Record results

- [ ] **Test 6: Classification Tuned+Adapt**
  - [ ] tuned=True, adapt=True
  - [ ] Run on car test set
  - [ ] Calculate accuracy
  - [ ] Record results

#### Results:
- [ ] Print results table
- [ ] Verify tuned > untuned (approximately)
- [ ] Save results to file or CSV

### Verification:
- [ ] All 6 tests run without errors
- [ ] Results make sense
- [ ] Pattern: Tuned > Untuned
- [ ] Pattern: Adaptation/Learning help

---

## ✅ PHASE 9: Code Quality & Documentation

**Expected Duration**: 1-2 hours

### Code Documentation:
- [ ] Add docstrings to all functions
- [ ] Add inline comments explaining complex logic
- [ ] Document each adaptation rule clearly
- [ ] Document why features are weighted as they are
- [ ] Add type hints to functions

### Code Quality:
- [ ] No hard-coded paths (use relative paths)
- [ ] Error handling for edge cases
- [ ] Consistent variable naming
- [ ] Clean, readable code
- [ ] Remove debug print statements
- [ ] Set random seed for reproducibility

### Code Organization:
- [ ] Each file has clear responsibility
- [ ] Related functions grouped together
- [ ] No unnecessary duplication
- [ ] Efficient implementations

---

## ✅ PHASE 10: Write README.md

**Expected Duration**: 45 minutes

### Required Sections:
- [ ] **Title**: CBR System for Car Evaluation and Energy Efficiency
- [ ] **Description**: Brief overview of what the system does
- [ ] **Installation**: How to install dependencies
  - [ ] Python version required
  - [ ] Required libraries
  - [ ] `pip install -r requirements.txt` instructions
- [ ] **Usage**: How to run the code
  - [ ] Command: `python main.py`
  - [ ] Expected output
  - [ ] Description of results table
- [ ] **Files**: What each file does
  - [ ] Brief description of each .py file
  - [ ] Data files location
- [ ] **Results**: Summary of 6 test results
  - [ ] Table showing all conditions and metrics
  - [ ] Key findings
- [ ] **Authors**: Team members and their contributions
- [ ] **Notes**: Any important information

---

## ✅ PHASE 11: Write Report (PDF)

**Expected Duration**: 2-3 hours

### For Car Evaluation (Classification):
- [ ] **Introduction**
  - [ ] What problem are we solving?
  - [ ] Dataset description (1,728 cars, 6 features)
  - [ ] Why is this problem interesting?

- [ ] **Retrieval Strategy**
  - [ ] How do you measure similarity?
  - [ ] Formula for similarity calculation
  - [ ] Feature comparison methods
  - [ ] Feature weights for tuned condition
  - [ ] Justification for weights
  - [ ] Example: "Safety is weighted 0.30 because..."

- [ ] **Adaptation Strategy**
  - [ ] List 2-4 adaptation rules
  - [ ] For each rule:
    - [ ] Name and purpose
    - [ ] How it works (steps or pseudocode)
    - [ ] Why you chose it
  - [ ] Example: "Rule 1: Feature Refinement - If safety improves, upgrade class"

- [ ] **Results**
  - [ ] Table showing all 3 test conditions
  - [ ] Accuracy percentages
  - [ ] Analysis:
    - [ ] Did tuning help? By how much?
    - [ ] Did adaptation help? By how much?
    - [ ] Comparison to expected results

- [ ] **Conclusion**
  - [ ] Summary of findings
  - [ ] Were results as expected?
  - [ ] Any surprising results? Why?
  - [ ] What was most challenging?
  - [ ] What did you learn about CBR?

### For Energy Efficiency (Regression):
- [ ] **Introduction**
  - [ ] What problem are we solving?
  - [ ] Dataset description
  - [ ] Why is this problem interesting?

- [ ] **Retrieval Strategy**
  - [ ] How do you measure similarity?
  - [ ] Normalization of numerical features
  - [ ] Feature weights for tuned condition
  - [ ] Justification for weights
  - [ ] Distance metrics used

- [ ] **Adaptation Strategy**
  - [ ] List 4+ adaptation rules
  - [ ] For each rule:
    - [ ] Name and purpose
    - [ ] Formula or pseudocode
    - [ ] Why you chose it
  - [ ] Example: "Rule 1: Difference Scaling - Scale solution by feature delta magnitude"

- [ ] **Results**
  - [ ] Table showing all 3 test conditions
  - [ ] Error metrics (MAE/RMSE)
  - [ ] Analysis:
    - [ ] Did tuning help? By how much?
    - [ ] Did adaptation help? By how much?
    - [ ] Did learning help? Evidence?
    - [ ] Comparison to expected results

- [ ] **Conclusion**
  - [ ] Summary of findings
  - [ ] Were results as expected?
  - [ ] Any surprising results? Why?
  - [ ] What was most challenging?
  - [ ] What did you learn about CBR for regression?

### General:
- [ ] Professional appearance
- [ ] Clear writing
- [ ] No spelling/grammar errors
- [ ] Figures/tables as needed
- [ ] Proper citations if used external sources

---

## ✅ PHASE 12: Final Review & Submission

**Expected Duration**: 1 hour

### Code Review:
- [ ] All files present and complete
- [ ] All functions documented
- [ ] No syntax errors
- [ ] Runs without crashing
- [ ] Results are saved and printed clearly

### Documentation Review:
- [ ] README.md is complete and clear
- [ ] report.pdf has all required sections
- [ ] Writing is clear and professional
- [ ] Results are presented clearly
- [ ] Analysis is thoughtful

### Testing:
- [ ] Run main.py one final time
- [ ] Verify all 6 tests pass
- [ ] Verify results make sense
- [ ] Verify tuned > untuned

### Submission Preparation:
- [ ] Organize all files in assignment folder
- [ ] Create final submission archive if needed
- [ ] Double-check Canvas submission format
- [ ] **SUBMIT on Canvas**

---

## 📊 Results Verification Checklist

### Expected Pattern Check:
```
Regression should show:
[ ] Test 1 (untuned) >> Test 2 (tuned)
[ ] Test 2 (learning) < Test 3 (no learning)
[ ] Pattern: untuned >> tuned with learning >> tuned no learning

Classification should show:
[ ] Test 4 (untuned) < Test 5 (tuned)
[ ] Test 5 (tuned) < Test 6 (tuned+adapt)
[ ] Pattern: untuned < tuned < tuned+adaptation
```

### If results DON'T show this pattern:
- [ ] Review similarity calculation
- [ ] Check weight application
- [ ] Verify adaptation rules are working
- [ ] Check learning is actually happening
- [ ] Review case base updates

---

## 🎯 Success Criteria

✅ **Must Have** (for full credit):
- [ ] All 6 tests run successfully
- [ ] Code is well-documented
- [ ] Report includes all required sections
- [ ] Tuned performs better than untuned
- [ ] Results are clearly presented

✅ **Should Have** (for good credit):
- [ ] Code is well-organized
- [ ] Adaptation rules are thoughtfully designed
- [ ] Report includes detailed analysis
- [ ] Results match expected pattern
- [ ] Learning effect is demonstrated

✅ **Nice to Have** (for excellent credit):
- [ ] Code is optimized
- [ ] Multiple weight configurations tested
- [ ] Comparative analysis of rules
- [ ] Visualization of results
- [ ] Discussion of computational efficiency

---

## 📅 Schedule (Adjust as Needed)

**DAY 1 (Feb 27)**:
- Morning (2 hrs): Read planning documents
- Afternoon (2 hrs): Complete Phases 1-2
- Evening (1 hr): Start Phase 3

**DAY 2 (Feb 27)**:
- Full day (8 hrs): Complete Phases 3-4
- Checkpoint: data loading + similarity working

**DAY 3 (Feb 28)**:
- Full day (8 hrs): Complete Phases 5-6
- Checkpoint: CBR loop running

**DAY 4 (Feb 28)**:
- Morning (4 hrs): Complete Phases 7-8
- Afternoon (3 hrs): Code review, fix bugs
- Evening (1 hr): Begin Phase 9

**DAY 5 (Mar 1)**:
- Early (2 hrs): Complete Phase 9
- Mid (3 hrs): Complete Phase 10-11
- Late (2 hrs): Final review and submission
- **SUBMIT BEFORE 11:59 PM**

---

## 🚨 Red Flags (Stop and Fix if These Happen)

If you encounter these issues:

❌ **"Data won't load"**
→ Check file paths, encoding, format

❌ **"Similarity always 0 or 1"**
→ Review feature comparison logic, normalization

❌ **"Tuned worse than untuned"**
→ Check weight application, values

❌ **"Adaptation makes accuracy worse"**
→ Review rule logic, test each rule individually

❌ **"Learning doesn't help"**
→ Verify case_base.add() is actually happening

❌ **"All results identical"**
→ Check that different conditions are being tested

❌ **"Code crashes on test set"**
→ Add error handling, test with smaller set

---

## 💡 Pro Tips

1. **Test early and often** - Don't wait until end to test
2. **Start with one test condition** - Get it working perfectly
3. **Then add others** - Easier to debug
4. **Keep backups** - Save working versions before major changes
5. **Print intermediate results** - Know what your code is doing
6. **Set random seed** - Make results reproducible
7. **Document as you code** - Harder to do later
8. **Reference planning docs** - Don't try to remember everything

---

## ✨ You've Got This!

You have:
✅ Comprehensive planning documents
✅ Clear checklist to follow
✅ Expected results to verify against
✅ Timeline to stay on track

**Just follow the checklist step-by-step and you'll complete this assignment successfully!**

---

**Start with Phase 1 → Work through each phase → SUBMIT by deadline**

**Good luck! 🚀**
