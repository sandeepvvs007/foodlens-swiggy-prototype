# FoodLens: Swiggy Order History Insights Prototype

FoodLens is a local prototype for a Swiggy Builders Club application. It analyzes mocked Swiggy order history and produces user-facing insights about spending, favorite dishes, repeat restaurants, cuisine preferences, usual ordering times, budget leakage, savings opportunities, and practical recommendations.

## Why this exists

Swiggy MCP production access is whitelist-based. This prototype lets you demonstrate the end-to-end product experience before receiving staging credentials.

## Run locally

```bash
cd swiggy_food_insights_prototype
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
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
5. `agent_graph.py` runs a LangGraph workflow over those grounded metrics.
6. An LLM can later be added inside the graph nodes to generate richer summaries while preserving the same guardrails.

No cart changes or ordering actions should happen without explicit user confirmation.

## Agent architecture

The prototype uses LangGraph nodes and edges:

```text
START
  -> ground_context
  -> spend_analysis
  -> habit_analysis
  -> risk_detection
  -> recommendation_drafter
  -> guardrail_review
  -> final_response
END
```

Prompt grounding is kept in `prompts.py`. The graph treats deterministic analytics as the source of truth and runs guardrail checks for unsupported medical claims, invented metrics, hidden cart/order actions, and ungrounded recommendations.
