---
created: '2026-03-19T22:19:46+00:00'
evidence:
- stage-11/schedule.json
id: resource_planning-rc-20260319-220921-d02b4b
run_id: rc-20260319-220921-d02b4b
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
      "id": "prep-env",
      "name": "Validate environment and config for lane_1_H1_global_gate_lora",
      "depends_on": [],
      "gpu_count": 0,
      "estimated_minutes": 2,
      "priority": 1
    },
    {
      "id": "train-H1-lane1",
      "name": "Train recurrent_rwkv with global_sequence gate + LoRA on wikitext-2 (20 steps)",
      "depends_on": [
        "prep-env"
      ],
      "gpu_count": 1,
      "estimated_minutes": 10,
      "priority": 1
    },
    {
      "id": "eval-H1-lane1",
      "name": "Evaluate val_bpb and runtime vs quick_harness baseline; verify artifacts <=16MB",
      "depends_on": [
        "train-H1-lane1"
      ],
      "gpu_count": 1,
      "estimated_minutes": 5,
      "priority": 1
    }
  ],
  "total_gpu_budget": 1,
  "generated": "2026-03-19T00:00:00Z"
}