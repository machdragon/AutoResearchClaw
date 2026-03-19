---
created: '2026-03-19T11:19:47+00:00'
evidence:
- stage-02/problem_tree.md
id: problem_decompose-rc-20260319-111718-2fdb44
run_id: rc-20260319-111718-2fdb44
stage: 02-problem_decompose
tags:
- problem_decompose
- stage-02
- run-rc-20260
title: 'Stage 02: Problem Decompose'
---

# Stage 02: Problem Decompose

## Source

User-provided project brief: “Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact compliance on promotion” for the `parameter-golf-autorc` project, targeting an AutoRC-style controller that learns early-signal–conditioned compression policies (architecture, pruning, quantization, tokenizer) under:
- primary objective: minimize validation bits-per-byte (val_bpb) on Enwik8/Text8-style benchmarks,
- hard constraints: ≤16MB full artifact (weights + tokenizer + config + glue) and quick-harness wall-clock budget (minutes-scale per run),
- compute: single-GPU, ~50–150 GPU hours total.

---

## Sub-questions

1. **How should we formally define and parameterize the “Parameter Golf” search space so that every candidate configuration is both (a) quick-harness feasible and (b) mappable to a precise 16MB artifact budget, including tokenizer and glue code?**  
   - What architectural knobs (layers, d_model, heads, FFN width, context length) and compression knobs (pruning structure, quantization schemes, vocab size/structure) are in-scope?  
   - How do we build a fast, differentiable-or-at-least-smooth *artifact size estimator* that accounts for all bundle components, not just weights?  
   - How do we ensure that search proposals almost never violate the quick-harness runtime and 16MB size constraints (e.g., via hard feasibility filters or penalty terms)?

2. **Which early-training signals are most predictive of final val_bpb under this constrained regime, and how can we reliably extract and encode them within the quick-harness budget?**  
   - Over what horizon (number of steps / minutes) and at what granularity (per-batch, per-epoch) do we log signals like training loss trajectory, early val_bpb, gradient norms, activation statistics, sparsity evolution, etc.?  
   - How stable are these signals across random seeds and small hyperparameter perturbations, given very short runs?  
   - Can we construct compact feature representations (e.g., curve summaries, low-dimensional statistics) that preserve predictive power while keeping controller overhead negligible?

3. **How should the AutoRC-style controller be designed, trained, and constrained so that it can map early signals to effective, artifact-aware compression and architecture policies that improve val_bpb under the 16MB and quick-harness constraints?**  
   - What is the controller’s action space (e.g., per-layer sparsity targets, per-module bitwidths, vocab pruning decisions, small architecture tweaks) and how frequently can it intervene (once at init, staged schedule, or iterative refinement)?  
   - Which learning paradigm is most appropriate under limited evaluations: RL (e.g., bandits), Bayesian optimization with early-signal features, supervised regression from early signals to final outcomes, or a hybrid?  
   - How do we enforce constraint satisfaction in the controller (e.g., via constrained optimization, Lagrangian penalties, or projection onto a feasible artifact-size set) while maintaining sample efficiency?

4. **What baseline systems and evaluation protocol are needed to credibly demonstrate that early-signal–conditioned, artifact-aware policies yield superior val_bpb–size trade-offs versus strong static and heuristic baselines under the same quick-harness budget?**  
   - Which baselines are mandatory (e.g., hand-designed tiny Transformer, uniform quantization + global pruning, simple heuristic parameter golf, random / grid search) and how are they tuned fairly under the same compute and wall-clock constraints?  
   - How do we structure the experimental protocol (number of seeds, dataset splits, training schedules) so that differences of 5–10% relative val_bpb are statistically convincing?  
   - What ablations and diagnostics (e.g., removing early-signal conditioning, ignoring tokenizer in size accounting, freezing architecture but varying compression) are necessary to isolate the contribution of each component?

5. **How do tokenizer design and vocab-level compression interact with model architecture and weight compression to jointly satisfy the 16MB artifact constraint while minimizing val_bpb?**  
   - What tokenizer families (e.g., BPE, unigram, character-level) and vocab sizes are viable under the constraint, and how does vocab pruning or factorization affect both artifact size and compression performance?  
   - How do embedding layer design choices (e.g., shared input/output embeddings, low-rank factorization, tied softmax) co-adapt with tokenizer decisions and quantization?  
   - Can the controller meaningfully reason about tokenizer-level actions (e.g., shrinking vocab, merging rare tokens) based on early signals without retraining from scratch each time?

6. **Given the strict quick-harness gate and limited global compute, what meta-experiment design and optimization strategy will allow us to efficiently explore the Parameter Golf space and train the controller to convergence?**  
   - How do we sc

... (truncated, see full artifact)
