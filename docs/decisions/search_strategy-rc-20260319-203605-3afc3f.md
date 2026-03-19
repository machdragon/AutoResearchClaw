---
created: '2026-03-19T20:38:53+00:00'
evidence:
- stage-03/search_plan.yaml
- stage-03/sources.json
- stage-03/queries.json
id: search_strategy-rc-20260319-203605-3afc3f
run_id: rc-20260319-203605-3afc3f
stage: 03-search_strategy
tags:
- search_strategy
- stage-03
- run-rc-20260
title: 'Stage 03: Search Strategy'
---

# Stage 03: Search Strategy

deduplication:
  fuzzy_threshold: 0.9
  method: title_doi_hash
filters:
  language:
  - en
  min_year: 2020
  peer_review_preferred: true
generated: '2026-03-19T20:38:53+00:00'
search_strategies:
- max_results_per_query: 60
  name: keyword_core
  queries:
  - Parameter Golf val_bpb minimization — lane_6
  - Byte-grouped serialization for artifact compression. Hypothesis
  - If we serialize quantized weights with byte-grouped packing
  - artifact bytes will decrease without hurting
  - golf val_bpb
  sources:
  - arxiv
  - semantic_scholar
  - openreview
- depth: 1
  name: backward_forward_citation
  queries:
  - val_bpb minimization
  - minimization byte-grouped
  - byte-grouped serialization
  sources:
  - semantic_scholar
  - google_scholar
topic: 'Parameter Golf val_bpb minimization — lane_6: Byte-grouped serialization for
  artifact compression. Hypothesis: If we serialize quantized weights with byte-grouped
  packing, artifact bytes will decrease without hurting post-roundtrip val_bpb. Artifact
  limit 16MB. Quick-gate: runtime <= 1.10x baseline.'


{
  "sources": [
    {
      "id": "s1",
      "name": "Dettmers et al., \"GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers\"",
      "type": "paper",
      "url": "https://arxiv.org/abs/2210.17323",
      "status": "planned",
      "query": "GPTQ weight packing layout 4-bit transformer",
      "verified_at": null
    },
    {
      "id": "s2",
      "name": "Lin et al., \"AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration\"",
      "type": "paper",
      "url": "https://arxiv.org/abs/2306.00978",
      "status": "planned",
      "query": "AWQ weight packing int4 int8 LLM",
      "verified_at": null
    },
    {
      "id": "s3",
      "name": "Tim Dettmers et al., bitsandbytes library documentation and source",
      "type": "library_docs",
      "url": "https://github.com/TimDettmers/bitsandbytes",
      "status": "planned",
      "query": "bitsandbytes 4-bit quantization weight packing layout",
      "verified_at": null
    },
    {
      "id": "s4",
      "name": "GGUF format specification (GGML/GGUF quantized model format)",
      "type": "spec",
      "url": "https://github.com/ggerganov/ggml/tree/master/docs",
      "status": "planned",
      "query": "GGUF weight format bit layout 4-bit 8-bit",
      "verified_at": null
    },
    {
      "id": "s5",
      "name": "TensorRT INT8/INT4 quantization and engine serialization docs",
      "type": "library_docs",
      "url": "https://docs.nvidia.com/deeplearning/tensorrt/developer-guide/index.html",
      "status": "planned",
      "query": "TensorRT int8 weight format bit packing checkpoint serialization",
      "verified_at": null
    },
    {
      "id": "s6",
      "name": "TensorFlow Lite quantization specification and converter docs",
      "type": "library_docs",
      "url": "https://www.tensorflow.org/lite/performance/quantization_spec",
      "status": "planned",
      "query": "TFLite int8 quantization weight layout serialization",
      "verified_at": null
    },
    {
      "id": "s7",
      "name": "ONNX Runtime quantization format and per-channel scale/zero-point handling",
      "type": "library_docs",
      "url": "https://onnxruntime.ai/docs/performance/quantization.html",
      "status": "planned",
      "query": "ONNX quantization format per-channel scales zero points layout",
      "verified_at": null
    },
    {
      "id": "s8",
      "name": "Apache TVM quantization and packed weight layout (relay.quantize, int8/int4)",
      "type": "library_docs",
      "url": "https://tvm.apache.org/docs",
      "status": "planned",
      "query": "TVM quantized weight packing layout int8 int4",
      "verified_at": null
    },
    {
      "id": "s9",
      "name": "Marlin: 4-bit Matrix Multiplication for Transformers (int4 kernel and packing scheme)",
      "type": "paper_or_repo",
      "url": "https://github.com/IST-DASLab/marlin",
      "status": "planned",
      "query": "Marlin LLM quantization kernel int4 performance packed weights",
      "verified_at": null
    },
    {
      "id": "s10",
      "name": "Liu et al., \"LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale\"",
      "type": "paper",
      "url": "https://arxiv.org/abs/2208.07339",
      "status": "planned",
      "query": "LLM.int8 weight packing layout",
      "verified_at": null
    },
    {
      "id": "s11",
      "name": "General bit-plane coding and entropy analysis for quantized data (survey/example paper)",
      "type": "paper",
      "url": "https://scholar.google.com/scholar?q=%22bit-plane+coding%22+quantized+integer+lossless",
      "status": "planned",
      "query": "\"bit-plane coding\" quantized integer lossless entropy",
      "verified_at": null
    },
    {
      "id": "s12",
      "name": "Checkpoint/model artifact compression for deep neural networks (representative paper)",
      "type": "paper",
      "url": "https://scholar.google.com/scholar?q=\"neural+network\"+\"checkpoint+compression\"+\"lossless\"",
      "status": "planned",
      "query": "\"neural network\" \"checkpoint compression\" \"lossless\"",
      "verified_at": null
    },
    {
      "id": "s13",
      "name": "System papers on LLM serving and model loading (e.g., vLLM, FlexGen, etc.)",
      "type": "paper",
      "url": "https://arxiv.org/search/?query=LLM+serving+checkpoint+compression+loading&searchtype=all",
      "status": "planned",
      "query": "\"LLM serving\" checkpoint compression loading quantization",
      "verified_at": null
    },
    {
      "id": "s14",
      "name": "GGML/GGUF performance discussions for packed quantized weights",
      "type": "repo_docs",
      "url": "https://github.com/ggerganov/llama.cpp",
      "status": "planned",
      "query": "GGML GGUF quantization performance packed weights",
      "verified_at": null
    },
    {
      "id": "s15",
      "name": "Reproducibility and determinism in quantized inference (representative study)",
      "type": "paper",
      "url"

... (truncated, see full artifact)


{
  "queries": [
    "Parameter Golf val_bpb minimization \u2014 lane_6",
    "Byte grouped serialization artifact compression Hypothesis",
    "If we serialize quantized weights with byte-grouped packing",
    "artifact bytes will decrease without hurting",
    "golf val_bpb",
    "val_bpb minimization",
    "minimization byte-grouped",
    "byte-grouped serialization"
  ],
  "year_min": 2020
}