---
created: '2026-03-19T22:18:45+00:00'
evidence:
- stage-09/exp_plan.yaml
id: experiment_design-rc-20260319-220921-d02b4b
run_id: rc-20260319-220921-d02b4b
stage: 09-experiment_design
tags:
- experiment_design
- stage-09
- run-rc-20260
title: 'Stage 09: Experiment Design'
---

# Stage 09: Experiment Design

constraints:
  artifact_bytes_max: 16000000
  runtime_factor_max: 1.1
  time_budget_seconds: 1200
environment:
  BATCH_SIZE: '32'
  CHECKPOINT_DIR: /workspace/checkpoints/lane1_H1_global_gate_lora
  DATASET_CONFIG: wikitext-2-v1
  DATASET_NAME: wikitext
  DATA_ROOT: /workspace/data
  DROPOUT: '0.1'
  ENABLE_RUNTIME_MONITOR: '1'
  GATE_ACTIVATION: tanh
  GATE_APPLY_MODE: scale_lora
  GATE_DIM: '16'
  GATE_DROPOUT: '0.0'
  GATE_HIDDEN_DIM: '32'
  GATE_POOLING: mean
  GATE_TYPE: global_sequence
  GRAD_CLIP_NORM: '1.0'
  LOG_EVERY_STEPS: '1'
  LORA_ALPHA: '16'
  LORA_DROPOUT: '0.05'
  LORA_ENABLED: '1'
  LORA_RANK: '8'
  LORA_TARGET_MODULES: in_proj,out_proj
  LR: 3e-4
  MAX_ARTIFACT_BYTES: '16000000'
  MODEL_TYPE: recurrent_rwkv
  NUM_LORA_EXPERTS: '1'
  NUM_RECURRENCE_LOOPS: '3'
  NUM_SHARED_BLOCKS: '3'
  OPTIMIZER: adamw
  REPORT_METRIC_NAME: val_bpb
  RESIDUAL_GATE_ENABLED: '1'
  ROUTING_STRATEGY: none
  SAVE_EVERY_STEPS: '0'
  SEED: '1337'
  SEQ_LEN: '512'
  TRAIN_STEPS: '20'
  WARMUP_STEPS: '2'
  WEIGHT_DECAY: '0.01'
hypothesis_id: H1
knobs:
  backbone:
    MODEL_TYPE:
      rationale: RWKV-style recurrent LM aligns with lane_1 recurrence focus.
      value: recurrent_rwkv
    NUM_RECURRENCE_LOOPS:
      rationale: Increases effective depth without many extra parameters; matches
        lane seed.
      value: 3
    NUM_SHARED_BLOCKS:
      rationale: Shared-block recurrence for cheap depth at small artifact size.
      value: 3
  gating:
    GATE_APPLY_MODE:
      rationale: Gate modulates LoRA adapters only, minimizing interference with backbone.
      value: scale_lora
    GATE_DIM:
      rationale: Very small gate vector to keep parameters and runtime overhead minimal.
      value: 16
    GATE_HIDDEN_DIM:
      rationale: Tiny MLP on pooled state; overhead negligible under 1.10× runtime
        cap.
      value: 32
    GATE_POOLING:
      rationale: Simple, cheap sequence pooling aligned with H1 description.
      value: mean
    GATE_TYPE:
      rationale: Implements H1’s graded global gate variant (sequence-wise, not token-wise).
      value: global_sequence
    RESIDUAL_GATE_ENABLED:
      rationale: Activate residual/global gating as required by lane_1 composite design.
      value: true
  lora:
    LORA_ALPHA:
      rationale: Standard alpha ≈ 2×rank for stable scaling.
      value: 16
    LORA_DROPOUT:
      rationale: Mild regularization to avoid overfitting small adapter capacity.
      value: 0.05
    LORA_ENABLED:
      rationale: Test LoRA specialization on top of recurrent backbone per lane hypothesis.
      value: true
    LORA_RANK:
      rationale: Modest rank that fits easily under 16MB while providing nontrivial
        capacity.
      value: 8
    LORA_TARGET_MODULES:
      rationale: Target core recurrent projections where specialization is most impactful.
      value: in_proj,out_proj
  training:
    BATCH_SIZE:
      rationale: Reasonable token throughput on GPU without memory spikes.
      value: 32
    DROPOUT:
      rationale: Mild regularization across backbone.
      value: 0.1
    LR:
      rationale: Conservative AdamW learning rate for small recurrent LMs.
      value: 3e-4
    SEQ_LEN:
      rationale: Standard LM context length for wikitext-2 quick evaluation.
      value: 512
    TRAIN_STEPS:
      rationale: Matches quick_harness baseline for comparable val_bpb under time
        budget.
      value: 20
    WEIGHT_DECAY:
      rationale: Standard regularization to avoid overfitting.
      value: 0.01
lane_id: lane_1
run_command: 'torchrun --standalone --nproc_per_node=1 /parameter-golf/train_gpt.py

  '
success_criteria:
  description: "This quick-gate candidate tests H1’s “graded global gate” variant\
    \ on top of a recurrent shared-block + LoRA backbone.\nSuccess requires:\n  -\
    \ val_bpb strictly lower than the recurrence-only baseline from quick_harness.sh,\n\
    \  - runtime_ms <= 1.10 × that baseline on the same harness,\n  - total serialized\
    \ artifact size ≤ 16MB.\nThis run establishes whether a cheap sequence-global\
    \ gate modulating shared LoRA adapters yields measurable val_bpb gains within\
    \ the tight runtime and artifact constraints of lane_1."
  direction: minimize
  primary_metric: val_bpb
  quick_gate:
    max_artifact_bytes: 16000000
    must_improve_bpb: true
    runtime_factor: 1.1
topic: 'Parameter Golf val_bpb minimization — lane_1: Recurrence + LoRA + lightweight
  routing/gating composite. Hypothesis: If we start from recurrence-only and add LoRA
  specialization plus residual gating, post-roundtrip val_bpb will improve at fixed
  artifact budget while keeping runtime under 1.10x baseline. Artifact limit 16MB.
  Quick-gate: runtime <= 1.10x baseline.'
