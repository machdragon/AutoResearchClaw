---
created: '2026-03-19T22:10:36+00:00'
evidence:
- stage-02/problem_tree.md
id: problem_decompose-rc-20260319-220921-d02b4b
run_id: rc-20260319-220921-d02b4b
stage: 02-problem_decompose
tags:
- problem_decompose
- stage-02
- run-rc-20260
title: 'Stage 02: Problem Decompose'
---

# Stage 02: Problem Decompose

## Source

Problem:  
Parameter Golf val_bpb minimization under strict deployment constraints, focusing on a **recurrent LM baseline** progressively augmented with **LoRA specialization** and **lightweight routing/gating**, with:

- Artifact size ≤ 16MB (base + LoRA + gates).
- Runtime ≤ 1.10× recurrence-only baseline.
- Objective: minimize **validation bits-per-byte (val_bpb)** on a byte-level LM benchmark (e.g., enwik8).

Hypothesis: Starting from a recurrence-only model and adding LoRA + residual gating can improve post-roundtrip val_bpb at fixed artifact budget while staying under the runtime quick-gate.

---

## Sub-questions

1. **Baseline & Budget Accounting: What is the best achievable val_bpb and runtime profile for a pure recurrence-only model under the 16MB artifact cap, and how do we decompose this cap into base vs. adapter/gate budget?**  
   - How many parameters / which architecture (e.g., RWKV-like vs. GRU/LSTM) gives the strongest val_bpb for ≤16MB when trained end-to-end?  
   - What is the exact baseline runtime (train-step time, tokens/sec, val-pass time) and its variance for target batch/sequence settings?  
   - How do different precision choices (fp16/bf16/int8) and serialization formats affect the “effective” parameter budget and runtime?  
   - How much of the 16MB budget must be reserved for LoRA + gating to leave meaningful capacity for specialization (e.g., 70–90% base, 10–30% adapters), and what is the most promising baseline size at that split?

2. **LoRA Placement & Rank: Where should LoRA be injected in the recurrent LM (which matrices/layers), and at what ranks, to maximize val_bpb improvement per byte while staying within the artifact and runtime budgets?**  
   - Among input-to-hidden, hidden-to-hidden, and output projections, which placements yield the best val_bpb gain per added parameter at constant training compute?  
   - What is the marginal benefit curve of LoRA rank (e.g., r = 2, 4, 8, 16) on val_bpb, and where is the diminishing-return knee under the 16MB cap?  
   - Does concentrating LoRA budget on a subset of “critical” layers outperform evenly spreading low-rank adapters across all layers at equal total bytes?  
   - How much runtime overhead does each LoRA configuration introduce, and which configurations stay under the ≤1.10× quick-gate while offering non-trivial val_bpb gains?

3. **Gating/Routing Design: What is the simplest residual gating/routing scheme that meaningfully improves val_bpb over LoRA-only variants without violating the ≤1.10× runtime constraint?**  
   - Do scalar gates per layer, per-channel/vector gates, or tiny MLP gates provide the best val_bpb/byte trade-off under the small parameter budget?  
   - Is it better to gate between (a) base vs. base+LoRA outputs, (b) multiple LoRA “experts,” or (c) different recurrent subpaths, given the runtime constraint?  
   - How many experts (1–3) are feasible before routing overhead (extra matmuls, branching, cache effects) pushes runtime above 1.10× baseline?  
   - Compared to a control that uses the same additional parameters as plain dense recurrent weights (no gating), does gating + LoRA give strictly better val_bpb at equal artifact and runtime budgets?

4. **Pareto & Robustness: How does the recurrence + LoRA + gating composite populate the Pareto frontier of (val_bpb, artifact size, runtime), and are the observed gains robust across scales and training regimes?**  
   - Across multiple budget points (e.g., 8MB, 12MB, 16MB), does the composite consistently dominate recurrence-only and recurrence+LoRA-only baselines in val_bpb at matched or lower runtime?  
   - How sensitive are the gains to training budget (epochs, learning rate schedule, LoRA/gate initialization) and data sub-sampling; do improvements persist under mild under-training or over-regularization?  
   - Do the best-performing configurations generalize across sequence lengths and evaluation conditions (e.g., streaming vs. fixed-length) without runtime blowups?  
   - Can we extract simple design rules (e.g., “X% budget to hidden-to-hidden LoRA, scalar gates per layer only”) that reproduce most of the gains when ported to a second recurrent architecture or dataset?

---

## Priority Ranking

1. **Baseline & Budget Accounting (Sub-question 1)**  
   - Highest priority: anchors everything else. Without a precise baseline and budget split, LoRA/gating results and runtime claims are uninterpretable.

2. **LoRA Placement & Rank (Sub-question 2)**  
   - Next priority: directly tests the first part of the hypothesis (recurrence-only → +LoRA), and likely delivers most of the early val_bpb gains under the cap.

3. **Gating/Routing Design (Sub-question 3)**  
   - Third: adds complexity and runtime overhead. Should be explored only once a strong LoRA-only configuration is established, to isolate gating’s incremental value.

4. **Pareto & Robustness (Sub-question 4)**  
   - Fourth: integrates answers from 1–3 into a publishable story; cruci

... (truncated, see full artifact)
