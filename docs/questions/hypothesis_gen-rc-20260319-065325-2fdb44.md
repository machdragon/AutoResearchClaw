---
created: '2026-03-19T06:59:55+00:00'
evidence:
- stage-08/hypotheses.md
- stage-08/novelty_report.json
id: hypothesis_gen-rc-20260319-065325-2fdb44
run_id: rc-20260319-065325-2fdb44
stage: 08-hypothesis_gen
tags:
- hypothesis_gen
- stage-08
- run-rc-20260
title: 'Stage 08: Hypothesis Gen'
---

# Stage 08: Hypothesis Gen

Here is a synthesized final set of hypotheses that pulls the strongest ideas from all three perspectives, makes them testable and feasible, and explicitly preserves key disagreements.

---

## Hypothesis A – Thin Controller + External Graph Can Match Larger Models *On-Harness*, But May Fail Off-Harness

### Claim

A ≤16MB “thin compliance controller” that offloads policy knowledge to an external artifact graph can match or exceed a 10× larger monolithic model on *quick-harness* metrics (accuracy, refusal stability, explainability) at lower val_bpb. However, this architecture is more vulnerable to off-harness failures (out-of-distribution prompts, graph drift/poisoning, orchestration bugs) than weight-heavy baselines.

This merges:
- Innovator/pragmatist’s “thin controller + graph can beat monolith under a 16MB gate”
- Contrarian’s “this may be illusory compression and fragile off-harness”

### Rationale

- PACT and related work show that much compliance knowledge can be externalized into an artifact graph and exploited via retrieval, allowing small models to compete with much larger ones on in-distribution tasks.
- Compression work (M-PACE, distillation) and the pragmatist’s proposal show that 20–40M parameter backbones, quantized to ≤16MB, are feasible and performant.
- The contrarian points out that:
  - The 16MB + quick-harness regime encourages overfitting to the harness and offloading complexity into external systems.
  - Retrieval graphs and orchestration introduce new failure and drift modes that quick-harnesses typically under-measure.

### Measurable Predictions

We compare two systems:

- **System S (Thin+Graph):**
  - ≤16MB controller (20–40M params, quantized).
  - PACT-style external artifact graph (policies, precedents, examples).
  - Retrieval + decision aggregation + pointer-based explanations.

- **System L (Weight-Heavy Baseline):**
  - 100–300MB monolithic model (e.g., DistilBERT/small LLaMA), fine-tuned end-to-end for classification + explanation.
  - Minimal external retrieval; policy mostly in weights.

**On-harness (in-distribution) predictions:**

1. On a quick-harness that includes:
   - Compliance F1 / AUROC on held-out data,
   - Refusal-boundary entropy (RBE) on Heverin-style perturbations,
   - Explanation adequacy (policy traceability ratings),
   
   System S will:
   - Achieve ≥95% of System L’s classification F1.
   - Achieve ≥95% of System L’s robust-refusal score.
   - Have non-inferior explanation adequacy (no significant drop at p<0.05).
   - Have lower or equal val_bpb and ≤16MB artifact size.

**Off-harness (stress-test) predictions:**

2. On an *adversarially constructed, out-of-harness* suite:
   - New perturbation families not used in training or harness design,
   - Edge-case scenarios (long-tail policy combinations, atypical formats),
   - Simulated graph issues (e.g., subtle mislinks, stale nodes),
   
   System S will:
   - Show a higher rate of unsafe allowances (false negatives on harmful content) than System L, at comparable accuracy on benign/typical cases.
   - Show more decision instability across time when the graph is updated (same prompt, different day → more label changes).
   - Have a higher fraction of failures attributable to retrieval/orchestration issues vs. pure model misgeneralization.

### Failure Conditions

This hypothesis fails if:

- **On-harness:** System S cannot meet the 95% non-inferiority targets on accuracy and robustness, or its explanation adequacy is significantly worse than System L’s; **and/or**
- **Off-harness:** Under broad, adversarial tests and simulated drift:
  - System S does *not* exhibit higher unsafe-allowance rates or instability than System L (i.e., it matches or beats System L on out-of-distribution robustness and consistency), *without* requiring a dramatically more complex or larger external graph than initially specified.

### Unresolved Disagreements

- **Innovator/pragmatist vs. contrarian:**  
  - Innovator/pragmatist expect System S to be a *net win* if the graph and controller are well-designed; they see offloading as a manageable engineering problem.
  - Contrarian believes System S’s apparent wins are largely benchmark artifacts; true system-level robustness and simplicity favor a somewhat larger, more self-contained System L.
- **Metric of “efficiency”:**  
  - Innovator/pragmatist emphasize model val_bpb and artifact size.
  - Contrarian argues for “total system bits” and operational complexity as the relevant efficiency metric.

---

## Hypothesis B – Refusal-Boundary Entropy Outweighs Val_bpb for Adoption Under a Size Ceiling

### Claim

Once models are under a realistic artifact-size ceiling (e.g., ≤16MB), *refusal-boundary entropy* (RBE) is a stronger predictor of real-world adoption and trust than further improvements in val_bpb. Compression pipelines that explicitly optimize for low RBE at fixed size will yield systems that practitioners prefer over more aggressively compressed, higher-RBE models, e

... (truncated, see full artifact)


{
  "topic": "Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact compliance on promotion.",
  "hypotheses_checked": 13,
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
  "generated": "2026-03-19T06:59:55+00:00"
}