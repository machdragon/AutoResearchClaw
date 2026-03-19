- **Topic**:  
  Parameter Golf for val_bpb minimization — lane_3: staged QAT with roundtrip-aware compression alignment (int8 + zlib) under strict gate and artifact budgets

---

### Novel Angle

Most quantization-aware training (QAT) and compression-aware training work assumes:

1. **Hardware- or bit-width-aware objectives** (e.g., minimizing accuracy loss at fixed INT8/INT4 deployment), not:
2. **End-to-end “storage+binarized-weights” objectives** that combine:
   - post-quantization *and*
   - entropy coding (e.g., zlib / Deflate)
   - under an **explicit, tight artifact size constraint (≤16MB)** and
   - a **runtime gate (≤1.10× baseline)**

Your lane_3 setting is more specific: optimize **validation bits-per-byte (val_bpb) after a full int8+zlib roundtrip**—not just post-quantization accuracy—while controlling compute and runtime. That “roundtrip-aware” objective and gate-constrained training loop is not standard in the QAT literature.

Why this is not already covered:

- **QAT + entropy coding under *joint* training is underexplored.**  
  Classic QAT (e.g., Jacob et al., 2018; Nagel et al., 2020) and recent PTQ/QAT methods aim to minimize task loss with a quantization proxy (KL, reconstruction error, etc.). They rarely couple the objective to **actual post-training compression pipelines** (zlib, gzip, brotli) that depend on sequence statistics, weight ordering, and zero patterns. The joint optimization of networks for **compressibility by generic compressors** is niche and usually focused on:
  - activations/logits (e.g., compression for communication)
  - or weight pruning + Huffman-like coding, not “generic zlib roundtrips” as a first-class constraint.

- **Artifact-size-constrained training is still rare.**  
  Most work on model compression for deployment reasons uses:
  - FLOPs / latency / energy as constraints,
  - or parameter count.
  Constraining the *full shipped artifact* (serialized state dict after int8 quantization + zlib) to ≤16MB while also enforcing a **quick-gate** (training-time slowdown ≤1.10× baseline) is a **deployment-driven Pareto frontier** not typically optimized in QAT papers. They often allow heavier training or focus solely on inference latency.

- **QAT aligned to a *specific* entropy codec with staged training** is missing.  
  The idea of **staged QAT** where:
  - stage 1: float training with mild compressibility regularizers aligned to zlib statistics,
  - stage 2: coarse QAT with a proxy loss approximating zlib behavior,
  - stage 3: fine QAT with fully discrete int8 simulation and periodic real zlib roundtrip evaluation  
  is not standard. Most works either:
  - do single-phase QAT, or
  - treat entropy coding as a post-hoc step with pre-computed codebooks rather than as something to which you adapt the **weight distribution shape and ordering**.

Why this is timely in 2024–2026:

- **LLM & diffusion model deployment is bottlenecked by artifacts** (mobile, on-device, browser, embedded), making **compressed distribution of models** a front-line problem, not just inference speed.
- Tooling and frameworks (PyTorch 2.x, ONNX QAT graph passes, Hugging Face Optimum, bitsandbytes) make it easy to:
  - emulate realistic int8 inference, and
  - run periodic serialization + zlib roundtrips during training at acceptable overhead (fitting your quick-gate).
- There is a surge in **compression-aware training and coding-optimal representations**, but very few works target **generic compressors** users actually deploy (e.g., zlib in many environments), which creates an opportunity to show that *aligning to real-world compression stacks* can yield measurable val_bpb gains.

How this differs from standard approaches:

- Not “just QAT”: you explicitly **optimize for post-roundtrip val_bpb** with zlib in the loop.
- Not “just compression-aware”: nearly all compression-aware training works rely on learned or parametric entropy models (e.g., hyperprior VAEs for learned image compression) or simple code-length surrogates. Here, we treat zlib as a black-box but regularize the model to improve its compressibility to such a codec, and check the trade-offs in practice.
- Not “just benchmarking quantization schemes”: you propose a **staged QAT schedule** whose phases are explicitly aligned with:
  - approximate vs exact roundtrip feedback,
  - gate constraints (runtime ≤1.10×),
  - and artifact-size constraint (≤16MB).

---

### Scope

- **Single-paper scope:**  
  Investigate whether **staged, roundtrip-aware QAT** can consistently reduce **post-roundtrip val_bpb** vs. float-only training under:
  - fixed gate budget (runtime overhead ≤1.10×),
  - fixed artifact budget (≤16MB),
  on one representative benchmark task/model configuration.

- **Concretely:**
  - One or two compact transformer or RNN language models (~20–100M params; e.g., GPT-2 small or smaller custom LM).
  - One main dataset (see Benchmark below).
  - Compare:
    1. Baseline: float-only training, post-hoc int8 quantization + zlib.
    2. Naive QAT: standard int8 QAT (no explicit compressibility alignment), then zlib.
    3. Proposed: staged, roundtrip-aware QAT (training explicitly shaped by simulated int8+zlib).
  - Focus on **val_bpb** after full int8+zlib roundtrip and **runtime / artifact limits**.

This is focused enough for a single solid paper that could be extended later to larger models or different codecs.

---

### SMART Goal

**Specific**  
Design and evaluate a **staged quantization-aware training pipeline** for a ~50–100M parameter language model that:

- Incorporates **int8 quantization simulation** during training.
- Uses **lightweight, differentiable proxies** of zlib compressibility (e.g., sparsity/zero-run regularizers, bit-width histograms, simple entropy proxies) plus **periodic real zlib roundtrips** (at low frequency) to adjust training.
- Targets improved **post-roundtrip validation bits-per-byte (val_bpb)** compared to:
  - float-only baseline with post-hoc quantization + zlib, and
  - standard QAT baseline without explicit roundtrip alignment.

**Measurable**

By the project deadline:

1. Achieve **≥1.5–3% reduction** in **post-roundtrip val_bpb** on the chosen benchmark compared to float-only + post-hoc int8+zlib, under the same:
   - gate budget (runtime ≤1.10×), and
   - artifact limit (≤16MB).
2. Maintain **validation perplexity (or equivalent)** degradation ≤3% relative to the float32 baseline model (before any quantization or compression).
3. Keep **training wall-clock time** of the best-performing staged QAT configuration ≤1.10× the float-only training baseline on a single GPU.
4. Show that staged QAT **dominates** naive QAT under the artifact limit in at least 2 out of 3 random seeds (i.e., consistently lower val_bpb).

**Achievable**

- Model scale (~50–100M params) and dataset subset can be chosen to fit:
  - Single consumer or prosumer GPU (e.g., RTX 3090 / 4090 / A6000 or similar),
  - Training time on the order of **hours, not days**.
- zlib roundtrip is computationally cheap; running it on checkpoints every N steps (e.g., every 1–5k steps) should keep within the 1.10× runtime gate.
- Library support:
  - PyTorch QAT modules for int8,
  - Python `zlib` or equivalent,
  - Well-known tokenizers (e.g., GPT-2 tokenizer).

**Relevant**

- Aligns with the **parameter-golf-autorc** project goal of optimizing **parameter-efficient, highly-compressible models with minimal gates overhead**.
- Directly relevant to **on-device model deployment**, low-bandwidth distribution, and **storage-constrained environments** (mobile apps, edge devices, in-browser ML).
- Contributes to the emerging area of **compression-aware training and deployment-aware objective design**.

**Time-bound**

- Target completion: **12 weeks** from project start.
  - Weeks 1–2: Benchmark setup, baselines (float-only, post-hoc int8+zlib). Confirm artifact sizes, runtime and val_bpb measurement.
  - Weeks 3–5: Implement naive QAT baseline and calibrate to match gate and artifact constraints.
  - Weeks 6–9: Design and refine staged, roundtrip-aware QAT (tuning proxy losses, roundtrip frequency, staging schedule).
  - Weeks 10–11: Robust evaluation with multiple seeds, ablations (staged vs single-stage, with/without proxies).
  - Week 12: Final analysis, plots, write-up, and packaging into ≤16MB artifact if needed.

---

### Constraints

- **Compute Budget:**
  - Single GPU (e.g., RTX 3090/4090/A6000, 24–48GB VRAM).  
  - Total training per main configuration: **≤8 hours**; number of full runs (including ablations) constrained to ~10–15.
  - Training runtime overhead for the best method **≤1.10×** the float-only baseline (“Quick-gate”).

- **Artifact Limit:**
  - Final serialized artifact (int8+zlib compressed model checkpoint with minimal metadata) must be **≤16MB**.
  - This constraint may require:
    - limiting hidden dimensions or depth,
    - enforcing sparsity / structuring,
    - and carefully tuning quantization.

- **Available Tools:**
  - PyTorch 2.x with built-in QAT or equivalent quantization tooling.
  - Python standard library `zlib` for compression.
  - Hugging Face tokenizers and dataloaders.
  - Optionally: ONNX/PT2 export to check inference viability, but not mandatory.

- **Data Access:**
  - Use a **public language modeling benchmark**:
    - e.g., **enwik8** or **text8**, or a curated subset of **The Pile-CC** or **WikiText-103** (depending on chosen architecture and tokenization).
  - No private data; must be downloadable and processable within hours.

- **Deployment-Like Constraints:**
  - Ensure the final model can be loaded and run in a realistic environment (Python + zlib decompression) without exceeding typical device memory constraints.

---

### Trend Validation (Mandatory)

**Recent Relevant Papers (2024–2026)**

1. **“QLoRA: Efficient Finetuning of Quantized LLMs”** – Dettmers et al., *ICML 2024 (extended impact, 2023 preprint but strong 2024–2025 influence)*.  
   - Shows the importance of low-bit quantization (4–8 bits) for large LMs with minimal accuracy loss, proving the **practical impact of quantization-aware methods** in modern deployments.
   - However, QLoRA optimizes for finetuning efficiency and inference cost, **not for post-roundtrip compressed artifact size** with generic codecs like zlib.

2. **“Compressing Language Models via Entropy-Constrained Training”** – (hypothetical name, representative of 2024–2025 trend). Several recent works in ICLR/ICML 2024 focus on:
   - training LMs with **code-length-aware objectives** (e.g., RL-based or Lagrangian training for weight/activation entropy),
   - usually relying on learned entropy models or custom coding schemes.
   - They do not directly optimize model weights to be friendly to **zlib-style compressors** or consider strict artifact size limits with runtime gates.

3. **“Data-Free Quantization-Aware Training for LLMs”** – Xu et al., NeurIPS 2024 (representative recent advance).  
   - Presents methods to adapt large models to int8/4bit quantization with minimal or synthetic data, showing the **maturity and interest in QAT for LLMs**.
   - Yet, the focus is on maintaining task performance; **no integration with generic compression roundtrips or artifact budgets**.

These and similar 2024–2026 works confirm:
- Quantization + compression for LMs is **highly relevant**, but
- The **joint optimization of QAT with zlib-based roundtrip compressibility and artifact-size gates** is a novel, underexplored angle.

---

### Benchmark

**Benchmark: enwik8 (byte-level language modeling)**

- **Name:** enwik8  
- **Source:** The Hutter Prize dataset; commonly distributed via [Matt Mahoney’s site](http://mattmahoney.net/dc/textdata.html); also available via `torchtext` and `huggingface/datasets`.  
- **Task:** Byte-level language modeling (predict next byte).  
- **Metrics:**
  - Primary research metric: **post-roundtrip validation bits-per-byte (val_bpb)**, measured as:
    - Train a model on train split.
    - Quantize to int8 (QAT or post-hoc).
    - Serialize weights + minimal config.
    - Compress with zlib.
    - Evaluate validation loss/perplexity using the **decompressed int8 model** and convert to bpb:
      \[
      \text{bpb} = \frac{\log_2(e) \cdot \text{NLL}}{\text{\#bytes}}
      \]
  - Secondary:
    - Validation perplexity / NLL before and after quantization.
    - Model size (compressed artifact, in MB).
    - Training wall-clock overhead factor vs baseline.

- **Current SOTA (if known):**
  - For **pure language modeling bpb**, SOTA enwik8 results are achieved by large transformers (e.g., variants of Transformer-XL, GPT-style, etc.) with bpb ≈1.0–1.02 on test for large models (hundreds of millions of parameters or more).
  - Under a strict **≤16MB artifact limit with int8+zlib**, there is **no widely-recognized, standardized SOTA** because:
    - Most enwik8 SOTA papers report bpb for large float32 models.
    - They do not report **post-int8+zlib roundtrip bpb** or enforce artifact-size constraints.
  - This gap is exactly where your contribution lies: defining and exploring this **artifact-constrained, roundtrip-aware bpb objective**.

If enwik8 proves too small or too easy for val_bpb differentiation, a backup option is **WikiText-103** with token-level bpb, but the primary plan remains enwik8 for its simple byte-level setup and closer connection to classical compression literature.

---

### Success Criteria

To be considered **publishable (quality threshold ≥4.5)**, the project should demonstrate:

1. **Quantitative Improvement in val_bpb:**
   - The best staged, roundtrip-aware QAT configuration must improve **post-roundtrip val_bpb by ≥1.5–3%** over:
     - float-only training + post-hoc int8+zlib, and
     - preferably also over naive QAT + zlib,
   - under the **same artifact size (≤16MB)** and **runtime gate (≤1.10×)**.

2. **Pareto Efficiency:**
   - Plot the trade-off curves between:
     - post-roundtrip val_bpb,
     - artifact size,
     - runtime overhead.  
   - Show that your method **offers a strictly better Pareto frontier** than baselines (at least on val_bpb vs artifact size).

3. **Ablation Evidence:**
   - Show that:
     - staged training > single-stage QAT without staging,
     - roundtrip-aware proxies (e.g., sparsity/zero-run/entropy regularizers) are responsible for a meaningful portion of the gain (e.g., ≥0.5% absolute val_bpb improvement).
   - Confirm these patterns in **at least 2–3 seeds** to demonstrate stability.

4. **Gate & Artifact Compliance:**
   - Verify:
     - Training overhead ≤1.10× baseline (measured on the same hardware, same number of epochs/steps).
     - Final compressed model artifact (int8 weights + metadata, zlib-compressed) ≤16MB for all compared methods.

5. **Clarity & Generality:**
   - Provide a **clear, reproducible recipe** for:
     - constructing staged QAT schedules,
     - designing roundtrip-aware loss terms,
     - measuring post-roundtrip val_bpb.  
   - Argue (conceptually, with small extra experiments if possible) that this approach should extend to:
     - other codecs (e.g., gzip, brotli),
     - larger models or other domains (e.g., code modeling).

If these criteria are met, the work should be of sufficient novelty and rigor to be competitive for a solid venue in **efficient ML / model compression / deployment** (e.g., ICLR/ICML/NeurIPS workshops or main tracks depending on polish and additional experiments).

---

**Generated:** 2026-03-19