# Insights Readout

A written summary of what the analysis found and what to do about it.

## 1. The funnel leaks most at cart to payment

Of 12,840 sessions, 97.2% reach item discovery, 42.7% reach cart creation, 30.8% reach address selection, and 27.9% reach a successful payment.

The largest raw drop is discovery to cart, at 56.0%. That is a browsing behaviour. Most people who open a product are not ready to buy, and that is normal in quick commerce. The drop that is worth fixing is cart to payment, because those users have already decided to buy.

## 2. First time buyers drop twice as hard as repeat buyers

First time buyers drop from cart to payment at 37.0%. Repeat buyers drop at 17.7%. Repeat buyers are simply more practised. They have a saved address and they know the total cost. The gap of 19 points is the value of a smooth first checkout.

This matters beyond the first order. Users whose first checkout was rough repeat less. The 30 day repeat rate is 13.1% overall, and it is lower for the channels and checkout paths with the most friction.

## 3. Late fee disclosure costs about 11 points

When the delivery fee is first shown at the payment step, first time buyer cart drop is 43.0%. When it is shown at the cart, it is 32.0%.

45.1% of first time sessions see the fee late. If every one of those sessions saw it at the cart instead, the blended first time cart drop would fall from 37.0% to roughly 32%, which is worth about 3 points of checkout conversion.

This is the cheapest fix in the study. It is a placement change, not a build.

## 4. Every address step costs conversion

| Steps | Address rate | Cart drop |
| --- | --- | --- |
| 1 | 76.2% | 33.7% |
| 2 | 77.6% | 31.2% |
| 3 | 66.7% | 39.4% |
| 4 | 56.3% | 47.3% |

One and two step entry behave the same. The damage starts at three steps. Going from two to four steps loses about 21 points of cart users. The fix is a single screen with saved addresses and pin code auto fill.

## 5. Paid traffic is the weakest and has the most headroom

| Channel | Conversion | First time cart drop | 30 day repeat |
| --- | --- | --- | --- |
| Organic | 33.8% | 34.1% | 18.9% |
| Referral | 31.8% | 30.4% | 14.5% |
| Push | 27.0% | 38.7% | 11.7% |
| Influencer | 24.1% | 40.5% | 9.9% |
| Paid Ads | 23.0% | 40.6% | 8.3% |

Paid Ads brings the most sessions (3,802) and converts the worst (23.0%), and also retains the worst (8.3%). The pattern says paid traffic arrives with lower intent. Lower intent users are less tolerant of friction, so checkout fixes should help paid traffic the most. Roll the fixes out to paid traffic first and read the result per channel.

## 6. Payments fail more than they should

10.6% of payment attempts fail. Today a failed payment sends the user back to the cart, and many do not come back. A one tap retry that keeps the cart and address intact is a small build with a clear path to recovery.

## 7. What to do

1. Move the delivery fee to the cart screen. Expected impact: about 3 points of first time conversion.
2. Collapse address entry to one screen with saved addresses and pin code auto fill. Expected impact: recover most of the 21 point loss between two and four steps.
3. Add one tap UPI retry on failure. Expected impact: recover a share of the 10.6% failed attempts.
4. Roll out to paid traffic first.

Together the A/B plan projects a 14% relative lift in checkout conversion and a 9% relative lift in 30 day repeat.

## 8. How to be sure

These effect sizes come from simulated data, so they should be treated as hypotheses. The A/B test plan in `docs/ab_test_plan.md` lays out how to confirm them in production: a two arm user level test, 2,372 users per arm for the conversion read, and a 90 day window for the retention read.

## 9. What we would watch after launch

- Cart creation rate, in case showing the fee earlier deters cart adds.
- Address entry error rate, in case the single screen lets bad addresses through.
- Payment retry success, to size the value of the retry flow.
- Repeat rate by channel, to confirm the checkout fixes also lift lifetime value.
