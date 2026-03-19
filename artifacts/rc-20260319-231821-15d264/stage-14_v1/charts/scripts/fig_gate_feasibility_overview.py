
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

# Data
conditions = ['metrics']
values = [3.3919]
ci_low = [3.3919]
ci_high = [3.3919]

# Plot
fig, ax = plt.subplots(figsize=(3.5, 3.0))
x = np.arange(len(conditions))
bar_colors = [COLORS[i % len(COLORS)] for i in range(len(conditions))]

yerr_lo = [max(0, v - lo) for v, lo in zip(values, ci_low)]
yerr_hi = [max(0, hi - v) for v, hi in zip(values, ci_high)]

bars = ax.bar(x, values, color=bar_colors, alpha=0.85, edgecolor="white", linewidth=0.5)
ax.errorbar(x, values, yerr=[yerr_lo, yerr_hi],
            fmt="none", ecolor="#333", capsize=4, capthick=1.2, linewidth=1.2)

# Value labels
offset = max(yerr_hi) * 0.08 if yerr_hi and max(yerr_hi) > 0 else max(values) * 0.02
for i, v in enumerate(values):
    ax.text(i, v + offset, f"{v:.4f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

ax.set_xlabel("Constraint Type")
ax.set_ylabel("Pass (1) / Fail (0)")
ax.set_title("Feasibility Under Runtime and Artifact Constraints")
ax.set_xticks(x)
ax.set_xticklabels([c.replace("_", " ") for c in conditions], rotation=25, ha="right", fontsize=9)
ax.grid(True, axis="y", alpha=0.3)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig("/home/alex/Projects/AutoResearchClaw/artifacts/rc-20260319-231821-15d264/stage-14/charts/fig_gate_feasibility_overview.png")
plt.close(fig)
print(f"Saved: /home/alex/Projects/AutoResearchClaw/artifacts/rc-20260319-231821-15d264/stage-14/charts/fig_gate_feasibility_overview.png")
