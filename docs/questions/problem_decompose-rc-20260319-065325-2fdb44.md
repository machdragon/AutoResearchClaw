---
created: '2026-03-19T06:54:26+00:00'
evidence:
- stage-02/problem_tree.md
id: problem_decompose-rc-20260319-065325-2fdb44
run_id: rc-20260319-065325-2fdb44
stage: 02-problem_decompose
tags:
- problem_decompose
- stage-02
- run-rc-20260
title: 'Stage 02: Problem Decompose'
---

# Stage 02: Problem Decompose

## Source

User-provided project description: “Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact compliance on promotion” (parameter-golf-autorc; domains: ML, efficient-training, model-compression; target quality ≥4.5).

---

## Sub-questions

1. **Objective & metric fidelity under quick-harness**  
   - How reliably does **quick-harness val_bpb** (short validation runs on 50–200k tokens) predict **full-validation val_bpb** for compressed models, and how should the harness be designed (corpus slice, length, seeding, batching) to maximize this correlation under tight wall-clock budgets?

2. **Search space & constraint modeling for artifact-level optimization**  
   - What is an effective and tractable **compression parameter space** (bit-width schedules, sparsity patterns, encoding schemes, metadata formats) and **artifact-size accounting model** that allows the parameter golf procedure to:  
     - Enforce the **16MB end-to-end artifact constraint** (weights + codebooks + masks + decompressor), and  
     - Still explore enough diversity to find near-optimal val_bpb configurations within a small search budget?

3. **Optimization algorithm design for low-compute parameter golf**  
   - Given the quick-harness gate and 16MB constraint, which **black-box optimization strategy** (e.g., Bayesian optimization, evolutionary search, bandit-style adaptive sampling) best balances:  
     - Sample efficiency (≤100–200 candidates),  
     - Robust handling of hard constraints (feasible vs. infeasible configurations), and  
     - Practical implementation complexity on a single 24GB GPU?

4. **Baseline comparison and empirical benefits over naive compression**  
   - Relative to simple baselines (e.g., uniform 4-bit quantization, global pruning with fixed sparsity, off-the-shelf PTQ recipes), how much **val_bpb improvement at ≤16MB** does parameter golf provide, and under what conditions (model size, dataset, harness length) does it clearly outperform or fail to beat these baselines?

5. **Generalization, robustness, and transferability of learned compression schemes**  
   - Do compression configurations discovered by parameter golf on one **model–dataset–harness** triplet generalize to:  
     - Full validation sets (beyond the quick harness),  
     - Slightly different datasets (e.g., WikiText-103 → Pile-CC slice), or  
     - Nearby model variants (e.g., same architecture with different initialization or size),  
   and what regularities (e.g., layer-wise bit-width patterns) emerge that could inform reusable heuristics?

6. **System design and measurement of the end-to-end artifact**  
   - How should the **artifact packaging and measurement pipeline** be structured so that:  
     - The 16MB limit is **accurately and reproducibly** enforced across platforms (filesystem, runtime assumptions),  
     - Decompressor/runtime overhead is fairly accounted for (e.g., shared libraries vs. custom code), and  
     - The pipeline remains simple enough for others to adopt and extend?

---

## Priority Ranking

1. **Objective & metric fidelity under quick-harness** (Q1)  
   - If quick-harness val_bpb is not a reliable proxy for full-validation val_bpb, the core premise (optimize only via quick-harness) breaks. Establishing this correlation and designing the harness is foundational.

2. **Search space & constraint modeling for artifact-level optimization** (Q2)  
   - Without a well-defined compression parameter space and precise artifact-size accounting, the optimization problem is ill-posed; you cannot reliably satisfy the 16MB constraint or reason about trade-offs.

3. **Optimization algorithm design for low-compute parameter golf** (Q3)  
   - Once the objective and search space are defined, you must find a search strategy that works within the compute budget. This determines whether the method is actually practical.

4. **Baseline comparison and empirical benefits over naive compression** (Q4)  
   - Necessary to demonstrate novelty and value. Even a well-designed method is uninteresting if naive baselines perform similarly under the same constraints.

5. **Generalization, robustness, and transferability of learned compression schemes** (Q5)  
   - Important for research impact and claims of robustness, but can be explored after the core pipeline works and shows gains over baselines.

6. **System design and measurement of the end-to-end artifact** (Q6)  
   - Some aspects (basic size accounting) are required early, but the more nuanced, cross-platform/system-level questions can be refined later. Hence, conceptually important but slightly lower research priority than Q1–Q4.

---

## Risks

1. **Weak correlation between quick-harness and full val_bpb**  
   - If short validation runs are too noisy or unrepresentative, the optimizer may overfit to the harness and yield configurations that underperform on full validation, undermining the central “quick-harness gate” idea.

2. **Overly complex o

... (truncated, see full artifact)
