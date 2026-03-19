## Cluster Overview

1. **Cluster 1 – Training-time enhancements without inference overhead**  
   Focus: Techniques that change only the training procedure (multi-size inputs, auxiliary losses, dropout, distillation) to improve accuracy while keeping inference-time architecture and complexity fixed.  
   Key card: zhang2020training.

2. **Cluster 2 – Representation learning and self-distillation under resource constraints**  
   Focus: Learning more discriminative representations (two-branch networks, CAMs, self-supervision, knowledge distillation) in low-data settings, with attention to training cost vs. deployment needs.  
   Key card: zhang2021rssskd.

3. **Cluster 3 – Model class choice vs. classical baselines under fixed feature budget**  
   Focus: Comparing classical models (OLS) with more flexible ones (Random Forest) using the same features, showing that better use of existing signals yields large performance gains under the same “input budget.”  
   Key card: hong2020house.

Below, I relate each cluster to the target topic:

> Parameter Golf val_bpb minimization — lane_3: QAT + roundtrip-aware compression alignment.  
> Hypothesis: If we enable staged QAT aligned to int8+zlib roundtrip, post-roundtrip val_bpb will improve versus float-only training under the same gate budget. Artifact limit 16MB. Quick-gate: runtime <= 1.10× baseline.

The synthesis interprets “gate budget” and “no inference overhead / no extra parameters” analogously: you may alter training and internal flows to align with quantization + compression, but deployed model size, runtime, and architecture must remain tightly constrained.


---

## Cluster 1 – Training-time Enhancements Without Inference Overhead

**Core idea from zhang2020training**

- Modify only the *training* pipeline:
  - Multi-size image training → robustness to scale.
  - Auxiliary triplet-loss branch → more structured embeddings.
  - Dropout between feature extractor and classifier.
- At inference, all these additions are *inactive* or removed:
  - Architecture, parameter count, and FLOPs are identical to the vanilla ResNet-18 baseline.
- Gains: ~+1.61 percentage points in accuracy on OPTIMAL, with no inference-time overhead.

**Conceptual transfer to QAT + roundtrip-aware compression**

Analogies to the Parameter Golf setup:

- **Multi-size training ↔ multi-condition training for quantization/compression**  
  - Instead of multi-size images, use multi-condition forward passes:
    - Clean float32 forward.
    - Quantized int8 emulation (fake quantization).
    - Int8 + zlib “roundtrip” emulation (quantize → pack → compress → decompress → unpack → dequantize).
  - The model learns robustness to the *distribution shift* introduced by quantization and entropy coding, analogous to scale robustness.

- **Triplet loss branch ↔ auxiliary roundtrip consistency / margin losses**  
  - Add a training-only branch or loss that:
    - Forces representations *after* the int8+zlib roundtrip to remain close (or margin-separated) relative to clean float32 outputs.
  - Example parallels:
    - Use a “triplet-like” structure:
      - Anchor: clean float output.
      - Positive: int8 roundtrip output on same input.
      - Negative: roundtrip output on other samples.
    - Encourage post-roundtrip val_bpb (negative log-likelihood per byte, or compression-related metric) to remain as low as clean float’s val_bpb, within a margin under the same model capacity and runtime budget.

- **Dropout ↔ stochastic regularization to mimic quantization noise**  
  - Standard dropout acts as regularization, improving generalization.
  - Analogous methods here:
    - Inject quantization-like noise in activations/weights during training to pre-condition the model for int8 discretization.
    - Stochastic masking of channels/heads that emulates reduced precision or packed representation constraints.

**Implications for the hypothesis**

- It is empirically plausible, by analogy, that:
  - A *staged* training regimen that explicitly sees int8+zlib artifacts can outperform float-only training on post-roundtrip val_bpb.
  - This is consistent with the principle: “Train under the constraints you will deploy under, but keep those constraints as training-only modules whose overhead is discarded at inference.”
- Key structural lesson:  
  - Keep the *deployed* model identical (same “gate budget,” same runtime) but invest extra complexity in training to learn quantization/compression-robust representations.


---

## Cluster 2 – Representation Learning and Self-Distillation Under Constraints

**Core idea from zhang2021rssskd (RS-SSKD)**

- Two-branch network:
  - Each branch sees original–transformed image pairs.
  - Uses CAMs to emphasize category-discriminative regions.
- Self-supervision + self-knowledge distillation:
  - The model distills knowledge from its own stronger predictions or intermediate representations.
- Designed for *few-shot* settings:
  - Extract maximally informative embeddings when labeled data is scarce.
- Training complexity is higher; however, *deployment* uses the learned embedding network without necessarily carrying the full complexity of the training setup.

**Conceptual transfer to QAT + compression alignment**

- **Two-branch / multi-view design ↔ clean vs. roundtrip branches**
  - Interpret two “views” of a sample:
    - View A: clean float forward.
    - View B: int8+zlib roundtrip forward.
  - Use a two-branch architecture *only during training* (or two pathways in the same network):
    - Shared weights, distinct forward paths.
    - Use attention-like mechanisms (analogous to CAMs) to:
      - Identify which internal features are *most sensitive* to quantization+compression.
      - Emphasize features that are stable across the two branches.
  - This aligns the model to represent information that survives an int8+zlib roundtrip while still being predictive.

- **Self-distillation ↔ teacher-student alignment under quantization**
  - Teacher: full-precision, unconstrained version (or early-stage checkpoint) of the network.
  - Student: the quantization-aware, roundtrip-aligned version.
  - Use self-distillation losses:
    - KL divergence between teacher logits (clean) and student logits (post-roundtrip).
    - Feature matching between intermediate activations (e.g., L2 loss).
  - This is especially relevant under strict artifact limits (16MB) and runtime constraints:
    - Self-distilled students can maintain performance under aggressive compression/quantization.

- **Few-shot analogy ↔ limited training budget for new gate budgets**
  - Few-shot: maximize information from few labeled samples.
  - Your setting: maximize performance with strict resource limits (parameter count, artifact size, 1.10× runtime cap).
  - Representation quality is critical:
    - For compression, high-quality, structured latent spaces can improve entropy coding efficiency and hence val_bpb after zlib.
    - Distilled, compression-robust features could reduce entropy (more predictable, lower Kolmogorov complexity from the coder’s perspective) and thus lower bits per byte while preserving task performance.

**Implications for the hypothesis**

- RS-SSKD supports the idea that:
  - Carefully designing training-time branches and distillation strategies yields markedly better representations under constraints.
  - Applying this to QAT:
    - A staged QAT process that treats the float model as a teacher and the int8+zlib pipeline as the student is likely to outperform naive float-only training when evaluated *after* roundtrip.
  - This suggests that **roundtrip-aware self-distillation** is a promising ingredient in your lane_3 design.


---

## Cluster 3 – Model Class Choice vs. Classical Baselines Under Fixed Feature Budget

**Core idea from hong2020house**

- Compare:
  - OLS hedonic model vs. Random Forest.
- Same feature set, same data; different model classes.
- Results:
  - RF reduces average percentage deviation from ~20% (OLS) to ~5.5%.
  - RF substantially increases the probability of predictions within ±5% of actual prices.

**Conceptual transfer to QAT and gate budgets**

- **Same feature / gate budget, different utilization**
  - In Hong et al., both models consume the same input signals; RF simply uses capacity better.
  - For Parameter Golf:
    - Under the same “gate budget” (e.g., fixed parameter count, FLOPs, artifact size), you can still significantly change how capacity is used:
      - Float-only training optimized only for float inference.
      - Staged QAT + roundtrip-aware training optimized explicitly for int8+zlib deployment.

- **Nonlinear vs. linear analogy ↔ quantization-aware vs. oblivious training**
  - OLS ≈ linearly constrained estimator.
  - RF ≈ flexible, nonlinear model adapting to data idiosyncrasies.
  - Similarly:
    - Float-only training is “oblivious” to downstream quantization and compression.
    - Roundtrip-aware QAT acts as a more *specialized* estimator, explicitly modeling distribution shifts and distortions caused by int8+zlib.

**Implications for the hypothesis**

- The Hong et al. pattern is strong: *within the same resource envelope,* you can achieve order-of-magnitude error reduction by picking a model better suited to the data and downstream constraints.
- By analogy:
  - You should expect **non-trivial improvements in post-roundtrip val_bpb** once you treat quantization and compression as part of the model design, not an afterthought.
  - The constraint “artifact limit 16MB” parallels “same features; cannot add new data” — yet better learning strategy can change outcomes drastically.


---

## Gap 1 – Lack of Explicit End-to-End Quantization + Compression Training

**Observed across clusters**

- zhang2020training and zhang2021rssskd:
  - Focus on feature robustness or representation quality.
  - Do *not* explicitly integrate a *real* compression codec (e.g., zlib) into training.
- hong2020house:
  - No notion of discretization or compression in the pipeline; solely about predictor choice.

**Gap relative to your topic**

- No work directly trains models with:
  - A full **int8 quantization + zlib** (or other lossless codec) in the loop.
  - End-to-end objectives like val_bpb *after* roundtrip.
- Likely reasons:
  - Zlib is non-differentiable and complex to backpropagate through.
  - Most ML practice treats quantization/compression as a post-hoc step.

**Opportunity**

- Develop *roundtrip-aware* training that:
  - Integrates quantization simulation and approximate compression-sensitive objectives (e.g., entropy, code length proxy).
  - Uses straight-through estimators or surrogate losses for non-differentiable operations.


---

## Gap 2 – Absence of Formal Runtime / Gate-Budget–Aware Training Schedules

**Observed across clusters**

- zhang2020training:
  - Claims no inference overhead, but training-time compute increase is not carefully quantified.
- zhang2021rssskd:
  - Training time vs. baselines is discussed, but not framed as a strict operational gate (e.g., <1.10× runtime).
- hong2020house:
  - No runtime/memory budget tradeoff; only predictive accuracy is considered.

**Gap relative to your topic**

- Your quick-gate: **runtime ≤ 1.10× baseline** and artifact limit of **16MB**.
- The literature:
  - Provides qualitative or loose quantitative tracking of cost, but not a hard constraint-aware optimization regime.

**Opportunity**

- Design staged QAT schedules that:
  - Are explicitly bounded in training and inference-time compute.
  - Use profiling to enforce the 1.10× runtime quick-gate.
  - Treat *gate budget* and *artifact limit* as first-class constraints in the training plan.


---

## Gap 3 – No Systematic Comparison of Float-Only vs. Quantization-Aware Training Under Identical Capacity

**Observed across clusters**

- zhang2020training:
  - Compares vanilla training vs. enhanced training with additional auxiliary modules, but:
    - Both evaluated in the same float32 precision regime.
- zhang2021rssskd:
  - Compares with state of the art, but not vs. quantized deployments.
- hong2020house:
  - Compares OLS vs. RF, but not precision or deployment variants.

**Gap relative to your topic**

- You need:
  - A controlled comparison:
    - Same architecture, same parameter count, same inference precision (int8), same runtime budget.
    - Training regimen A: naive float-only → post-hoc quantization+zlib.
    - Training regimen B: staged QAT + roundtrip-aware alignment.
  - Outcome: difference in **post-roundtrip val_bpb** and accuracy/likelihood.

**Opportunity**

- Conduct rigorous A/B studies where:
  - Quantization is fixed at int8; zlib settings are fixed.
  - Only training strategy differs.
  - You measure:
    - val_bpb (main objective).
    - Standard metrics (perplexity, accuracy).
    - Runtime and artifact size to verify adherence to the gate budget.


---

## Gap 4 – Limited Use of Self-Distillation for Quantization Robustness

**Observed across clusters**

- RS-SSKD shows self-distillation improves robustness and representation quality.
- Yet:
  - No work applies this directly to quantization / compression robustness.
  - Teacher-student setups are usually float→float.

**Gap relative to your topic**

- You have a natural teacher-student divide:
  - Teacher: float32, unconstrained-precision model.
  - Student: quantization-aware, int8+zlib-simulated model.
- There is no existing blueprint in these cards for:
  - Self-distillation where the student is explicitly trained to match the teacher’s outputs under quantization+compression distortions.

**Opportunity**

- Implement **roundtrip-aware self-distillation**:
  - Teacher sees float path.
  - Student sees int8+zlib path.
  - Distillation loss encourages invariance to roundtrip artifacts.
  - Evaluate val_bpb and task performance jointly.


---

## Gap 5 – No Direct Optimization of Compression-Oriented Metrics (val_bpb)

**Observed across clusters**

- Metrics used:
  - Accuracy (scene classification).
  - Prediction error in percentage deviation (house pricing).
- None optimize:
  - Bits per symbol / bits per byte.
  - Explicit entropy or codelength under a given codec.

**Gap relative to your topic**

- Your main evaluation metric is **val_bpb** after int8+zlib.
- The literature:
  - Optimizes surrogate tasks (classification, regression).
  - Assumes standard cross-entropy tasks correlate with compression metrics (they often do, but indirectly).

**Opportunity**

- Integrate val_bpb or its proxy into optimization:
  - E.g., penalize high-entropy latent codes:
    - Encourage more compressible internal representations without harming predictive loss.
  - Or multi-objective training:
    - L = task_loss + λ · compression_loss (entropy proxy over activations or parameters to be serialized).


---

## Prioritized Opportunities

1. **Primary: End-to-End Roundtrip-Aware QAT with Self-Distillation (High Impact, Directly Tests Hypothesis)**  
   - Implement a staged training regimen:
     - Stage 1: float32 baseline training to achieve good task performance.
     - Stage 2: introduce fake quantization (int8 emulation) in weights and activations.
     - Stage 3: integrate an int8+zlib roundtrip simulator:
       - Quantize model or activations as they will be stored or transmitted.
       - Simulate zlib compression + decompression (or approximate its effect).
     - In Stage 2/3, add:
       - Teacher-student self-distillation: teacher = Stage 1 float model, student = quantized+roundtrip model.
       - Roundtrip consistency losses (feature/logit matching between clean and roundtrip paths).
   - Evaluate:
     - Post-roundtrip val_bpb vs. float-only training (with post-hoc quantization + zlib).
     - Confirm adherence to runtime ≤ 1.10× baseline and artifact ≤ 16MB.

2. **Secondary: Compression-Oriented Auxiliary Losses Under a Fixed Gate Budget**  
   - Design proxy compression losses:
     - Entropy regularization over output distributions or internal codes.
     - Sparsity or clustering in representations to promote compressibility.
   - Keep the deployed architecture/resources fixed; all extra logic is training-only.
   - Examine how these losses influence:
     - val_bpb after zlib.
     - Task metrics and stability.

3. **Tertiary: Controlled Capacity-Matched Studies of QAT vs. Float-Only Training**  
   - Systematically vary:
     - With or without staged QAT.
     - With or without roundtrip-aware branches.
   - Ensure:
     - Architecture, parameter count, int8 inference mode, and zlib configuration are identical in all runs.
   - Report:
     - val_bpb improvements as a function of training schedule and auxiliary losses.
     - Any trade-offs with predictive accuracy.

4. **Exploratory: CAM/Attention-Based Sensitivity Mapping to Guide Quantization**  
   - Inspired by RS-SSKD’s CAM-based focusing:
     - Identify layers/units most sensitive to quantization errors.
     - Possibly allocate slightly higher precision or milder quantization there, while being more aggressive elsewhere, but:
       - Maintain overall gate budget by redistributing precision.
   - Could also guide:
     - Where to attach auxiliary losses (attention to particularly fragile features).
   - Goal:
     - Improve robustness and val_bpb without increasing average runtime or model size.

If you’d like, I can next propose a concrete staged-training schedule (epochs, loss terms, and roundtrip simulation strategy) tailored to your exact model architecture and current float-only baseline.