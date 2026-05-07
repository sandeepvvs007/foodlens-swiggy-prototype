from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timedelta
from statistics import mean


def _parse_date(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _bucket_hour(hour: int) -> str:
    if 5 <= hour < 11:
        return "Morning"
    if 11 <= hour < 16:
        return "Lunch"
    if 16 <= hour < 19:
        return "Evening snack"
    if 19 <= hour < 23:
        return "Dinner"
    return "Late night"


def _top(counter: Counter, limit: int = 5) -> list[dict]:
    return [{"name": name, "count": count} for name, count in counter.most_common(limit)]


def _ordered_counts(counter: Counter, labels: list[str]) -> list[dict]:
    return [{"name": label, "count": counter.get(label, 0)} for label in labels]


def _classify_items(items: list[str]) -> set[str]:
    text = " ".join(items).lower()
    tags = set()
    if any(word in text for word in ["ice cream", "dessert", "chocolate", "muffin"]):
        tags.add("dessert")
    if any(word in text for word in ["coke", "soda", "coffee", "latte"]):
        tags.add("drink")
    if any(word in text for word in ["biryani", "rice", "meal"]):
        tags.add("rice-heavy")
    if any(word in text for word in ["chicken", "paneer", "protein", "egg"]):
        tags.add("protein-oriented")
    if any(word in text for word in ["fries", "kebab", "burger", "wrap"]):
        tags.add("fast-food")
    return tags


def _estimate_item_macros(item: str) -> dict[str, int]:
    text = item.lower()
    if "biryani" in text:
        return {"Protein": 25, "Carbs": 78, "Fats": 24, "Fiber": 4, "Sugar": 5}
    if "raita" in text:
        return {"Protein": 4, "Carbs": 6, "Fats": 4, "Fiber": 0, "Sugar": 4}
    if "meal" in text:
        return {"Protein": 20, "Carbs": 82, "Fats": 18, "Fiber": 8, "Sugar": 6}
    if "coffee" in text or "latte" in text:
        return {"Protein": 4, "Carbs": 18, "Fats": 6, "Fiber": 0, "Sugar": 16}
    if "muffin" in text:
        return {"Protein": 5, "Carbs": 48, "Fats": 18, "Fiber": 2, "Sugar": 26}
    if "kebab" in text or "wrap" in text:
        return {"Protein": 27, "Carbs": 48, "Fats": 22, "Fiber": 4, "Sugar": 5}
    if "burger" in text:
        return {"Protein": 28, "Carbs": 45, "Fats": 28, "Fiber": 4, "Sugar": 7}
    if "fries" in text:
        return {"Protein": 5, "Carbs": 48, "Fats": 22, "Fiber": 5, "Sugar": 1}
    if "ice cream" in text or "chocolate" in text:
        return {"Protein": 5, "Carbs": 38, "Fats": 16, "Fiber": 1, "Sugar": 32}
    if "rice bowl" in text:
        return {"Protein": 24, "Carbs": 68, "Fats": 18, "Fiber": 7, "Sugar": 6}
    if "protein" in text or "paneer" in text:
        return {"Protein": 34, "Carbs": 52, "Fats": 22, "Fiber": 6, "Sugar": 5}
    if "coke" in text or "soda" in text:
        return {"Protein": 0, "Carbs": 35, "Fats": 0, "Fiber": 0, "Sugar": 35}
    return {"Protein": 12, "Carbs": 45, "Fats": 14, "Fiber": 4, "Sugar": 8}


def _empty_response(period_days: int | None, monthly_budget: int) -> dict:
    return {
        "period": {"label": _period_label(period_days), "days": period_days},
        "budget": {"monthly_budget": monthly_budget},
        "metrics": {},
        "top_dishes": [],
        "top_restaurants": [],
        "top_cuisines": [],
        "macro_breakdown": [],
        "time_buckets": [],
        "hourly_breakdown": [],
        "weekday_breakdown": [],
        "budget_insights": [],
        "budget_burn": {},
        "hidden_costs": [],
        "habit_triggers": [],
        "weekly_goal": {},
        "savings_opportunities": [],
        "food_personality": {},
        "pattern_tags": [],
        "insights": ["No order history was found for this period."],
        "recommendations": []
    }


def _period_label(period_days: int | None) -> str:
    labels = {
        7: "Last 7 days",
        14: "Last 2 weeks",
        30: "Last 1 month",
        120: "Last 4 months",
        180: "Last 6 months",
    }
    return labels.get(period_days, "All available history")


def _filter_orders(enriched: list[dict], period_days: int | None) -> list[dict]:
    if not period_days or not enriched:
        return enriched
    anchor_date = max(order["dt"] for order in enriched)
    cutoff = anchor_date - timedelta(days=period_days - 1)
    return [order for order in enriched if order["dt"] >= cutoff]


def analyze_orders(
    orders: list[dict],
    period_days: int | None = 30,
    monthly_budget: int = 6000,
) -> dict:
    if not orders:
        return _empty_response(period_days, monthly_budget)

    all_enriched = [{**order, "dt": _parse_date(order["ordered_at"])} for order in orders]
    enriched = _filter_orders(all_enriched, period_days)
    if not enriched:
        return _empty_response(period_days, monthly_budget)

    amounts = [order["amount"] for order in enriched]
    delivery_fees = [order.get("delivery_fee", 0) for order in enriched]

    dish_counter: Counter = Counter()
    restaurant_counter: Counter = Counter()
    cuisine_counter: Counter = Counter()
    time_counter: Counter = Counter()
    hourly_counter: Counter = Counter()
    weekday_counter: Counter = Counter()
    tag_counter: Counter = Counter()
    macro_totals: defaultdict[str, int] = defaultdict(int)
    restaurant_spend: defaultdict[str, int] = defaultdict(int)
    high_spend_orders = 0
    small_orders = 0
    add_on_spend = 0
    high_value_spend = 0

    for order in enriched:
        for item in order["items"]:
            dish_counter[item] += 1
            for macro, grams in _estimate_item_macros(item).items():
                macro_totals[macro] += grams
            item_tags = _classify_items([item])
            if "dessert" in item_tags or "drink" in item_tags:
                add_on_spend += min(round(order["amount"] * 0.22), 180)
        for tag in _classify_items(order["items"]):
            tag_counter[tag] += 1
        restaurant_counter[order["restaurant"]] += 1
        cuisine_counter[order["cuisine"]] += 1
        time_counter[_bucket_hour(order["dt"].hour)] += 1
        hourly_counter[f"{order['dt'].hour:02d}:00"] += 1
        weekday_counter[order["dt"].strftime("%A")] += 1
        restaurant_spend[order["restaurant"]] += order["amount"]
        if order["amount"] >= 450:
            high_spend_orders += 1
            high_value_spend += order["amount"]
        if order["amount"] < 300:
            small_orders += 1

    first_order = min(order["dt"] for order in enriched)
    last_order = max(order["dt"] for order in enriched)
    days_observed = max((last_order - first_order).days + 1, 1)
    order_count = len(enriched)
    total_spend = sum(amounts)
    top_restaurant = restaurant_counter.most_common(1)[0]
    top_dish = dish_counter.most_common(1)[0]
    top_cuisine = cuisine_counter.most_common(1)[0]
    peak_time = time_counter.most_common(1)[0]
    peak_hour = hourly_counter.most_common(1)[0]
    peak_day = weekday_counter.most_common(1)[0]
    peak_day_name = peak_day[0]
    unique_restaurant_count = len(restaurant_counter)
    top_three_orders = sum(count for _, count in restaurant_counter.most_common(3))
    repeat_concentration = round(top_three_orders / order_count * 100)
    experimentation_score = round(unique_restaurant_count / order_count * 100)
    delivery_fee_total = sum(delivery_fees)
    observed_days_for_projection = period_days or days_observed
    projected_monthly_spend = round(total_spend / max(observed_days_for_projection, 1) * 30)
    projected_over_budget = max(projected_monthly_spend - monthly_budget, 0)
    budget_remaining = monthly_budget - projected_monthly_spend
    budget_used_percent = min(round(projected_monthly_spend / max(monthly_budget, 1) * 100), 999)
    daily_budget = monthly_budget / 30
    daily_spend_rate = total_spend / max(observed_days_for_projection, 1)
    projected_budget_runout_day = (
        min(round(monthly_budget / daily_spend_rate), 30) if daily_spend_rate else 30
    )
    burn_status = "over pace" if projected_monthly_spend > monthly_budget else "on track"

    weekend_orders = sum(
        1 for order in enriched if order["dt"].strftime("%A") in {"Saturday", "Sunday"}
    )
    dinner_or_late = sum(
        count for bucket, count in time_counter.items() if bucket in {"Dinner", "Late night"}
    )

    insights = [
        f"You placed {order_count} orders over {days_observed} days and spent Rs {total_spend:,}.",
        f"Your average order value is Rs {round(mean(amounts)):,}, with delivery fees averaging Rs {round(mean(delivery_fees)):,}.",
        f"Your strongest repeat pattern is {top_dish[0]}, ordered {top_dish[1]} times.",
        f"{top_restaurant[0]} is your most repeated restaurant and accounts for Rs {restaurant_spend[top_restaurant[0]]:,} of spend.",
        f"You order most often during {peak_time[0].lower()}, which represents {peak_time[1]} of your orders.",
        f"Your peak ordering slot is around {peak_hour[0]}, and your busiest ordering day is {peak_day_name}.",
    ]

    budget_insights = [
        {
            "title": "Projected monthly spend",
            "value": f"Rs {projected_monthly_spend:,}",
            "detail": (
                f"At this pace you are Rs {projected_over_budget:,} over your Rs {monthly_budget:,} budget."
                if projected_over_budget
                else f"At this pace you stay Rs {abs(budget_remaining):,} under your Rs {monthly_budget:,} budget."
            ),
        },
        {
            "title": "Delivery fee leakage",
            "value": f"Rs {delivery_fee_total:,}",
            "detail": f"{small_orders} smaller orders may be pushing up fee impact.",
        },
        {
            "title": "High-value orders",
            "value": f"{high_spend_orders}",
            "detail": "Orders above Rs 450 are the easiest place to create savings.",
        },
        {
            "title": "Repeat concentration",
            "value": f"{repeat_concentration}%",
            "detail": "Share of orders coming from your top 3 restaurants.",
        },
    ]

    food_subtotal = max(total_spend - delivery_fee_total, 0)
    hidden_costs = [
        {
            "name": "Food subtotal",
            "amount": food_subtotal,
            "detail": "Estimated spend on items before delivery fees.",
        },
        {
            "name": "Delivery fees",
            "amount": delivery_fee_total,
            "detail": "Fees paid across orders in this period.",
        },
        {
            "name": "Dessert/drink add-ons",
            "amount": add_on_spend,
            "detail": "Estimated spend linked to dessert and drink items.",
        },
        {
            "name": "Rs 450+ orders",
            "amount": high_value_spend,
            "detail": "Spend from higher-value orders where swaps can save money.",
        },
    ]

    swiggy_one_suggestion = None
    if delivery_fee_total >= 250 or round(mean(delivery_fees)) >= 35:
        swiggy_one_suggestion = {
            "title": "Check Swiggy One savings",
            "detail": (
                f"You paid Rs {delivery_fee_total:,} in delivery fees this period. "
                "If you order often, compare that against Swiggy One's fee savings before subscribing."
            ),
        }

    weekly_budget_goal = round(monthly_budget / 4)
    current_weekly_pace = round(projected_monthly_spend / 4)
    target_order_count = max(round(order_count / max(observed_days_for_projection, 1) * 7) - 1, 1)
    weekly_goal = {
        "title": "This week's goal",
        "budget": weekly_budget_goal,
        "current_pace": current_weekly_pace,
        "actions": [
            f"Keep Swiggy spend under Rs {weekly_budget_goal:,}.",
            f"Limit restaurant orders to {target_order_count} planned orders.",
            "Avoid unplanned dessert or drink add-ons twice this week.",
            "Check delivery fee before checkout; prefer nearby options when fee is high.",
        ],
    }

    habit_triggers = [
        f"Peak trigger: {peak_day_name} around {peak_hour[0]}. Add a planned meal reminder 60-90 minutes earlier.",
        f"{round(dinner_or_late / order_count * 100)}% of your orders are dinner or late-night decisions.",
        f"{round(weekend_orders / order_count * 100)}% of your orders happen on weekends.",
    ]
    if tag_counter:
        top_tag = tag_counter.most_common(1)[0]
        habit_triggers.append(
            f"Your strongest food pattern is {top_tag[0]}, appearing in {top_tag[1]} orders."
        )

    weekly_saving_from_high_orders = min(high_spend_orders, 2) * 150
    dessert_saving = tag_counter.get("dessert", 0) * 90
    savings_opportunities = [
        {
            "title": "Swap expensive repeats",
            "amount": f"Rs {weekly_saving_from_high_orders * 4:,}/month",
            "detail": "Replace up to two Rs 450+ orders per week with good options under Rs 300.",
        },
        {
            "title": "Reduce dessert add-ons",
            "amount": f"Rs {dessert_saving:,}/period",
            "detail": "Keep dessert as a planned treat instead of an automatic dinner add-on.",
        },
        {
            "title": "Lower delivery fee impact",
            "amount": f"Rs {round(delivery_fee_total * 0.25):,}/period",
            "detail": "Batch snack/cafe cravings or choose nearby restaurants when fee impact is high.",
        },
    ]

    if repeat_concentration >= 70:
        personality_name = "Loyalist"
        personality_detail = "You strongly repeat trusted restaurants and dishes."
    elif experimentation_score >= 75:
        personality_name = "Explorer"
        personality_detail = "You frequently try different restaurants."
    elif dinner_or_late / order_count >= 0.65:
        personality_name = "Dinner Decider"
        personality_detail = "Your Swiggy usage is mostly evening decision support."
    else:
        personality_name = "Balanced Regular"
        personality_detail = "You mix repeat choices with some exploration."

    food_personality = {
        "name": personality_name,
        "detail": personality_detail,
        "experimentation_score": experimentation_score,
        "unique_restaurants": unique_restaurant_count,
    }

    recommendations = []
    if top_cuisine[1] >= max(3, order_count // 4):
        recommendations.append(
            f"Create a '{top_cuisine[0]} craving' shortcut with one premium pick, one budget pick, and one lighter option."
        )
    if dinner_or_late / order_count >= 0.6:
        recommendations.append(
            "Add a dinner budget guardrail, because most of your ordering happens when impulse choices are easiest."
        )
    if weekend_orders / order_count >= 0.3:
        recommendations.append(
            "Separate weekday and weekend budgets; your weekend behavior is likely different from routine meals."
        )
    if mean(amounts) > 400:
        recommendations.append(
            "Show cheaper alternatives for your top restaurants when the cart crosses Rs 400."
        )
    if cuisine_counter.get("Desserts", 0) >= 2:
        recommendations.append(
            "Flag dessert add-ons after dinner orders and suggest a smaller portion when the user wants to save."
        )

    if not recommendations:
        recommendations.append(
            "Use this order history to create faster reorder suggestions and monthly spending summaries."
        )

    return {
        "period": {"label": _period_label(period_days), "days": period_days},
        "budget": {"monthly_budget": monthly_budget},
        "metrics": {
            "order_count": order_count,
            "total_spend": total_spend,
            "average_order_value": round(mean(amounts)),
            "average_delivery_fee": round(mean(delivery_fees)),
            "projected_monthly_spend": projected_monthly_spend,
            "delivery_fee_total": delivery_fee_total,
            "days_observed": days_observed,
            "orders_per_week": round(order_count / days_observed * 7, 1),
        },
        "top_dishes": _top(dish_counter),
        "top_restaurants": _top(restaurant_counter),
        "top_cuisines": _top(cuisine_counter),
        "macro_breakdown": [
            {"name": macro, "count": macro_totals[macro], "unit": "g"}
            for macro in ["Protein", "Carbs", "Fats", "Fiber", "Sugar"]
        ],
        "time_buckets": _top(time_counter, 6),
        "hourly_breakdown": _ordered_counts(
            hourly_counter,
            [f"{hour:02d}:00" for hour in range(24)]
        ),
        "weekday_breakdown": _ordered_counts(
            weekday_counter,
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        ),
        "budget_insights": budget_insights,
        "budget_burn": {
            "status": burn_status,
            "budget_used_percent": budget_used_percent,
            "monthly_budget": monthly_budget,
            "projected_monthly_spend": projected_monthly_spend,
            "projected_budget_runout_day": projected_budget_runout_day,
            "detail": (
                f"At your current pace, your Rs {monthly_budget:,} budget would last about "
                f"{projected_budget_runout_day} days."
            ),
        },
        "hidden_costs": hidden_costs,
        "swiggy_one_suggestion": swiggy_one_suggestion,
        "habit_triggers": habit_triggers,
        "weekly_goal": weekly_goal,
        "savings_opportunities": savings_opportunities,
        "food_personality": food_personality,
        "pattern_tags": _top(tag_counter, 6),
        "insights": insights,
        "recommendations": recommendations,
    }
