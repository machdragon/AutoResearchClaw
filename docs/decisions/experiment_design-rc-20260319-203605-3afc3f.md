---
created: '2026-03-19T20:48:08+00:00'
evidence:
- stage-09/exp_plan.yaml
id: experiment_design-rc-20260319-203605-3afc3f
run_id: rc-20260319-203605-3afc3f
stage: 09-experiment_design
tags:
- experiment_design
- stage-09
- run-rc-20260
title: 'Stage 09: Experiment Design'
---

# Stage 09: Experiment Design

baselines:
- Full Fine-Tuning
- LoRA
- QLoRA
constraints:
  artifact_bytes_max: 16000000
  notes: '- setup.py is responsible for downloading WikiText-2 to /workspace/data
    using HuggingFace datasets.

    - main.py must run fully offline (no network).

    - Quantization must be post-hoc on pretrained GPT-2; no training/fine-tuning allowed
    in this quick-gate run.

    - Only change allowed between modes is serialization layout + grouping; the in-memory
    tensors used for evaluation must be bitwise identical to the baseline float32
    or quantized baseline.

    '
  quick_gate_runtime_factor: 1.1
  time_budget_s: 1200
datasets:
- Alpaca
- MMLU
- HellaSwag
environment:
  dependencies:
  - transformers==4.39.0
  - datasets==2.17.0
  - tokenizers==0.15.2
  - torch==2.2.0
  - torchvision==0.17.0
  - zstandard==0.22.0
  - numpy==1.26.4
  framework: pytorch
  framework_version: '2.2'
  hardware:
    cpu_cores: 8
    gpu: A100-40GB
    num_gpus: 1
    ram_gb: 64
  python_version: '3.10'
hypothesis_id: lane_6_h1_byte_group_64_quickgate
knobs:
  checks:
    allow_val_bpb_degradation: false
    output_bitwise_equality: true
    weight_bitwise_equality: true
  data:
    data_root: /workspace/data
    dataset_config_name: wikitext-2-raw-v1
    dataset_name: wikitext
    max_val_tokens: 2000000
    seq_len: 512
    text_column: text
    tokenizer_name_or_path: gpt2
    truncation: true
    val_split: validation
  evaluation:
    batch_size: 4
    metrics:
    - val_bpb
    - runtime_ms
    - artifact_bytes
    num_workers: 4
    rng_seed: 42
    runtime_measurement:
      measure_batches: 50
      measure_load_time: true
      warmup_batches: 5
    seq_len: 512
  model:
    model_name_or_path: gpt2
    quantization:
      enabled: true
      fake_quant: false
      granularity: tensor
      observer: min_max
      quant_bits: 8
      round_mode: nearest
      scheme: per_tensor_symmetric
  serialization:
    compressor:
      level: 19
      name: zstd
    modes:
    - byte_group: null
      description: 'Baseline serialization: flat tensor-wise dump of 8-bit quantized
        weights

        in standard row-major order. No reordering of bytes beyond framework default.

        '
      name: default
    - byte_group: 64
      description: 'Byte-grouped serialization: for each quantized tensor, pack bytes
        into

        contiguous groups of 64 bytes, ordered by tensor index modulo 64.

        Concretely, for a flat byte array w[0..N-1], construct groups

        G_k = { w[i] | i % 64 == k } concatenated over k in [0, 63].

        Store the concatenation of all G_k as the serialized payload for that tensor.

        At load, invert this permutation exactly to reconstruct the original flat

        tensor bytes before dequantization.

        '
      name: byte_group_64
lane_id: lane_6
run_command: 'python main.py --model_name_or_path gpt2 --dataset_name wikitext --dataset_config_name
  wikitext-2-raw-v1 --data_root /workspace/data --output_dir /workspace/artifacts/lane_6_h1_byte_group_64_quickgate
  --quant_bits 8 --serialize_modes default byte_group_64 --compressor zstd --zstd_level
  19 --val_split validation --max_val_tokens 2000000 --batch_size 4 --seq_len 512
  --num_workers 4 --time_budget_s 1200

  '
success_criteria:
  detailed:
  - comparison: <
    description: "Require that the compressed artifact for byte_group_64 is strictly\
      \ smaller\nthan for default under identical zstd settings:\n  artifact_bytes(byte_group_64)\
      \ < artifact_bytes(default)\n"
    lhs: artifact_bytes[byte_group_64]
    name: artifact_size_improvement
    rhs: artifact_bytes[default]
  - comparison: <
    description: "Post-roundtrip val_bpb for byte_group_64 must be less than or equal\
      \ to\nbaseline (default) val_bpb (strict improvement required by quick-gate):\n\
      \  val_bpb(byte_group_64) < val_bpb(default)\n"
    lhs: val_bpb[byte_group_64]
    name: val_bpb_non_degradation
    rhs: val_bpb[default]
  - comparison: <=
    description: "End-to-end evaluation runtime (including model load + evaluation\
      \ loop)\nfor byte_group_64 must not exceed 1.10x that of default:\n  runtime_ms(byte_group_64)\
      \ <= 1.10 * runtime_ms(default)\n"
    lhs: runtime_ms[byte_group_64]
    name: runtime_constraint
    rhs: 1.10 * runtime_ms[default]
  - comparison: <=
    description: "Both modes must produce compressed artifacts under the 16 MB limit:\n\
      \  artifact_bytes(mode) <= 16,000,000\n"
    lhs: max(artifact_bytes[default], artifact_bytes[byte_group_64])
    name: artifact_cap
    rhs: '16000000'
  - comparison: ==
    description: "For both modes, after deserialization and dequantization to the\
      \ in-memory\nevaluation format, all model weights must match a reference checkpoint\n\
      bitwise (checked via tensor-wise SHA-256):\n  weights_sha256(byte_group_64)\
      \ == weights_sha256(default)\n"
    lhs: weights_sha256[byte_group_64]
    name: bitwise_weight_invariance
    rhs: 

... (truncated, see full artifact)
