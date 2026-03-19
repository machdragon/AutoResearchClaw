---
created: '2026-03-19T13:41:28+00:00'
evidence:
- stage-15/decision.md
- stage-15/decision_structured.json
id: research_decision-rc-20260319-125447-2fdb44
run_id: rc-20260319-125447-2fdb44
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

The current work does **not** satisfy the minimum quality criteria for PROCEED, but it also does **not** show that the underlying hypotheses are wrong. The issues are overwhelmingly about implementation, instrumentation, and statistics—not about the conceptual direction.

Key points:

- The run is marked failed; secondary metrics (including all safety/robustness signals) do not execute due to an API mismatch.
- Critical ablations are non-functional (identical outputs), so core levers like boundary weighting, hash chaining, and summaries are not actually being tested.
- Only a single primary metric (val_bpb) is effectively available, with n=1 per condition and no variance estimates.
- The analysis quality is explicitly rated 3/10, below the ≥4/10 bar.

These are all fixable engineering and methodology gaps. There is no evidence yet that the core hypotheses (about compression tradeoffs and boundary-weighted robustness) are fundamentally flawed—just that they have not been properly tested.

Given the explicit rules: because at least one minimum criterion for PROCEED is not met (analysis quality rating < 4/10, no multi-seed results, broken ablations), the only permissible choice is REFINE rather than PROCEED. PIVOT is not warranted because the conceptual framing still looks sound.

## Evidence

- **Run status:** Marked `status: "failed"` due to `GlobalValBPBCompressor.infer_logits()` signature error in `evaluate_secondary_metrics`.
- **Ablation integrity failures:**
  - `boundary_weighted_robustness_controller` ≡ `trace_heavy_without_hash_chaining_ablation`.
  - `core_only_no_summaries_ablation` ≡ `globally_compressed_valbpb_minimizer`.
- **Metrics available:**
  - Only `val_bpb` and a coarse `success_rate`.
  - `val_bpb` in a narrow band (~0.1239–0.1266); `success_rate = 1.0` except for two broken configs.
  - No artifact size, compute, latency, or safety/robustness metrics.
- **Statistical gaps:**
  - n=1 per condition; no multiple seeds, no variance, no tests.
  - Meaning of indices 0–19 is undocumented.
- **Explicit assessment:** Overall analysis/result quality rated **3/10**, below the ≥4/10 requirement.

These directly violate PROCEED criteria #3, #4, and #5, and undermine any inferential claims.

## Next Actions

Focus on turning this from a plumbing/debug snapshot into a scientifically valid experiment.

### 1. Fix Core Infrastructure

1.1. **Repair environment and APIs**
- Correct `requirements.txt` (remove `__future__`, pin concrete versions).
- Resolve `infer_logits(regime)` signature mismatch so `evaluate_secondary_metrics` runs end-to-end.
- Add a minimal CI test that:
  - Installs deps.
  - Runs a tiny quick-harness job.
  - Executes secondary metrics without error.

1.2. **Harden logging**
- Ensure every condition logs:
  - `val_bpb`
  - artifact size (bytes / MB)
  - parameter count
  - training/eval token counts and wall-clock
  - all safety/robustness metrics once implemented.

### 2. Make Ablations Real and Verifiable

2.1. **Implement functional toggles**
- Ensure that:
  - Boundary weighting,
  - Hash chaining,
  - Summaries vs core-only
actually change code paths and outputs.

2.2. **Unit-test ablations**
- For each ablation pair, add tests on a fixed synthetic batch that assert:
  - Output logits or artifacts differ beyond a small numerical tolerance.
- Fail fast if any ablation is identical to its parent.

### 3. Align Metrics With Hypotheses

3.1. **Compression and resource tradeoffs**
- Log for each run:
  - Final artifact size under the 16MB cap.
  - Compression ratio vs an uncompressed baseline.
  - Quick-harness resource use (tokens, steps, wall-clock).

3.2. **Safety and boundary robustness**
- Implement and log:
  - Boundary-local robustness metric (e.g., violation/jailbreak rate as a function of distance to promotion boundary).
  - RBE or similar boundary entropy metric, if that’s part of the design.
  - Overall jailbreak/violation rates on a held-out adversarial set.

### 4. Add Minimal Statistical Rigor

4.1. **Seeds and aggregation**
- For each key condition (at least: 2 baselines + proposed method), run ≥3 independent seeds.
- Aggregate:
  - mean ± std of val_bpb
  - mean ± std of safety metrics
  - artifact size distribution.

4.2. **Clarify indices**
- Explicitly define what indices 0–19 represent (seeds, folds, checkpoints).
- Do not treat them as independent samples unless they truly are.

4.3. **Basic comparisons**
- Pre-specify a small set of comparisons (e.g., proposed vs baseline A/B).
- Run simple tests (e.g., t-test or bootstrap) to check if differences exceed noise.

### 5. Design the Next Experimental Pass

5.1. **Baseline set**
- Include at minimum:
  - A plain, low/no-compression baseline.
  - A naive compression baseline.
  - The proposed method.
- Verify all three satisfy:
  - ≥3 seeds.
  - Full metric suite (val_bpb, size, safety).

5.2. **Scope reduction for robustness**
- For the next iteration, reduce the number of con

... (truncated, see full artifact)


{
  "decision": "refine",
  "raw_text_excerpt": "## Decision\nREFINE\n\n## Justification\n\nThe current work does **not** satisfy the minimum quality criteria for PROCEED, but it also does **not** show that the underlying hypotheses are wrong. The issues are overwhelmingly about implementation, instrumentation, and statistics\u2014not about the conceptual direction.\n\nKey points:\n\n- The run is marked failed; secondary metrics (including all safety/robustness signals) do not execute due to an API mismatch.\n- Critical ablations are non-functional (identica",
  "generated": "2026-03-19T13:41:28+00:00"
}