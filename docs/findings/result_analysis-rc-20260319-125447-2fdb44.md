---
created: '2026-03-19T13:40:59+00:00'
evidence:
- stage-14/analysis.md
- stage-14/experiment_summary.json
- stage-14/results_table.tex
id: result_analysis-rc-20260319-125447-2fdb44
run_id: rc-20260319-125447-2fdb44
stage: 14-result_analysis
tags:
- result_analysis
- stage-14
- run-rc-20260
title: 'Stage 14: Result Analysis'
---

# Stage 14: Result Analysis

## Metrics Summary

- Reported metrics: `val_bpb` (validation bits-per-byte), `success_rate`.
- Scope: many controller/ablation conditions × {low_compression, high_compression} × 20 indices each.
- Numerical pattern:
  - `val_bpb` tightly clustered ≈ 0.1239–0.1266.
  - `success_rate` = 1.0 for all “working” conditions; 0.0 only for two broken ablations.
- Run status: **failed** due to `GlobalValBPBCompressor.infer_logits()` signature error; requirements file also invalid.
- No variance, no multiple seeds, no artifact size, no latency, no safety/robustness metrics.

---

## Consensus Findings

Across perspectives, there is strong agreement on the following high‑confidence points:

1. **Infrastructure partially works, but the run is not scientifically valid yet.**
   - Training loops execute; many conditions finish and produce val_bpb.
   - The overall run is marked `status: "failed"` due to an `infer_logits(regime)` TypeError in the secondary metrics path.
   - Therefore, the run is best seen as a *plumbing/debug* snapshot, not a complete experiment.

2. **Key ablations are broken (identical outputs).**
   - `boundary_weighted_robustness_controller` ≡ `trace_heavy_without_hash_chaining_ablation` on all reported metrics.
   - `core_only_no_summaries_ablation` ≡ `globally_compressed_valbpb_minimizer` on all reported metrics.
   - This implies the differentiating flags (boundary weighting, hash chaining, summaries) are not actually wired into behavior.

3. **Only val_bpb is really available; core safety/robustness claims are unsupported.**
   - Adversarial/boundary metrics fail to compute because the run crashes in `evaluate_secondary_metrics`.
   - There is no RBE, no jailbreak rate, no boundary-conditioned robustness metric.
   - Any statements about “compression-induced fragility” or “boundary-weighted robustness” are not empirically grounded in this run.

4. **Statistical support is absent.**
   - Each logged metric has `n=1`; no multiple seeds, no variance, no confidence intervals, no hypothesis tests.
   - Differences between conditions are on the order of 1e‑3 in val_bpb—well within plausible run‑to‑run noise.

5. **Resource and constraint metrics are missing.**
   - The 16MB artifact cap and quick-harness budget are not actually quantified in the metrics: no artifact size, no parameter count, no wall-clock or token counts.
   - Thus, “joint optimization under a 16MB cap and quick-harness” is asserted in design but not evidenced.

These are robust, shared conclusions: the run demonstrates that the harness can train multiple configurations and produce val_bpb, but it does **not** yet provide valid evidence for the core scientific claims.

---

## Consensus Findings (Positive but Narrow)

Within those limits, there are a few cautiously reliable positive signals (as *engineering* observations, not scientific results):

1. **Quick-harness regime is operational and stable.**
   - Many different controller/condition combinations run to completion (before the secondary-metric crash) and converge to reasonable val_bpb without divergence.
   - This suggests the basic training loop and “parameter golf” machinery are usable.

2. **Compression appears “safe” at this horizon.**
   - For most conditions, low vs high compression variants differ only slightly in val_bpb, and both have `success_rate = 1.0`.
   - Under this short training horizon and dataset, aggressive compression does not catastrophically break training.

3. **Several design families are at least competitive on val_bpb.**
   - `model_heavy_log_light_compliance_gate`, `artifact_maximal_retrieval_llm`, and `uniform_trace_density_ablation` all achieve val_bpb in the best part of the observed band.
   - This indicates multiple qualitatively different controllers can operate within the quick-harness and (presumably) size constraints without obvious performance collapse.

These are engineering‑level takeaways: the system can run, and there is a nontrivial design space that doesn’t immediately fail.

---

## Contested Points

Here are the main disagreements or overstatements and how they should be resolved.

### 1. “Model-heavy, log-light” and “artifact-maximal retrieval” are *better* designs

- Optimist: reads small val_bpb differences as evidence that `model_heavy_log_light_compliance_gate` and `artifact_maximal_retrieval_llm` are superior.
- Skeptic & methodologist: point out:
  - No variance estimates.
  - Unknown meaning of indices 0–19.
  - No significance tests; differences are tiny (1e‑3).
  - Possible confounds (seeds, data ordering, hyperparameter drift).

**Resolution:**  
You can say these designs are *at least not obviously worse* under this setup and are promising candidates for further study. You **cannot** claim they are statistically better or that they improve safety or boundary robustness. Treat them as “interesting configurations that run stably and land in the best‑observed val_bpb band,” nothing more.

### 2. Evidence for “boundary-weight

... (truncated, see full artifact)


{
  "metrics_summary": {
    "globally_compressed_valbpb_minimizer/low_compression/0/val_bpb": {
      "min": 0.124788,
      "max": 0.124788,
      "mean": 0.124788,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/val_bpb": {
      "min": 0.125324,
      "max": 0.125324,
      "mean": 0.125324,
      "count": 1
    },
    "val_bpb": {
      "min": 0.125324,
      "max": 0.125324,
      "mean": 0.125324,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/1/val_bpb": {
      "min": 0.124361,
      "max": 0.124361,
      "mean": 0.124361,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/2/val_bpb": {
      "min": 0.125246,
      "max": 0.125246,
      "mean": 0.125246,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/3/val_bpb": {
      "min": 0.124301,
      "max": 0.124301,
      "mean": 0.124301,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/4/val_bpb": {
      "min": 0.124554,
      "max": 0.124554,
      "mean": 0.124554,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/5/val_bpb": {
      "min": 0.124651,
      "max": 0.124651,
      "mean": 0.124651,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/6/val_bpb": {
      "min": 0.124811,
      "max": 0.124811,
      "mean": 0.124811,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/7/val_bpb": {
      "min": 0.124897,
      "max": 0.124897,
      "mean": 0.124897,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/8/val_bpb": {
      "min": 0.125464,
      "max": 0.125464,
      "mean": 0.125464,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/9/val_bpb": {
      "min": 0.125001,
      "max": 0.125001,
      "mean": 0.125001,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/10/val_bpb": {
      "min": 0.124673,
      "max": 0.124673,
      "mean": 0.124673,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/11/val_bpb": {
      "min": 0.124718,
      "max": 0.124718,
      "mean": 0.124718,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/12/val_bpb": {
      "min": 0.124951,
      "max": 0.124951,
      "mean": 0.124951,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/13/val_bpb": {
      "min": 0.124901,
      "max": 0.124901,
      "mean": 0.124901,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/14/val_bpb": {
      "min": 0.124842,
      "max": 0.124842,
      "mean": 0.124842,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/15/val_bpb": {
      "min": 0.125017,
      "max": 0.125017,
      "mean": 0.125017,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/16/val_bpb": {
      "min": 0.124319,
      "max": 0.124319,
      "mean": 0.124319,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/17/val_bpb": {
      "min": 0.12471,
      "max": 0.12471,
      "mean": 0.12471,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/18/val_bpb": {
      "min": 0.12445,
      "max": 0.12445,
      "mean": 0.12445,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/19/val_bpb": {
      "min": 0.125172,
      "max": 0.125172,
      "mean": 0.125172,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/low_compression/success_rate": {
      "min": 1.0,
      "max": 1.0,
      "mean": 1.0,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/success_rate": {
      "min": 1.0,
      "max": 1.0,
      "mean": 1.0,
      "count": 1
    },
    "success_rate": {
      "min": 1.0,
      "max": 1.0,
      "mean": 1.0,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/high_compression/0/val_bpb": {
      "min": 0.124857,
      "max": 0.124857,
      "mean": 0.124857,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/high_compression/1/val_bpb": {
      "min": 0.125031,
      "max": 0.125031,
      "mean": 0.125031,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/high_compression/2/val_bpb": {
      "min": 0.124798,
      "max": 0.124798,
      "mean": 0.124798,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/high_compression/3/val_bpb": {
      "min": 0.125031,
      "max": 0.125031,
      "mean": 0.125031,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/high_compression/4/val_bpb": {
      "min": 0.124942,
      "max": 0.124942,
      "mean": 0.124942,
      "count": 1
    },
    "globally_compressed_valbpb_minimizer/high_compression/5/val_bpb": {
      "min": 0.12487,
      "max": 0.12487,
      "mean": 0.12487,
      "count": 1
    },


... (truncated, see full artifact)


\begin{table}[h]
\centering
\caption{Experiment Results (Best Refinement Iteration)}
\begin{tabular}{lrrrr}
\hline
Metric & Min & Max & Mean & N \\
\hline
adversarially_pruned_core_artifact_selector/high_compression/0/val_bpb & 0.1251 & 0.1251 & 0.1251 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/1/val_bpb & 0.1257 & 0.1257 & 0.1257 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/10/val_bpb & 0.1244 & 0.1244 & 0.1244 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/11/val_bpb & 0.1255 & 0.1255 & 0.1255 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/12/val_bpb & 0.1245 & 0.1245 & 0.1245 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/13/val_bpb & 0.1252 & 0.1252 & 0.1252 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/14/val_bpb & 0.1250 & 0.1250 & 0.1250 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/15/val_bpb & 0.1252 & 0.1252 & 0.1252 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/16/val_bpb & 0.1249 & 0.1249 & 0.1249 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/17/val_bpb & 0.1249 & 0.1249 & 0.1249 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/18/val_bpb & 0.1252 & 0.1252 & 0.1252 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/19/val_bpb & 0.1253 & 0.1253 & 0.1253 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/2/val_bpb & 0.1246 & 0.1246 & 0.1246 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/3/val_bpb & 0.1255 & 0.1255 & 0.1255 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/4/val_bpb & 0.1247 & 0.1247 & 0.1247 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/5/val_bpb & 0.1254 & 0.1254 & 0.1254 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/6/val_bpb & 0.1248 & 0.1248 & 0.1248 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/7/val_bpb & 0.1249 & 0.1249 & 0.1249 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/8/val_bpb & 0.1254 & 0.1254 & 0.1254 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/9/val_bpb & 0.1253 & 0.1253 & 0.1253 & 1 \\
adversarially_pruned_core_artifact_selector/high_compression/success_rate & 1.0000 & 1.0000 & 1.0000 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/0/val_bpb & 0.1248 & 0.1248 & 0.1248 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/1/val_bpb & 0.1250 & 0.1250 & 0.1250 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/10/val_bpb & 0.1251 & 0.1251 & 0.1251 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/11/val_bpb & 0.1249 & 0.1249 & 0.1249 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/12/val_bpb & 0.1247 & 0.1247 & 0.1247 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/13/val_bpb & 0.1246 & 0.1246 & 0.1246 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/14/val_bpb & 0.1249 & 0.1249 & 0.1249 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/15/val_bpb & 0.1248 & 0.1248 & 0.1248 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/16/val_bpb & 0.1249 & 0.1249 & 0.1249 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/17/val_bpb & 0.1256 & 0.1256 & 0.1256 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/18/val_bpb & 0.1250 & 0.1250 & 0.1250 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/19/val_bpb & 0.1246 & 0.1246 & 0.1246 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/2/val_bpb & 0.1252 & 0.1252 & 0.1252 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/3/val_bpb & 0.1253 & 0.1253 & 0.1253 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/4/val_bpb & 0.1247 & 0.1247 & 0.1247 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/5/val_bpb & 0.1251 & 0.1251 & 0.1251 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/6/val_bpb & 0.1252 & 0.1252 & 0.1252 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/7/val_bpb & 0.1252 & 0.1252 & 0.1252 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/8/val_bpb & 0.1248 & 0.1248 & 0.1248 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/9/val_bpb & 0.1247 & 0.1247 & 0.1247 & 1 \\
adversarially_pruned_core_artifact_selector/low_compression/success_rate & 1.0000 & 1.0000 & 1.0000 & 1 \\
adversarially_pruned_core_artifact_selector/success_rate & 1.0000 & 1.0000 & 1.0000 & 1 \\
adversarially_pruned_core_artifact_selector/val_bpb & 0.1253 & 0.1253 & 0.1253 & 1 \\
artifact_maximal_retrieval_llm/high_compression/0/val_bpb & 0.1244 & 0.1244 & 0.1244 & 1 \\
artifact_maximal_retrieval_llm/high_compression/1/val_bpb & 0.1250 & 0.1250 & 0.1250 & 1 \\
artifact_maximal_retrieval_llm/high_compression/10/val_bpb & 0.1252 &

... (truncated, see full artifact)
