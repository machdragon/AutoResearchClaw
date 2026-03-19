---
created: '2026-03-19T22:11:21+00:00'
evidence:
- stage-03/search_plan.yaml
- stage-03/sources.json
- stage-03/queries.json
id: search_strategy-rc-20260319-220921-d02b4b
run_id: rc-20260319-220921-d02b4b
stage: 03-search_strategy
tags:
- search_strategy
- stage-03
- run-rc-20260
title: 'Stage 03: Search Strategy'
---

# Stage 03: Search Strategy

high_level_strategy:
- Combine three literature streams: 1) Strong small-scale recurrent/sequence models
    on enwik8/text8 with explicit parameter counts and/or model sizes. 2) LoRA and
    related low-rank adapters, with any work applying them to RNNs or recurrent/sequence
    models and reporting overhead. 3) Lightweight gating/routing and conditional computation
    (scalar or small-vector gates, few-expert MoE), especially when constrained by
    latency or on-device deployment.
- Emphasize sources that report:
  - Exact or approximate model size (MB) or parameter counts.
  - Validation/test bpb or bits-per-character on enwik8/text8.
  - Inference/runtime or latency measurements; ideally overhead due to adapters/gates.
- Where direct evidence is missing, prioritize methodology papers to guide experimental
  design and budget splits.
key_entities:
- recurrent language model
- RWKV, SRNN, Mogrifier LSTM, QRNN, GRU, LSTM
- LoRA, low-rank adaptation, adapters
- mixture-of-experts, routing, gating, residual gates, conditional computation
- byte-level language modeling, enwik8, text8
- model compression, small models, on-device deployment
overall_objective: "Identify architectures, parameterizations, and empirical results\
  \ relevant to:\n  - Byte-level recurrent language models (e.g., enwik8/text8) optimized\
  \ for low bits-per-byte (bpb).\n  - Very small deployment artifacts (<= 16MB total,\
  \ including base + LoRA + gates).\n  - Low runtime overhead: added LoRA and routing/gating\
  \ must keep inference/training runtime within 1.10x of a recurrence-only baseline.\n\
  Focus on configurations where starting from a recurrence-only model and adding LoRA\
  \ specialization plus residual gating improves validation bpb at fixed artifact\
  \ budget.\n"
prioritization:
- first: baseline_recurrence_and_parameter_budget
- second: lora_for_recurrent_and_sequence_models
- third: on_device_and_small_model_constraints
- fourth: gating_routing_lightweight_moe
- fifth: pareto_frontiers_and_eval_methodology
search_blocks:
- extraction:
  - architecture type and details (RNN, LSTM, GRU, RWKV, SSM etc.)
  - parameter counts and any explicit MB sizes
  - validation/test bpb/bpc on enwik8/text8 or similar
  - reported training/inference runtime, throughput, or latency
  - scaling trends of performance vs parameters for small models (<50M params)
  filters:
    types:
    - paper
    - preprint
    - benchmark
    - blog
    years:
    - 2015
    - 2026
  goal: 'Establish best known bpb for small recurrent/sequence models under tight
    parameter/size budgets and extract guidance on architecture choice and parameter
    scaling.

    '
  name: baseline_recurrence_and_parameter_budget
  queries:
  - query: '"enwik8" "bits per byte" recurrent OR RNN OR LSTM OR GRU OR "RWKV" OR
      "state space" "parameter count" "model size"

      '
    tags:
    - baseline
    - enwik8
    - recurrence
  - query: '"enwik8" "bits-per-character" LSTM OR GRU OR QRNN OR "mogrifier LSTM"
      "number of parameters" OR "million parameters"

      '
    tags:
    - baseline
    - bpc
    - rnn
  - query: 'RWKV language model enwik8 bits per byte

      '
    tags:
    - rwkv
    - baseline
  - query: '"small" "recurrent neural network" "language model" "on-device" "<20MB"
      OR "edge" latency

      '
    tags:
    - on_device
    - small_models
  - query: '"state space models" "enwik8" OR "character-level" "bpc" "parameter count"

      '
    tags:
    - ssm
    - baseline
- extraction:
  - specific matrices/layers where LoRA is applied in any RNN/sequence LM (input-to-hidden,
    hidden-to-hidden, output, attention, etc.)
  - rank choices and their effect on validation metrics
  - parameter overhead formulas and typical % overhead at given ranks
  - any runtime/latency measurements or claims about minimal overhead
  - design heuristics for allocating LoRA budget across layers
  filters:
    types:
    - paper
    - preprint
    - blog
    - code
    years:
    - 2019
    - 2026
  goal: 'Understand where and how to inject LoRA (or similar low-rank adapters) into
    recurrent or sequence models and quantify parameter vs performance trade-offs
    and runtime overhead.

    '
  name: lora_for_recurrent_and_sequence_models
  queries:
  - query: 'LoRA "low-rank adaptation" recurrent OR RNN OR LSTM OR GRU OR "sequence
      model" enwik8 OR language modeling

      '
    tags:
    - lora
    - rnn
  - query: '"LoRA" "language model" "parameter-efficient" adapters gating

      '
    tags:
    - lora
    - lm
  - query: '"low-rank" adapters "RNN" OR "LSTM" "language modeling"

      '
    tags:
    - low_rank
    - rnn
  - query: '"parameter-efficient fine-tuning" "recurrent" OR "sequence" model

      '
    tags:
    - peft
    - sequence
  - query: '"LoRA" "rank" r=2 OR r=4 OR r=8 language model parameters overhead

      '
    tags:
    - lora_rank
- extraction:
  - gate types (scalar per layer, vector per channel, small MLP) and para

... (truncated, see full artifact)


{
  "sources": [
    {
      "id": "s1",
      "name": "arXiv",
      "type": "paper_index",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "\"enwik8\" \"bits per byte\" recurrent OR RNN OR LSTM OR GRU OR \"RWKV\" OR \"state space\" \"parameter count\" \"model size\"",
      "verified_at": null
    },
    {
      "id": "s2",
      "name": "Papers With Code - enwik8 benchmarks",
      "type": "benchmark_index",
      "url": "https://paperswithcode.com/sota/language-modelling-on-enwik8",
      "status": "planned",
      "query": "enwik8 bits per byte recurrent OR RNN OR RWKV OR LSTM parameter count",
      "verified_at": null
    },
    {
      "id": "s3",
      "name": "RWKV official repository and docs",
      "type": "code_repo",
      "url": "https://github.com/BlinkDL/RWKV-LM",
      "status": "planned",
      "query": "enwik8 bits-per-byte parameter count small RWKV model",
      "verified_at": null
    },
    {
      "id": "s4",
      "name": "Original LoRA paper (Hu et al. 2021+)",
      "type": "paper",
      "url": "https://arxiv.org/abs/2106.09685",
      "status": "planned",
      "query": "\"LoRA\" \"low-rank adaptation\" language model runtime overhead",
      "verified_at": null
    },
    {
      "id": "s5",
      "name": "LoRA and PEFT implementations (e.g., Hugging Face PEFT)",
      "type": "code_repo",
      "url": "https://github.com/huggingface/peft",
      "status": "planned",
      "query": "LoRA implementation overhead rank r runtime",
      "verified_at": null
    },
    {
      "id": "s6",
      "name": "Parameter-efficient tuning for RNN/sequence models",
      "type": "paper_index",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "\"low-rank\" adapters \"RNN\" OR \"LSTM\" \"language modeling\"",
      "verified_at": null
    },
    {
      "id": "s7",
      "name": "Lightweight MoE / gating for language models",
      "type": "paper_index",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "\"mixture of experts\" \"lightweight\" \"few experts\" \"gating\" \"latency\" language model",
      "verified_at": null
    },
    {
      "id": "s8",
      "name": "Conditional computation / scalar gating in deep nets",
      "type": "paper_index",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "\"scalar gating\" residual neural network language modeling",
      "verified_at": null
    },
    {
      "id": "s9",
      "name": "On-device and tiny LM work (e.g., edge/phone LMs)",
      "type": "paper_index",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "\"on-device\" \"language model\" quantization 8-bit \"model size\"",
      "verified_at": null
    },
    {
      "id": "s10",
      "name": "Tiny / mobile LM repositories",
      "type": "code_repo",
      "url": "https://github.com",
      "status": "planned",
      "query": "\"tiny\" \"language model\" \"mobile\" \"Android\" recurrent",
      "verified_at": null
    },
    {
      "id": "s11",
      "name": "Pareto trade-off analyses for model size vs latency vs accuracy",
      "type": "paper_index",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "\"Pareto frontier\" \"model size\" \"latency\" \"accuracy\" \"language model\"",
      "verified_at": null
    },
    {
      "id": "s12",
      "name": "State-space or RNN SOTA on enwik8 (e.g., S4, retina-like SSMs)",
      "type": "paper_index",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "\"state space\" model enwik8 bits per character parameter count",
      "verified_at": null
    }
  ],
  "count": 12,
  "generated": "2026-03-19T22:11:21+00:00"
}

{
  "queries": [
    "Parameter Golf val bpb minimization lane",
    "Parameter Golf val bpb benchmark",
    "Parameter Golf val bpb survey",
    "Golf val bpb minimization",
    "Parameter Golf val comparison",
    "Parameter Golf val deep learning",
    "val bpb minimization lane"
  ],
  "year_min": 2020
}