---
created: '2026-03-19T07:40:19+00:00'
evidence:
- stage-02/problem_tree.md
id: problem_decompose-rc-20260319-073848-2fdb44
run_id: rc-20260319-073848-2fdb44
stage: 02-problem_decompose
tags:
- problem_decompose
- stage-02
- run-rc-20260
title: 'Stage 02: Problem Decompose'
---

# Stage 02: Problem Decompose

## Source

User-provided research plan: *“Parameter Golf for val_bpb minimization under a quick-harness gate with 16MB artifact size compliance on promotion”* in the context of small LMs, compression, and AutoRC.

---

## Sub-questions

1. **Quick-Harness Design & Predictiveness**  
   1.1 How should the quick-harness (data slice, evaluation protocol, time budget) be designed so that it is reliably executable in ≤10 minutes on a single GPU?  
   1.2 How strongly does `val_bpb_harness` correlate with `val_bpb_full` across diverse architectures, compression schemes, and training recipes?  
   1.3 What harness design choices (dataset slice selection, size, token distribution, domain mix) most improve this correlation per unit of compute?  
   1.4 Under what conditions does the quick-harness gate fail (e.g., overfitting to the slice, domain shift, unstable training recipes), and how can we detect or correct these failures?

2. **Search Space & Constraint Modeling for 16MB Artifacts**  
   2.1 How should the architecture, compression, and training knobs be parameterized so that the AutoRC controller can efficiently explore configurations that plausibly fit within the 16MB artifact budget?  
   2.2 How can we accurately and cheaply predict total artifact size (weights + tokenizer + minimal runtime metadata) during search, before full training/compression is done?  
   2.3 Which components dominate artifact size at this scale (e.g., vocab size vs. width vs. depth vs. quantization level), and how do they interact?  
   2.4 What is the empirical Pareto frontier between `val_bpb_full` and artifact size near the 16MB boundary, and where do diminishing returns set in?

3. **Parameter-Golf AutoRC Algorithm Design**  
   3.1 Which search strategy (e.g., Bayesian optimization, evolutionary search, bandits, multi-fidelity HPO) best balances exploration and exploitation under tight compute and harness constraints?  
   3.2 How should multi-fidelity signals (shorter training runs, lower-resolution harness evaluations, approximate compression) be integrated to guide “parameter golf” toward promising regions?  
   3.3 How can the controller enforce the hard 16MB constraint—strict rejection, surrogate penalties, or feasibility-aware search—while still effectively optimizing `val_bpb`?  
   3.4 Compared to strong hand-tuned and simple random/grid baselines, how much improvement in `val_bpb_full` (and search efficiency) does the parameter-golf AutoRC framework deliver?

4. **Compression & Recipe Knob Importance Under Tiny Budgets**  
   4.1 Among pruning, quantization, low-rank factorization, weight tying, and KV-cache tricks, which provide the largest `val_bpb` gains per MB saved at ≤16MB?  
   4.2 How do architecture choices (depth, width, number of heads, embedding dim, vocab size) trade off against compression choices under the size cap?  
   4.3 How much do training-recipe choices (distillation, LR schedule, data subsampling, mixed precision) matter once architecture and compression are near-optimized?  
   4.4 Which combinations of knobs consistently appear in the best-performing configurations, suggesting general design patterns for tiny LMs?

5. **Generalization & Robustness of the Framework**  
   5.1 Does a parameter-golfed configuration tuned on one corpus (e.g., C4-like English) transfer well—under the same 16MB constraint—to another domain (e.g., code or math text)?  
   5.2 How sensitive are the learned recipes to changes in hardware (different single-GPU setups) or minor changes in harness definition?  
   5.3 Can the framework be scaled or adapted to slightly larger artifact budgets (e.g., 32–50MB) without redesigning the entire AutoRC pipeline?  
   5.4 What reusable guidelines or heuristics emerge that could inform future low-footprint LM design beyond this specific setup?

---

## Priority Ranking

1. **Quick-Harness Design & Predictiveness (Sub-question 1)**  
   - Rationale: The quick-harness gate is central to the method; if it is not predictive or cannot run within the time budget, the entire AutoRC loop becomes unreliable.

2. **Search Space & Constraint Modeling for 16MB Artifacts (Sub-question 2)**  
   - Rationale: Without a well-structured, size-aware search space and accurate artifact-size modeling, the controller will waste compute on infeasible or poorly calibrated configurations.

3. **Parameter-Golf AutoRC Algorithm Design (Sub-question 3)**  
   - Rationale: Once harness and constraints are defined, the core contribution is the AutoRC controller that exploits them; its design determines practical gains over baselines.

4. **Compression & Recipe Knob Importance Under Tiny Budgets (Sub-question 4)**  
   - Rationale: Provides the main empirical insights and informs both the search space design and the broader community; secondary to getting the framework working but critical for a strong paper.

5. **Generalization & Robustness of the Framework (Sub-question 5)**  
   - Rationale: Important for cla

... (truncated, see full artifact)
