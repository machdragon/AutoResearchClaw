---
created: '2026-03-19T11:27:11+00:00'
evidence:
- stage-08/hypotheses.md
- stage-08/novelty_report.json
id: hypothesis_gen-rc-20260319-111718-2fdb44
run_id: rc-20260319-111718-2fdb44
stage: 08-hypothesis_gen
tags:
- hypothesis_gen
- stage-08
- run-rc-20260
title: 'Stage 08: Hypothesis Gen'
---

# Stage 08: Hypothesis Gen

Below is a synthesized set of three hypotheses that:

- Keep the most novel ideas (phase-diagram view, defect vectors, structured quick-harnesses),
- Explicitly bake in the contrarian’s critiques (scale-dependence, metric distortion, 16MB as an active constraint),
- Stay runnable with modest compute and simple logging (pragmatist’s constraints),
- Preserve genuine disagreements.

For each: rationale, measurable prediction, failure condition, and explicit notes on unresolved contention.

---

## Hypothesis 1 – Local Phase Diagrams Exist, But Only for Narrow, Task-Specific Regimes

**Claim (synthesis of “phase-diagram training” + contrarian skepticism):**

LLM training does admit **sharp, low-dimensional “stability windows”** in a 3D process space:

1. effective LR/optimizer aggressiveness (α),
2. data-quality gate intensity (G),
3. curriculum “non‑solvent” rate (R: introduction of harder/noisier/long‑tail data),

but:

- These windows are **local and task-specific**, not global.
- They are reliably discoverable only if:
  - You condition on a **narrow deployment regime** (e.g., web-style text vs code-heavy vs safety-critical),
  - And you augment scalar val_bpb with a **small, structured defect vector** during exploration.

Within a given regime, you can:

- Map a simply connected, compact “good region” in (α,G,R) where:
  - val_bpb and key defect rates scale predictably with compute,
- Using:
  - small quick-harness models,
  - ultra-compressed logs (≤16MB per sweep).

Outside that regime, the “window” fragments; global stability windows across heterogeneous tasks are mostly a mirage.

### Rationale

Strong elements taken:

- From innovator:
  - The phase-diagram analogy and focus on a **low-dimensional process space** (α,G,R).
  - The idea of **sharp boundaries** between “good” and “bad” regimes.
  - Cross-scale mapping using small harness models and tiny logs.

- From contrarian:
  - **Scale- and task-dependence**: what’s good for small models or easy tasks may be bad for large models or hard tasks.
  - Apparent global stability windows can be artifacts of:
    - Coarse scalar metrics,
    - Under-sampled rare failures.
  - Therefore, any “window” must be **contextualized**.

- From pragmatist:
  - Use of **1.3B / ~300–400M** models, RedPajama-like data, and **simple artifact budgets**.
  - Straightforward logging: val_bpb + a few defect dimensions.

So this hypothesis narrows the ambition: not “one phase diagram to rule them all,” but **multiple, local phase diagrams** per deployment regime, discovered with small models and compact, structured metrics.

### Measurable Prediction

**Setup:**

- Choose one *specific* deployment regime, e.g.:
  - “General web text & Q/A, English-only, no code”  
  or  
  - “Code-centric tasks”  
  or  
  - “Safety-sensitive conversational assistant.”
- Fix:
  - Model family (e.g., decoder-only transformer).
  - Two sizes: ~300–400M (harness) and ~1.3B (target).
  - Total training tokens per size (e.g., 5–8B for harness, 30–50B for target).
- Define a 3D grid over:
  - α: {0.3×, 1×, 3× baseline LR scale},
  - G: 3–5 data-quality thresholds (e.g., low/med/high quality),
  - R: 3–5 curriculum schedules for injecting harder/noisier data.
- For each configuration:
  - Train the harness model.
  - Log:
    - Final val_bpb on a regime-matched validation set,
    - A small defect vector (e.g., k=5–10 dimensions: hallucination, incoherence, repetition, toxicity, format errors) estimated from ≤1,000 generations,
    - Minimal training curves (heavily downsampled).

**Prediction 1A – Local Stability Window (Harness Scale):**

For the harness model in this **single regime**:

1. The set of configurations whose **joint objective**  
   `J_small(c) = normalized(val_bpb) + Σ_i w_i * normalized_defect_i`  
   is within 2% of the optimum forms a **simply connected, compact region** in (α,G,R).
2. Crossing the boundary in any single dimension (α, G, or R) leads to:
   - ≥5% degradation in J_small,
   - Or clear qualitative instability (e.g., divergence, exploding loss, defect rates spiking).

**Prediction 1B – Partial Cross-Scale Transfer:**

- Train the large (1.3B) model for a **subset** of configurations that:
  - Tile the interior and exterior of the harness “good region.”
- Compute the analogous large-model objective `J_large(c)` (same metric definitions, larger eval sets).
- Train a classifier or regressor on the **harness logs (val_bpb + defect vector)** to predict whether a config is “good” for the large model (within 2–3% of best J_large).

Expect:

- Classification accuracy ≥ 80–85% on held-out configs *within that same deployment regime*.
- However, if you repeat the experiment in a **different regime** (e.g., code instead of web text), the earlier phase diagram **does not transfer**: the good region’s shape and/or location shifts significantly.

**Artifact constraint:**

- All harness logs (for O(10²–10³) configs) can be compressed into ≤16MB:
  - Per config: a few dozen floats +

... (truncated, see full artifact)


{
  "topic": "Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact compliance on promotion.",
  "hypotheses_checked": 11,
  "search_queries": [
    "Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact compliance on promotion.",
    "below synthesized set three hypotheses"
  ],
  "similar_papers_found": 0,
  "novelty_score": 1.0,
  "assessment": "high",
  "similar_papers": [],
  "recommendation": "proceed",
  "similarity_threshold": 0.25,
  "search_coverage": "full",
  "total_papers_retrieved": 45,
  "generated": "2026-03-19T11:27:11+00:00"
}