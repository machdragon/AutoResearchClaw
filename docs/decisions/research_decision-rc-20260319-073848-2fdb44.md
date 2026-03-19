---
created: '2026-03-19T08:19:22+00:00'
evidence:
- stage-15/decision.md
- stage-15/decision_structured.json
id: research_decision-rc-20260319-073848-2fdb44
run_id: rc-20260319-073848-2fdb44
stage: 15-research_decision
tags:
- research_decision
- stage-15
- run-rc-20260
title: 'Stage 15: Research Decision'
---

# Stage 15: Research Decision

## Decision
REFINE

## Justification
The work is blocked at the infrastructure/methodology level, not at the hypothesis level.

- The core hypotheses (early vs final val_bpb, surrogate modeling, search under a 16MB constraint) remain conceptually sound and plausible.
- However, **no scientific experiments have actually run**; the only observed run is an infra failure.
- The analysis quality is explicitly rated **2/10**, below the minimum threshold for PROCEED.
- Several minimum PROCEED criteria are not met: no baselines, no metrics, no seeds, no primary metric instantiated.

This is not evidence that the hypotheses are fundamentally wrong; it is evidence that the experimental system is not yet capable of testing them. That calls for **REFINE**, not PIVOT.

## Evidence

- **Zero successful ML runs**
  - “Number of successful ML runs: 0”
  - “Metrics logged: none (`metrics: {}`)”
- **Infra failure is the only outcome**
  - Error: `could not select device driver "" with capabilities: [[gpu]]`
  - Runtime ~0.34s, consistent with immediate infra failure.
- **Analysis quality rating**
  - “Result quality (for scientific conclusions): 2 / 10”
- **Missing PROCEED criteria**
  - No baselines with results.
  - No primary metric instantiated in practice (no val_bpb values).
  - No seeds, no per-condition variability.
- **Conceptual plan still coherent**
  - Early val_bpb as quick-harness signal, surrogate R², 16MB artifact constraint described as “conceptually coherent” and “promising but methodologically incomplete.”

Given this, the right move is to repair infra, formalize the experimental design, and generate *actual data*, not to abandon the direction.

## Next Actions

### 1. Unblock Infrastructure (Hard Prerequisite)

1.1 Fix GPU/container configuration
- Install and configure NVIDIA container toolkit (or equivalent).
- Validate with a simple command:
  - `docker run --gpus all nvidia/cuda:XX.Y-base nvidia-smi`
- Ensure the experiment runner uses the correct runtime and device flags.

1.2 Add a minimal GPU sanity test in the pipeline
- New “sanity” task that:
  - Instantiates a tiny model.
  - Runs 10–100 training steps on GPU.
  - Logs:
    - `train_loss`, `val_bpb` (or analogous primary metric).
    - Wall-clock time.
- Make this test a gate before any large-scale search.

---

### 2. Instantiate the Primary Metric and Artifact Constraint

2.1 Define and implement val_bpb concretely
- Fix:
  - Tokenization scheme.
  - Dataset slice for validation.
- Implement a single function that:
  - Takes a model + tokenizer.
  - Returns `val_bpb` with units and direction (lower is better).
- Ensure this metric is logged for every run, including sanity tests.

2.2 Formalize the 16MB artifact definition
- Decide exactly what counts:
  - Model weights (required).
  - Tokenizer.
  - Config / metadata.
  - Any runtime stubs needed for deployment.
- Implement a deterministic artifact-size checker:
  - Single script that:
    - Builds the deployable artifact as it would ship.
    - Measures on-disk size in bytes.
    - Logs `artifact_size_bytes`.
- Add a simple enforcement rule:
  - Runs exceeding 16MB are flagged and/or disqualified in the controller logic.

---

### 3. Design and Register Baselines

3.1 Specify at least two concrete baselines
Examples (you can adjust, but must commit):

- Baseline A: Small dense model under 16MB, tuned with standard hyperparameter search.
- Baseline B: Quantization-only or pruning-only model under 16MB, with no fancy controller or surrogate.

3.2 Define fairness and budgets
- For each method (baselines + proposed):
  - Same training data.
  - Same evaluation metric (val_bpb).
  - Comparable search/tuning budget (e.g., number of trials or total GPU-hours).

3.3 Encode baselines in the orchestration
- Create explicit experiment configs for each baseline method.
- Ensure each config:
  - Runs on GPU.
  - Logs metrics and artifact size.
  - Is repeatable across seeds.

---

### 4. Establish Minimum Experimental Protocol

4.1 Data splits and anti-leakage
- Define:
  - Training set.
  - Quick-harness validation set (for early val_bpb and controller decisions).
  - Final evaluation set (for reporting only; never used by the controller or surrogate).
- Enforce in code:
  - Surrogate is trained only on training + quick-harness signals.
  - Final eval set is read-only for reporting.

4.2 Seed and replication policy
- Decide a minimum of **≥3 seeds per condition** (per baseline and per proposed method).
- Encode seeds in configs; log them explicitly.

4.3 Ablation integrity
- Ensure that:
  - Different conditions (e.g., with/without surrogate, different quick-harness budgets) differ in config.
  - No copy-paste reuse of metrics across conditions.

---

### 5. Run Initial Scientific Sanity Experiments

Once infra is stable and metric definitions are implemented:

5.1 Run a tiny, controlled experiment set
- For each of:
  - Baseline A.
  - Baseline B.
  - Proposed method (even in a simplified form, e.g., e

... (truncated, see full artifact)


{
  "decision": "refine",
  "raw_text_excerpt": "## Decision\nREFINE\n\n## Justification\nThe work is blocked at the infrastructure/methodology level, not at the hypothesis level.\n\n- The core hypotheses (early vs final val_bpb, surrogate modeling, search under a 16MB constraint) remain conceptually sound and plausible.\n- However, **no scientific experiments have actually run**; the only observed run is an infra failure.\n- The analysis quality is explicitly rated **2/10**, below the minimum threshold for PROCEED.\n- Several minimum PROCEED criteria ",
  "generated": "2026-03-19T08:19:22+00:00"
}