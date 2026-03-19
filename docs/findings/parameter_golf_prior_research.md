# Parameter Golf — Prior Research Summary

**Source documents**: `parameter-golf/docs/deep-research-report.md`,
`PR_APPROACHES.md`, `WORLD_RECORD_RESEARCH.md`, and
`arc_inputs/case_matrix_v1.json` (4 research lanes).

---

## Problem Definition

Minimize post-roundtrip **val_bpb** (bits-per-byte on FineWeb validation set) subject to:

- **Artifact size ≤ 16,000,000 bytes** (int8-quantized + zlib-compressed checkpoint)
- **Quick gate runtime ≤ 1.10× baseline** (train_time_ms ceiling)
- Training uses `train_gpt.py` via `quick_harness.sh` (20 steps, seed=1337)
- Evaluation uses the post-roundtrip path (int8 → zlib → reload → eval)

---

## Baseline

| Metric | Value |
|--------|-------|
| val_bpb | **3.37944261** |
| train_time_ms | **62992** (~63 s for 20 steps) |
| Runtime ceiling (1.10×) | **69291 ms** |
| Model size | 17M params |
| Architecture | 9 layers, 512 dim, GQA 8h/4kv |
| Seed | 1337 |
| Dataset | FineWeb10B, sp1024 tokenizer |

---

## Key Findings from Prior Research

### Recurrence + Weight Sharing (highest confidence)
- Sharing transformer blocks across recurrence loops achieves effective depth without proportionally increasing stored parameters.
- Weight sharing directly attacks the 16MB artifact constraint — fewer unique weights = smaller checkpoint.
- Low-rank adapters (LoRA) per loop recover loop-specific specialization at negligible storage cost.
- **Recommended first test**: `num_shared_blocks=3, num_recurrence_loops=3, lora_rank=8, lora_alpha=16`

### GQA/MQA Efficiency
- Reducing KV heads under recurrence can improve quality/runtime tradeoff.
- Baseline already uses GQA (8h/4kv); further reduction to 2kv heads may help under recurrence.
- Risk: val_bpb regression if KV bottleneck is too tight.

### Compression-Aware Training (QAT)
- Training aligned to the int8 roundtrip path can reduce post-roundtrip quality degradation.
- QAT schedules that kick in after initial convergence (qat_start_frac ~0.5) have shown promise.
- Dependency: requires model to converge first; riskier to test in isolation.

### Tokenizer Lane (deferred)
- Tokenizer changes affect comparability with baseline — require stricter accounting.
- Deferred to later runs after recurrence lanes are validated.

---

## Research Lanes (arc_inputs/case_matrix_v1.json)

### Lane 1 — Recurrence + LoRA specialization ⭐ INITIAL FOCUS
- **Hypothesis**: Weight sharing + low-rank loop specialization improves quality per stored byte.
- **Knobs**: `num_shared_blocks`, `num_recurrence_loops`, `lora_rank`, `lora_alpha`, `lora_dropout`
- **Gate**: single quick-gate pass required for promotion

### Lane 2 — Recurrence + MQA/GQA efficiency
- **Hypothesis**: Lighter KV parameterization preserves quality/runtime tradeoff under recurrence.
- **Knobs**: `num_heads`, `num_kv_heads`, `head_dim`, `num_recurrence_loops`
- **Gate**: single quick-gate pass

### Lane 3 — Compression-aware / QAT
- **Hypothesis**: QAT schedules matching int8+zlib deployment path preserve post-roundtrip quality.
- **Knobs**: `qat_enabled`, `qat_start_frac`, `qat_group_size`, `compression_reg_lambda`, `quant_error_weight`
- **Gate**: single quick-gate pass

### Lane 4 — Tokenizer (strict gate)
- **Hypothesis**: Tokenizer choices can improve val_bpb but require stricter reproducibility.
- **Gate**: single_pass_plus_manual_review — **defer to later runs**

---

## Guardrails

- Do NOT modify `train_gpt.py`, `scripts/`, or canonical entrypoints without explicit approval.
- All performance claims must come from real harness output — no synthetic metrics.
- Write experiment outputs to `/workspace`, not to `/parameter-golf` (mounted read-only).
- Promotion requires: artifact ≤ 16MB + val_bpb improved + run metadata archived.

---

## Run Strategy for Run 2

1. Test **Lane 1** with **one condition** vs baseline only (single seed=1337).
2. Parse `val_bpb` from `train_gpt.py` stdout: `re.search(r"val_bpb[:\s=]+([0-9.]+)", stdout)`.
3. Report real metric — if val_bpb < 3.37944261 and runtime ≤ 69291ms, gate passes.
4. Do not sweep multiple seeds until single-seed gate is confirmed working.
