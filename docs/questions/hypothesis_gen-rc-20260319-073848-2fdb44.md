---
created: '2026-03-19T07:46:33+00:00'
evidence:
- stage-08/hypotheses.md
- stage-08/novelty_report.json
id: hypothesis_gen-rc-20260319-073848-2fdb44
run_id: rc-20260319-073848-2fdb44
stage: 08-hypothesis_gen
tags:
- hypothesis_gen
- stage-08
- run-rc-20260
title: 'Stage 08: Hypothesis Gen'
---

# Stage 08: Hypothesis Gen

Here is a synthesized final set of hypotheses, combining the strongest ideas, explicitly addressing contrarian concerns, and staying within what looks realistically testable. I keep 3 hypotheses: one about early-vs-final predictivity, one about search in configuration space, and one about data curricula. For each: rationale, measurable prediction, and clear failure conditions. I also note where perspectives still disagree.

---

## Hypothesis A – Early val_bpb Is a *Useful but Imperfect* Proxy for Final val_bpb, and a Tiny Surrogate Can Exploit It Safely

### Core claim

Early val_bpb from very short “quick-harness” runs is neither as good as the innovator assumes (R² ≥ 0.9) nor as untrustworthy as the contrarian fears. Instead:

1. Across realistic data-filter and training-parameter configurations, **Spearman rank correlation between early and final val_bpb is in the 0.6–0.85 range**, not perfect but strong enough for practical use.
2. A **very small surrogate model (<1MB)** that uses early val_bpb plus a few simple features (data mixture summaries, learning rate scale, etc.) can:
   - Achieve **R² ≥ 0.8** predicting final val_bpb on held-out configs,  
   - Enable **≥3× search speedup** via early stopping,  
   - While **rarely discarding the truly best configs** (miss rate on top-5% <10%).

This is a moderated version of the innovator’s “Early-BPB Renormalization” plus the pragmatist’s “early val_bpb proxy” hypothesis, constrained by the contrarian’s concern about inversions and regime changes.

### Rationale (synthesis of views)

- From innovator & pragmatist:
  - There is substantial empirical evidence in NAS/AutoML and existing LLM work that early validation metrics correlate with final performance, especially when the search space is not pathological.
  - Quick-harness runs are the only way to make parameter golf feasible at modest compute.

- From contrarian:
  - Learning curves can cross; some configurations that look great early do worse later.
  - Over-aggressive schedules and “val-like” data mixtures can overfit early val_bpb.
  - Therefore, treating early val_bpb as a *noisy, biased* signal and explicitly modeling that bias is safer than assuming near-perfect linear predictivity.

- Compromise structure:
  - We keep the **tiny surrogate** idea (innovator) and **feasible protocol** (pragmatist),
  - But we **lower the bar** from R² ≥ 0.9 to ≥0.8 and explicitly track **inversion rates** (contrarian),
  - And we treat the surrogate as a *gate with guardrails*, not an oracle.

### Measurable predictions

1. **Correlation and predictivity**

   On a held-out set of configurations that vary both data filters and training dynamics:

   - Spearman ρ(early_val_bpb, final_val_bpb) ∈ [0.6, 0.85].  
   - A tiny surrogate `S` using:
     - Inputs: early val_bpb at a few checkpoints + 5–20 simple static features (e.g., domain entropy, quality threshold, LR scale, schedule type),
     - Output: predicted final_val_bpb,
     achieves on held-out configs:
       - **R² ≥ 0.8**,  
       - **MAE ≤ 0.015 val_bpb**.

2. **Search speedup with safety**

   Using `S` as a gate:

   - You can **terminate ≥70% of candidate configs** after ≤3% of full training steps.
   - The best final val_bpb found under this gated search is:
     - Within **0.01 val_bpb** of the best achievable by fully training all configs in the same initial candidate set.
   - The fraction of runs where the *true* top-5% configs are entirely discarded by the gate is **<10%**.

3. **Inversion rate explicitly measured**

   Among the top-k configs ranked by early val_bpb (e.g., k = 10–20), the fraction of pairwise inversions when ranked by final val_bpb is **non-trivial but manageable**, say **10–25%**, not the near-zero of the optimist nor the 30%+ the contrarian fears for “top of the distribution.”

### Failure conditions

Hypothesis A is falsified if any of the following hold in a well-powered experiment:

- **Weak correlation / poor surrogate:**
  - Spearman ρ < 0.5, or
  - Surrogate R² < 0.7 or MAE > 0.02 val_bpb on held-out configs.

- **Unsafe gating:**
  - Using `S` as a gate causes the search to miss all of the true top-5% configs in >20% of runs, or
  - The best-found final val_bpb under gating is consistently worse than the ungated baseline by >0.02.

- **High inversion at the top:**
  - Among the top-k early winners, inversion rates by final val_bpb exceed ~30–40%, indicating early rankings are too unstable to be safely used in a simple surrogate.

### Unresolved disagreements

- Innovator still believes R² ≥ 0.9 and very aggressive truncation (1–2% of training) may be achievable; this hypothesis sets a more conservative target.
- Contrarian suspects inversion rates at the top may be so high that even R² ≈ 0.8 hides dangerous mis-rankings; this hypothesis explicitly tests that by tracking inversions and miss rates.

---

## Hypothesis B – Latent/Smooth Search in Config Space Beats Pure Random Search, *But Only When Grounded in Multi-Fide

... (truncated, see full artifact)


{
  "topic": "Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact compliance on promotion.",
  "hypotheses_checked": 16,
  "search_queries": [
    "Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact compliance on promotion.",
    "here synthesized final set hypotheses"
  ],
  "similar_papers_found": 0,
  "novelty_score": 1.0,
  "assessment": "high",
  "similar_papers": [],
  "recommendation": "proceed",
  "similarity_threshold": 0.25,
  "search_coverage": "full",
  "total_papers_retrieved": 45,
  "generated": "2026-03-19T07:46:33+00:00"
}