# Mixpanel Tracking Plan

This is the event spec that powers the funnel and retention views in Mixpanel. It maps one to one with the `events` table in `data/events.csv`.

## 1. Naming rules

- Event names use snake_case.
- Event names describe what the user did, not what the system did.
- Property names use snake_case.
- Every event carries the super properties listed below.

## 2. Super properties

These are attached to every event automatically.

| Property | Type | Description |
| --- | --- | --- |
| user_id | string | Stable user identifier. |
| session_id | string | Session identifier, regenerated per visit. |
| channel | string | Acquisition channel. One of Paid Ads, Organic, Push, Referral, Influencer. |
| device | string | Android, iOS or Web. |
| city_tier | string | Tier 1, Tier 2 or Tier 3. |
| is_new | boolean | True if the user has never ordered. |
| app_version | string | Client build. |
| ts | timestamp | Event time in ISO 8601. |

## 3. Events

### item_view
Fired when a product detail view is opened.

| Property | Type | Description |
| --- | --- | --- |
| product_id | string | Product viewed. |
| category | string | Category name. |
| price | number | Unit price in rupees. |
| position | number | Position in the feed, if from a list. |

### add_to_cart
Fired when an item is added to the cart.

| Property | Type | Description |
| --- | --- | --- |
| product_id | string | Product added. |
| quantity | number | Units added. |
| price | number | Unit price in rupees. |
| cart_value | number | Cart total after the add. |

### checkout_start
Fired when the user taps the checkout button on the cart.

| Property | Type | Description |
| --- | --- | --- |
| cart_value | number | Cart total. |
| delivery_fee | number | Delivery fee, zero if free. |
| fee_stage | string | cart or payment, where the fee was first shown. |
| item_count | number | Distinct items in cart. |

### select_address
Fired when an address is chosen or saved.

| Property | Type | Description |
| --- | --- | --- |
| addr_steps | number | Number of steps the user went through. |
| addr_source | string | saved, autocomplete or manual. |
| pin_code | string | Delivery pin code. |

### payment_attempt
Fired when the user taps pay.

| Property | Type | Description |
| --- | --- | --- |
| payment_method | string | UPI, Card, Wallet or COD. |
| amount | number | Total payable. |
| delivery_fee | number | Delivery fee. |

### payment_failed
Fired when a payment attempt fails.

| Property | Type | Description |
| --- | --- | --- |
| payment_method | string | Method used. |
| reason | string | Failure reason code. |
| attempt_number | number | Which attempt this was. |

### payment_success
Fired when a payment succeeds.

| Property | Type | Description |
| --- | --- | --- |
| payment_method | string | Method used. |
| amount | number | Total paid. |
| order_id | string | Order created. |
| attempt_number | number | Which attempt succeeded. |

## 4. User profile properties

| Property | Type | Description |
| --- | --- | --- |
| first_order_date | date | Date of first order. |
| orders_count | number | Lifetime orders. |
| ltv | number | Lifetime value in rupees. |
| last_order_date | date | Date of most recent order. |
| repeat_30d | boolean | Whether the user ordered again within 30 days. |

## 5. Funnel definition in Mixpanel

Steps, in order, with a 30 minute conversion window:

1. item_view
2. add_to_cart
3. select_address
4. payment_success

Breakdown: is_new, channel, device.

## 6. Retention definition in Mixpanel

Cohort by first order date. Return event: payment_success. Read at day 1, 3, 7, 14, 21 and 30.

## 7. Properties to add for this project

These do not exist today and are needed for the fixes to be measurable.

| Property | Event | Why |
| --- | --- | --- |
| fee_stage | checkout_start | To measure the fee disclosure experiment. |
| addr_steps | select_address | To measure the address step experiment. |
| attempt_number | payment_attempt | To measure retry behaviour. |
| reason | payment_failed | To classify failures. |

## 8. Data quality checks

- Every payment_success must have a matching order_id.
- Every session must have at least one item_view.
- fee_stage must be set on every checkout_start.
- No event may fire without user_id and session_id.
