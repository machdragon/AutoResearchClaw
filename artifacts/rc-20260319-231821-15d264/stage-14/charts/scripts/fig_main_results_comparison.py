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
    # Hardcoded experiment data
    baseline_val_bpb = 3.37944261
    qat_val_bpb = 3.3919
    delta_bpb = qat_val_bpb - baseline_val_bpb

    strategies = [
        "Float-only\n(baseline)",
        "QAT + int8\nroundtrip-aligned",
    ]
    values = np.array([baseline_val_bpb, qat_val_bpb])

    # Figure and axis
    fig, ax = plt.subplots(figsize=(3.5, 3.0), constrained_layout=False)

    x = np.arange(len(strategies))
    width = 0.6

    # Bars
    bars = ax.bar(
        x,
        values,
        width=width,
        color=[COLORS[0], COLORS[1]],
        edgecolor='black',
        linewidth=0.8,
    )

    # Axis labels and title
    ax.set_ylabel("Validation bits-per-byte (val_bpb) ↓")
    ax.set_xlabel("Training / Deployment Strategy")
    ax.set_title("Validation bpb for Float-only vs. QAT+Roundtrip-aligned Models")

    # X ticks
    ax.set_xticks(x)
    ax.set_xticklabels(strategies)

    # Y limits with small padding
    ymin = min(values) - 0.01
    ymax = max(values) + 0.02
    ax.set_ylim(ymin, ymax)

    # Enable a light grid on y-axis if not already styled
    ax.yaxis.grid(True, linestyle=':', linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)

    # Legend placed below the axes to avoid crowding with annotations
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=COLORS[0], ec='black', lw=0.8),
        plt.Rectangle((0, 0), 1, 1, color=COLORS[1], ec='black', lw=0.8),
    ]
    labels = ["Float-only baseline", "QAT + roundtrip-aligned"]
    ax.legend(
        handles,
        labels,
        loc='upper center',
        bbox_to_anchor=(0.5, -0.12),
        ncol=1,
        frameon=False,
    )

    # Delta annotation: bracket between bars
    x0, x1 = x[0], x[1]
    y0, y1 = values[0], values[1]
    y_mid = max(y0, y1) + 0.003

    # Horizontal bracket line from left to right bar
    ax.plot(
        [x0, x1],
        [y_mid, y_mid],
        color='black',
        linewidth=0.8,
        clip_on=False,
    )
    # Small vertical ticks at each bar
    tick_height = 0.002
    ax.plot([x0, x0], [y_mid - tick_height, y_mid + tick_height],
            color='black', linewidth=0.8, clip_on=False)
    ax.plot([x1, x1], [y_mid - tick_height, y_mid + tick_height],
            color='black', linewidth=0.8, clip_on=False)

    # Delta text
    delta_text = f"Δ = {delta_bpb:+.3f} bpb"
    ax.text(
        (x0 + x1) / 2.0,
        y_mid + 0.003,
        delta_text,
        ha='center',
        va='bottom',
    )

    # Annotate numerical values atop bars
    for xi, val in zip(x, values):
        ax.text(
            xi,
            val + 0.002,
            f"{val:.3f}",
            ha='center',
            va='bottom',
        )

    # Ensure layout is tight to avoid clipping labels and annotations
    fig.tight_layout()

    output_path = "/home/alex/Projects/AutoResearchClaw/artifacts/rc-20260319-231821-15d264/stage-14/charts/fig_main_results_comparison.png"
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    main()