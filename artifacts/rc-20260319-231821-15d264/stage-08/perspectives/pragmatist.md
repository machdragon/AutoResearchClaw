Hypothesis 1 and 2 below are both feasible with modest GPUs and short training schedules, and they differ enough that you can run both as A/B experiments.

---

## Hypothesis 1 – Staged QAT + Dual-Path Consistency Improves Post-Roundtrip val_bpb

### Concrete, testable claim

Under a fixed architecture and gate budget, a **2‑stage training schedule** with fake-int8 and zlib roundtrip simulation plus a dual-path consistency loss will **reduce post-roundtrip val_bpb by at least 1–2%** versus a float-only baseline that is quantized+zlib’d post‑hoc, with:

- Same model size (≤16MB serialized artifact).
- Same inference precision (int8).
- Inference runtime ≤ 1.10× baseline.

#### Methodology

1. **Baseline (float-only)**
   - Train model in float32 with your existing objective (e.g., NLL / bpb).
   - After convergence:
     - Apply standard post‑training static int8 quantization.
     - Export int8 weights; pack them into the deployment artifact (≤16MB).
     - Evaluate val_bpb on validation by:
       - Running int8 model inference.
       - Serializing relevant outputs / latents as in deployment.
       - Applying zlib compress→decompress.
       - Measuring codelength → compute val_bpb.
   - Record:
     - `val_bpb_baseline`
     - Inference latency (`t_base`) on fixed hardware.
     - Artifact size (`S_base`).

2. **Proposed: staged QAT + roundtrip path**

   Stage 1: Float pretraining  
   - Train the same architecture in float32 to roughly the same task performance as baseline (can even reuse the baseline checkpoint as starting point).

   Stage 2: QAT + dual-path forward
   - Insert fake-quantization ops (weights + key activations) emulating int8 (per-tensor or per-channel).
   - In each training step:
     - **Clean path**: forward pass with float32 weights/activations (or higher-precision copy).
     - **QAT+roundtrip path**:
       - Fake-quantize weights and activations to int8.
       - Option A (fast): Instead of actual zlib, use a differentiable proxy:
         - Measure sample-wise entropy or bit-estimate over the tensors that would be serialized.
         - Optionally inject small noise/compression-like perturbations to approximate zlib artifacts.
       - Option B (slower but still feasible if done sparsely, e.g., every N batches):
         - Quantize → serialize to bytes → run zlib (compress+decompress) on CPU.
         - Deserialize back to int8 → dequantize.
     - Compute loss:
       - Main task loss on QAT+roundtrip path: `L_task(QRT)`.
       - Consistency loss between clean and QRT paths, e.g.:
         - `L_feat = ||h_clean - h_qrt||²` on one or two chosen layers.
         - `L_logit = KL(p_clean || p_qrt)` over output distribution.
       - Optional compression proxy loss:
         - `L_comp = H_proxy(activations_to_be_serialized)` (e.g., logit entropy or histogram-based entropy estimate).
       - Total: `L = L_task(QRT) + α L_feat + β L_logit + λ L_comp`.
   - Train for a modest number of epochs (e.g., 20–30% of baseline training steps).

   Deployment
   - From the final QAT checkpoint, generate the int8 weights in the same format/zlib pipeline as baseline.
   - Ensure artifact size ≤16MB and that inference graph is identical to baseline’s int8 graph (no extra ops).

3. **Evaluation**
   - Use the *same* int8 runtime and zlib configuration for both models.
   - Evaluate post-roundtrip val_bpb on the same validation set:
     - Measure `val_bpb_qat`.
   - Verify:
     - Runtime ≤ 1.10× `t_base`.
     - Artifact size ≤16MB and not larger than baseline by more than, say, 1–2% (ideally equal).

### Why achievable with limited compute

- QAT with fake quantization is standard and adds only light per-tensor ops.
- Dual-path forward can be implemented via shared weights; the second path reuses most compute graphs.
- Compression simulation:
  - Differentiable proxies are cheap.
  - True zlib roundtrip can be amortized by:
    - Running on CPU, batched over a subset of minibatches (e.g., 1 in 10).
    - Or approximating its rate via entropy proxy most of the time.
- Training-time overhead is maybe 1.3–1.7× vs baseline, but:
  - Training can be shorter in stage 2 (fine-tune only).
  - Inference-time overhead is zero (same graph, just int8).

This is a small project on a single 16–24GB GPU or 2 smaller GPUs.

### Rationale based on proven techniques

- QAT: Widely used to recover performance lost by post‑training quantization, especially to int8; known to shrink gaps vs float.
- Dual-path / consistency: Matches cluster 1 and 2 ideas (auxiliary branches and self-distillation) but without changing deployed graph.
- Training-with-noise: Treats quantization + compression artifacts as structured noise during training, similar to dropout and data augmentation, improving robustness to deployment conditions.

### Measurable prediction and failure condition

- **Prediction**:  
  `val_bpb_qat ≤ 0.99 * val_bpb_baseline` (1%+ relative improvement) with:
  - Int8 inference runtime ≤ 1.10× `t_base`.
  - Artifact size within 16MB and within +2% of baseline.

- **Failure conditions (any of these)**:
  - `val_bpb_qat > val_bpb_baseline` (no improvement in post-roundtrip val_bpb).
  - Inference runtime > 1.10× `t_base`.
  - Artifact > 16MB or materially larger than baseline under same packing.

### Resource requirements estimate

- Hardware: 1× mid-range GPU (e.g., 12–24GB VRAM) + CPU for occasional zlib.
- Training time:
  - Baseline float training: whatever you already use (e.g., 8–24 hours).
  - QAT fine-tune: ~20–40% of baseline steps (few more hours).
- Memory:
  - Need to hold both clean and QRT activations for consistency loss at selected layers; still under typical GPU limits for moderate models.

---

## Hypothesis 2 – Float Teacher → Int8+Zlib Student Distillation Improves Post-Roundtrip val_bpb at Same Runtime

### Concrete, testable claim

A **teacher–student self-distillation setup**, where a fixed float32 teacher guides an int8+zlib-simulated student during training, will **improve post-roundtrip val_bpb by at least 1–2%** compared to a QAT‑only student trained without teacher signals, under the same gate budget and runtime constraints.

This directly tests whether the RS-SSKD-style idea (teacher guidance under constraints) provides extra benefit on top of QAT.

#### Methodology

1. **Baseline student (QAT-only)**
   - Use the *best* QAT schedule you currently have that passes the 1.10× runtime and 16MB limits, but without any teacher/stage‑1 distillation:
     - Fake-int8 + (approx) zlib roundtrip in training.
     - Optimize only task loss on the QRT path.
   - Produce final int8 weights and zlib artifact.
   - Measure:
     - `val_bpb_qat_only`
     - Inference runtime `t_qat_only` (must pass quick-gate).
     - Artifact size `S_qat_only`.

2. **Teacher‑student setup**

   Teacher
   - Train or reuse a strong float32 model (float baseline or slightly larger but not deployed).
   - Freeze it after convergence.

   Student
   - Same architecture and int8 deployment as QAT baseline; gate budget identical.
   - During training, for each minibatch:
     - Run teacher in float32 on input: get teacher logits and optionally intermediate features.
     - Run student with fake-int8 + roundtrip proxy (as in Hypothesis 1).
   - Loss:
     - Main task loss on student outputs: `L_task(student_qrt)`.
     - Distillation term:
       - KL divergence between teacher logits and student logits after roundtrip: `L_KD = KL(p_teacher || p_student_qrt)`.
       - Optionally feature matching on 1–2 layers: `L_feat = ||f_teacher - f_student_qrt||²`.
     - Total: `L = L_task + γ L_KD + δ L_feat`.
   - Train from scratch or fine-tune from a QAT pre-init for a moderate number of epochs.

   Deployment
   - Discard teacher; export only int8 student + zlib artifact.
   - Inference is identical in cost to QAT-only student.

3. **Evaluation**
   - Use identical deployment conditions (int8 kernel, zlib config).
   - Compute `val_bpb_student` on validation after zlib roundtrip.
   - Check:
     - Runtime `t_student` ≈ `t_qat_only` (same graph, so they should match).
     - Artifact size `S_student` ≤16MB.

### Why achievable with limited compute

- Teacher runs only during training; inference uses the same student graph as QAT-only baseline.
- Student architecture is unchanged; all extra cost is in training-time teacher forward + distillation losses.
- Teacher can be early-stopped or reused from existing experiments.
- You can reduce teacher cost:
  - Use a smaller teacher than the student (still helpful).
  - Run teacher at lower input resolution or less frequently (e.g., only on every Nth batch).

Feasible on 1–2 GPUs; training time roughly 1.5–2× that of QAT-only fine-tune, but still considerably less than doubling full end‑to‑end training because you can start from a QAT-pretrained checkpoint.

### Rationale based on proven techniques

- Self/distillation (cluster 2) improves robustness and representation quality under constraints, even when teacher and student are the same architecture.
- Distillation has been shown to help quantized students match float teachers in many production systems.
- Here, the student learns *specifically* to match teacher outputs after quantization + (proxy) compression, aligning with deployment conditions.

### Measurable prediction and failure condition

- **Prediction**:  
  `val_bpb_student ≤ 0.99 * val_bpb_qat_only` (≥1% relative improvement) with:
  - `t_student ≤ 1.10× t_qat_only` (practically equal since same model).
  - `S_student ≤ 16MB`.

- **Failure conditions (any of these)**:
  - `val_bpb_student ≥ val_bpb_qat_only` (no gain over QAT-only).
  - Distillation degrades core task quality (if you also track accuracy/perplexity) without val_bpb benefit.
  - Any increase in deployed runtime or artifact size (shouldn’t happen if you enforce identical student architecture and quantization scheme).

### Resource requirements estimate

- Hardware: same as Hypothesis 1; 1× 16–24GB GPU is enough.
- Training time:
  - Reuse QAT-only checkpoint as init.
  - Distillation fine‑tune: ~25–50% of baseline training steps.
  - Teacher forward adds overhead but is just an extra forward; total wall time maybe ~1.5× QAT-only fine-tune.
- Memory:
  - Need teacher + student in memory for training, but both are moderate models; gradients only for student.

---

If you want to implement just one first, start with Hypothesis 1: it’s simpler (no separate teacher) and directly tells you how much benefit you get from roundtrip-aware QAT alone. Then layer in Hypothesis 2 if you see any gap between float and int8+zlib performance.