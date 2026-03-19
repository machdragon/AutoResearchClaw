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

# Hardcoded data from experiment description
baseline_val_bpb = 3.37944261
qat_roundtrip_val_bpb = 3.3919

categories = ["Baseline (float-only)", "QAT + roundtrip-aligned"]
values = np.array([baseline_val_bpb, qat_roundtrip_val_bpb])

# Figure setup
fig, ax = plt.subplots(figsize=(3.5, 3.0))

x = np.arange(len(categories))
bar_width = 0.6

bars = ax.bar(
    x,
    values,
    width=bar_width,
    color=[COLORS[0], COLORS[1]],
    edgecolor="black",
    linewidth=0.8,
)

# Axis labels and title
ax.set_title("Validation bpb Comparison: Float Training vs QAT + Roundtrip Alignment")
ax.set_xlabel("Training / Compression Strategy")
ax.set_ylabel("Validation bits-per-byte (val_bpb)")

# X-axis ticks
ax.set_xticks(x)
ax.set_xticklabels(categories, rotation=15, ha="right")

# Add numeric value labels above bars
for rect, val in zip(bars, values):
    height = rect.get_height()
    ax.text(
        rect.get_x() + rect.get_width() / 2.0,
        height + 0.002,
        f"{val:.3f}",
        ha="center",
        va="bottom",
    )

# Optional slight y-limits padding for clarity
y_min = min(values) * 0.995
y_max = max(values) * 1.005
ax.set_ylim(y_min, y_max)

# Add a compact caption-like note below the plot area, inside figure
caption = (
    "Lower val_bpb indicates better compression performance.\n"
    "Baseline (float-only) vs QAT with roundtrip-aware compression alignment under the same budget."
)
fig.text(0.5, -0.02, caption, ha="center", va="top", fontsize=8)

fig.tight_layout()

output_path = "/home/alex/Projects/AutoResearchClaw/artifacts/rc-20260319-231821-15d264/stage-14/charts/fig_main_results_val_bpb.png"
fig.savefig(output_path, format="png")
plt.close(fig)

print(f"Saved: {output_path}")