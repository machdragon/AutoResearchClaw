Below is an audit of the experimental methodology given the information you provided. I’ll separate “what we can infer” from “what’s missing/broken” and end with a concrete checklist of fixes.

---

## 1. Baseline Fairness and Completeness

### 1.1. Baseline comparability

You report:

- `baseline_val_bpb = 3.37944`
- `baseline_runtime_ms = 62992`
- Candidate (QAT + compression-reg):
  - `val_bpb = 3.3919` (worse)
  - `candidate_runtime_ms = 80894` (slower)
  - `runtime_ratio = 1.2842` (> 1.10 quick-gate; fails)
  - `quick_gate_passed = 0`

Baseline fairness hinges on:

- Same architecture
- Same data
- Same training budget (steps, epochs, optimizer schedule, seed policy)
- Only the QAT/compression knobs change

You do not show:

- The exact baseline training hyperparameters
- Whether the baseline also obeys the artifact limit (≤16MB) and same int8+zlib roundtrip
- Whether the baseline is truly “float-only training with later quantization” or also involves some quant-aware behavior

Thus, baseline fairness is currently **not demonstrably established**. It is plausible but not guaranteed.

**Required clarifications / fixes:**

1. Explicit baseline spec:
   - Condition name, flags: `qat_enabled=false`, `compression_reg_enabled=false`, `qat_start_frac` unused, etc.
   - Same training steps, optimizer, LR schedule, batch size, seed.
   - Same post-training processing: int8 quantization + zlib, not special-cased.

2. Ensure both baseline and candidate are evaluated *after the exact same deployment pipeline*:
   - float weights → int8 quantization → serialized → zlib compress
   - `val_bpb` computed on the same validation set, same decoding logic.

3. Confirm artifact cap enforcement is identical:
   - If candidate training is constrained or altered by hitting the 16MB limit (e.g., pruning, structured reordering), baseline must be subject to the same constraint; otherwise you are not comparing under the same deployment regime.

### 1.2. Baseline completeness

Your hypothesis is about:

- **Codec-guided distillation vs the best standard QAT + distillation baseline**

But we only see one candidate run, labelled `"condition": "full_staged_QAT"`, with `compression_reg_enabled=true`. There’s no actual “best standard QAT+KD” reference in the logs you provided.

So the current baseline set is incomplete relative to the hypothesis:

- We need at least:
  - Float-only training (+ standard KD if desired) + post-hoc int8 + zlib
  - Strong QAT without compression-regularization (+ KD)
  - Your proposed codec-guided teacher/QAT config

Without those, you can’t disentangle:

- Effect of QAT itself
- Effect of compression-aligned regularizers
- Effect of KD vs no KD

---

## 2. Metric Appropriateness for the Research Question

### 2.1. Primary metric: `val_bpb`

Given the research goal (“Parameter Golf for val_bpb minimization” after **int8+zlib roundtrip**), `val_bpb` is an appropriate primary metric, *if and only if*:

- It is computed **post-roundtrip**:
  - Model is quantized to int8
  - Weights serialized
  - Zlib compressed
  - Then evaluation uses this compressed artifact (or faithfully simulated equivalent) to run inference.
- `val_bpb` is defined precisely (e.g., negative log-likelihood bits-per-byte, or bits-per-token normalized to bytes of raw text).

Missing details:

- Whether `val_bpb` is:
  - (a) perplexity-like metric over the validation set (task performance), or
  - (b) compression ratio of model weights / activations.
- Whether the int8+zlib artifact is only used for model storage size or also used in runtime (e.g., on-the-fly decompression or stored-only).

Because the context says: “optimize validation bits-per-byte after a full int8+zlib roundtrip”, I will assume this is the **task metric (compression of text / NLL)**, not model-size metric. If so, it is appropriate, but this should be aggressively documented.

### 2.2. Secondary metrics: runtime, artifact size

You track:

- `candidate_runtime_ms`, `baseline_runtime_ms`
- `runtime_ratio`
- `quick_gate_passed` (<=1.10 threshold)

This is conceptually aligned with the quick-gate constraint, but:

- Runtime needs variance estimates: the current numbers have `n=1`, so no sense of noise.
- It is unclear if `runtime_ms` includes:
  - Training only?
  - Training + evaluation?
  - Whether I/O, zlib calls, and quantization overheads are counted.

Given that the gate is quite tight (1.10×), minor measurement noise or environment variation can flip gate outcomes. You need repeated measurements or at least stable timing conditions.

### 2.3. Missing: artifact-size metric

You state a **16MB artifact limit**, but there’s no artifact metric in the exposed results:

- You should log:
  - `artifact_size_bytes`
  - `artifact_size_ratio = artifact_size_bytes / (16 * 1024 * 1024)`
  - A boolean `artifact_gate_passed`

Without this, we cannot audit whether you’re truly on the feasible frontier (size & runtime constraints) or just optimizing `val_bpb` and runtime.

---

## 3. Evaluation Protocol: Data Leakage & Contamination Risks

Given only the summary logs, we cannot see:

- Dataset splits
- Preprocessing pipeline
- Whether there is reuse of validation data for training heuristics

Potential leakage/contamination points in a setup like this:

1. **Codec-guided regularization using validation data**  
   If you ever:
   - Compute zlib-based losses on validation samples during training, or
   - Tune quantization/entropy parameters based on validation labels directly,

   you contaminate the validation set.

2. **Selection of checkpoints based on validation `val_bpb` repeatedly**  
   Early stopping or checkpoint selection on the same validation set is standard, but:
   - If your final claims are on that same `val_bpb`, that’s okay but must be reported (no hidden test set).
   - If there’s also a “real test set”, it must not enter training decisions.

3. **Teacher/Student data overlap**  
   If you use a distilled teacher:
   - Ensure teacher training did not include the evaluation subset in ways that bias the comparison (usually acceptable, but worth stating: teacher is pre-trained, frozen).

Because none of this is specified, contamination risk assessment is **incomplete**. For now, we must say:

- No explicit evidence of leakage, but
- No safeguards are documented.

**Minimum improvements:**

- Clearly document:
  - Training / validation / test splits.
  - That the compression regularization signal (`L_zlib`, weight compressibility) is computed on training-only data (or on weights only).
  - That no validation samples are used to adapt the compression objective or thresholds.
  - If you use a separate test set for final reported numbers, show it.

---

## 4. Ablation Completeness and the Critical Ablation Warning

You report:

> CRITICAL ABLATION WARNINGS:
> - ABLATION FAILURE: Conditions 'hyperparameters' and 'metrics' produce identical outputs across all 1 metrics. The ablation is invalid — the differentiating parameter is likely not used in the code.

Then the “run context” shows just a single run:

```json
"hyperparameters": {
  "condition": "full_staged_QAT",
  "qat_enabled": true,
  "qat_start_frac": 0.5,
  "qat_group_size": 32,
  "compression_reg_enabled": true,
  "compression_reg_lambda": 0.0001,
  "compression_reg_scope": "final_proj,embed",
  "compression_reg_target": "teacher",
  "quant_error_weight": 1.0,
  "fake_quant_strength": 1.0,
  "seed": 1337
}
```

And identical metrics across all “conditions” in the ablation.

This is **methodologically fatal** for any claims about specific hyperparameters. It strongly suggests:

- Either:
  - Ablation script is not actually changing hyperparameters between conditions, or
  - The training code ignores those hyperparameters (e.g., `compression_reg_enabled` or `qat_enabled` are not wired).

Consequences:

- You **cannot** claim any effect from:
  - `compression_reg_lambda`
  - `compression_reg_scope`
  - `compression_reg_target`
  - `qat_start_frac`
  - `qat_group_size`
  - or even from QAT vs non-QAT, if the code path doesn’t actually switch.

- Your current experiment is effectively N=1 with a **single operative configuration**, and ablation comparisons are meaningless.

**Required ablation fixes:**

1. **Sanity check toggles with gross metrics:**
   - Run a minimal 2-condition test:
     - `qat_enabled=false, compression_reg_enabled=false`
     - `qat_enabled=true, compression_reg_enabled=true`
   - Add debug prints:
     - For each batch or epoch, log whether fake-quant hooks are active and whether `compression_reg_loss` is non-zero.
   - If metrics are still identical and logs show no behavior change, the flags are not being used.

2. **Wire the hyperparameters explicitly:**
   - Ensure `qat_enabled` guards the insertion of quantization stubs/fake-quant modules.
   - Ensure `compression_reg_enabled` controls whether `L_zlib` or similar term is computed and added to the loss.
   - Ensure `compression_reg_scope` is parsed and applied to the right modules.
   - Verify `compression_reg_lambda` actually scales the additional loss.

3. **Once wiring is confirmed**, design a proper ablation grid:
   - Baseline vs QAT:
     - `qat_enabled=false, compression_reg_enabled=false`
     - `qat_enabled=true, compression_reg_enabled=false`
   - Compression-aware vs plain QAT:
     - `qat_enabled=true, compression_reg_enabled=false`
     - `qat_enabled=true, compression_reg_enabled=true`
   - Optional:
     - Vary `compression_reg_lambda` across e.g. {0, 1e-5, 1e-4, 1e-3}.

4. **Per-condition run count:**
   - For at least the key hypotheses, run ≥3 seeds per condition to estimate variance in `val_bpb` and runtime.

Until this is done, the ablation claims are **invalid** by your own diagnostic.

---

## 5. Reproducibility Assessment

### 5.1. What’s logged

You log:

- Hyperparameters object, including seed
- Metrics object with final `val_bpb` and runtime stats
- `stdout` includes the same final metrics
- `elapsed_sec` and completion metadata

This is a good start, but incomplete for full reproducibility.

### 5.2. Missing elements for replication

To be able to re-run and verify:

1. **Exact training configuration:**
   - Optimizer type + hyperparams (LR, betas, weight decay, warmup, schedule)
   - Batch size, number of steps/epochs
   - Data loading parameters (shuffling, num_workers, tokenization/vocab)
   - Model architecture details (layers, hidden size, heads, etc.)

2. **Quantization details:**
   - Quantization scheme: per-tensor / per-channel, symmetric/asymmetric, calibration method, rounding mode.
   - Where fake-quant is inserted (weights only, weights+activations, which layers).
   - QAT schedule: at what step or epoch is `qat_start_frac=0.5` applied; how is it implemented.

3. **Compression pipeline details:**
   - Exact zlib settings (compression level, window size, strategy).
   - Serialization format of weights (endianness, tensor ordering, whether you pack biases, etc.).
   - Any pre-processing of weights (e.g., reordering, sparsification) before zlib is applied.

4. **Environment:**
   - Framework versions (PyTorch/TensorFlow/etc. + CUDA/cuDNN).
   - Hardware specifics (CPU, GPU type), especially if runtime is part of the objective.

5. **Randomness control:**
   - Seeds are logged, but confirm:
     - `torch.manual_seed`, `numpy`, and Python `random` all set.
     - CUDA deterministic flags if needed.

Given that only a small subset of this is shown, reproducibility is **partial at best**.

**Improvements needed:**

- Provide a `config.yaml` or equivalent that fully specifies the experiment.
- Provide a single entry-point script / command with all arguments logged.
- Log git commit hash and any local modifications.

---

## 6. Specific Methodology Improvements

Here is a concise checklist tailored to your setting.

### 6.1. Fix ablation design and wiring (highest priority)

- Ensure hyperparameters actually control code paths:
  - Add runtime assertions like:
    - “QAT enabled: injecting fake-quant modules into layers X,Y,Z” with a count.
    - “Compression regularization enabled: L_comp=…” printed for first few steps.
- Rerun ablations and verify that at least some metrics differ across conditions.
- Only after wiring is verified, interpret differences in `val_bpb` or runtime.

### 6.2. Strengthen baseline definition

- Define and log an explicit **float-only baseline**:
  - `qat_enabled=false`, `compression_reg_enabled=false`.
  - Same training budget, same data, same evaluation pipeline (int8+zlib roundtrip).
- Define a **strong QAT baseline**:
  - `qat_enabled=true`, but no compression regularization or special teacher aligned to codec.
- Compare your proposed “compression-teacher QAT” only against this strong QAT baseline, not just float-only, to test the hypothesis as stated.

### 6.3. Clarify and enforce constraints (runtime and size)

- Runtime:
  - Measure `candidate_runtime_ms` and `baseline_runtime_ms` in a controlled setting.
  - Use at least 3 runs per condition or repeated timing on the same hardware to get mean/std.
  - Report whether runtime includes full training or only a fixed evaluation window.

- Artifact size:
  - Log `artifact_size_bytes` for both baseline and candidate.
  - Enforce the ≤16MB constraint either:
    - As a hard reject (config invalid if >16MB), or
    - As a soft constraint (penalty term in the objective), but then report violations.

### 6.4. Evaluation protocol and leakage control

- Explicitly state:
  - Training set, validation set, and (if present) test set.
  - That no validation samples are used to compute training-time compression regularization or to tune codec-related hyperparameters.
- If you rely on early stopping or model selection using `val_bpb`, acknowledge that the reported metric is a *validation metric*, not a held-out test metric.

### 6.5. More complete metric reporting

- For each condition and seed, record:
  - `val_bpb`, `candidate_runtime_ms`, `artifact_size_bytes`.
- Also record:
  - Training loss curves.
  - Compression-regularization loss component magnitude over training (to see if it is actually active and influencing gradients).
- Aggregate:
  - Mean and std over seeds.
  - Confidence intervals for `delta_bpb` vs baseline.

### 6.6. Alignment of metric to hypothesis

- Your hypothesis is stated in relative improvements: “≥1.5% relative reduction in post-roundtrip val_bpb vs baseline.”
  - For each ablation:
    - Compute `%improvement = (baseline_val_bpb - candidate_val_bpb) / baseline_val_bpb * 100`.
    - Explicitly test against thresholds (≥1.5% success, <0.5% failure) with variance.
- Ensure the baseline used in that comparison is indeed “the best standard QAT+distillation baseline” you can build, not an arbitrary weaker one.

---

## 7. Summary

- Current evidence shows **one** run where the candidate QAT+compression-reg setup:
  - Slightly **worsens** `val_bpb` (+0.0125 absolute, ~0.37% worse).
  - Significantly **violates** the runtime quick-gate (1.28× vs allowed 1.10×).
- Ablation diagnostics indicate that hyperparameter toggles probably **do not actually change the code path**, so all ablation-based interpretations are invalid.
- Baseline fairness is not fully established; baseline completeness vs your own hypothesis (best QAT+KD) is missing.
- Metric choice (val_bpb + runtime) is conceptually aligned, but artifact size constraint is not exposed in the metrics, and runtime is measured only once.
- Reproducibility is partial; critical aspects of training/quantization/compression configuration are absent from logs.

Until the wiring and ablations are fixed and baselines are clearly defined, **no substantive claim** about the benefit of codec-guided QAT or compression-teacher alignment can be supported by this experiment.