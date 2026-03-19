---
created: '2026-03-19T22:34:15+00:00'
evidence:
- stage-15/decision.md
- stage-15/decision_structured.json
id: research_decision-rc-20260319-220921-d02b4b
run_id: rc-20260319-220921-d02b4b
stage: 15-research_decision
tags:
- research_decision
- stage-15
- run-rc-20260
title: 'Stage 15: Research Decision'
---

# Stage 15: Research Decision

## Decision

REFINE

## Justification

The system warning about a “degenerate REFINE cycle” is advisory, not a relaxation of the explicit decision rules. By your stated criteria, PROCEED is disallowed unless **all** minimum quality conditions are met. They are not:

1. Only single-run (n=1) metrics are available per condition; the ≥3 seeds requirement is violated.
2. The ablation checker reports that nominally different variants are behaviorally identical, indicating compromised ablation integrity.
3. The run is marked failed (`ModuleNotFoundError: No module named 'harness'`), so the pipeline is not yet trustworthy.
4. Runtime metrics are clearly broken (`runtime_ratio = 0.0` for all variants), so latency-related claims cannot be substantiated.
5. The analysis quality rating is 2/10, below the ≥4/10 threshold.

Because at least one — and in fact several — of the PROCEED criteria fail, I must choose REFINE, not PROCEED, regardless of the degenerate-cycle warning.

A PIVOT is not warranted because the conceptual hypotheses (small recurrent backbone + LoRA + gating under strict runtime/size constraints; global vs token-wise gating effects) remain coherent and well-motivated. The issues are infrastructural and methodological, not conceptual.

## Evidence

- **Seed replication lacking**
  - “n = 1 for all metrics (no replication).”  
  - Violates: “Each condition has results from ≥3 seeds.”

- **Ablation integrity violated**
  - “Ablation checker reports: all three ‘recurrence_*’ conditions produce identical outputs across all metrics.”
  - Violates: “No identical per-seed values across different conditions (ablation integrity).”

- **Run and infrastructure failures**
  - “Run is marked failed due to `ModuleNotFoundError: No module named 'harness'`.”
  - Reported metrics come from a failed, non-reproducible run.

- **Broken runtime metrics**
  - “All `runtime_ratio = 0.0`, `quick_gate_passed = 1.0`.”
  - Runtimes inconsistent across baseline vs variants (baseline ~62,992 ms vs others ~0.004–0.014 ms), showing instrumentation is invalid.

- **Low analysis quality rating**
  - Explicitly rated: “Result Quality Rating: 2 / 10.”  
  - Violates: “The analysis quality rating is ≥4/10.”

- **System warning context**
  - “SYSTEM WARNING — DEGENERATE REFINE CYCLE DETECTED… You SHOULD choose PROCEED with a quality caveat rather than REFINE again.”
  - This is guidance, but does not override the hard logical rule: “If ANY criterion is not met, you MUST choose REFINE (not PROCEED).”

## Next Actions

Focus on making the *same* hypotheses testable and the pipeline trustworthy; do not change the scientific direction yet.

1. **Fix condition wiring and ablation integrity**
   - Ensure `recurrence_only`, `recurrence_lora`, and `recurrence_lora_gated`:
     - Instantiate different parameter sets (parameter counts differ as expected).
     - Produce measurably different logits on a fixed batch of inputs.
   - Add a small unit test:
     - Build each condition with a fixed seed.
     - Run on a fixed synthetic batch.
     - Assert that at least one metric (e.g., mean absolute logit difference) differs above a small threshold between each pair of conditions.
   - Only proceed to full runs once this test passes.

2. **Repair the harness and pipeline reliability**
   - Resolve `No module named 'harness'`:
     - Add harness as a dependency, or vendor the module; verify import in a clean environment.
   - Create a minimal CI-style “smoke run”:
     - Single tiny batch, single step, all conditions.
     - Verifies: import success, forward pass, metric logging, and ablation test.
   - Require this smoke run to pass before launching any large or multi-seed experiments.

3. **Make runtime and artifact constraints first-class**
   - Define a fixed runtime protocol:
     - Hardware (GPU model, CPU), batch size, sequence length, warmup iterations, number of timed iterations.
   - Implement correct timing:
     - Use appropriate synchronization (`torch.cuda.synchronize()` etc.) and log per-condition mean ± std latency.
     - Compute `runtime_ratio` relative to a clearly specified baseline (e.g., large uncompressed baseline or recurrent baseline).
   - Log artifact size:
     - Persist each model.
     - Measure total bytes on disk.
     - Enforce a hard ≤16MB constraint for the “tiny” regime; fail the run if exceeded.

4. **Introduce proper replication**
   - Plan for ≥3–5 seeds per condition:
     - Different seeds for initialization and data order.
   - Aggregate metrics:
     - Log mean ± std for val_bpb and runtime.
   - Use this to estimate the noise floor so that future improvements can be meaningfully interpreted.

5. **Add hypothesis-relevant diagnostics**
   - For the gating hypothesis (H1: global vs token-wise gating behavior):
     - Implement logging of gate activations (mean, variance, entropy, sparsity).
     - Add head vs tail token bpb and short vs long sequence bpb, if feasible.
   - For LoRA:
     - Log adapter parameter co

... (truncated, see full artifact)


{
  "decision": "refine",
  "raw_text_excerpt": "## Decision\n\nREFINE\n\n## Justification\n\nThe system warning about a \u201cdegenerate REFINE cycle\u201d is advisory, not a relaxation of the explicit decision rules. By your stated criteria, PROCEED is disallowed unless **all** minimum quality conditions are met. They are not:\n\n1. Only single-run (n=1) metrics are available per condition; the \u22653 seeds requirement is violated.\n2. The ablation checker reports that nominally different variants are behaviorally identical, indicating compromised ablation integri",
  "quality_warnings": [],
  "generated": "2026-03-19T22:34:15+00:00"
}