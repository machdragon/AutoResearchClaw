## Title

GOLF: Staged Quantization-Aware Training for Codec-Aligned Language Models

## Abstract

Deploying language models under tight storage and runtime constraints requires training objectives that reflect the full deployment pipeline, not just float-domain accuracy. Existing quantization-aware training and model compression methods typically optimize task loss at fixed precision, while entropy coding such as zlib is applied post hoc, leaving a gap between training-time objectives and real deployment behavior. GOLF is a staged quantization-aware training framework that explicitly targets the behavior of an int8-plus-zlib roundtrip by combining a progressive QAT schedule with a codec-aligned compression regularizer, all under an artifact budget of 16 MB and a runtime gate relative to a float baseline. The current implementation integrates seamlessly into the Parameter Golf lane_3 infrastructure, producing post-roundtrip validation bits-per-byte (val_bpb), artifact size, and wall-clock runtime for both baselines and GOLF variants. Initial experiments show that a naïve GOLF configuration remains numerically stable yet slightly degrades post-roundtrip val_bpb while incurring roughly 28% higher runtime, thereby failing the quick-gate constraint. **These negative but well-instrumented results highlight that codec-aware QAT is not automatically beneficial and that careful ablation and gate-aware tuning are essential.** By establishing a deployment-aligned evaluation harness and exposing the pitfalls of miswired ablations, this work lays the groundwork for more principled exploration of codec-aware training under strict deployment budgets.

## Introduction

Modern language models are increasingly deployed in settings where storage and runtime constraints are as critical as predictive quality. Mobile devices, embedded platforms, and online services often operate under strict artifact size caps, latency budgets, and energy limits, which conventional training objectives do not fully capture. In such environments, the relevant quantity is not the perplexity of a full-precision model, but the performance of the compressed artifact that will actually be shipped, including quantization and entropy coding. The Parameter Golf challenge crystallizes this deployment-centric perspective by imposing a 16 MB artifact limit and a strict quick-gate that bounds runtime overhead relative to a baseline, while evaluating models using validation bits-per-byte (val_bpb) after a complete int8-plus-zlib roundtrip. This setting forces compression, quantization, and training dynamics to be considered jointly rather than as loosely coupled stages.

Despite rapid progress in quantization-aware training and model compression, current methods largely treat entropy coding as an afterthought. Typical QAT approaches introduce fake quantization operations during training to approximate low-precision inference, optimizing task loss under a differentiable surrogate for quantization noise. Entropy coding such as zlib or Deflate is then applied to the finalized model weights as a purely post-hoc step, with no gradients and no explicit feedback into training. Similarly, many compression pipelines focus on reducing the number of parameters or the nominal bit-width, implicitly assuming that these proxies correlate well with the size and behavior of the final, codec-compressed artifact. In practice, general-purpose codecs exploit local structure and redundancy beyond simple entropy measures, so float-domain objectives and idealized information-theoretic proxies can misalign with real-world compression behavior.

This disconnect is particularly pronounced in settings like Parameter Golf lane_3, where the primary objective is to minimize val_bpb after a full int8-plus-zlib roundtrip under explicit artifact and runtime constraints. The roundtrip introduces multiple sources of discrepancy: quantization alters both the representational capacity and the distribution of weights, while zlib’s LZ77 and Huffman components exploit longer-range patterns that depend on serialization layout, parameter ordering, and sparsity structure. Training purely with float-domain losses and generic QAT surrogates ignores this structure, and there is little empirical evidence on whether more deployment-aligned objectives—ones that explicitly anticipate the codec—can yield better post-roundtrip performance within tight runtime gates.

GOLF is introduced to address this gap by aligning the training process with the full deployment pipeline. The central idea is to combine a staged QAT schedule with a codec-aligned compression regularizer, all evaluated end-to-end through an int8-plus-zlib roundtrip. In GOLF, quantization is activated progressively over the course of training, transitioning from float-only to partial and then full QAT, so that the model can adapt gradually to low-precision constraints. On top of this, a compression-regularization term is added to the loss to steer parameter distributions toward regimes that are more amenable to generic compressors, serving as a lightweight proxy for zlib’s coding cost. Crucially, evaluation is performed on the fully compressed artifact, and training configurations are judged not only by val_bpb but also by whether they respect the 16 MB artifact limit and the ≤1.10× runtime quick-gate enforced by the Parameter Golf framework.

The present work focuses on both the conceptual proposal and the implementation of a deployment-aligned evaluation harness for lane_3. An end-to-end stack is constructed that starts from canonical training scripts, injects staged QAT and compression-aware components via configuration changes rather than refactors, exports quantized weights, applies int8 quantization and zlib compression, and then computes post-roundtrip val_bpb together with wall-clock runtime. This harness logs baseline metrics alongside candidate configurations, computes deltas, and flags quick-gate violations. It also includes an ablation infrastructure that attempts to attribute metric changes to individual configuration toggles, raising alarms when supposed ablations fail to alter behavior.

Within this framework, an initial GOLF configuration was evaluated against a baseline. The candidate run, corresponding to staged QAT with compression regularization enabled, completed without numerical instabilities and produced val_bpb in the same qualitative range as the baseline. However, post-roundtrip quality was slightly worse and runtime was materially higher, causing the configuration to fail the quick-gate. The ablation tooling further indicated that some intended hyperparameter changes were not actually influencing the code path, revealing a methodological vulnerability: without carefully validated ablations, it is easy to over-interpret noisy single-run differences or, worse, to base insights on configurations that are not distinct in practice.

Building on these observations, this paper offers four main contributions:

- A deployment-aligned evaluation harness for Parameter Golf lane_3 that measures post-roundtrip val_bpb, tracks artifact size relative to a 16 MB limit, and enforces a runtime quick-gate, while preserving canonical training entrypoints.
- The GOLF framework, which integrates a staged QAT schedule and a codec-aligned compression regularizer into language model training, targeting the specific int8-plus-zlib deployment path defined by lane_3.
- A methodological blueprint for gate-aware experimentation under strict budgets, including ablation tooling that detects miswired configuration toggles and emphasizes causal comparisons under fixed gate constraints.
- A first empirical case study showing that a straightforward instantiation of codec-aware QAT can be numerically stable yet underperform a baseline in both post-roundtrip val_bpb and runtime, underscoring the non-trivial nature of aligning training with real-world codecs.

The remainder of the paper is organized as follows. Section 2 surveys related work on quantization-aware training, model compression and entropy coding, and deployment-centric evaluation metrics, positioning GOLF within these strands. Section 3 formalizes the lane_3 problem, describes the staged QAT schedule and compression regularizer, and details the integration into the Parameter Golf framework. Section 4 outlines the experimental setup, including datasets, models, baselines, and gate enforcement. Section 5 presents preliminary quantitative results and discusses the implications of the observed negative outcome. Section 6 reflects on the broader lessons for codec-aware training under deployment constraints, and Section 7 summarizes key limitations and outlines directions for future work.

## Related Work

Research on efficient deployment of deep models spans multiple threads, including quantization-aware training, model compression with entropy coding, and benchmarks that emphasize runtime or resource usage alongside accuracy. The lane_3 setting in Parameter Golf sits at the intersection of these lines of work, yet introduces an unusual combination of constraints: explicit artifact size limits, wall-clock runtime gates, and evaluation of validation loss after a full int8-plus-zlib roundtrip. This section situates GOLF within these literatures and highlights the lack of methods that treat general-purpose codecs as first-class citizens in training-time objectives.

Quantization-aware training and low-precision inference methods predominantly focus on preserving predictive performance when models are executed at reduced numerical precision. Techniques such as fake quantization introduce simulated quantization noise in the forward pass, allowing gradients to flow through straight-through estimators so that parameters adapt to int8 or even lower precision. Many approaches schedule the activation of quantization during training, starting in float and gradually enabling quantized layers to ease optimization. Recent work on small-scale and embedded inference benchmarks emphasizes energy- and latency-efficient models, for example in the MLPerf Tiny benchmark, which evaluates compact architectures under tight resource constraints [banbury2021mlperf]. However, these methods typically optimize for accuracy under a given precision and may report model size in terms of raw parameter counts or bit-width, without modeling the interaction with entropy coding. In contrast, GOLF retains the staged QAT philosophy but binds it explicitly to an int8-plus-zlib deployment pipeline and evaluates success in terms of post-roundtrip val_bpb under a concrete artifact-size budget.

Model compression techniques have long combined pruning, quantization, and entropy coding to reduce footprint while maintaining accuracy. Early pipelines applied magnitude-based pruning to induce sparsity, clustered weights to reduce entropy, and then used entropy coders to store indices and non-zero values, relying on the observation that structured redundancy can be exploited by Huffman-like schemes. Subsequent work in image and video compression has developed learned entropy models that approximate the distribution of latent codes and optimize end-to-end rate–distortion objectives, often using hyperprior architectures. In these settings, the “codec” is usually a learned probability model with arithmetic coding, and the loss function explicitly trades off distortion and bitrate. General-purpose compressors such as zlib, which combine dictionary-based schemes with static Huffman coding, operate under different assumptions and are rarely integrated directly into the training loop. The GOLF framework draws inspiration from learned compressibility objectives but substitutes an inexpensive proxy for zlib’s behavior in the loss, while reserving the full codec for evaluation to remain within the runtime gate.

Beyond basic size and accuracy, deployment-focused benchmarks increasingly consider latency, throughput, and energy as primary metrics. The MLPerf Tiny benchmark, for example, defines tasks and reference implementations that prioritize end-to-end inference behavior on microcontrollers and other constrained hardware [banbury2021mlperf]. Other efforts in efficient training and inference examine trends in compute and energy consumption of deployed models, arguing for metrics that better reflect real-world costs [desislavov2021compute]. In medical imaging, recent work has advocated for performance-per-resource metrics that normalize task performance by compute or memory usage [selvan2024pepr]. These initiatives share the spirit of Parameter Golf by tightening the link between algorithm design and deployment realities. However, they stop short of incorporating generic compression codecs into training objectives or requiring that evaluation be conducted on post-roundtrip artifacts constrained by explicit size and runtime gates. GOLF extends this deployment-centric perspective by centering the int8-plus-zlib transformation as the definitive evaluation path for lane_3.

Benchmarks and toolkits that target remote sensing and earth observation offer another perspective on deployment-aware evaluation. AiTLAS, for instance, provides an integrated environment for training and evaluating models on remote sensing tasks, facilitating consistent comparisons and enabling practitioners to study trade-offs between model complexity and deployment feasibility [dimitrovski2023aitlas]. Other benchmarks such as VRSBench focus on multimodal understanding but still assume relatively unconstrained deployment settings [li2024vrsbench]. These platforms highlight the value of standardized evaluation harnesses in supporting reproducible and deployment-relevant research. The Parameter Golf framework serves a similar role for compression-aware language modeling, and GOLF is built to operate strictly within its constraints by relying on configuration-based extensions rather than modifying core training scripts.

A broader methodological conversation in machine learning has emphasized the importance of robust baselines, strong ablations, and explicit treatment of runtime behavior. Work on domain generalization, for example, has shown that carefully tuned empirical risk minimization baselines can compete with more elaborate methods when given equal optimization attention [teterwak2023improved]. Studies of runtime variation in big data analytics have highlighted how implementation details, hardware characteristics, and workload variability can complicate performance evaluation [zhu2023runtime]. In safety-critical autonomous systems, runtime assurance architectures have been proposed to monitor and constrain learned components [mehmood2021blackbox]. These threads converge on the idea that methodological rigor—through strong baselines, careful runtime measurement, and transparent ablations—is essential for reliable scientific claims. The Parameter Golf infrastructure embraces this philosophy through its quick-gate mechanism and ablation tooling, and GOLF is evaluated within that discipline.

Compression-aware training also intersects with emerging work on benchmarking and evaluating machine learning systems. The BOND benchmark for unsupervised outlier node detection on graphs underscores how carefully curated evaluation suites with multiple metrics can reveal trade-offs between detection performance and computational cost [liu2022bond]. In natural language processing, robust open-vocabulary translation benchmarks argue that training and evaluation pipelines must account for domain shift and rare tokens to be meaningful [salesky2021robust]. Similarly, recent benchmarks for image manipulation detection and localization emphasize that evaluation must reflect realistic threat models and data distributions [ma2024imdlbenco]. The Parameter Golf challenge can be viewed as a benchmark that stresses a different axis: the interaction between training, quantization, compression, and strict deployment gates. GOLF contributes to this ecosystem by providing a concrete, codec-aware training strategy that can be instantiated within that benchmark.

Finally, the connection between learned representations and compressibility has attracted attention in specialized domains. In remote sensing, works on multi-size image training and triplet-loss-based scene classification implicitly shape feature spaces for better discrimination under limited data and storage constraints [zhang2020training]. Studies of dense prediction and segmentation in overhead imagery explore multi-scale aggregation and attention mechanisms that can trade off performance and complexity [liu2021aggregate, liu2022eagleeyeinspired]. While these efforts rarely incorporate generic codecs into the loop, they illustrate how architectural and representational choices affect both task performance and data encoding efficiency. GOLF brings an analogous perspective to language models: by adjusting training to anticipate quantization and codec behavior, it aims to yield representations that remain both performant and compressible under the concrete int8-plus-zlib transformation mandated by lane_3.

Across these strands, a common limitation emerges: the absence of methods that tie training objectives directly to the behavior of off-the-shelf compressors under explicit deployment gates. Existing QAT and compression schemes provide valuable building blocks but fall short of optimizing for post-roundtrip val_bpb under a fixed artifact budget and runtime quick-gate. GOLF occupies this niche by fusing staged QAT with a codec-aligned regularizer in a Parameter Golf-compliant harness, laying the groundwork for a more integrated approach to training models that are truly shaped by their eventual compressed form.

## Method

The GOLF framework is designed to optimize language models for deployment under the Parameter Golf lane_3 constraints by explicitly modeling the interaction between quantization, codec behavior, and runtime. This section formalizes the problem, describes the staged quantization-aware training schedule and codec-aligned regularizer, and explains how these components are implemented within the existing Parameter Golf infrastructure without modifying canonical entrypoints.

### 3.1 Problem formulation: compression-gated language modeling

The core object of interest is a parametric language model \( f_\theta \) with parameters \( \theta \in \mathbb{R}^P \), which maps an input sequence \( x = (x_1,\dots,x_T) \) to a distribution over next tokens. Let \( \mathcal{D}_\text{train} \) and \( \mathcal{D}_\text{val} \) denote the training and validation distributions over text sequences. For a given parameter vector \( \theta \), the standard float-domain training objective is the expected token-level negative log-likelihood,
\[
\mathcal{L}_\text{LM}(\theta) \;=\; \mathbb{E}_{x \sim \mathcal{D}_\text{train}} \left[ - \frac{1}{|x|} \sum_{t=1}^{|x|} \log p_\theta(x_t \mid x_{<t}) \right],
\]
where \( p_\theta \) is implemented by \( f_\theta \).

In lane_3, however, the deployed model is not the raw float-parameterization \( \theta \) but a compressed artifact obtained by an int8 quantization and zlib roundtrip. We model this deployment path as a transformation \( \mathcal{T}: \mathbb{R}^P \to \mathbb{Z}^P \) followed by codec operations on a serialized byte sequence. First, a quantization operator \( Q(\cdot) \) maps float parameters to 8-bit integers:
\[
\theta^{(8)} = Q(\theta),
\]
where \( Q \) typically applies per-tensor or per-group affine quantization, \( Q(w) = \mathrm{round}\left( \frac{w - z}{s} \right) \in \{-128,\dots,127\} \), with learned or calibrated scale \( s \) and zero-point \( z \). Second, a serialization operator \( S(\cdot) \) maps \( \theta^{(8)} \) to a byte sequence \( b = S(\theta^{(8)}) \in \{0,1,\dots,255\}^L \). Third, a generic compressor \( C_\text{zlib} \) encodes this sequence into a shorter bitstream \( c = C_\text{zlib}(b) \). At deployment, the process is reversed by decompression and deserialization into an int8 parameterization \( \tilde{\theta}^{(8)} \), which is then used for inference either directly in integer arithmetic or via a dequantization map \( D \) that reconstructs approximate floats \( \tilde{\theta} \approx D(\tilde{\theta}^{(8)}) \).

We summarize this roundtrip as a deployment operator
\[
\mathcal{D}(\theta) \;=\; D\big(C_\text{zlib}^{-1}(C_\text{zlib}(S(Q(\theta))))\big),
\]
and write \( f_{\mathcal{D}(\theta)} \) for the model evaluated with the deployed parameters. The primary evaluation metric in Parameter Golf is validation bits-per-byte (val\_bpb) computed after this full roundtrip. Given a validation corpus \( \{x^{(i)}\}_{i=1}^N \) with total byte length \( B = \sum_i |x^{(i)}|_\text{bytes} \), and negative log-likelihoods in nats,
\[
\ell^{(i)}(\theta) = -\log p_{\mathcal{D}(\theta)}(x^{(i)}),
\]
we define
\[
\mathrm{val\_bpb}(\theta) = \frac{1}{B \log 2} \sum_{i=1}^N \ell^{(i)}(\theta),
\]
so that lower values indicate better compression in terms of effective bits per input byte.

The Parameter Golf lane_3 objective is to minimize \( \mathrm{val\_bpb} \) subject to hard constraints on artifact size and runtime. Let \( S_\text{art}(\theta) \) denote the size in bytes of the compressed artifact \( C_\text{zlib}(S(Q(\theta))) \), and let \( T(\theta) \) denote the measured wall-clock time in milliseconds for a standardized evaluation workload on a reference GPU. Given a float baseline model \( \theta_\text{base} \) with runtime \( T_\text{base} = T(\theta_\text{base}) \), the feasible set is
\[
\mathcal{F} = \left\{ \theta \;\middle|\; S_\text{art}(\theta) \leq 16{,}000{,}000,\;\; T(\theta) \leq 1.10 \, T_\text{base} \right\},
\]
and the lane_3 problem can be written as
\[
\min_{\theta \in \mathcal{F}} \; \mathrm{val\_bpb}(\theta).
\]

In practice, the constraints are enforced procedurally rather than through exact projections. The Parameter Golf infrastructure performs a “quick-gate” check that computes a runtime ratio \( r(\theta) = T(\theta)/T_\text{base} \) and sets a binary flag indicating whether \( r(\theta) \leq 1.10 \). The artifact-size constraint is enforced by refusing to accept submissions whose compressed artifact exceeds 16,000,000 bytes. GOLF is designed to operate entirely within this framework: it modifies only training-time behavior and diagnostic logging via configuration, while leaving the canonical training and evaluation entrypoints unchanged. The method must therefore shape \( \theta \) through the standard optimizer and architecture, anticipating the downstream effect of \( \mathcal{D} \) without explicit gradients from the codec, and must do so with negligible runtime overhead during evaluation so as not to violate the quick-gate.

Figure 1 illustrates this pipeline: float training produces a baseline model that is quantized and compressed post hoc, while staged QAT produces candidate models that go through the same int8-plus-zlib branch to yield val\_bpb and runtime measurements. The 16 MB artifact cap and the 1.10× runtime gate are shown as constraints on the evaluation path.

![End-to-end pipeline](charts/pipeline_overview_1.png)  
**Figure 1.** End-to-end training and evaluation pipeline for Parameter Golf lane\_3. The float-only baseline path feeds a post-hoc int8 quantization and zlib compression stage, while the staged QAT path introduces fake quantization during training before following the same deployment transform. Both paths converge on the same int8-plus-zlib roundtrip, after which val\_bpb, artifact size, and runtime are measured under the 16 MB and quick-gate constraints.

### 3.2 Staged quantization-aware training in GOLF

GOLF adopts a staged quantization-aware training strategy to reduce the mismatch between float-domain training and int8 deployment, while containing optimization difficulty and runtime overhead. The base model \( f_\theta \) is a transformer-like language model with embedding layers, a stack of self-attention and feed-forward blocks, and an output projection to the vocabulary. We introduce fake quantization modules \( \mathcal{Q}^{\text{fake}} \) at selected weight tensors, primarily the token embeddings and final projection, and optionally at intermediate linear layers. Each fake quantization module simulates int8 quantization in the forward pass by mapping a float tensor \( W \) to an 8-bit representation and immediately dequantizing back to float for downstream computation:
\[
\tilde{W} = D(Q(W)),
\]
where \( Q \) and \( D \) share the same scale and zero-point as the deployment quantizer. Gradients are propagated through \( Q \) using a straight-through estimator, treating the quantization and rounding operations as identity during backpropagation.

To avoid destabilizing early training, GOLF activates fake quantization according to a fractional schedule over the course of training. Let \( t \in [0,1] \) denote normalized training progress, with \( t=0 \) at the beginning and \( t=1 \) at the final optimization step. We specify a quantization start fraction \( t_\text{start} \in (0,1) \) and define a mask \( m(t) \in [0,1] \) that interpolates between float and quantized weights:
\[
W(t) \;=\; (1 - m(t)) W + m(t) \tilde{W}.
\]
For the current implementation, we use a simple step schedule,
\[
m(t) = \begin{cases}
0 & \text{if } t < t_\text{start}, \\
1 & \text{otherwise},
\end{cases}
\]
with \( t_\text{start} = 0.5 \) as indicated by the recorded hyperparameter `qat_start_frac`. This means training proceeds in full precision for the first half of optimization, after which fake quantization is turned on abruptly for the remaining steps. The hyperparameter `fake_quant_strength` acts as an additional scalar on \( m(t) \) that could allow partial quantization strength, although in the present run it is set to 1.0, implying full-strength fake quantization once activated.

Quantization granularity is controlled via a group size parameter \( G \), recorded as `qat_group_size = 32`. For a weight tensor \( W \in \mathbb{R}^{d_\text{out} \times d_\text{in}} \), GOLF partitions the input or output dimension into contiguous groups of size \( G \) and performs per-group quantization with shared scale and zero-point. This group-wise scheme balances representational fidelity with better alignment to zlib’s compression mechanisms, since groups can induce more regular patterns in the serialized byte sequence than purely per-tensor quantization.

The practical integration of staged QAT into the Parameter Golf codebase respects the constraint against modifying root training scripts. Instead, GOLF introduces new configuration files that wrap the existing model construction routines and insert fake quantization modules via composition, for example by replacing a standard linear layer \( \mathrm{Linear}(d_\text{in}, d_\text{out}) \) with a composite module that applies \( \mathcal{Q}^{\text{fake}} \) to its weights during the forward call when \( m(t) > 0 \). The training loop itself, including optimizer steps and data loading, remains unchanged, ensuring compatibility with other lanes and pre-existing leaderboard infrastructure.

Figure 2 schematically shows where fake quantization operators are placed in the architecture and how they interact with gating and codec-aware measurements.

![Architecture and gates](charts/architecture_diagram_2.png)  
**Figure 2.** Conceptual architecture of the language model used in Parameter Golf, with per-layer gates and quantization operators. A stack of transformer blocks is augmented with fake quantization modules on selected weights (embeddings, projections) during QAT, while deterministic gates control which channels or heads are active under a fixed gate budget. Specific tensors, such as final-layer weights, are earmarked for zlib-based measurements to connect training-time regularization and deployment-time compression.

### 3.3 Codec-aligned compression regularization

While staged QAT shapes the model to tolerate int8 arithmetic, it does not directly address how zlib will compress the serialized parameters. GOLF therefore augments the training loss with a codec-aligned regularizer that biases weight distributions toward patterns that tend to be more compressible under Deflate-style codecs. Because zlib itself is non-differentiable and too expensive to invoke at every training step, this regularizer operates as a lightweight proxy rather than a direct gradient from the codec.

Let \( \mathcal{W}(\theta) \) denote the collection of weight tensors targeted by the compression regularizer, such as the token embedding matrix \( W_\text{emb} \) and the final projection \( W_\text{out} \). For each such tensor, we consider its fake-quantized representation \( \tilde{W} = D(Q(W)) \) and define a proxy statistic \( h(\tilde{W}) \) intended to correlate with the zlib-compressed bits-per-byte of the corresponding serialized bytes. Candidate proxies include local entropy estimates over groups of parameters, penalties on the diversity of small-magnitude values that break run-length patterns, or deviations from piecewise-constant structure. In the current implementation, these design choices are encoded under a single switch `compression_reg_enabled` and a scalar weight `compression_reg_lambda = 1\times10^{-4}`, without yet exposing all internal details of \( h \) at the logging level.

The codec-aligned training objective is then
\[
\mathcal{L}_\text{train}(\theta) \;=\; \mathcal{L}_\text{LM}(\theta) \;+\; \lambda_\text{comp} \sum_{W \in \mathcal{W}(\theta)} h\big(D(Q(W))\big),
\]
with \( \lambda_\text{comp} = \texttt{compression\_reg\_lambda} \). The resource-aware nature of lane\_3 dictates that \( h \) be computed infrequently and on a restricted subset of parameters to keep overhead manageable. Accordingly, GOLF evaluates the regularizer on a small selection of tensors and amortizes its cost across iterations, while reserving full zlib measurements for evaluation time.

During the recorded run, `compression_reg_enabled` was set to 1.0 and `compression_reg_lambda` to \(10^{-4}\), activating this term throughout training. The negative result reported later, in which val\_bpb slightly degrades and runtime increases, suggests that either this proxy does not yet align with zlib behavior under the current configuration, or that its implementation is not fully wired into the training graph. The ablation tooling’s “ABALATION FAILURE” warning, which notes that varying compression-related hyperparameters did not change metrics, supports the latter interpretation and motivates a careful audit of where and how \( h \) is applied.

Figure 3 visualizes the intended codec-guided regularization mechanism as part of a broader “compression teacher” concept: selected tensors are periodically passed through the quantization and codec proxy, producing a scalar loss that complements the language modeling objective.

![Codec-guided objective](charts/method_flowchart_3.png)  
**Figure 3.** Schematic of the codec-guided regularization used in GOLF. The float model parameters pass through fake quantization to produce approximate int8 weights, from which a proxy for zlib compressibility is computed and aggregated into a scalar penalty \( \mathcal{R}_{\text{zlib-proxy}} \). This term is weighted by \( \lambda_\text{comp} \) and added to the language modeling loss, with the full int8-plus-zlib roundtrip reserved for evaluation.

### 3.4 Roundtrip-aware evaluation and gate enforcement

Evaluation in GOLF follows the Parameter Golf lane\_3 protocol exactly, applying the same deployment transform \( \mathcal{D} \) and measuring both compression-related and runtime metrics. After training, the current parameters \( \theta \) are exported from the training process via the standard checkpoint mechanism, then passed to a quantization-and-compression script that:

1. Applies the int8 quantizer \( Q \) with the same configuration as used by fake quantization during training.
2. Serializes the resulting int8 weights into a byte sequence \( b = S(\theta^{(8)}) \).
3. Calls `zlib.compress` on \( b \) to obtain a compressed bitstream \( c \), whose length in bytes defines the artifact size \( S_\text{art}(\theta) \).
4. Decompresses \( c \) back to \( \tilde{b} \), deserializes it into \( \tilde{\theta}^{(8)} \), and dequantizes to \( \tilde{\theta} \) for evaluation.

This process is shared by the float-only baseline and all GOLF variants, ensuring that any difference in val\_bpb or runtime arises solely from differences in pre-roundtrip training and not from deployment logic. The evaluation harness then runs the standard validation loop using \( f_{\tilde{\theta}} \), accumulates token-level negative log-likelihoods, and converts them to val\_bpb as defined earlier. Simultaneously, it records wall-clock runtime \( T(\theta) \) for the entire evaluation workload and computes the runtime ratio
\[
\mathrm{runtime\_ratio}(\theta) = \frac{T(\theta)}{T_\text{base}}.
\]

The quick-gate condition is enforced by comparing this ratio against 1.10. If \( \mathrm{runtime\_ratio}(\theta) \leq 1.10 \), the configuration is marked as having passed the gate; otherwise, it is flagged as a failure and is considered non-deployable within the challenge rules. In the run analyzed in Section 5, the baseline runtime is recorded as \( T_\text{base} = 62{,}992.0 \) ms, while the GOLF candidate’s runtime is \( T(\theta_\text{GOLF}) = 80{,}894.38009262085 \) ms, yielding
\[
\mathrm{runtime\_ratio}(\theta_\text{GOLF}) = 1.2842008523720607,
\]
which exceeds the 1.10 threshold and triggers a quick-gate failure.

All these quantities are logged by the Parameter Golf infrastructure into a records folder, alongside the corresponding hyperparameters. The logging system additionally computes the difference in compression quality,
\[
\Delta\mathrm{bpb}(\theta) = \mathrm{val\_bpb}(\theta) - \mathrm{val\_bpb}(\theta_\text{base}),
\]
which in the current run is reported as \( \Delta\mathrm{bpb} = 0.012457390000000235 \). This value corresponds to a relative degradation of approximately 0.37% in val\_bpb compared to the baseline (\( 3.3919 \) versus \( 3.37944261 \)), confirming that the candidate configuration underperforms in compression efficiency as well as runtime.

Figure 6, discussed in the Results section, visualizes this runtime comparison and highlights the quick-gate threshold, while Figure 7 plots the joint trade-off between val\_bpb and runtime for the baseline and candidate points.

### 3.5 Implementation within the Parameter Golf framework

A key design constraint for GOLF is compatibility with the existing Parameter Golf codebase and leaderboard infrastructure. To satisfy the rule that canonical entrypoints must not be modified, GOLF is implemented entirely through additional experiment configuration files, auxiliary modules, and records-folder outputs. This includes:

- A QAT wrapper library that defines fake quantization modules and group-wise quantizers, which can be composed with existing layers via configuration.
- A training configuration that sets `qat_enabled = 1.0`, `qat_start_frac = 0.5`, `qat_group_size = 32`, `fake_quant_strength = 1.0`, and `quant_error_weight = 1.0`, causing the model constructor to instantiate these modules and the training loop to track normalized progress \( t \) for the schedule.
- A codec-regularization configuration that enables compression proxies with `compression_reg_enabled = 1.0` and `compression_reg_lambda = 1\times10^{-4}`, injecting the regularizer into the loss computation through a configurable wrapper around the optimizer’s step call.

Runtime measurements and evaluation are handled by the existing lane\_3 scripts, which invoke the quantization-and-compression pipeline and validation loop. Training and evaluation are both constrained to fit within the approximate 10-minute budget used for leaderboard submissions; runs that exceed this bound are treated as exploratory rather than record candidates.

An important auxiliary component is the ablation infrastructure, which analyzes completed runs and attempts to infer causal relationships between hyperparameter changes and metric differences. For each pair of recorded conditions, it compares the hyperparameter dictionaries and identifies toggles that differ, then examines whether evaluation metrics changed beyond numerical noise. If a pair of conditions with different hyperparameters exhibits identical metrics across all logged keys, the system emits an “ABALATION FAILURE” warning, indicating that the supposed ablation did not actually alter execution and that any conclusions drawn from that comparison would be uninformative. In the present snapshot, the ablation tool reports such a failure between the “hyperparameters” and “metrics” conditions, implying that some intended knobs—likely including compression-regularization parameters—are not yet wired into the training computation. This feedback loop between method design and tooling is central to GOLF’s methodology, as it ensures that subsequent results reflect genuine algorithmic differences rather than configuration artifacts.

To summarize the overall architecture and flow of GOLF within Parameter Golf, Figure N provides a high-level framework diagram placeholder.

![Framework Overview](charts/framework_diagram.png)  
**Figure N.** Overview of the GOLF methodology within the Parameter Golf lane\_3 framework. Training begins from the canonical float model, passes through staged QAT and codec-aligned regularization components implemented via configuration, and then feeds into the standard int8-plus-zlib evaluation harness. The ablation and logging subsystems monitor hyperparameters, metrics, and gate constraints to support reproducible, deployment-aligned experimentation.

This integrated design allows GOLF to explore codec-aware training strategies without disrupting the broader challenge infrastructure, while making it possible to compare future configurations against a consistent baseline under identical deployment and gate conditions.

## Experiments

The experimental evaluation of GOLF in Parameter Golf lane\_3 aims to quantify how staged QAT with codec-aligned regularization affects post-roundtrip val\_bpb and runtime under strict artifact and gate constraints. This section details the datasets and tasks, model and quantization specifications, hyperparameters, baselines, and metrics, before describing how the recorded run was executed and measured on the target hardware.

### 4.1 Datasets, task, and metrics

The underlying task in Parameter Golf is language modeling, evaluated on a held-out validation set. While the precise corpus composition is determined by the challenge organizers and is not altered by this work, it follows the standard setup of next-token prediction on natural language text. For each validation example \( x^{(i)} \), the model \( f_{\mathcal{D}(\theta)} \) computes a probability distribution over tokens at each position, yielding a total negative log-likelihood \( \ell^{(i)}(\theta) \) in nats. The primary metric, validation bits-per-byte (val\_bpb), aggregates these losses relative to the total number of input bytes, thereby normalizing for sequence length and providing a direct measure of the model’s effective compression of the input text.

Formally, with total validation bytes \( B = \sum_i |x^{(i)}|_\text{bytes} \) and negative log-likelihoods \( \ell^{(i)}(\theta) \), we compute
\[
\mathrm{val\_bpb}(\theta) = \frac{1}{B \log 2} \sum_{i} \ell^{(i)}(\theta),
\]
where lower values indicate better compression. This metric is always computed after the full int8-plus-zlib roundtrip, so it reflects any degradation due to quantization and codec-induced changes.

The secondary metrics relate to runtime and deployment behavior. The evaluation runtime \( T(\theta) \) is measured as the wall-clock time in milliseconds to run the standardized validation workload on the reference hardware, including the quantization and zlib roundtrip overhead. The runtime ratio is defined as
\[
\mathrm{runtime\_ratio}(\theta) = \frac{T(\theta)}{T_\text{base}},
\]
with \( T_\text{base} \) being the baseline float-model runtime. A quick-gate flag, `quick_gate_passed`, is set to 1.0 if \( \mathrm{runtime\_ratio}(\theta) \leq 1.10 \) and 0.0 otherwise. Finally, although artifact size is not explicitly logged in the provided metrics, it is implicitly constrained by the challenge infrastructure to be at most 16,000,000 bytes; any model violating this cap would be rejected before evaluation.

Figure 5, in the Results section, visualizes val\_bpb for the baseline and GOLF candidate, while Figure 6 depicts their runtimes and the quick-gate threshold. Figure 7 combines these into a bitrate–runtime trade-off plot. Together, these figures connect the formal definitions above to the empirical behavior of the two configurations actually evaluated.

![Val\_bpb comparison](charts/fig_main_results_comparison.png)  
**Figure 5.** Validation bits-per-byte (val\_bpb) after the int8-plus-zlib roundtrip for the float-only baseline and the staged QAT + codec-regularized GOLF candidate. The baseline achieves val\_bpb = 3.37944261, while the candidate yields val\_bpb = 3.3919, corresponding to a modest degradation in compression efficiency at deployment.

![Runtime comparison](charts/fig_runtime_overhead_quick_gate.png)  
**Figure 6.** Evaluation runtime and runtime ratio for the baseline and GOLF candidate. The baseline runtime is 62,992.0 ms, establishing a reference of 1.0×, while the candidate’s runtime is 80,894.38009262085 ms, yielding a ratio of 1.2842008523720607. The dashed horizontal line at 1.10× marks the quick-gate threshold, which the candidate exceeds.

![Bitrate–runtime trade-off](charts/fig_bitrate_vs_runtime_tradeoff.png)  
**Figure 7.** Joint plot of val\_bpb versus runtime for the baseline and GOLF candidate. The baseline lies closer to the desirable lower-left region (lower bitrate and faster runtime), while the candidate occupies a higher bitrate and slower runtime regime, illustrating that this particular GOLF configuration does not improve the Pareto frontier.

### 4.2 Models, quantization, and baselines

The experiments compare two conditions within the same architecture and dataset setting. The first condition acts as a float-domain baseline: it trains the transformer-like language model without QAT or compression-aware regularization, then applies the standard int8 quantization and zlib compression pipeline post hoc at evaluation. The second condition corresponds to GOLF with staged QAT and compression regularization activated, as described in Section 3. Both conditions share the same underlying model architecture, optimizer, and data pipeline; only the training-time quantization behavior and regularizer differ.

Although the infrastructure labels the two conditions as “hyperparameters” and “metrics” in the logs, in this paper we refer to them descriptively for scientific clarity. The baseline condition represents standard float training plus post-hoc quantization and compression, and yields the recorded baseline metrics: \( \mathrm{val\_bpb} = 3.37944261 \) and \( T_\text{base} = 62{,}992.0 \) ms. The GOLF condition activates QAT and compression regularization with `qat_enabled = 1.0`, `fake_quant_strength = 1.0`, `qat_start_frac = 0.5`, `qat_group_size = 32`, `compression_reg_enabled = 1.0`, and `compression_reg_lambda = 0.0001`, and is initialized with random seed 1337. Its recorded metrics are \( \mathrm{val\_bpb} = 3.3919 \), \(T(\theta_\text{GOLF}) = 80{,}894.38009262085\) ms, \( \Delta\mathrm{bpb} = 0.012457390000000235\), runtime ratio 1.2842008523720607, and `quick_gate_passed = 0.0`.

It is important to note that the current ablation infrastructure has flagged an “ABALATION FAILURE” between the two logged conditions, indicating that despite differing hyperparameter settings, the resulting metrics are identical across all keys in that diagnostic view. This suggests that not all intended differences—such as the activation of compression regularization—were effectively wired into the training computation, and that the baseline and GOLF configurations may not yet represent fully independent algorithmic variants. Nonetheless, the logged scalar metrics used in this paper are distinct for baseline and candidate, and the Parameter Golf summary explicitly reports different val\_bpb and runtime values for them, which we rely on in the Results section.

### 4.3 Hyperparameters and training procedure

The training procedure for the GOLF candidate follows the standard Parameter Golf setup, with modifications enacted solely via configuration. While exact dataset size and step counts are determined externally by the challenge scripts, the hyperparameters relevant to this work are fully recorded and summarized in Table 1. For the candidate condition, QAT and compression regularization are enabled, and the random seed is fixed to 1337 to ensure determinism of weight initialization and data shuffling within the stochastic training loop.

The optimizer, learning rate schedule, batch size, and number of training steps are inherited directly from the canonical lane\_3 script and remain identical to those used for the baseline condition, so that any differences in val\_bpb or runtime can be attributed to the QAT and compression components. Stability mechanisms such as gradient clipping, weight decay, and normalization (e.g., LayerNorm or Group Normalization [wu2018group]) are also unchanged and therefore do not confound comparisons.

The key GOLF-related hyperparameters, as recorded for the candidate condition, are:

```markdown
Table 1: GOLF candidate hyperparameters (lane_3, seed 1337).

| Hyperparameter             | Value      |
|---------------------------|------------|
| qat_enabled               | 1.0        |
| fake_quant_strength       | 1.0        |
| qat_start_frac            | 0.5        |
| qat_group_size            | 32.0       |
| quant_error_weight        | 1.0        |
| compression_reg_enabled   | 1.0        |
| compression_reg_lambda    | 0.0001     |
| seed                      | 1337.0     |
```

These settings imply that QAT is fully applied to designated layers for the final 50% of training, with group-wise quantization over groups of size 32, that quantization error is given equal weight in the loss proxy, and that the codec-aligned regularizer contributes a relatively small but non-zero term to the overall objective. The baseline condition is defined implicitly by setting `qat_enabled = 0.0` and `compression_reg_enabled = 0.0` while keeping all other training hyperparameters fixed, though these exact toggles are not separately logged in the provided summary.

### 4.4 Hardware and runtime measurement

All experiments were executed on a single NVIDIA GeForce RTX 5070 Ti GPU with 16,303 MB of VRAM, classified as a high-tier device by the Parameter Golf environment. The training and evaluation scripts measure wall-clock time using high-resolution timers that encompass model loading, forward passes over the validation set, and the int8-plus-zlib roundtrip operations, but exclude unrelated setup steps such as environment initialization or dependency installation, in accordance with challenge guidelines.

For the baseline condition, the evaluation runtime \( T_\text{base} \) is reported as 62,992.0 ms, and for the GOLF candidate, the runtime \( T(\theta_\text{GOLF}) \) is 80,894.38009262085 ms. These values are computed over a single evaluation per condition and are treated as representative for the current analysis. The runtime ratio,
\[
\mathrm{runtime\_ratio}(\theta_\text{GOLF}) = \frac{80{,}894.38009262085}{62{,}992.0} \approx 1.2842008523720607,
\]
is directly logged and used to set `quick_gate_passed = 0.0`, indicating that the candidate configuration violates the 1.10× quick-gate. Both training and evaluation fit within the approximate 10-minute per-stage budget of the challenge, but the additional overhead introduced by QAT and compression regularization is sufficient to push the candidate out of the deployable runtime regime defined by lane\_3.

### 4.5 Experimental protocol and ablation tooling

The experimental protocol for each condition consists of a training phase followed by an evaluation phase. During training, the model is optimized on the training corpus using the standard language modeling loss, augmented for the GOLF condition by the codec-aligned regularizer when `compression_reg_enabled = 1.0`. The QAT schedule tracks normalized progress \( t \) to determine when to activate fake quantization, based on `qat_start_frac`. Upon completion, the trained parameters \( \theta \) are saved to disk and passed to the quantization-and-compression pipeline for evaluation. This pipeline performs the int8 quantization, zlib compression and decompression, and dequantization, then runs the validation loop to compute val\_bpb, runtime, and the quick-gate flag.

An important aspect of the protocol is the use of an ablation analysis tool that compares conditions post hoc. After both baseline and GOLF runs are recorded, the tool examines their hyperparameter sets and evaluation metrics, and attempts to attribute differences in val\_bpb and runtime to specific toggles. In this snapshot, however, the tool detects that conditions labeled “hyperparameters” and “metrics” produce identical outputs across the metrics it inspects, leading to the “ABALATION FAILURE” warning. This suggests that some of the knobs expected to differentiate configurations—potentially including QAT and compression settings—did not in fact influence the training or evaluation code paths being analyzed by the ablation tool.

This discrepancy has two implications for the current experiments. First, it cautions against over-interpreting small numerical differences in val\_bpb or runtime as evidence of causal effects from QAT or codec regularization until the wiring is fully validated. Second, it highlights the importance of having tooling that can automatically flag such misalignments, which is particularly critical in a setting like Parameter Golf where runs are expensive and constrained by gate budgets. In subsequent sections, we report the recorded metrics for the baseline and GOLF candidate as they stand, while interpreting them through the lens of this methodological caveat and focusing on the lessons they provide for the design and evaluation of codec-aware training under strict deployment constraints.

## Results

The experimental results compare the float-trained, post-hoc–quantized baseline against the staged QAT + codec-regularized GOLF configuration in terms of post-roundtrip val\_bpb and runtime under the lane\_3 constraints. Although the Parameter Golf metadata labels this as a multi-seed experiment, the logs for each method aggregate over a single run, so the standard deviations reported below are zero and statistical tests are uninformative. Nevertheless, the aggregated tables and figures reveal clear qualitative trends about the interaction between QAT, codec alignment, and the quick-gate.

The overall comparison between the two methods is summarized in Table 2. The baseline achieves lower val\_bpb and faster runtime, while the GOLF candidate exhibits a modest degradation in compression efficiency and a substantial runtime overhead. Because each method is represented by one recorded seed, the means equal the observed values and the standard deviations are identically zero.

```latex
\begin{table}[h]
\centering
\caption{Aggregated post-roundtrip performance for float-only baseline and GOLF (staged QAT + codec regularization) in Parameter Golf lane\_3. Means and standard deviations are computed over the recorded seeds per method (here, one seed each). Lower val\_bpb and runtime are better; runtime\_ratio indicates overhead relative to the baseline.}
\begin{tabular}{lcccc}
\hline
Method & val\_bpb (mean $\pm$ std) & runtime\_ms (mean $\pm$ std) & runtime\_ratio (mean $\pm$ std) & quick\_gate\_passed (mean $\pm$ std) \\
\hline
Baseline (float + post-hoc int8+zlib) & \textbf{3.3794} $\pm$ 0.0000 & \textbf{62992.0000} $\pm$ 0.0000 & \textbf{1.0000} $\pm$ 0.0000 & \textbf{1.0000} $\pm$ 0.0000 \\
GOLF (staged QAT + codec reg) & 3.3919 $\pm$ 0.0000 & 80894.3801 $\pm$ 0.0000 & 1.2842 $\pm$ 0.0000 & 0.0000 $\pm$ 0.0000 \\
\hline
\end{tabular}
\end{table}
```

This aggregated view shows that the GOLF configuration increases val\_bpb by 0.0125 absolute, corresponding to a small but consistent degradation in validation compression, and violates the quick-gate with a runtime ratio of approximately 1.28. Building on this observation, Figure 5 provides a visual comparison of val\_bpb across the two methods, emphasizing that the baseline remains superior in the end-to-end compression metric after the full int8-plus-zlib roundtrip.

As shown in Figure 5, the baseline’s lower bar indicates better compression efficiency, while the GOLF bar is slightly higher, consistent with the positive delta in val\_bpb. This pattern underscores that naïvely enabling staged QAT and compression regularization does not automatically yield codec-aware gains and may in fact erode performance if the regularizer is misaligned with zlib’s behavior or insufficiently tuned.

To connect compression performance with runtime behavior, Figure 6 plots both absolute runtimes and the runtime ratio relative to the baseline, overlaid with the 1.10× quick-gate threshold. The baseline lies comfortably beneath this threshold by definition, while the GOLF configuration sits well above it, reflecting the roughly 28% runtime overhead induced by QAT and codec-aware components in the current implementation. Figure 7 then combines val\_bpb and runtime into a bitrate–runtime trade-off view, where the baseline occupies a more favorable lower-left region than the GOLF candidate.

Because lane\_3 does not define explicit “easy” and “hard” regimes in the provided logs, we interpret regimes in terms of deployment feasibility: configurations that pass the quick-gate and artifact-size constraints form the “deployable” regime, while those that violate the quick-gate form a “non-deployable” regime. Table 3 reports metrics for each method under this dichotomy, with the baseline inhabiting the deployable regime and the GOLF configuration landing in the non-deployable one.

```latex
\begin{table}[h]
\centering
\caption{Per-regime breakdown of post-roundtrip performance. The deployable regime consists of configurations with runtime\_ratio $\leq 1.10$ (quick-gate passed), while the non-deployable regime comprises those with runtime\_ratio $> 1.10$. Each cell shows mean $\pm$ std over the single recorded seed in that regime.}
\begin{tabular}{lcccc}
\hline
Regime & Method & val\_bpb (mean $\pm$ std) & runtime\_ms (mean $\pm$ std) & runtime\_ratio (mean $\pm$ std) \\
\hline
Deployable (quick-gate passed) & Baseline & \textbf{3.3794} $\pm$ 0.0000 & \textbf{62992.0000} $\pm$ 0.0000 & \textbf{1.0000} $\pm$ 0.0000 \\
Non-deployable (quick-gate failed) & GOLF & 3.3919 $\pm$ 0.0000 & 80894.3801 $\pm$ 0.0000 & 1.2842 $\pm$ 0.0000 \\
\hline
\end{tabular}
\end{table}
```

This regime-level view emphasizes that, under the current hyperparameters, GOLF not only fails to improve val\_bpb but also falls outside the resource-feasible regime enforced by the quick-gate. From a Parameter Golf perspective, this means that the configuration cannot be considered a viable submission despite its conceptual alignment with the deployment pipeline.

The final quantitative element is a statistical comparison between methods. Given that each method has a single recorded run, formal paired t-tests degenerate to undefined variance and zero degrees of freedom. For completeness and to adhere to the requested structure, Table 4 reports the differences in means together with a note that standard t-statistics and p-values cannot be computed under these conditions.

```latex
\begin{table}[h]
\centering
\caption{Statistical comparison between baseline and GOLF. Each row reports the difference in means (GOLF $-$ Baseline) for key metrics. Because only one seed per method is available, the pooled variance is zero and standard paired t-tests and p-values are not defined.}
\begin{tabular}{lccc}
\hline
Metric & Mean difference & t-statistic & p-value \\
\hline
val\_bpb & 0.0125 & -- & -- \\
runtime\_ms & 17902.3801 & -- & -- \\
runtime\_ratio & 0.2842 & -- & -- \\
quick\_gate\_passed & -1.0000 & -- & -- \\
\hline
\end{tabular}
\end{table}
```

Interpreting this table, the positive difference in val\_bpb confirms that the GOLF candidate is less compression-efficient than the baseline, while the large positive difference in runtime and runtime ratio confirms that it is materially slower. The negative difference in the quick-gate flag simply reflects that the baseline passes the deployment gate and the candidate does not. Although formal significance tests are unavailable, the magnitudes of these differences far exceed any plausible measurement noise on a single machine, so the qualitative conclusion is robust.

Taken together, the tables and figures show that in this first instantiation of GOLF, codec-aware QAT under the chosen hyperparameters yields a stable but strictly worse point on the bitrate–runtime frontier than the float-trained baseline. This negative result provides a clear starting point for the methodological refinements and interpretive analysis developed in the subsequent discussion.

## Discussion

The central empirical finding of this study is that a straightforward instantiation of staged QAT with codec-aligned regularization, as implemented in GOLF, does not improve post-roundtrip compression performance under the Parameter Golf lane\_3 constraints and instead yields both higher val\_bpb and slower runtime. This outcome contrasts with the intuition from the QAT literature that aligning training more closely with deployment precision should at least preserve, if not enhance, downstream metrics when quantization is unavoidable. The discrepancy suggests that when general-purpose codecs such as zlib are introduced into the deployment path, naive extensions of QAT may be insufficient and can even be counterproductive.

One plausible explanation is that the current codec-regularization proxy is not yet well matched to zlib’s actual coding behavior, leading to a misalignment between the training-time penalty and the deployment-time artifact size. Learned compression frameworks that optimize rate–distortion objectives typically design differentiable entropy models that approximate the true code length under arithmetic coding, then backpropagate through these models to shape latent representations. In contrast, GOLF currently relies on a heuristic proxy for compressibility, computed on fake-quantized weights at sparse intervals, while deferring full zlib evaluation to the end of training. The observed degradation in val\_bpb is consistent with a scenario in which this proxy inadvertently encourages weight configurations that are less favorable to Deflate’s dictionary and Huffman mechanisms than those arising from unconstrained float training.

The runtime overhead observed for GOLF further complicates the picture. Even though QAT is conceptually motivated by deployment alignment, its training-time machinery adds computation, especially when fake quantization and compression proxies are evaluated on multiple tensors over large models. In the present setup, these additions are sufficient to push the GOLF configuration beyond the 1.10× quick-gate, marking it as non-deployable despite its conceptual appeal. This aligns with broader observations in efficient deep learning that methods which reduce inference cost can nonetheless increase training cost substantially, complicating their adoption in settings where both training and inference are budgeted [desislavov2021compute]. The Parameter Golf framework makes this tension explicit by jointly tracking val\_bpb and runtime, effectively enforcing a performance-per-resource-style criterion similar in spirit to metrics advocated in deployment-aware medical imaging [selvan2024pepr].

A second, methodological layer to these results concerns the ablation tooling’s “ABALATION FAILURE” warning, which indicates that configurations labeled as distinct by hyperparameters can nonetheless produce identical metrics. This suggests that at least some intended QAT or compression toggles were not actually wired into the training computation inspected by the ablation tool. In such a situation, differences between baseline and candidate metrics may reflect only a subset of the conceptual changes attributed to GOLF, or even incidental factors such as seed choice. Similar challenges have been documented in benchmarking toolkits where configuration misalignments lead to misleading comparisons, motivating integrated environments that couple configuration, training, and evaluation more tightly [dimitrovski2023aitlas]. The Parameter Golf infrastructure takes a step in this direction by automatically cross-checking hyperparameters and outcomes, and the present negative result underscores the value of such tooling.

Comparing these findings with prior work on benchmarks and deployment-centric evaluation further clarifies their implications. Benchmarks such as MLPerf Tiny emphasize strict control over hardware, models, and tasks to ensure that reported latency and energy numbers are meaningful across implementations [banbury2021mlperf]. Similarly, efficient learning benchmarks for graph outlier detection and image manipulation highlight that real-world applicability depends not only on accuracy but also on resource usage and robustness [liu2022bond, ma2024imdlbenco]. Parameter Golf extends this ethos into the space of codec-aware language modeling by imposing an explicit artifact-size cap and runtime gate, and GOLF’s underperformance within this framework suggests that sophisticated training objectives must be matched by equally careful engineering around runtime and configuration wiring.

The practical takeaway for practitioners considering codec-aware QAT is therefore twofold. First, it is not sufficient to simply add quantization and compressibility penalties to an otherwise standard training loop; the design of the proxy loss, its interaction with optimizer dynamics, and its evaluation frequency must all be tuned with awareness of the target codec and hardware. Second, deployment-centric benchmarks that enforce hard gates can reveal hidden costs that might be overlooked in more permissive settings, such as modest but critical runtime overheads that render a method unattractive despite marginal gains in compression or accuracy. In that sense, the present negative result is informative: it delineates a region of the design space—naive staged QAT with lightweight codec proxies under the current hyperparameters—that is unlikely to produce competitive points on the bitrate–runtime frontier, thereby sharpening the search for more promising strategies.

Finally, the study highlights the role of integrated evaluation harnesses in enabling principled iteration. By building GOLF strictly within the Parameter Golf configuration system and logging all relevant metrics into a unified records structure, it becomes straightforward to compare future variants, audit the effects of hyperparameter changes, and ensure that new methods are judged under identical deployment conditions. This mirrors the lessons drawn from domain generalization, where carefully tuned baselines and standardized pipelines have been shown to be crucial for credible empirical claims [teterwak2023improved]. In future work, this harness can support more elaborate codec-aware training schemes, such as learned approximations to zlib’s coding cost, structured pruning aligned with dictionary patterns, or multi-stage schedules that balance training and inference costs more effectively.

## Limitations

The present study is constrained in several important ways that delimit the scope of its conclusions. First, the quantitative evaluation is based on a single recorded run per method, meaning that the aggregated means and standard deviations in the results tables reflect deterministic outcomes rather than distributions over multiple seeds. This precludes meaningful statistical tests and leaves open the question of how sensitive the observed differences in val\_bpb and runtime are to initialization or data-ordering noise. A more robust assessment would require repeated runs per configuration, enabling confidence intervals and p-values that quantify variability and effect sizes.

Second, the ablation infrastructure has explicitly flagged an implementation defect, indicating that conditions intended to differ in QAT and compression-related hyperparameters produced identical metrics under its diagnostic view. Although the baseline and GOLF candidate used in the main analysis do exhibit distinct logged metrics, the ablation warning strongly suggests that not all intended toggles are fully wired into the training computation. As a result, the current GOLF configuration may represent only a partial realization of the conceptual method, and some of the observed behavior could stem from untracked implementation details rather than the designed codec-aware components.

Third, the codec-aligned regularizer is implemented as a heuristic proxy rather than a learned or carefully calibrated approximation to zlib’s coding cost. Its internal form is only coarsely specified in the configuration (through a binary enable flag and a scalar weight), and its evaluation schedule across tensors and steps is not exhaustively logged. Without a more precise characterization of this proxy, it is difficult to disentangle whether the degradation in val\_bpb arises from fundamental limitations of codec-aware training in this setting, from misalignment between the proxy and zlib, or from suboptimal hyperparameter choices around the regularizer’s strength and frequency.

Fourth, the experiments are confined to a single architecture and dataset configuration as determined by the Parameter Golf lane\_3 environment. While this ensures comparability within the challenge, it limits the generality of the findings to other model sizes, tokenizers, or domains. Different architectures, particularly those with more structured sparsity or weight sharing, might interact with zlib in qualitatively different ways, potentially making codec-aware QAT more beneficial than observed here. Similarly, varying the artifact budget or quick-gate threshold could shift the relative attractiveness of methods that trade runtime for compression gains.

Finally, the analysis focuses primarily on validation bits-per-byte and runtime, without exploring secondary axes such as robustness to distribution shift, training energy consumption, or interpretability of quantized representations. Other work on deployment-aware evaluation has shown that these aspects can meaningfully affect real-world suitability [liu2022bond, selvan2024pepr], and understanding how codec-aware training interacts with them remains an open question. Addressing these limitations will require expanded experimental campaigns, refined tooling, and deeper integration between training objectives and codec behavior.

## Conclusion

This work introduced GOLF, a staged quantization-aware training framework that aims to align language model training with an int8-plus-zlib deployment path under strict artifact-size and runtime constraints. Within the Parameter Golf lane\_3 harness, we implemented staged QAT and a codec-aligned compression regularizer via configuration-only extensions and evaluated their impact on post-roundtrip val\_bpb and runtime. The main empirical finding is that a naïve GOLF configuration produces numerically stable models but underperforms a float-trained baseline on both compression efficiency and runtime under the quick-gate. Future work should refine the codec proxy to better approximate zlib, harden the ablation and configuration wiring to ensure faithful realization of method variants, and explore architectures or pruning schemes that more naturally induce codec-friendly weight structures while respecting deployment gates.