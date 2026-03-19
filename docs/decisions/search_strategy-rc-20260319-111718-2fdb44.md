---
created: '2026-03-19T11:20:44+00:00'
evidence:
- stage-03/search_plan.yaml
- stage-03/sources.json
- stage-03/queries.json
id: search_strategy-rc-20260319-111718-2fdb44
run_id: rc-20260319-111718-2fdb44
stage: 03-search_strategy
tags:
- search_strategy
- stage-03
- run-rc-20260
title: 'Stage 03: Search Strategy'
---

# Stage 03: Search Strategy

hard_constraints:
- description: Full serialized artifact (weights + tokenizer + config + glue) must
    be <= 16MB.
  enforcement: hard_filter
  metric: artifact_mb
  name: artifact_size
  safety_margin_mb: 0.5
  threshold_mb: 16.0
- description: Each candidate must be trainable and evaluable within minutes-scale
    quick-harness runs.
  enforcement: hard_filter
  max_minutes_per_run: 20
  metric: wall_clock_minutes
  name: quick_harness_runtime
- budget_range_hours:
  - 50
  - 150
  description: Total search + controller training compute.
  metric: gpu_hours
  name: global_compute_budget
output_expectations:
- structured_summaries_per_subquestion
- quantitative_baseline_table_for_enwik8_text8
- catalog_of_early_signals_and_their_reported_predictivity
- design_patterns_for_constraint_aware_controllers
phases:
- goals:
  - Finalize exact artifact format and packer implementation.
  - Benchmark quick-harness runtime envelope on target hardware.
  name: phase_0_scoping
  search_targets: []
  tasks:
  - description: Implement reference artifact packer and measure size for a few seed
      models.
    id: P0_T1
    outputs:
    - packer_cli
    - artifact_schema
  - description: Measure wall-clock per step and per epoch for small transformer configs
      on Enwik8/Text8.
    id: P0_T2
    outputs:
    - runtime_profile
- goals:
  - Define structured search space over architectures, compression, and tokenizers.
  - Implement fast artifact size estimator calibrated to exact packer.
  - Enforce quick-harness and 16MB feasibility at proposal time.
  name: phase_1_Q1_search_space_and_size_model
  search_targets:
  - artifact_mb
  - estimated_minutes
  tasks:
  - description: Specify discrete/continuous knobs and parameterization for Parameter
      Golf.
    details:
      architecture_knobs:
      - name: num_layers
        range:
        - 4
        - 24
        step: 2
        type: integer
      - name: d_model
        type: integer
        values:
        - 192
        - 256
        - 320
        - 384
        - 448
        - 512
      - constraint: d_model % num_heads == 0
        name: num_heads
        type: integer
        values:
        - 3
        - 4
        - 6
        - 8
      - name: ffn_multiplier
        type: categorical
        values:
        - 2
        - 3
        - 4
      - name: context_length
        type: categorical
        values:
        - 256
        - 512
        - 1024
      - name: weight_tying
        type: categorical
        values:
        - tied_input_output
        - untied
      compression_knobs:
      - name: global_sparsity
        range:
        - 0.0
        - 0.9
        type: continuous
      - name: sparsity_pattern
        type: categorical
        values:
        - unstructured
        - n_m_block
        - per_head_pruning
      - name: weight_bitwidth
        type: categorical
        values:
        - 8
        - 6
        - 4
      - name: activation_bitwidth
        type: categorical
        values:
        - 16
        - 8
      - description: Piecewise-constant sparsity over depth (e.g., three segments).
        name: per_layer_sparsity_profile
        type: structured
      tokenizer_knobs:
      - name: tokenizer_family
        type: categorical
        values:
        - bpe
        - unigram
        - character
      - log_scale: true
        name: vocab_size
        range:
        - 256
        - 32768
        type: integer
      - name: vocab_pruning_template
        type: categorical
        values:
        - none
        - prune_tail_10pct
        - prune_tail_30pct
    id: Q1_T1_search_space_definition
  - description: Build differentiable-or-smooth artifact size estimator calibrated
      to true packer.
    estimator_components:
    - formula: sum_over_params(param_count * effective_bits / 8)
      name: weight_storage
    - included_in_artifact: false
      name: optimizer_state
    - approximation: a * vocab_size + b * num_merges + c
      name: tokenizer_storage
    - approximation: constant_kb_with_small_margins
      name: config_and_glue_overhead
    id: Q1_T2_artifact_size_estimator
    validation_plan:
    - sample_size: 100
    - sampling_strategy: latin_hypercube_over_search_space
    - metric: mean_absolute_error_mb
    - target_mae_mb: 0.05
  - description: Implement hard filters for artifact size and quick-harness runtime.
    id: Q1_T3_feasibility_filters
    methods:
    - artifact_size_filter:
        logic: reject_if(estimated_artifact_mb > (16.0 - safety_margin_mb))
    - runtime_filter:
        calibration: fit_linear_model_to_measured_wallclock
        limit: max_minutes_per_run
        proxy_metric: estimated_flops_per_step * training_steps
  - description: For controller training or BO, define soft penalties near constraint
      boundaries.
    id: Q1_T4_penalty_terms
    penalty_formulation:
    - artifact_penalty: lambda_size * max(0, estimated_artifact_mb - 15.5)
    - runtime_penalty: lambda_time * max(0, estimated_min

... (truncated, see full artifact)


{
  "sources": [
    {
      "id": "S1",
      "name": "arXiv",
      "type": "preprint_index",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "neural architecture search parameter budget tiny transformer 16MB model size quantization pruning tokenizer size accounting",
      "verified_at": null
    },
    {
      "id": "S2",
      "name": "OpenReview",
      "type": "conference_repository",
      "url": "https://openreview.net",
      "status": "planned",
      "query": "AutoML controller early stopping signals architecture search under resource constraints",
      "verified_at": null
    },
    {
      "id": "S3",
      "name": "Semantic Scholar",
      "type": "literature_index",
      "url": "https://www.semanticscholar.org",
      "status": "planned",
      "query": "learning curve extrapolation early training signals for neural network performance prediction",
      "verified_at": null
    },
    {
      "id": "S4",
      "name": "Google Scholar",
      "type": "literature_index",
      "url": "https://scholar.google.com",
      "status": "planned",
      "query": "multi fidelity hyperparameter optimization early stopping successive halving hyperband neural networks",
      "verified_at": null
    },
    {
      "id": "S5",
      "name": "GitHub",
      "type": "code_repository",
      "url": "https://github.com",
      "status": "planned",
      "query": "tiny transformer enwik8 bits per byte pruning quantization implementation",
      "verified_at": null
    },
    {
      "id": "S6",
      "name": "arXiv (tokenizer & vocab compression)",
      "type": "preprint_index",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "tokenizer vocabulary size effect on language model compression enwik8 vocabulary pruning subword tokenizer compression model size tradeoff",
      "verified_at": null
    }
  ],
  "count": 6,
  "generated": "2026-03-19T11:20:44+00:00"
}

{
  "queries": [
    "Parameter Golf val bpb minimization under",
    "Parameter Golf val bpb benchmark",
    "Parameter Golf val bpb survey",
    "Golf val bpb minimization",
    "Parameter Golf val comparison",
    "Parameter Golf val deep learning",
    "val bpb minimization under"
  ],
  "year_min": 2020
}