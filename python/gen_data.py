import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dpath = os.path.join(root, "data")
os.makedirs(dpath, exist_ok=True)

n_users = 11700
start = pd.Timestamp("2026-08-01")
days = 61

chan = ["Paid Ads", "Organic", "Push", "Referral", "Influencer"]
cw = [0.30, 0.25, 0.20, 0.13, 0.12]

dev = ["Android", "iOS", "Web"]
dw = [0.62, 0.16, 0.22]

tier = ["Tier 1", "Tier 2", "Tier 3"]
tw = [0.48, 0.34, 0.18]

pay = ["UPI", "Card", "Wallet", "COD"]
pw = [0.63, 0.19, 0.06, 0.12]

chan_cart = {"Paid Ads": 0.90, "Organic": 1.12, "Push": 1.00, "Referral": 1.06, "Influencer": 0.95}
chan_addr = {"Paid Ads": 0.94, "Organic": 1.08, "Push": 1.00, "Referral": 1.04, "Influencer": 0.97}

u_id = np.arange(100001, 100001 + n_users)
u_chan = rng.choice(chan, n_users, p=cw)
u_dev = rng.choice(dev, n_users, p=dw)
u_tier = rng.choice(tier, n_users, p=tw)
u_day = rng.integers(0, days, n_users)
u_date = start + pd.to_timedelta(u_day, unit="D")

users = pd.DataFrame({
    "user_id": u_id,
    "acq_channel": u_chan,
    "device": u_dev,
    "city_tier": u_tier,
    "signup_date": u_date.date,
})


def sim(pv, pc, pa, pp):
    v = rng.random() < pv
    c = bool(v) and rng.random() < pc
    a = c and rng.random() < pa
    p = a and rng.random() < pp
    return v, c, a, p


def make_session(sid, uid, ch, dv, tr, ts, new):
    pc = (0.42 if new else 0.58) * chan_cart[ch]
    pa = (0.84 if new else 0.90) * chan_addr[ch]
    pp = 0.90 if new else 0.94
    pp *= {"Android": 0.98, "iOS": 1.03, "Web": 1.00}[dv]
    pp *= {"Tier 1": 1.02, "Tier 2": 1.00, "Tier 3": 0.95}[tr]

    late = rng.random() < (0.45 if new else 0.25)
    if new:
        steps = int(rng.choice([1, 2, 3, 4], p=[0.18, 0.34, 0.31, 0.17]))
    else:
        steps = int(rng.choice([1, 2, 3], p=[0.62, 0.28, 0.10]))

    pa2 = pa
    if late:
        pa2 *= 0.80
    if steps == 3:
        pa2 *= 0.86
    if steps == 4:
        pa2 *= 0.72

    val = round(float(rng.lognormal(5.75, 0.5)), 2)
    fee = 0.0 if val >= 499 else float(rng.choice([29, 39, 49]))

    v, c, a, p = sim(0.97, pc, pa2, pp)

    evs = []
    base = ts
    t = base
    if v:
        t = t + pd.Timedelta(seconds=int(rng.integers(3, 25)))
        evs.append(("item_view", t))
        for _ in range(int(rng.integers(1, 4))):
            t = t + pd.Timedelta(seconds=int(rng.integers(2, 20)))
            evs.append(("item_view", t))
    if c:
        t = t + pd.Timedelta(seconds=int(rng.integers(5, 40)))
        evs.append(("add_to_cart", t))
        t = t + pd.Timedelta(seconds=int(rng.integers(2, 15)))
        evs.append(("checkout_start", t))
    if a:
        t = t + pd.Timedelta(seconds=int(rng.integers(8, 60)))
        evs.append(("select_address", t))
    if p:
        t = t + pd.Timedelta(seconds=int(rng.integers(10, 90)))
        evs.append(("payment_attempt", t))
        if rng.random() < 0.06:
            t = t + pd.Timedelta(seconds=int(rng.integers(3, 25)))
            evs.append(("payment_failed", t))
            t = t + pd.Timedelta(seconds=int(rng.integers(4, 40)))
        evs.append(("payment_success", t))
    elif a:
        t = t + pd.Timedelta(seconds=int(rng.integers(10, 60)))
        evs.append(("payment_attempt", t))
        if rng.random() < 0.5:
            t = t + pd.Timedelta(seconds=int(rng.integers(3, 25)))
            evs.append(("payment_failed", t))

    pm = rng.choice(pay, p=pw)
    if fee > 0 and rng.random() < 0.35:
        pm = "COD"
    fee_stage = "payment" if late else "cart"

    srow = {
        "session_id": sid,
        "user_id": uid,
        "ts": base,
        "channel": ch,
        "device": dv,
        "city_tier": tr,
        "is_new": int(new),
        "cart_value": val,
        "delivery_fee": fee,
        "fee_stage": fee_stage,
        "addr_steps": steps,
        "reached_view": int(v),
        "reached_cart": int(c),
        "reached_addr": int(a),
        "reached_pay": int(p),
        "converted": int(p),
        "payment_method": pm if p else "",
    }
    erows = [{
        "session_id": sid,
        "user_id": uid,
        "ts": et,
        "event": en,
        "channel": ch,
        "device": dv,
        "is_new": int(new),
        "cart_value": val,
        "delivery_fee": fee,
        "fee_stage": fee_stage,
    } for en, et in evs]
    return srow, erows


sessions = []
events = []
sid = 500001
orders = []
oid = 900001

for i in range(n_users):
    ts = pd.Timestamp(u_date[i]) + pd.Timedelta(hours=int(rng.integers(7, 23)), minutes=int(rng.integers(0, 60)))
    s, e = make_session(sid, int(u_id[i]), u_chan[i], u_dev[i], u_tier[i], ts, True)
    sessions.append(s)
    events.extend(e)
    if s["converted"]:
        orders.append({
            "order_id": oid,
            "user_id": int(u_id[i]),
            "session_id": sid,
            "order_ts": ts + pd.Timedelta(minutes=int(rng.integers(2, 10))),
            "amount": s["cart_value"],
            "delivery_fee": s["delivery_fee"],
            "payment_method": s["payment_method"],
            "status": "delivered",
        })
        oid += 1
        ret_p = 0.50 if u_chan[i] == "Organic" else 0.36
        if s["fee_stage"] == "payment":
            ret_p *= 0.82
        if s["addr_steps"] >= 3:
            ret_p *= 0.88
        k = 0
        if rng.random() < ret_p:
            k = 1
        if rng.random() < ret_p * 0.45:
            k = 2
        for j in range(k):
            gap = int(rng.integers(1, 44))
            ts2 = ts + pd.Timedelta(days=gap, hours=int(rng.integers(0, 10)))
            if ts2 > start + pd.Timedelta(days=days - 1):
                break
            sid += 1
            s2, e2 = make_session(sid, int(u_id[i]), u_chan[i], u_dev[i], u_tier[i], ts2, False)
            sessions.append(s2)
            events.extend(e2)
            if s2["converted"]:
                orders.append({
                    "order_id": oid,
                    "user_id": int(u_id[i]),
                    "session_id": sid,
                    "order_ts": ts2 + pd.Timedelta(minutes=int(rng.integers(2, 10))),
                    "amount": s2["cart_value"],
                    "delivery_fee": s2["delivery_fee"],
                    "payment_method": s2["payment_method"],
                    "status": "delivered",
                })
                oid += 1
    sid += 1

sdf = pd.DataFrame(sessions)
edf = pd.DataFrame(events)
odf = pd.DataFrame(orders)
edf = edf.sort_values(["session_id", "ts"]).reset_index(drop=True)
edf.insert(0, "event_id", np.arange(7000001, 7000001 + len(edf)))
edf["ts"] = edf["ts"].dt.strftime("%Y-%m-%d %H:%M:%S")
sdf["ts"] = sdf["ts"].dt.strftime("%Y-%m-%d %H:%M:%S")
odf["order_ts"] = odf["order_ts"].dt.strftime("%Y-%m-%d %H:%M:%S")

sdf.to_csv(os.path.join(dpath, "sessions.csv"), index=False)
edf.to_csv(os.path.join(dpath, "events.csv"), index=False)
odf.to_csv(os.path.join(dpath, "orders.csv"), index=False)
users.to_csv(os.path.join(dpath, "users.csv"), index=False)

print("users", len(users))
print("sessions", len(sdf))
print("events", len(edf))
print("orders", len(odf))
new = sdf[sdf.is_new == 1]
cart = new.reached_cart.sum()
conv = new.reached_pay.sum()
print("new cart", cart, "conv", conv, "drop", round((cart - conv) / cart * 100, 1))
rep = sdf[sdf.is_new == 0]
cart2 = rep.reached_cart.sum()
conv2 = rep.reached_pay.sum()
print("rep cart", cart2, "conv", conv2, "drop", round((cart2 - conv2) / cart2 * 100, 1))
