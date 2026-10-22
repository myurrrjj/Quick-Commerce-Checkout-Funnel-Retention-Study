# A/B Test Plan: Streamlined Checkout

## 1. Objective

Measure whether the streamlined checkout (fee at cart, one screen address, one tap UPI retry) improves first time buyer checkout conversion, without harming guardrail metrics.

## 2. Hypotheses

H1: Showing the delivery fee at the cart increases first time buyer checkout conversion.

H2: Reducing address entry to one screen increases the cart to address step rate.

H3: One tap UPI retry increases payment retry success and reduces cart abandonment after failure.

H4: A better first checkout experience increases 30 day repeat rate.

## 3. Design

Type: two arm randomised controlled test.
Unit of randomisation: user, not session, so a user sees the same experience across sessions.
Arms:
- Control: current checkout.
- Treatment: streamlined checkout.

Split: 50 / 50.
Eligibility: first time buyers on mobile web and app.
Exclusions: users with an existing cart at test start, and internal accounts.

## 4. Primary metric

First time buyer checkout conversion, defined as sessions reaching a successful payment divided by sessions reaching cart creation.

Baseline: 25.8%.
Target: 29.4%, a 14% relative lift.

## 5. Secondary metrics

- Cart to address step rate. Baseline 70.1% for first time buyers.
- Cart to payment drop. Baseline 37.2%.
- Address step drop. Baseline 27.9%.
- Payment retry success rate. Not tracked today.
- 30 day repeat rate. Baseline 13.2%.

## 6. Guardrail metrics

- Cart creation rate. Must not fall by more than 3% relative, since showing the fee earlier could deter cart creation.
- Order cancellation rate.
- Payment failure rate.
- Support tickets per 1,000 orders.
- Average order value. Baseline Rs 358.

## 7. Sample size

Assumptions: two sided test, alpha 0.05, power 0.80.

| Metric | Baseline | Detectable lift | Sample per arm |
| --- | --- | --- | --- |
| Checkout conversion | 25.8% | +14% relative | 2,402 |
| Address step drop | 27.9% | -21% relative | 853 |
| 30 day repeat | 13.2% | +9% relative | 13,269 |

At roughly 192 first time sessions per day, the conversion test needs about 2,400 per arm, or 4,800 total, which is about 25 days. Plan for 4 weeks of running time to cover weekly seasonality.

Note on retention: the repeat metric needs about 13,300 per arm to detect a 9% relative lift at 80% power. That is more than a 4 week window can supply. Read retention after 90 days, and treat the 4 week number as directional only. If retention is the decision metric, extend the test window or increase the traffic share.

## 8. Duration

Minimum 4 weeks. Do not stop early on a positive peek, since that inflates false positives. One interim read at 2 weeks is allowed for guardrails only.

## 9. Analysis plan

- Run a two proportion z test on the primary metric.
- Report relative lift with a 95% confidence interval.
- Segment results by channel, since paid traffic has the largest gap to close.
- Check sample ratio mismatch before reading any result.
- Apply no peeking corrections for the primary metric. Guardrail peeks use a Bonferroni adjusted threshold.

## 10. Projected impact

| Metric | Baseline | Projected | Basis |
| --- | --- | --- | --- |
| Checkout conversion | 25.8% | 29.4% | 14% relative lift |
| Cart to payment drop | 37.2% | 32.0% | fee and address fixes |
| 30 day repeat | 13.2% | 14.4% | better first experience |

If the treatment delivers the fee fix alone, the cart drop for the affected 44.6% of first time sessions moves from 43.5% to 32.2%, which is worth roughly 3 points of conversion on its own. The address fix adds the rest.

## 11. Decision rules

Ship if: primary metric improves by at least 10% relative with p under 0.05, and no guardrail degrades by more than 5%.

Iterate if: primary metric improves but a guardrail degrades, or the lift is under 10%.

Stop if: primary metric does not improve, or any guardrail degrades by more than 5% with significance.

## 12. Risks and mitigations

- Novelty effect on returning users: restrict the primary read to first time buyers.
- Channel mix shift during the test: monitor channel mix daily and use a fixed randomisation.
- Fee change mid test: freeze pricing for the duration.

## 13. Rollout after a win

1. Roll out to first time buyers on mobile.
2. Extend to paid traffic first, given the largest headroom.
3. Extend to returning buyers and desktop.
4. Re run the guardrail read one week after full rollout.
