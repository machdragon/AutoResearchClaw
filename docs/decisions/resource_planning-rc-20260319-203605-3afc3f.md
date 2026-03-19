---
created: '2026-03-19T20:59:04+00:00'
evidence:
- stage-11/schedule.json
id: resource_planning-rc-20260319-203605-3afc3f
run_id: rc-20260319-203605-3afc3f
stage: 11-resource_planning
tags:
- resource_planning
- stage-11
- run-rc-20260
title: 'Stage 11: Resource Planning'
---

# Stage 11: Resource Planning

{
  "tasks": [
    {
      "id": "env-check",
      "name": "Environment & data setup validation (offline, WikiText-2 present)",
      "depends_on": [],
      "gpu_count": 0,
      "estimated_minutes": 3,
      "priority": 1
    },
    {
      "id": "quant-impl-default",
      "name": "Implement & unit-test 8-bit post-hoc quantization + default serialization",
      "depends_on": [
        "env-check"
      ],
      "gpu_count": 0,
      "estimated_minutes": 10,
      "priority": 1
    },
    {
      "id": "quant-impl-bytegroup",
      "name": "Implement & unit-test byte_group_64 serialization + inverse permutation",
      "depends_on": [
        "env-check"
      ],
      "gpu_count": 0,
      "estimated_minutes": 12,
      "priority": 1
    },
    {
      "id": "bitwise-checks",
      "name": "Bitwise equality tests for weights and outputs (default vs byte_group_64)",
      "depends_on": [
        "quant-impl-default",
        "quant-impl-bytegroup"
      ],
      "gpu_count": 1,
      "estimated_minutes": 6,
      "priority": 1
    },
    {
      "id": "quickgate-default",
      "name": "Quick-gate evaluation: default serialization (runtime, val_bpb, artifact_bytes)",
      "depends_on": [
        "bitwise-checks"
      ],
      "gpu_count": 1,
      "estimated_minutes": 6,
      "priority": 1
    },
    {
      "id": "quickgate-bytegroup",
      "name": "Quick-gate evaluation: byte_group_64 serialization (runtime, val_bpb, artifact_bytes)",
      "depends_on": [
        "bitwise-checks"
      ],
      "gpu_count": 1,
      "estimated_minutes": 6,
      "priority": 1
    },
    {
      "id": "success-criteria-check",
      "name": "Check quick-gate success criteria (artifact size, val_bpb, runtime, invariance)",
      "depends_on": [
        "quickgate-default",
        "quickgate-bytegroup"
      ],
      "gpu_count": 0,
      "estimated_minutes": 2,
      "priority": 1
    },
    {
      "id": "baseline-full-ft-plan",
      "name": "Planning only: Full Fine-Tuning baseline (no run in quick-gate)",
      "depends_on": [],
      "gpu_count": 0,
      "estimated_minutes": 5,
      "priority": 3
    },
    {
      "id": "baseline-lora-plan",
      "name": "Planning only: LoRA baseline (no run in quick-gate)",
      "depends_on": [],
      "gpu_count": 0,
      "estimated_minutes": 5,
      "priority": 3
    },
    {
      "id": "baseline-qlora-plan",
      "name": "Planning only: QLoRA baseline (no run in quick-gate)",
      "depends_on": [],
      "gpu_count": 0,
      "estimated_minutes": 5,
      "priority": 3
    }
  ],
  "total_gpu_budget": {
    "gpu_count": 1,
    "estimated_total_gpu_minutes": 20
  },
  "generated": "2026-03-19T00:00:00Z"
}