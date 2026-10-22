import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
o = os.path.join(root, "outputs")
c = os.path.join(o, "charts")
os.makedirs(c, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 150,
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#c8ccd4",
    "axes.labelcolor": "#2b2f38",
    "text.color": "#2b2f38",
    "xtick.color": "#5b6270",
    "ytick.color": "#5b6270",
    "font.family": "DejaVu Sans",
})

ind = "#4f46e5"
tea = "#0d9488"
amb = "#d97706"
red = "#dc2626"
gray = "#94a3b8"

f = pd.read_csv(os.path.join(o, "funnel_overall.csv"))
fig, ax = plt.subplots(figsize=(8, 4.6))
y = np.arange(len(f))[::-1]
bars = ax.barh(y, f.pct_of_top, color=[ind, "#6366f1", "#818cf8", "#a5b4fc"], height=0.62)
ax.set_yticks(y)
ax.set_yticklabels(f.stage)
ax.set_xlim(0, 110)
ax.set_xlabel("Share of sessions reaching stage (%)")
for b, v, u in zip(bars, f.pct_of_top, f.users):
    ax.text(v + 2, b.get_y() + b.get_height() / 2, f"{v:.1f}%  ({u:,})", va="center", fontsize=9.5)
for i, r in f.iterrows():
    if i > 0:
        ax.text(1.5, y[i] - 0.42, f"drop {r.step_drop:.1f}%", fontsize=8.5, color=red)
ax.set_title("Checkout funnel, all sessions", fontsize=13, weight="bold", loc="left")
fig.tight_layout()
fig.savefig(os.path.join(c, "funnel_overall.png"))
plt.close(fig)

ch = pd.read_csv(os.path.join(o, "channel_performance.csv")).sort_values("new_cart_drop")
fig, ax = plt.subplots(figsize=(8, 4.4))
x = np.arange(len(ch))
ax.bar(x - 0.2, ch.new_cart_drop, 0.4, label="First time buyers", color=ind)
ax.bar(x + 0.2, ch.cart_drop, 0.4, label="All buyers", color=tea)
ax.set_xticks(x)
ax.set_xticklabels(ch.channel)
ax.set_ylabel("Cart to payment drop off (%)")
ax.legend(frameon=False)
ax.set_title("Cart drop off by acquisition channel", fontsize=13, weight="bold", loc="left")
for i, v in enumerate(ch.new_cart_drop):
    ax.text(i - 0.2, v + 0.6, f"{v:.1f}", ha="center", fontsize=8.5)
fig.tight_layout()
fig.savefig(os.path.join(c, "dropoff_by_channel.png"))
plt.close(fig)

rc = pd.read_csv(os.path.join(o, "retention_curve.csv"))
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(rc.day, rc.repeat_rate, marker="o", color=ind, linewidth=2.4)
ax.fill_between(rc.day, rc.repeat_rate, color=ind, alpha=0.10)
for xx, yy in zip(rc.day, rc.repeat_rate):
    ax.text(xx, yy + 0.7, f"{yy:.1f}%", ha="center", fontsize=9)
ax.set_xlabel("Days after first order")
ax.set_ylabel("Repeat rate (%)")
ax.set_ylim(0, max(rc.repeat_rate) * 1.35)
ax.set_title("Repeat purchase curve after first order", fontsize=13, weight="bold", loc="left")
fig.tight_layout()
fig.savefig(os.path.join(c, "retention_curve.png"))
plt.close(fig)

fr = pd.read_csv(os.path.join(o, "fee_disclosure_impact.csv"))
fig, ax = plt.subplots(figsize=(7, 4.2))
bars = ax.bar(fr.fee_bucket, fr.cart_drop, color=[tea, red], width=0.5)
for b, v in zip(bars, fr.cart_drop):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.6, f"{v:.1f}%", ha="center", fontsize=10.5)
ax.set_ylabel("Cart drop off, first time buyers (%)")
ax.set_ylim(0, 55)
ax.set_title("Impact of late delivery fee disclosure", fontsize=13, weight="bold", loc="left")
fig.tight_layout()
fig.savefig(os.path.join(c, "fee_disclosure.png"))
plt.close(fig)

ar = pd.read_csv(os.path.join(o, "address_steps_impact.csv"))
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.bar(ar.addr_steps.astype(str), ar.cart_drop, color=[tea, tea, amb, red], width=0.55)
for i, v in enumerate(ar.cart_drop):
    ax.text(i, v + 0.7, f"{v:.1f}%", ha="center", fontsize=10)
ax.set_xlabel("Address entry steps")
ax.set_ylabel("Cart drop off, first time buyers (%)")
ax.set_ylim(0, 55)
ax.set_title("Impact of multi step address entry", fontsize=13, weight="bold", loc="left")
fig.tight_layout()
fig.savefig(os.path.join(c, "address_steps.png"))
plt.close(fig)

base = 26.03
lift = 14
fig, ax = plt.subplots(figsize=(7, 4.2))
vals = [base, base * (1 + lift / 100)]
bars = ax.bar(["Current", "Projected with fixes"], vals, color=[gray, ind], width=0.5)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.4, f"{v:.1f}%", ha="center", fontsize=11)
ax.set_ylabel("Checkout conversion, first time buyers (%)")
ax.set_ylim(0, 34)
ax.annotate("", xy=(1, vals[1]), xytext=(0, vals[0]),
            arrowprops=dict(arrowstyle="->", color=red, lw=1.6))
ax.text(0.5, vals[1] - 2.4, "+14% relative", color=red, ha="center", fontsize=10)
ax.set_title("Projected checkout conversion lift", fontsize=13, weight="bold", loc="left")
fig.tight_layout()
fig.savefig(os.path.join(c, "ab_projection.png"))
plt.close(fig)

print("charts written")
