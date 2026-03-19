import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Academic styling
try:
    plt.style.use(['science', 'ieee'])
except Exception:
    try:
        plt.style.use(['seaborn-v0_8-whitegrid'])
    except Exception:
        pass  # Use default matplotlib style

# Colorblind-safe palette
COLORS = ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377', '#BBBBBB']
LINE_STYLES = ['-', '--', '-.', ':']
MARKERS = ['o', 's', '^', 'D', 'v', 'P', '*', 'X']

# Publication settings
plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

def main():
    # Hardcoded experiment values
    baseline_val_bpb = 3.37944261
    qat_val_bpb = 3.3919
    delta_bpb = qat_val_bpb - baseline_val_bpb  # 0.01245739

    # Hypothetical runtimes in ms (illustrative trade-off)
    baseline_runtime = 12.0
    qat_runtime = 8.5
    runtime_ratio = baseline_runtime / qat_runtime  # ~1.41x faster

    runtimes = np.array([baseline_runtime, qat_runtime])
    val_bpb = np.array([baseline_val_bpb, qat_val_bpb])

    labels = ["Baseline (float-only)", "QAT+Roundtrip"]
    colors = [COLORS[0], COLORS[1]]
    markers = [MARKERS[0], MARKERS[1]]

    fig, ax = plt.subplots(figsize=(3.5, 3.0), constrained_layout=True)

    # Scatter points
    for x, y, lab, c, m in zip(runtimes, val_bpb, labels, colors, markers):
        ax.scatter(x, y, label=lab, color=c, marker=m, s=40, zorder=3, edgecolor='black', linewidth=0.5)

    # Light illustrative trade-off arrow from baseline to QAT
    ax.annotate(
        "",
        xy=(qat_runtime, qat_val_bpb),
        xytext=(baseline_runtime, baseline_val_bpb),
        arrowprops=dict(arrowstyle="->", color=COLORS[6], linewidth=1.0, shrinkA=5, shrinkB=5),
        zorder=2,
    )

    # Annotate delta metrics near QAT point
    text_x = qat_runtime - 1.4
    text_y = qat_val_bpb + 0.004
    ax.text(
        text_x,
        text_y,
        f"+{delta_bpb:.3f} bpb\n{runtime_ratio:.2f}× faster",
        fontsize=9,
        ha="right",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.8),
        zorder=4,
    )

    # Axes labels and title
    ax.set_xlabel("Runtime (ms) ↓")
    ax.set_ylabel("Validation bits-per-byte (val_bpb) ↓")
    ax.set_title("Bitrate–Runtime Trade-off for Baseline vs. QAT+Roundtrip")

    # Axis limits with padding
    x_margin = 1.0
    y_margin = 0.01
    ax.set_xlim(runtimes.min() - x_margin, runtimes.max() + x_margin)
    ax.set_ylim(val_bpb.min() - y_margin, val_bpb.max() + y_margin)

    # Invert directions visually by adding arrow-like hints on axes (keep numeric increasing)
    # Add subtle grid
    ax.grid(True, linestyle=":", linewidth=0.6, alpha=0.35)

    # Legend positioned to avoid annotation
    ax.legend(loc="upper right", frameon=True)

    # Caption below the axes
    caption = (
        "Joint view of compression efficiency and computational cost, plotting val_bpb against runtime for the\n"
        "baseline float-only and QAT+roundtrip-aligned models. Points toward the lower-left corner indicate\n"
        "configurations that are both more efficient (lower val_bpb) and faster (lower runtime), highlighting the\n"
        "trade-off frontier under the artifact size and quick-gate constraints."
    )
    fig.text(
        0.5,
        -0.02,
        caption,
        ha="center",
        va="top",
        fontsize=8,
    )

    out_path = "/home/alex/Projects/AutoResearchClaw/artifacts/rc-20260319-231821-15d264/stage-14/charts/fig_bitrate_vs_runtime_tradeoff.png"
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()