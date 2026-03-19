HYPERPARAMETERS = {
    "condition": "full_staged_QAT",          # single ablation: full staged QAT + compression reg + roundtrip
    "qat_enabled": True,
    "qat_start_frac": 0.5,
    "qat_group_size": 32,
    "compression_reg_enabled": True,
    "compression_reg_lambda": 1e-4,
    "compression_reg_scope": "final_proj,embed",
    "compression_reg_target": "teacher",
    "quant_error_weight": 1.0,               # defaulted to 1.0 for this lane
    "fake_quant_strength": 1.0,              # defaulted to 1.0 for this lane
    "seed": 1337,
}

import subprocess, os, re, time, sys
import json
import experiment_harness as _harness

def run_condition(extra_env: dict) -> tuple:
    """Run train_gpt.py with lane knobs. Returns (val_bpb, elapsed_ms)."""
    env = os.environ.copy()
    env.update({
        "DATA_PATH": "/home/alex/Projects/parameter-golf/data/datasets/fineweb10B_sp1024_1train",
        "TOKENIZER_PATH": "/home/alex/Projects/parameter-golf/data/tokenizers/fineweb_1024_bpe.model",
        "VOCAB_SIZE": "1024",
        "ITERATIONS": "20",
        "WARMUP_STEPS": "0",
        "VAL_LOSS_EVERY": "0",
        "MAX_VAL_TOKENS": "1000000",
        "SKIP_FINAL_INT8_ROUNDTRIP_EVAL": "1",
        "USE_COMPILE": "0",
        "SDP_CUDNN": "0",
        "SDP_FLASH": "1",
        "SDP_MEM_EFFICIENT": "0",
        "SDP_MATH": "0",
        "SEED": "1337",
    })
    env.update(extra_env)  # apply lane-specific knobs
    # Ensure outputs go to /tmp/pg_run as required
    env.setdefault("OUTPUT_DIR", "/tmp/pg_run/")
    os.makedirs(env["OUTPUT_DIR"], exist_ok=True)

    t0 = time.time()
    result = subprocess.run(
        [
            "/home/alex/Projects/parameter-golf/.venv/bin/torchrun",
            "--standalone",
            "--nproc_per_node=1",
            "/home/alex/Projects/parameter-golf/train_gpt.py",
        ],
        capture_output=True,
        text=True,
        env=env,
    )
    elapsed_ms = (time.time() - t0) * 1000.0
    output = result.stdout + result.stderr
    m = re.search(r"val_bpb[:\s=]+([0-9.]+)", output)
    if not m:
        raise RuntimeError(
            f"val_bpb not found in output (returncode={result.returncode})\n"
            f"Last 2000 chars:\n{output[-2000:]}"
        )
    return float(m.group(1)), elapsed_ms

def main():
    h = _harness.get_harness()

    # Baseline is already established — do NOT re-run it.
    # These numbers come from the official quick-harness baseline run (seed=1337, 20 steps).
    BASELINE_VAL_BPB = 3.37944261
    BASELINE_RUNTIME_MS = 62992.0
    GATE_RUNTIME_MS = BASELINE_RUNTIME_MS * 1.10  # 69291ms

    # Candidate: run train_gpt.py with lane-specific knobs only
    # Implement exactly ONE ablation: "full staged QAT" with compression+roundtrip knobs.
    candidate_env = {
        "QAT_ENABLED": "1",
        "QAT_START_FRAC": str(HYPERPARAMETERS["qat_start_frac"]),
        "QAT_GROUP_SIZE": str(HYPERPARAMETERS["qat_group_size"]),
        "COMPRESSION_REG_ENABLED": "1",
        "COMPRESSION_REG_LAMBDA": f"{HYPERPARAMETERS['compression_reg_lambda']}",
        "COMPRESSION_REG_SCOPE": HYPERPARAMETERS["compression_reg_scope"],
        "COMPRESSION_REG_TARGET": HYPERPARAMETERS["compression_reg_target"],
        "ROUNDTRIP_AWARE_TRAINING": "1",
        "ROUNDTRIP_INT8_ENABLED": "1",
        "ROUNDTRIP_CODEC": "zlib",
        # These two lane knobs are mentioned but not explicitly wired in the env plan;
        # we expose them as generic env vars so train_gpt.py can optionally consume them.
        "QUANT_ERROR_WEIGHT": f"{HYPERPARAMETERS['quant_error_weight']}",
        "FAKE_QUANT_STRENGTH": f"{HYPERPARAMETERS['fake_quant_strength']}",
    }

    candidate_bpb, candidate_ms = run_condition(candidate_env)

    h.report_metric("val_bpb", candidate_bpb)
    h.report_metric("candidate_runtime_ms", candidate_ms)
    h.report_metric("baseline_val_bpb", BASELINE_VAL_BPB)
    h.report_metric("baseline_runtime_ms", BASELINE_RUNTIME_MS)
    h.report_metric("delta_bpb", candidate_bpb - BASELINE_VAL_BPB)
    h.report_metric("runtime_ratio", candidate_ms / BASELINE_RUNTIME_MS)

    gate_passed = (candidate_bpb < BASELINE_VAL_BPB) and (candidate_ms <= GATE_RUNTIME_MS)
    h.report_metric("quick_gate_passed", float(gate_passed))
    h.finalize()

    # Write hyperparameters + metrics to results.json for the paper table.
    collected_metrics = {
        "val_bpb": candidate_bpb,
        "candidate_runtime_ms": candidate_ms,
        "baseline_val_bpb": BASELINE_VAL_BPB,
        "baseline_runtime_ms": BASELINE_RUNTIME_MS,
        "delta_bpb": candidate_bpb - BASELINE_VAL_BPB,
        "runtime_ratio": candidate_ms / BASELINE_RUNTIME_MS,
        "quick_gate_passed": float(gate_passed),
    }
    results = {"hyperparameters": HYPERPARAMETERS, "metrics": collected_metrics}
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()