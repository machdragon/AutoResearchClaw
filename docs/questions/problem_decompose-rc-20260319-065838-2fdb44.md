---
created: '2026-03-19T06:59:39+00:00'
evidence:
- stage-02/problem_tree.md
id: problem_decompose-rc-20260319-065838-2fdb44
run_id: rc-20260319-065838-2fdb44
stage: 02-problem_decompose
tags:
- problem_decompose
- stage-02
- run-rc-20260
title: 'Stage 02: Problem Decompose'
---

# Stage 02: Problem Decompose

## Source

Topic: Parameter Golf val_bpb minimization under a quick-harness gate, with 16MB artifact compliance on promotion, for automatic, compute-efficient parameter search over compression/architecture choices in small LMs.

---

## Sub-questions

1. **Quick-harness design and calibration**
   - How should we design the “quick-harness” (data subset, context length, vocab, evaluation protocol) so that its scores are:
     - strongly correlated with true validation bits-per-byte (val_bpb),
     - stable across different compression configurations (quantization, pruning, adapters),
     - and cheap enough to enable large search throughput under a fixed GPU-hour budget?
   - What statistical or learned calibration methods best map quick-harness scores to predicted full val_bpb, and how robust are these mappings across models and datasets?

2. **Search space and constraint modeling under a 16MB artifact cap**
   - How do we formally define and parameterize the joint search space over:
     - quantization (bit-widths, per-layer / per-tensor schemes, mixed precision),
     - pruning (sparsity levels, structured vs. unstructured, block sizes),
     - low-rank adapters and minor architectural toggles,
     such that every candidate can be efficiently checked for compliance with a hard 16MB artifact cap?
   - How do we model and compute the artifact size (including embeddings and metadata) quickly enough to serve as an inner-loop constraint during search?

3. **AutoRC controller / search algorithm for parameter golf**
   - Which search strategy (e.g., multi-fidelity Bayesian optimization, ASHA-style bandits, evolutionary search, PBT-like schemes) is best suited to:
     - operate on the defined compression search space,
     - use quick-harness scores as low-fidelity evaluations,
     - enforce the 16MB cap as a hard constraint,
     - and minimize overall compute while approaching the best achievable val_bpb?
   - How should the controller allocate budget between exploring new regions of the compression space and refining promising candidates with more accurate (full) evaluations?

4. **Empirical effectiveness and comparison to baselines**
   - Under equal 16MB artifact constraints and similar compute budgets, how does the proposed parameter-golf-autorc framework compare against:
     - fixed, hand-designed compression recipes (e.g., uniform 4-bit quantization + fixed pruning),
     - and simpler auto-compression baselines (e.g., AutoAWQ-style quantization-only search),
     in terms of val_bpb, search efficiency, and robustness?
   - What does the resulting Pareto frontier (val_bpb vs. artifact size, within and slightly below 16MB) look like, and where does AutoRC provide clear gains?

5. **Generalization, robustness, and transferability**
   - How well do quick-harness calibrations and learned controller policies transfer:
     - across datasets (e.g., SlimPajama subset vs. Enwik8),
     - across base models in the 50–125M parameter range,
     - and across slightly different artifact caps (e.g., 8MB, 24MB)?
   - Are there systematic failure modes where the quick-harness misranks candidates (e.g., certain quantization patterns, extreme sparsity) and how can we detect or mitigate them?

---

## Priority Ranking

1. **Quick-harness design and calibration**  
   Rationale: Everything else depends on having a reliable, cheap proxy for val_bpb. Without this, the AutoRC framing and compute savings collapse.

2. **Search space and constraint modeling under a 16MB artifact cap**  
   Rationale: You need a precise, efficiently computable size model and a well-structured compression search space before you can design a controller or run experiments.

3. **AutoRC controller / search algorithm for parameter golf**  
   Rationale: Once (1) and (2) are in place, the main algorithmic contribution is the controller that exploits quick-harness signals and enforces the size constraint.

4. **Empirical effectiveness and comparison to baselines**  
   Rationale: Essential for demonstrating value and publishability, but methodologically downstream of (1–3).

5. **Generalization, robustness, and transferability**  
   Rationale: Important for a strong paper and future work, but can be scoped or partially deferred if time/compute are tight.

---

## Risks

1. **Weak or unstable correlation between quick-harness and true val_bpb**
   - Risk: Quick-harness metrics may fail to rank candidates consistently, especially across diverse compression patterns, undermining the AutoRC approach.
   - Impact: Search degenerates into noisy exploration; compute savings vanish or quality degrades.
   - Mitigation: Systematic calibration studies; ensemble or multi-metric quick-harness; periodic re-calibration using a subset of full evaluations.

2. **Intractable or mis-specified search space under 16MB**
   - Risk: The joint space of quantization, pruning, and adapters may be too large or irregular; size estimation may be inaccurate for some librarie

... (truncated, see full artifact)
