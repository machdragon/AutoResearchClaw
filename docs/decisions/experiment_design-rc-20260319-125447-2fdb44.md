---
created: '2026-03-19T13:09:03+00:00'
evidence:
- stage-09/exp_plan.yaml
id: experiment_design-rc-20260319-125447-2fdb44
run_id: rc-20260319-125447-2fdb44
stage: 09-experiment_design
tags:
- experiment_design
- stage-09
- run-rc-20260
title: 'Stage 09: Experiment Design'
---

# Stage 09: Experiment Design

ablations:
  core_only_no_summaries_ablation:
    expected_effect: 'Tests whether small, sanitized summaries of non-core modalities
      provide useful signal without large attack surface; dropping them entirely may
      hurt benign compliance recall more than the full adversarially-pruned design.

      '
    how_it_differs: 'Disable generate_summaries and exclude N from retrieval and context
      entirely; only C is used.

      '
    what_is_removed: 'Summarization of non-core modalities in the adversarially-pruned
      design; non-core artifacts are entirely dropped.

      '
  no_adversarial_profiling_artifact_ablation:
    expected_effect: 'Should increase successful attacks and privacy leakage under
      adversarial regimes, even if benign performance is similar, isolating the contribution
      of adversarial-aware pruning.

      '
    how_it_differs: 'Skip profile_modalities and select_core_set; instead, define
      core set C by simple frequency/utility ranking without adversarial metrics,
      and do not include attack_success_rate or privacy_leakage_score in the loss.

      '
    what_is_removed: 'Adversarial profiling and risk-aware core selection in AdversarialCoreArtifactSelector;
      all modalities treated as equally safe/valuable.

      '
  no_boundary_conditioning_compression_ablation:
    expected_effect: 'Should increase RBE and violation rates near promotion boundaries,
      reducing the advantage over the globally compressed baseline and testing the
      importance of boundary conditioning.

      '
    how_it_differs: 'Replace estimate_boundary_risk outputs with a constant value
      and remove dependence on risk_class in compression and logging policy networks;
      effectively reverts to global compression while keeping the same controller
      framework.

      '
    what_is_removed: 'Boundary- and risk-conditioned compression policies in BoundaryWeightedAutoRC;
      compression becomes global and input-agnostic.

      '
  trace_heavy_without_hash_chaining_ablation:
    expected_effect: 'May slightly reduce bytes and complexity but should reduce forensic
      usefulness and potentially increase undetected tampering in adversarial settings.

      '
    how_it_differs: 'Remove hash-chaining nodes and integrity checks from the trace
      schema; traces are still structured but not tamper-evident.

      '
    what_is_removed: 'Hash-chained integrity of traces in the trace-heavy design.

      '
  uniform_trace_density_ablation:
    expected_effect: 'Should reduce audit benefits specifically for high-risk or near-boundary
      decisions while leaving average bytes similar, testing the value of boundary-weighted
      evidence.

      '
    how_it_differs: 'Fix trace_budget_fraction to a constant value for all decisions
      and bypass the policy that maps boundary risk to trace density.

      '
    what_is_removed: 'Boundary-weighted trace density allocation in TraceHeavyBoundaryAllocator;
      trace density no longer depends on boundary risk or risk class.

      '
baselines:
  artifact_maximal_retrieval_llm:
    description: 'PACT-style retrieval+LLM system that includes as many artifact modalities
      and metadata channels as possible within 16MB, with light compression but no
      adversarially-aware pruning. Represents the "artifacts as signal" extreme in
      Hypothesis 3.

      '
    fairness_rationale: 'Strong multi-modal retrieval baseline that uses full artifact
      heterogeneity as input to the LLM.

      '
    implementation_spec:
      algorithm_steps:
      - Index all available artifact modalities (code, tickets, logs, comments, docs)
        in a multi-modal embedding space.
      - For each decision, retrieve top-k items from each modality.
      - Pack retrieved artifacts into a multi-modal context for the LLM.
      - Predict compliance decision and free-form explanation.
      - Compress artifacts uniformly to fit within 16MB cap.
      class_name: ArtifactMaximalRAG
      differentiator: 'Maximizes artifact diversity and volume; no adversarial profiling
        or pruning, no boundary-weighted reallocation.

        '
      key_hyperparameters:
        beta: 0.2
        learning_rate: 1e-4
        max_tokens: 4096
        top_k_per_modality: 4
      key_methods:
      - __init__
      - build_artifact_index
      - retrieve_multimodal
      - forward
      - train_step
      loss_function: L = CE(y_pred, y_true) + beta * CE(explanation_tokens, explanation_target_tokens)
    reference_methods:
    - citation: OpenAI / Anthropic-style PACT or similar retrieval graphs (2024 system
        reports).
      name: pact_retrieval_graphs
    - citation: Shuster et al., Multi-modal Retrieval for LLMs, NeurIPS 2023.
      name: multi_modal_rag
  globally_compressed_valbpb_minimizer:
    description: 'Auto-compression and architecture search that globally minimizes
      validation bits-per-byte without explicit boundary or risk conditioning, 

... (truncated, see full artifact)
