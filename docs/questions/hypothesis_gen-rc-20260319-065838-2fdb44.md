---
created: '2026-03-19T07:06:51+00:00'
evidence:
- stage-08/hypotheses.md
- stage-08/novelty_report.json
id: hypothesis_gen-rc-20260319-065838-2fdb44
run_id: rc-20260319-065838-2fdb44
stage: 08-hypothesis_gen
tags:
- hypothesis_gen
- stage-08
- run-rc-20260
title: 'Stage 08: Hypothesis Gen'
---

# Stage 08: Hypothesis Gen

Here is a synthesized set of four hypotheses that:

- Keep the most novel ideas (safety micro‑dosing, multi‑profile deployment, constrained parameter golf, small harnesses),
- Directly engage the contrarian’s structural critiques (val_bpb anti‑correlation, harness overfitting),
- Stay realistically testable on modest compute.

For each: rationale, measurable prediction, and explicit failure condition. I’ll also call out key unresolved disagreements.

---

## Hypothesis A – Safety Micro‑Dosing Beats Macro‑Safety at Fixed or Slightly Relaxed val_bpb, but Only with Domain‑Weighted Loss

### Core claim

A very small, adversarially curated, artifact‑specific “safety micro‑dose” (≤0.5% of training tokens) can substantially improve local refusal robustness on high‑risk artifacts relative to a 5–10% generic safety fine‑tune, **provided** that:

1. Training uses a **domain‑weighted loss** that does *not* aggressively minimize global val_bpb on high‑risk domains (i.e., selectively higher loss on risky data), and  
2. Hyperparameters are tuned via **constrained parameter golf** with a safety/compliance quick‑harness gate.

In this regime, micro‑dosing can yield ≥30% better RBE/flip‑rate on targeted high‑risk neighborhoods than macro‑safety, at **similar global val_bpb or slightly worse (≤1–2% degradation)**.

### Rationale

Takes from innovator:

- Refusal boundaries are locally brittle; small, precisely shaped safety impulses can disproportionately stabilize fragile neighborhoods (e.g., ransomware text, exploit skeletons, prompts that tempt 16MB violations).
- A micro‑dose (0.1–0.5% highly targeted data) is more “energy efficient” than a large, diffuse safety corpus.

Takes from pragmatist:

- Feasible to explore micro vs macro safety as simple knobs in a 4–5D parameter golf space (safety FT strength, data mix, decoding, refusal threshold).
- Quick‑harness (≤16MB) with perturbations and artifact‑type slices is a practical gate.

Addresses contrarian:

- Instead of blindly minimizing global val_bpb, we adopt a **safety‑weighted conditional loss**:
  - Keep low loss on benign domains.
  - Enforce a **loss floor** or even up‑weight loss on high‑risk domains (code exploits, ransomware, compressed‑harm artifacts), so the model is *intentionally* less competent there.
- This directly responds to the argument that “pushing val_bpb down is structurally unsafe” by *modifying the objective* rather than assuming val_bpb is benign.

### Measurable prediction

Using a single base model:

1. Train/tune three variants under similar compute:
   - **Baseline**: no extra safety FT.
   - **Macro‑safety**: +5–10% generic safety FT, standard global val_bpb objective.
   - **Micro‑safety**: +0.1–0.5% adversarial, artifact‑specific safety data; **plus** domain‑weighted loss that enforces a loss floor on high‑risk domains.

2. For Macro‑ and Micro‑safety, run **constrained parameter golf**:
   - Objective: minimize (possibly domain‑weighted) validation loss / val_bpb.
   - Hard constraints: quick‑harness safety metrics (RBE/flip‑rate, 16MB violations) must be ≤ baseline or better.

3. At matched or slightly relaxed val_bpb:
   - Micro‑safety achieves:
     - ≥30% reduction in RBE/flip‑rate on targeted high‑risk textual/code artifact classes vs Macro‑safety.
     - ≥10% improvement in 16MB‑cap compliance on prompts that explicitly stress artifact size.
   - Global refusal rate is similar; improvements are local to high‑risk neighborhoods.

### Failure condition

The hypothesis is falsified if, after reasonable hyperparameter search:

- At comparable val_bpb (within +2% relative of Macro‑safety’s best), the Micro‑safety model:
  - Does **not** achieve at least 10% better RBE/flip‑rate in targeted high‑risk neighborhoods, **or**
  - Cannot match Macro‑safety’s safety metrics without **worse** val_bpb (>2% degradation).

Or:

- Domain‑weighted loss (with loss floors on high‑risk data) consistently **erases** the micro‑dose advantage: Micro‑safety no longer outperforms Macro‑safety even locally.

### Unresolved disagreements

- Innovator vs contrarian:
  - Innovator assumes you can keep val_bpb as the primary scalar; contrarian argues that’s structurally unsafe. This hypothesis sides with the contrarian by **changing the loss**, but keeps the innovator’s micro‑dose idea.
- Contrarian might still argue that any non‑trivial competence on high‑risk domains is dangerous under compression, even with loss floors; that’s not resolved here.

---

## Hypothesis B – Multi‑Profile (“Multi‑City”) Parameter Configurations Pareto‑Dominate a Single Global Profile Under Safety‑Weighted Objectives

### Core claim

When you:

1. Use **domain‑weighted objectives** that penalize excessive competence on high‑risk domains, and  
2. Evaluate via **profile‑specific quick‑harnesses** (consumer chat, code assistant, enterprise QA, etc.),

then a small family of **context‑specific parameter profiles** (per deployment “city”) will **Pareto‑dominate** a single global config

... (truncated, see full artifact)


{
  "topic": "Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact compliance on promotion.",
  "hypotheses_checked": 12,
  "search_queries": [
    "Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact compliance on promotion.",
    "here synthesized set four hypotheses"
  ],
  "similar_papers_found": 0,
  "novelty_score": 1.0,
  "assessment": "high",
  "similar_papers": [],
  "recommendation": "proceed",
  "similarity_threshold": 0.25,
  "search_coverage": "full",
  "total_papers_retrieved": 45,
  "generated": "2026-03-19T07:06:51+00:00"
}