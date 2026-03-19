---
created: '2026-03-19T07:04:08+00:00'
evidence:
- stage-09/exp_plan.yaml
id: experiment_design-rc-20260319-065325-2fdb44
run_id: rc-20260319-065325-2fdb44
stage: 09-experiment_design
tags:
- experiment_design
- stage-09
- run-rc-20260
title: 'Stage 09: Experiment Design'
---

# Stage 09: Experiment Design

ablations:
  degraded_graph_governance_pointer_explainer:
    base_method: PointerFirstGovernedGraphExplainer
    description: 'Governance ablation for Hypothesis C. Uses pointer-first explanations
      but with intentionally weakened graph governance.

      '
    expected_effect: 'Lower explainability and auditability ratings, higher time-to-validate,
      and more inconsistencies across runs, supporting the conditional nature of pointer-first
      benefits.

      '
    how_it_differs: 'Introduce random, unlogged modifications to node metadata and
      edges between training and evaluation; allow non-deterministic retrieval tie-breaking.

      '
    what_is_removed: Strict versioning and deterministic retrieval; governance logs.
  no_graph_retrieval_thin_controller:
    base_method: ThinGraphControllerParameterGolf
    description: 'Ablation of external graph usage for Hypothesis A and C. Tests how
      much of the thin controller’s performance depends on the artifact graph.

      '
    expected_effect: 'Reduced on-harness performance and explanation adequacy; potentially
      improved robustness to graph drift but worse traceability; tests contribution
      of the external graph to compression and performance.

      '
    how_it_differs: 'Replace retrieve_graph_nodes with a no-op; remove graph embeddings
      and pointer heads; controller operates purely on text with a classification
      head.

      '
    what_is_removed: Graph retrieval and node-based pointer mechanisms.
  no_parameter_golf_artifact_fixed:
    base_method: ThinGraphControllerParameterGolf
    description: 'Ablation of parameter golf itself. Tests whether the artifact-level
      search is necessary beyond standard compression.

      '
    expected_effect: 'Higher val_bpb and/or worse quick-harness performance at same
      size, showing the contribution of parameter golf to artifact-level optimization.

      '
    how_it_differs: 'Train the thin controller with fixed, pre-chosen quantization
      and sparsity settings; skip any iterative artifact optimization; export artifact
      directly.

      '
    what_is_removed: parameter_golf_step and artifact-level discrete search.
  no_phase_dynamics_standard_graph_controller:
    base_method: PhaseSynchronizedGraphController
    description: 'Control ablation for Hypothesis D. Same architecture as PHASE but
      with phase dynamics disabled, equivalent to a standard thin graph controller.

      '
    expected_effect: 'Similar performance to ThinGraphControllerParameterGolf; any
      additional gains in PHASE over this ablation isolate the effect of phase dynamics.

      '
    how_it_differs: 'Fix theta_i = 0 for all nodes and skip update_phases; use standard
      attention over node embeddings for decision and pointer prediction; remove phase
      regularization term from loss.

      '
    what_is_removed: Kuramoto-style phase updates and phase-based readout.
  no_rbe_regularization_stability_pipeline:
    base_method: RBEAwareStabilityFirstCompression
    description: 'Ablation for Hypothesis B. Removes perturbation-aware consistency
      loss while keeping compression and parameter golf identical.

      '
    expected_effect: 'Higher RBE (more refusal flips) at similar val_bpb and accuracy,
      showing the specific impact of the stability objective.

      '
    how_it_differs: 'Set lambda_stab = 0 and skip generate_perturbations; train only
      on original examples with standard classification and pointer losses.

      '
    what_is_removed: RBE consistency term and perturbation-based training pairs.
baselines:
  cost_first_quantized_compression_pipeline:
    architecture:
      artifact_size_target: <=16MB including quantization + metadata
      backbone: 20–40M parameter transformer distilled from a larger LM
    description: 'Modern cost-first compression baseline family (Axis A in Hypothesis
      B) that aggressively minimizes val_bpb and artifact size using pruning, quantization,
      and distillation without explicit RBE optimization.

      '
    implementation_spec:
      algorithm_steps:
      - Start from a distilled 20–40M parameter transformer backbone.
      - Apply structured and unstructured pruning guided by magnitude and Hessian
        approximations (SparseGPT-style).
      - Apply group-wise 4–8 bit weight quantization with activation-aware calibration
        (AWQ-style).
      - Fine-tune on compliance data with standard cross-entropy loss to recover accuracy.
      - Export artifact with compressed weights plus minimal decompressor to fit <=16MB.
      class_name: CostFirstCompressedComplianceModel
      differentiator: 'Optimizes for minimal val_bpb and artifact size using state-of-the-art
        compression techniques but does not include explicit RBE or graph-based explanation
        objectives.

        '
      key_hyperparameters:
        activation_bitwidth: 8
        base_learning_rate: 1e-4
        batch_size: 32
        

... (truncated, see full artifact)
