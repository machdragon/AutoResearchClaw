---
created: '2026-03-19T11:31:16+00:00'
evidence:
- stage-09/exp_plan.yaml
id: experiment_design-rc-20260319-111718-2fdb44
run_id: rc-20260319-111718-2fdb44
stage: 09-experiment_design
tags:
- experiment_design
- stage-09
- run-rc-20260
title: 'Stage 09: Experiment Design'
---

# Stage 09: Experiment Design

ablations:
- expected_effect: 'Degraded optimization efficiency and weaker correlation with large-model
    multi-objective quality, directly testing Hypothesis 2 that defect vectors carry
    crucial information beyond scalar val_bpb.

    '
  how_it_differs: 'Replace compute_defect_vector with a stub that returns zeros; the
    DefectVectorGuidedParamGolf controller then relies solely on scalar val_bpb and
    training curves as inputs to the surrogate and acquisition function.

    '
  name: no_defect_vector_ablation
  what_is_removed: Structured defect vector computation and usage in the parameter-golf
    controller.
- expected_effect: 'Reduced best-found configuration quality and fewer discovered
    distinct failure modes relative to AdaptiveSparseRichLoggingController, testing
    Hypothesis 3.

    '
  how_it_differs: 'Replace allocate_logging_budget with a fixed per-run byte budget
    and log the same minimal set of metrics and a fixed small number of examples for
    every run, regardless of surprise or configuration.

    '
  name: uniform_thin_logging_ablation
  what_is_removed: Adaptive logging budget allocation based on surprise in the logging
    controller.
- expected_effect: 'More frequent violations of the 16MB constraint and worse val_bpb-under-constraint
    tradeoff, illustrating the importance of artifact-aware decision-making.

    '
  how_it_differs: 'In EarlySignalPhaseWindowController, drop the artifact_mb_pred
    head and remove the artifact-size penalty term from the loss; compression schedule
    is predicted without regard to final artifact size and pruned only post-hoc.

    '
  name: artifact_unaware_phase_window_ablation
  what_is_removed: Differentiable artifact-size estimator and size penalty from the
    phase-window controller.
- expected_effect: 'Poorer ability to adapt to configuration-specific dynamics, slower
    convergence to good regions in phase space, and weaker cross-scale prediction,
    testing Hypothesis 1’s claim about early signals.

    '
  how_it_differs: 'Replace encode_early_signals with a constant embedding; the controller
    can only condition on regime metadata and random noise, effectively reducing to
    a learned prior over (α,G,R) and compression schedules.

    '
  name: early_signal_blind_ablation
  what_is_removed: Use of early-training curves and defect signals in the phase-window
    controller.
baselines:
- SGD + Momentum
- AdamW
- Full Fine-Tuning
- LoRA
- description: 'Dense grid search over (α,G,R) with fixed pruning/quantization schedules
    and uniform-thin scalar logging; uses harness-scale models only and picks the
    best configuration by final val_bpb subject to a post-hoc 16MB artifact check.
    Represents the non-adaptive, non-controller phase-diagram approach.

    '
  fairness_rationale: 'Strong manual hyperparameter sweeps over LR, data filtering,
    and curriculum are the de facto baseline in modern LLM training and compression
    work.

    '
  implementation_spec:
    algorithm_steps:
    - Define discrete grids for α (lr_scale), G (data_filter_threshold), R (curriculum_non_solvent_rate).
    - Enumerate all grid points and, for each, train a quick-harness model for a fixed
      number of tokens.
    - Log scalar val_bpb and minimal curves with uniform-thin logging under the campaign
      16MB budget.
    - Post-hoc compute estimated artifact size for each config using static pruning/quantization
      schedule.
    - Filter configs violating 16MB and select the one with lowest val_bpb.
    class_name: StaticPhaseDiagramGridSearch
    differentiator: 'No adaptive controller; exhaustive but static exploration of
      process space with uniform scalar logging and fixed compression schedule.

      '
    key_hyperparameters:
      curriculum_non_solvent_rates:
      - 0.0
      - 0.2
      - 0.4
      data_quality_thresholds:
      - 0.2
      - 0.5
      - 0.8
      harness_tokens: 2000000000
      lr_scales:
      - 0.3
      - 1.0
      - 3.0
      max_campaign_artifact_mb: 16.0
    key_methods:
    - __init__
    - generate_config_grid
    - run_harness_training
    - select_best_config
    loss_function: L = mean_token_NLL = - (1/T) * Σ_t log pθ(xt | x< t)
  name: static_phase_diagram_grid_search
  reference:
  - 'Touvron et al., LLaMA 2: Open Foundation and Fine-Tuned Chat Models, 2023'
  - 'Zhang et al., OPT: Open Pre-trained Transformer Language Models, 2022'
- description: 'Parameter-efficient fine-tuning using 4-bit QLoRA with fixed rank,
    applied post-hoc after full-precision quick-harness training, without early-signal-conditioned
    compression decisions. Represents modern PEFT-focused compression not tuned to
    artifact-level constraints.

    '
  fairness_rationale: 'QLoRA-style methods are widely used for efficient fine-tuning
    and compression; they are strong baselines for parameter-efficient training under
    memory constraints, though they do not optimize full artifact size or exploit


... (truncated, see full artifact)
