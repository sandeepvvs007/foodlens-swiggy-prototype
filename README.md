# FoodLens: Swiggy Order History Insights Prototype

FoodLens is a local prototype for a Swiggy Builders Club application. It analyzes mocked Swiggy order history and produces user-facing insights about spending, favorite dishes, repeat restaurants, cuisine preferences, usual ordering times, and practical recommendations.

## Why this exists

Swiggy MCP production access is whitelist-based. This prototype lets you demonstrate the end-to-end product experience before receiving staging credentials.

## Run locally

```bash
cd swiggy_food_insights_prototype
python3 app.py
```

Open:

```text
http://127.0.0.1:8000
```

OAuth callback placeholder for the access form:

```text
http://localhost:8000/auth/callback
```

## Future MCP integration

The mocked `data/mock_orders.json` file should later be replaced with calls to Swiggy's Food MCP server after OAuth consent. The analysis layer can stay the same:

1. User authorizes with OAuth 2.1 + PKCE.
2. Backend calls Swiggy MCP order/history tools when available.
3. Raw order data is normalized into the current order schema.
4. `analyzer.py` computes deterministic metrics.
5. An LLM generates a concise user-facing summary and recommendations.

No cart changes or ordering actions should happen without explicit user confirmation.
