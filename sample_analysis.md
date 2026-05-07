# FoodLens Sample Analysis

This is a human-readable sample of the analysis shown in the local FoodLens dashboard at:

```text
http://127.0.0.1:8000
```

The sample uses mocked Swiggy order-history data for the last 1 month with a monthly budget of Rs 6,000. It is meant to help reviewers understand the product output without running the local setup. The raw API payload is also available in `sample_analysis.json`.

## At a Glance

| Signal | Value | Context |
| --- | ---: | --- |
| Projected spend | Rs 5,631 | 94% of budget |
| Fees paid | Rs 513 | delivery leakage |
| Peak time | 20:00 | Dinner |
| Weekly goal | Rs 1,500 | 3 planned orders |
| Top repeat | Chicken Biryani | 4x ordered |
| Food personality | Dinner Decider | 73% explore score |

## Priority Actions

| # | Action | Why it matters | Confidence |
| ---: | --- | --- | --- |
| 1 | Set this week's Swiggy cap | Use Rs 1,500 as the limit before placing more orders. | Strong signal |
| 2 | Check Swiggy One before subscribing | You paid Rs 513 in delivery fees this period. If you order often, compare that against Swiggy One's fee savings before subscribing. | Strong signal |
| 3 | Put a pause before peak-hour orders | Show the budget nudge before 20:00, your strongest ordering slot. | Strong signal |
| 4 | Compare repeat alternatives | When Meghana Foods appears, compare it with two cheaper similar options. | Strong signal |

## Highest Impact Insights

| Area | Insight | Impact | Confidence |
| --- | --- | --- | --- |
| Budget | Projected spend is Rs 5,631 against a Rs 6,000 budget. | 94% budget pace | Strong signal |
| Fees | Delivery fees account for Rs 513 in this period. | Immediate savings lever | Strong signal |
| Timing | Your peak pattern is Dinner around 20:00. | Better pre-order decisions | Strong signal |
| Membership | Swiggy One may be worth checking based on delivery fee pressure. | Could reduce fee pressure | Strong signal |
| Goal | This week's suggested cap is Rs 1,500. | Simple behavior change | Strong signal |

## Trust & Value Checks

| Check | Result | Detail |
| --- | --- | --- |
| Analysis confidence | 90/100, strong | Strong confidence based on 15 orders over 27 observed days. |
| Subscription value | Worth checking | Delivery fee pressure is high enough to compare against Swiggy One savings before subscribing. |
| Nutrition confidence | 45/100, estimated | Macro split is useful for pattern awareness, but it is estimated from dish names. |

## Spend Metrics

| Metric | Value |
| --- | ---: |
| Orders | 15 |
| Total spend | Rs 5,631 |
| Average order value | Rs 375 |
| Average delivery fee | Rs 34 |
| Projected monthly spend | Rs 5,631 |
| Delivery fee total | Rs 513 |
| Days observed | 27 |
| Orders per week | 3.9 |

## Top Food Patterns

### Top Dishes

| Dish | Count |
| --- | ---: |
| Chicken Biryani | 4x |
| Raita | 3x |
| Mini Meals | 1x |
| Filter Coffee | 1x |
| Chicken Kebab Roll | 1x |

### Top Restaurants

| Restaurant | Count |
| --- | ---: |
| Meghana Foods | 5x |
| A2B | 1x |
| Empire Restaurant | 1x |
| Polar Bear | 1x |
| Third Wave Coffee | 1x |

### Estimated Nutrition Pattern

These are rough estimates from dish names, not verified nutrition facts.

| Macro | Estimated amount |
| --- | ---: |
| Protein | 345g |
| Carbs | 1111g |
| Fats | 364g |
| Fiber | 70g |
| Sugar | 270g |

## Ordering Time Patterns

### Meal Window

| Meal window | Orders |
| --- | ---: |
| Dinner | 10 |
| Lunch | 3 |
| Morning | 1 |
| Late night | 1 |

### Busiest Hours

| Hour | Orders |
| --- | ---: |
| 20:00 | 5 |
| 21:00 | 3 |
| 13:00 | 2 |
| 09:00 | 1 |
| 14:00 | 1 |
| 19:00 | 1 |
| 22:00 | 1 |
| 23:00 | 1 |

### Weekday Pattern

| Day | Orders |
| --- | ---: |
| Monday | 3 |
| Tuesday | 1 |
| Wednesday | 3 |
| Thursday | 2 |
| Friday | 2 |
| Saturday | 2 |
| Sunday | 2 |

## Budget & Hidden Costs

| Area | Value | Detail |
| --- | ---: | --- |
| Projected monthly spend | Rs 5,631 | At this pace you stay Rs 369 under your Rs 6,000 budget. |
| Delivery fee leakage | Rs 513 | 2 smaller orders may be pushing up fee impact. |
| High-value orders | 6 | Orders above Rs 450 are the easiest place to create savings. |
| Repeat concentration | 47% | Share of orders coming from top 3 restaurants. |

### Budget Burn Rate

| Signal | Value |
| --- | --- |
| Status | on track |
| Budget used | 94% |
| Monthly budget | Rs 6,000 |
| Projected monthly spend | Rs 5,631 |
| Budget runout estimate | 30 days |

### Hidden Cost Breakdown

| Cost | Amount | Detail |
| --- | ---: | --- |
| Food subtotal | Rs 5,118 | Estimated spend on items before delivery fees. |
| Delivery fees | Rs 513 | Fees paid across orders in this period. |
| Dessert/drink add-ons | Rs 443 | Estimated spend linked to dessert and drink items. |
| Rs 450+ orders | Rs 3,005 | Spend from higher-value orders where swaps can save money. |

## Savings Simulation

| Opportunity | Estimated impact | Detail |
| --- | ---: | --- |
| Swap expensive repeats | Rs 1,200/month | Replace up to two Rs 450+ orders per week with good options under Rs 300. |
| Reduce dessert add-ons | Rs 270/period | Keep dessert as a planned treat instead of an automatic dinner add-on. |
| Lower delivery fee impact | Rs 128/period | Batch snack/cafe cravings or choose nearby restaurants when fee impact is high. |

## Personal Badges

| Badge | Reason |
| --- | --- |
| Dinner Decider | Your Swiggy usage is mostly evening decision support. |
| Fee Watcher | Rs 513 paid in delivery fees this period. |
| Biryani Loyalist | Biryani is your strongest cuisine pattern. |
| Add-on Drifter | Estimated Rs 443 linked to dessert or drink add-ons. |
| Premium Picker | 6 orders crossed Rs 450. |

## Agent Summary

- Projected monthly spend is Rs 5,631 against a Rs 6,000 budget.
- Projected spend uses 94% of the monthly budget.
- Delivery fees account for Rs 513.
- Top priority: Keep this month under control.
- Next best action: Set this week's Swiggy cap.
- Analysis confidence: Strong signal.

## Agent Recommendations

- Create a one-tap 'Biryani' shortlist with premium, budget, and lighter picks.
- Prefer nearby restaurants or batch snack/cafe cravings when delivery fee impact is high.
- Compare recent delivery fees against Swiggy One savings before subscribing.
- Show a dessert/drink nudge only after the user confirms they want add-ons.
- Use Rs 1,500 as this week's ordering cap.

## Workflow Trace

The analysis is produced by a LangGraph workflow:

```text
ground_context
  -> data_quality_check
  -> spend_analysis
  -> budget_burn_analysis
  -> hidden_cost_analysis
  -> subscription_value_check
  -> habit_analysis
  -> nutrition_confidence_estimator
  -> goal_analysis
  -> risk_detection
  -> recommendation_drafter
  -> guardrail_review
  -> insight_prioritizer
  -> next_best_action_selector
  -> final_response
```

## Notes

This sample is based on mocked data. With real Swiggy MCP access, this can be improved with richer order metadata, live restaurant/menu context, real fee/subscription comparisons, stronger personalization, and more accurate nutrition information where available.
