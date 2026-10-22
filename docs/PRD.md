# PRD: Streamlined Checkout for First Time Buyers

Status: Draft for review
Owner: Product
Version: 1.0
Last updated: October 2026

## 1. Summary

First time buyers drop out of checkout at a rate of 37.2% between cart creation and payment. Repeat buyers drop out at 21.0%. The gap is friction, not intent. This document proposes a streamlined checkout that removes the two largest sources of that friction: late delivery fee disclosure and multi step address entry. It also adds a one tap UPI retry for failed payments.

## 2. Problem

Quick commerce checkout has four steps today: item discovery, cart creation, address selection and payment.

From 12,824 analysed sessions:

- 42.7% of sessions reach cart creation.
- 30.8% reach address selection.
- 27.7% reach a successful payment.

The largest absolute drop is discovery to cart, but that is a browsing behaviour and not a checkout defect. The drop that matters for this PRD is cart to payment, where the user has already decided to buy.

Two findings stand out.

**Finding 1: late fee reveal.** When the delivery fee is shown only at the payment step, first time buyer cart drop is 43.5%. When it is shown at the cart, it is 32.2%. 44.6% of first time sessions currently see the fee late.

**Finding 2: address steps.** Address entry with one or two steps holds around 77% of cart users. At four steps it holds 54.5%. The cart drop at four steps is 50.8% versus 30.9% at one step.

A third, smaller finding: payment failures happen on 10.5% of payment attempts, and there is no retry path other than going back to the cart.

## 3. Goals

Primary goal: increase first time buyer checkout conversion from 25.8% to at least 29.4% (a 14% relative lift) within one quarter of launch.

Secondary goal: increase 30 day repeat rate from 13.2% to 14.4% (a 9% relative lift), by removing the negative first experience that suppresses return visits.

Non goals: pricing, catalogue, delivery logistics, and the discovery to cart step.

## 4. Target user

First time buyers on mobile, who are 77.3% of sessions. Within that group, users arriving from paid traffic, who have the highest cart drop at 41.9% and the lowest repeat rate at 9.2%.

## 5. Proposed changes

### 5.1 Fee transparency at cart

Show the delivery fee and the final payable amount on the cart screen, above the checkout button, before any address is entered.

Rationale: this alone moves the cart drop from 43.5% to 32.2% in the current data.

Acceptance criteria:
- Delivery fee and total are visible on the cart screen for every session.
- The fee does not change between cart and payment.
- If the fee cannot be computed before address entry, show a clear "calculated at checkout, free over Rs 499" line and honour it.

### 5.2 One screen address entry

Replace the multi step address flow with a single screen that combines saved addresses, pin code auto fill, and a manual entry fallback.

Rationale: address entry at one or two steps holds 77% of cart users versus 54.5% at four steps.

Acceptance criteria:
- New users can enter a full address on one screen.
- Returning users see saved addresses at the top and can select one in a single tap.
- Pin code auto fills city and state.
- Address entry never exceeds two screens.

### 5.3 One tap UPI retry

On payment failure, keep the user in a payment sheet with a retry button instead of returning them to the cart.

Rationale: 10.5% of payment attempts fail, and today those users must restart from the cart.

Acceptance criteria:
- On failure, the user stays on the payment step.
- A retry button re initiates the same UPI intent.
- The cart and address are preserved.
- Failure reason is shown in plain language.

### 5.4 Paid traffic routing

Send paid traffic to the streamlined checkout first.

Rationale: paid traffic has the most to gain, with the highest drop and lowest repeat.

## 6. User stories

- As a first time buyer, I want to know the total cost before I enter my address, so I am not surprised at payment.
- As a first time buyer, I want to enter my address on one screen, so checkout does not feel long.
- As a buyer whose UPI payment failed, I want to retry without losing my cart, so I can finish my order.
- As a returning buyer, I want to pick a saved address in one tap, so reordering is fast.

## 7. Success metrics

| Metric | Current | Target | Window |
| --- | --- | --- | --- |
| First time checkout conversion | 25.8% | 29.4% | 4 weeks post launch |
| Cart to payment drop, first time | 37.2% | 32.0% | 4 weeks post launch |
| Address step drop | 27.9% | under 22% | 4 weeks post launch |
| 30 day repeat rate | 13.2% | 14.4% | 90 days post launch |
| Payment retry success | not tracked | 40% of failures | 4 weeks post launch |

Guardrail metrics: order cancellation rate, payment failure rate, and support ticket volume must not increase by more than 5%.

## 8. Scope

In scope: cart screen, address screen, payment screen, and the event tracking that supports them.

Out of scope: item discovery, search, catalogue, pricing, and logistics.

## 9. Risks

- Fee shown at cart may reduce cart creation, because users see the cost earlier. Monitor cart creation rate as a guardrail.
- Single screen address entry may increase invalid addresses. Mitigate with pin code validation and address autocomplete.
- Paid traffic may not respond the same way as organic. Roll out channel by channel and read results per channel.

## 10. Rollout

Phase 1: build and internal test, 2 weeks.
Phase 2: A/B test on 50% of first time buyers, 4 weeks. See `docs/ab_test_plan.md`.
Phase 3: full rollout to first time buyers on mobile.
Phase 4: rollout to returning buyers and desktop.

## 11. Open questions

- Can the delivery fee be computed before address entry for all pin codes?
- What is the right retry limit for UPI before we suggest another payment method?
- Should the streamlined checkout be the default for returning buyers, or only for first time buyers?

## 12. Wireframes

See `docs/wireframes.html` for the before and after screens.
