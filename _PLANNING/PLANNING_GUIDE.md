# CBR Assignment 3 - Planning Documents Index

## 📚 Complete Planning Documentation

This folder now contains comprehensive planning documents for your CBR assignment. Here's how to use them:

---

## 📖 Reading Guide

### Start Here (If Short on Time):
1. **ONE_PAGE_SUMMARY.md** ⭐ (5 min read)
   - TL;DR version of everything
   - Quick reference for implementation
   - Timeline and checklist

2. **EXECUTIVE_SUMMARY.md** (10 min read)
   - What you're building
   - Implementation roadmap
   - Key decisions to make

### Deep Understanding (Before Coding):
3. **QUICK_REFERENCE.md** (15 min read)
   - Overview of CBR process
   - Test configuration matrix
   - What to include in report

4. **ARCHITECTURE_DIAGRAMS.md** (15 min read)
   - Visual flowcharts
   - Data flow diagrams
   - How the 6 tests work

5. **CONCRETE_EXAMPLES.md** (20 min read)
   - Real worked examples with numbers
   - Show exactly how to calculate similarity
   - Demonstrate adaptation rules
   - Common pitfalls explained

### Strategic Reference (During Implementation):
6. **IMPLEMENTATION_PLAN.md** (25 min read)
   - Complete detailed strategy
   - All 4+ adaptation rules for regression
   - All 2-4 adaptation rules for classification
   - Feature weighting strategies
   - Evaluation methodology
   - Detailed checklist

---

## 📋 Document Summary Table

| Document | Purpose | Length | When to Use |
|----------|---------|--------|------------|
| **ONE_PAGE_SUMMARY.md** | Quick reference | 1 page | Before starting / reminder |
| **EXECUTIVE_SUMMARY.md** | Overview & roadmap | 3 pages | Planning phase |
| **QUICK_REFERENCE.md** | Concept summary | 2 pages | Need CBR reminder |
| **ARCHITECTURE_DIAGRAMS.md** | Visual flows | 4 pages | Understanding system design |
| **CONCRETE_EXAMPLES.md** | Worked examples | 5 pages | During implementation |
| **IMPLEMENTATION_PLAN.md** | Detailed strategy | 8 pages | Reference during coding |

**Total**: ~23 pages of comprehensive planning
**Time to read all**: ~90 minutes
**Time to skim key parts**: ~20 minutes

---

## 🎯 How to Use These Documents

### Phase 1: Understanding (Day 1)
- [ ] Read **ONE_PAGE_SUMMARY.md** (understand what you're building)
- [ ] Skim **EXECUTIVE_SUMMARY.md** (get implementation roadmap)
- [ ] Review **ARCHITECTURE_DIAGRAMS.md** (visualize the system)
- **Time**: 30 minutes

### Phase 2: Detailed Planning (Day 1)
- [ ] Read **IMPLEMENTATION_PLAN.md** (detailed strategy)
- [ ] Read **QUICK_REFERENCE.md** (CBR process details)
- [ ] Study **CONCRETE_EXAMPLES.md** (worked examples)
- **Time**: 1 hour

### Phase 3: Implementation (Days 2-4)
- [ ] Create **data_loader.py** (reference: IMPLEMENTATION_PLAN.md section 3.1)
- [ ] Build **cbr_system.py** (reference: ARCHITECTURE_DIAGRAMS.md)
- [ ] Add **car_cbr.py** (reference: CONCRETE_EXAMPLES.md)
- [ ] Add **energy_cbr.py** (reference: CONCRETE_EXAMPLES.md)
- [ ] Create **evaluation.py** (reference: IMPLEMENTATION_PLAN.md section 4.2)
- [ ] Write **main.py** (reference: ARCHITECTURE_DIAGRAMS.md section 7)
- Keep **ONE_PAGE_SUMMARY.md** as desk reference

### Phase 4: Testing (Day 4)
- [ ] Run all 6 conditions
- [ ] Compare results to expectations (ARCHITECTURE_DIAGRAMS.md section 8)
- [ ] Verify tuned > untuned

### Phase 5: Reporting (Day 5)
- [ ] Write README.md
- [ ] Write report.pdf
- [ ] Use **EXECUTIVE_SUMMARY.md** for report structure
- [ ] Reference **CONCRETE_EXAMPLES.md** for examples

---

## 🔍 Quick Lookup Guide

**What are the 4+ adaptation rules for regression?**
→ See **IMPLEMENTATION_PLAN.md** section 3.3 Part A

**How do I calculate similarity?**
→ See **CONCRETE_EXAMPLES.md** Example 1 & Example 2

**What are the 6 test conditions?**
→ See **ARCHITECTURE_DIAGRAMS.md** section 5

**What feature weights should I use?**
→ See **IMPLEMENTATION_PLAN.md** section 3.2 Part B
→ Or **CONCRETE_EXAMPLES.md** Example 1

**How do adaptation rules work?**
→ See **CONCRETE_EXAMPLES.md** Examples 2 & 3

**What's the expected output?**
→ See **ARCHITECTURE_DIAGRAMS.md** section 8

**What should be in my report?**
→ See **EXECUTIVE_SUMMARY.md** "Report Contents"

**What's my implementation timeline?**
→ See **ONE_PAGE_SUMMARY.md** or **IMPLEMENTATION_PLAN.md** section 7

---

## ✅ Implementation Checklist

Use this checklist from **IMPLEMENTATION_PLAN.md** section 6 while coding:

### Phase 1: Data Loading
- [ ] Load car.data with correct attribute names
- [ ] Load ENB2012 Excel file
- [ ] Create Case objects for each instance
- [ ] Implement 80/20 train/test split with random seed
- [ ] Normalize/encode categorical data appropriately

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
- [ ] Write PDF report with sections

---

## 📁 File Organization

```
Assignment3_KBAI/
│
├── 📋 PLANNING DOCUMENTS (these files)
│   ├── ONE_PAGE_SUMMARY.md
│   ├── EXECUTIVE_SUMMARY.md
│   ├── QUICK_REFERENCE.md
│   ├── ARCHITECTURE_DIAGRAMS.md
│   ├── CONCRETE_EXAMPLES.md
│   ├── IMPLEMENTATION_PLAN.md
│   └── PLANNING_GUIDE.md (this file)
│
├── 📊 DATA FILES
│   ├── car.data (1,728 cars)
│   ├── car.names (car attributes description)
│   └── ENB2012_data.xlsx (building data)
│
├── 💻 CODE FILES (create these)
│   ├── data_loader.py
│   ├── cbr_system.py
│   ├── car_cbr.py
│   ├── energy_cbr.py
│   ├── evaluation.py
│   └── main.py
│
├── 📝 OUTPUT FILES (create these)
│   ├── README.md
│   └── report.pdf
│
└── 📦 SUBMISSION
    └── All code + README + report.pdf
```

---

## 🚀 Quick Start Instructions

### Option A: 20-Minute Quick Start
1. Read **ONE_PAGE_SUMMARY.md**
2. Read **CONCRETE_EXAMPLES.md** Example 1 & 2
3. Start coding **data_loader.py**

### Option B: 90-Minute Complete Understanding
1. Read all 6 planning documents in order
2. Study **ARCHITECTURE_DIAGRAMS.md** carefully
3. Review **CONCRETE_EXAMPLES.md** for each concept
4. Start coding with full confidence

### Option C: Just-in-Time Reference
1. Start coding **data_loader.py**
2. When stuck, consult relevant section:
   - Similarity questions → **CONCRETE_EXAMPLES.md**
   - Architecture questions → **ARCHITECTURE_DIAGRAMS.md**
   - Adaptation rules → **IMPLEMENTATION_PLAN.md**
   - Timeline/checklist → **ONE_PAGE_SUMMARY.md**

---

## 💡 Pro Tips

1. **Keep ONE_PAGE_SUMMARY.md visible** while coding as reference
2. **Reference CONCRETE_EXAMPLES.md** for exact calculation methods
3. **Use ARCHITECTURE_DIAGRAMS.md** as pseudo-code for main functions
4. **Mark IMPLEMENTATION_PLAN.md** with bookmarks** for quick lookup
5. **Check EXECUTIVE_SUMMARY.md** before writing report

---

## 📞 When You Get Stuck

| Problem | Solution | Document |
|---------|----------|----------|
| "How do I calculate similarity?" | Look at worked example | CONCRETE_EXAMPLES.md |
| "What are the adaptation rules?" | See detailed list | IMPLEMENTATION_PLAN.md |
| "What's the system architecture?" | View flowchart | ARCHITECTURE_DIAGRAMS.md |
| "What should I code first?" | Check timeline | EXECUTIVE_SUMMARY.md |
| "How do I run the tests?" | See pseudo-code | ARCHITECTURE_DIAGRAMS.md |
| "What should be in my report?" | Check structure | EXECUTIVE_SUMMARY.md |

---

## 🎓 Learning Outcomes

After reading these documents, you will understand:
- ✅ What Case-Based Reasoning is and how it works
- ✅ The 4-step CBR cycle (retrieve → adapt → solve → retain)
- ✅ How to measure similarity between cases
- ✅ How to design adaptation rules for regression
- ✅ How to design adaptation rules for classification
- ✅ How to implement a complete CBR system
- ✅ How to evaluate CBR system performance
- ✅ Best practices for feature weighting and rule design

---

## 📅 Recommended Schedule

```
Day 1 (Feb 27):
  Morning: Read planning documents (90 min)
  Afternoon: Set up project, create data_loader.py
  
Day 2-3 (Feb 27-28):
  Implement similarity & retrieval functions
  Test with sample cases
  
Day 4 (Feb 28):
  Implement adaptation rules
  Run all 6 test conditions
  Fix any bugs
  
Day 5 (Mar 1):
  Write README.md
  Write report.pdf
  SUBMIT by 11:59 PM
```

---

## ✨ Summary

You have **6 comprehensive planning documents** covering:
- Strategic overview
- System architecture
- Detailed implementation strategy
- Worked examples
- Testing methodology
- Documentation requirements

**Total coverage**: Everything you need to implement a successful CBR system.

**Next step**: Pick where you want to start and begin reading!

---

**Good luck with your implementation! 🚀**

*Last updated: February 26, 2026*
*Assignment due: March 1, 2026*
