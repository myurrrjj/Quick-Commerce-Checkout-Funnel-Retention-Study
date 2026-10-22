import os
import numpy as np
import pandas as pd

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.join(root, "data")
o = os.path.join(root, "outputs")
os.makedirs(o, exist_ok=True)

s = pd.read_csv(os.path.join(d, "sessions.csv"), parse_dates=["ts"])
e = pd.read_csv(os.path.join(d, "events.csv"), parse_dates=["ts"])
od = pd.read_csv(os.path.join(d, "orders.csv"), parse_dates=["order_ts"])
u = pd.read_csv(os.path.join(d, "users.csv"))

steps = ["reached_view", "reached_cart", "reached_addr", "reached_pay"]
names = ["Item discovery", "Cart creation", "Address selection", "Payment done"]

tot = len(s)
rows = []
prev = tot
for c, n in zip(steps, names):
    k = int(s[c].sum())
    rows.append({
        "stage": n,
        "users": k,
        "pct_of_top": round(k / tot * 100, 2),
        "step_rate": round(k / prev * 100, 2) if prev else 0,
        "step_drop": round((prev - k) / prev * 100, 2) if prev else 0,
    })
    prev = k
funnel = pd.DataFrame(rows)
funnel.to_csv(os.path.join(o, "funnel_overall.csv"), index=False)

def funnel_for(df, label):
    t = len(df)
    out = []
    p = t
    for c, n in zip(steps, names):
        k = int(df[c].sum())
        out.append({
            "segment": label,
            "stage": n,
            "users": k,
            "pct_of_top": round(k / t * 100, 2) if t else 0,
            "step_rate": round(k / p * 100, 2) if p else 0,
        })
        p = k
    return out

seg = []
seg += funnel_for(s[s.is_new == 1], "First time")
seg += funnel_for(s[s.is_new == 0], "Repeat")
segdf = pd.DataFrame(seg)
segdf.to_csv(os.path.join(o, "funnel_by_user_type.csv"), index=False)

ch_rows = []
for ch, g in s.groupby("channel"):
    t = len(g)
    cart = int(g.reached_cart.sum())
    conv = int(g.reached_pay.sum())
    newg = g[g.is_new == 1]
    ncart = int(newg.reached_cart.sum())
    nconv = int(newg.reached_pay.sum())
    ch_rows.append({
        "channel": ch,
        "sessions": t,
        "cart_rate": round(cart / t * 100, 2),
        "conv_rate": round(conv / t * 100, 2),
        "cart_drop": round((cart - conv) / cart * 100, 2) if cart else 0,
        "new_cart_drop": round((ncart - nconv) / ncart * 100, 2) if ncart else 0,
        "aov": round(g[g.converted == 1].cart_value.mean(), 2),
    })
chdf = pd.DataFrame(ch_rows).sort_values("conv_rate", ascending=False)
chdf.to_csv(os.path.join(o, "channel_performance.csv"), index=False)

new = s[s.is_new == 1].copy()
new["fee_bucket"] = np.where(new.fee_stage == "payment", "Fee shown late", "Fee shown at cart")
fr = new.groupby("fee_bucket").apply(lambda g: pd.Series({
    "sessions": len(g),
    "cart": int(g.reached_cart.sum()),
    "conv": int(g.reached_pay.sum()),
    "cart_drop": round((g.reached_cart.sum() - g.reached_pay.sum()) / g.reached_cart.sum() * 100, 2),
}), include_groups=False).reset_index()
fr.to_csv(os.path.join(o, "fee_disclosure_impact.csv"), index=False)

ar = new.groupby("addr_steps").apply(lambda g: pd.Series({
    "sessions": len(g),
    "cart": int(g.reached_cart.sum()),
    "conv": int(g.reached_pay.sum()),
    "addr_rate": round(g.reached_addr.sum() / g.reached_cart.sum() * 100, 2),
    "cart_drop": round((g.reached_cart.sum() - g.reached_pay.sum()) / g.reached_cart.sum() * 100, 2),
}), include_groups=False).reset_index()
ar.to_csv(os.path.join(o, "address_steps_impact.csv"), index=False)

first = od.sort_values("order_ts").groupby("user_id", as_index=False).first()
first = first.rename(columns={"order_ts": "first_ts"})
first["cohort"] = first["first_ts"].dt.to_period("W").astype(str)
last = od.groupby("user_id", as_index=False).order_ts.max().rename(columns={"order_ts": "last_ts"})
cnt = od.groupby("user_id", as_index=False).size().rename(columns={"size": "orders"})
sec = od.sort_values("order_ts").groupby("user_id").order_ts.apply(
    lambda x: x.iloc[1] if len(x) > 1 else pd.NaT).rename("second_ts").reset_index()
r = first.merge(last, on="user_id").merge(cnt, on="user_id").merge(sec, on="user_id")
r["gap"] = (r["last_ts"] - r["first_ts"]).dt.days
r["gap2"] = (r["second_ts"] - r["first_ts"]).dt.days
r["repeat30"] = ((r["orders"] >= 2) & (r["gap2"] <= 30)).astype(int)
r["repeat_any"] = (r["orders"] >= 2).astype(int)
ch_map = u.set_index("user_id").acq_channel.to_dict()
r["channel"] = r.user_id.map(ch_map)

coh = r.groupby("cohort").apply(lambda g: pd.Series({
    "users": len(g),
    "orders": int(g.orders.sum()),
    "repeat_any": round(g.repeat_any.mean() * 100, 2),
    "repeat30": round(g.repeat30.mean() * 100, 2),
    "aov": round(od[od.user_id.isin(g.user_id)].amount.mean(), 2),
}), include_groups=False).reset_index()
coh.to_csv(os.path.join(o, "cohort_retention.csv"), index=False)

rch = r.groupby("channel").apply(lambda g: pd.Series({
    "users": len(g),
    "repeat30": round(g.repeat30.mean() * 100, 2),
    "orders_per_user": round(g.orders.mean(), 2),
}), include_groups=False).reset_index().sort_values("repeat30", ascending=False)
rch.to_csv(os.path.join(o, "retention_by_channel.csv"), index=False)

curve = []
for dd in [1, 3, 7, 14, 21, 30]:
    curve.append({"day": dd, "repeat_rate": round((r.gap2 <= dd).mean() * 100, 2)})
pd.DataFrame(curve).to_csv(os.path.join(o, "retention_curve.csv"), index=False)

rep = int((r.orders >= 2).sum())
summary = {
    "sessions": int(len(s)),
    "events": int(len(e)),
    "users": int(s.user_id.nunique()),
    "orders": int(len(od)),
    "overall_conv": round(s.converted.mean() * 100, 2),
    "new_conv": round(s[s.is_new == 1].converted.mean() * 100, 2),
    "new_cart_drop": round(
        (new.reached_cart.sum() - new.reached_pay.sum()) / new.reached_cart.sum() * 100, 2),
    "repeat_cart_drop": round(
        (s[s.is_new == 0].reached_cart.sum() - s[s.is_new == 0].reached_pay.sum())
        / s[s.is_new == 0].reached_cart.sum() * 100, 2),
    "aov": round(od.amount.mean(), 2),
    "repeat_rate30": round(r.repeat30.mean() * 100, 2),
    "repeat_users": rep,
    "fee_late_share": round((new.fee_stage == "payment").mean() * 100, 2),
    "mobile_share": round(s.device.isin(["Android", "iOS"]).mean() * 100, 2),
}
pd.Series(summary).to_csv(os.path.join(o, "kpi_summary.csv"), header=False)

print(funnel.to_string(index=False))
print()
print(chdf.to_string(index=False))
print()
print(fr.to_string(index=False))
print()
print(ar.to_string(index=False))
print()
print(rch.to_string(index=False))
print()
print(pd.Series(summary).to_string())
