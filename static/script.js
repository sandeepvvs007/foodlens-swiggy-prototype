const rupees = new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
  maximumFractionDigits: 0,
});

const metricLabels = {
  order_count: "Orders",
  total_spend: "Total spend",
  average_order_value: "Avg order",
  projected_monthly_spend: "Projected month",
  delivery_fee_total: "Fees paid",
  orders_per_week: "Orders / week",
};

let currentAnalysis = null;
const chartColors = ["#fc8019", "#2457c5", "#157f5b", "#d97706", "#7c3aed", "#0f766e"];

function formatMetric(key, value) {
  if (["total_spend", "average_order_value", "projected_monthly_spend", "delivery_fee_total"].includes(key)) {
    return rupees.format(value);
  }
  return value;
}

function renderMetrics(metrics) {
  const container = document.querySelector("#metrics");
  const visibleMetrics = [
    "order_count",
    "total_spend",
    "average_order_value",
    "projected_monthly_spend",
    "delivery_fee_total",
    "orders_per_week",
  ];
  container.innerHTML = visibleMetrics
    .filter((key) => Object.hasOwn(metrics, key))
    .map((key) => [key, metrics[key]])
    .map(([key, value]) => `
      <article class="metric">
        <span>${metricLabels[key] || key}</span>
        <strong>${formatMetric(key, value)}</strong>
      </article>
    `)
    .join("");
}

function renderInsightCards(selector, items) {
  document.querySelector(selector).innerHTML = items
    .map((item) => `
      <div class="insight-card">
        <span>${item.title}</span>
        <strong>${item.value}</strong>
        <p>${item.detail}</p>
      </div>
    `)
    .join("");
}

function renderSavings(selector, items) {
  document.querySelector(selector).innerHTML = items
    .map((item) => `
      <div class="saving-row">
        <div>
          <strong>${item.title}</strong>
          <span>${item.detail}</span>
        </div>
        <em>${item.amount}</em>
      </div>
    `)
    .join("");
}

function renderBudgetBurn(burn) {
  const percent = Math.min(burn.budget_used_percent || 0, 100);
  document.querySelector("#budgetBurn").innerHTML = `
    <div class="burn-header">
      <strong>${burn.budget_used_percent}%</strong>
      <span>${burn.status}</span>
    </div>
    <div class="burn-track">
      <div style="width: ${percent}%"></div>
    </div>
    <p>${burn.detail}</p>
    <div class="burn-meta">
      <span>Budget ${rupees.format(burn.monthly_budget || 0)}</span>
      <span>Projected ${rupees.format(burn.projected_monthly_spend || 0)}</span>
    </div>
  `;
}

function renderWeeklyGoal(goal) {
  document.querySelector("#weeklyGoal").innerHTML = `
    <div class="goal-number">${rupees.format(goal.budget || 0)}</div>
    <p>Current weekly pace: ${rupees.format(goal.current_pace || 0)}</p>
    <ul>
      ${(goal.actions || []).map((action) => `<li>${action}</li>`).join("")}
    </ul>
  `;
}

function renderHiddenCosts(costs, swiggyOneSuggestion) {
  const total = costs.reduce((sum, item) => sum + item.amount, 0);
  document.querySelector("#hiddenCosts").innerHTML = costs
    .map((item) => {
      const width = total ? Math.max((item.amount / total) * 100, 4) : 4;
      return `
        <div class="cost-row">
          <div class="cost-label">
            <strong>${item.name}</strong>
            <em>${rupees.format(item.amount)}</em>
          </div>
          <div class="cost-track">
            <div style="width: ${width}%"></div>
          </div>
          <p>${item.detail}</p>
        </div>
      `;
    })
    .join("");

  document.querySelector("#swiggyOneSuggestion").innerHTML = swiggyOneSuggestion
    ? `
      <div class="swiggy-one">
        <strong>${swiggyOneSuggestion.title}</strong>
        <p>${swiggyOneSuggestion.detail}</p>
      </div>
    `
    : "";
}

function renderFoodPersonality(personality, tags) {
  const tagMarkup = tags
    .map((tag) => `<span>${tag.name} · ${tag.count}x</span>`)
    .join("");
  document.querySelector("#foodPersonality").innerHTML = `
    <strong>${personality.name}</strong>
    <p>${personality.detail}</p>
    <div class="score-line">
      <span>Experimentation score</span>
      <em>${personality.experimentation_score}%</em>
    </div>
    <div class="score-track">
      <div style="width: ${personality.experimentation_score}%"></div>
    </div>
    <p>${personality.unique_restaurants} unique restaurants in this period.</p>
    <div class="tag-list">${tagMarkup}</div>
  `;
}

function renderList(selector, items) {
  document.querySelector(selector).innerHTML = items
    .map((item) => `<li>${item}</li>`)
    .join("");
}

function renderRanked(selector, items) {
  document.querySelector(selector).innerHTML = items
    .map((item, index) => `
      <div class="rank-row">
        <span>${index + 1}</span>
        <strong>${item.name}</strong>
        <em>${item.count}x</em>
      </div>
    `)
    .join("");
}

function renderPieChart(selector, items) {
  const total = items.reduce((sum, item) => sum + item.count, 0);
  if (!items.length || total === 0) {
    document.querySelector(selector).innerHTML = `<p class="empty-state">Not enough data for this period.</p>`;
    return;
  }

  let runningTotal = 0;
  const segments = items.map((item, index) => {
    const start = (runningTotal / total) * 100;
    runningTotal += item.count;
    const end = (runningTotal / total) * 100;
    return `${chartColors[index % chartColors.length]} ${start}% ${end}%`;
  });

  const legend = items
    .map((item, index) => {
      const percent = Math.round((item.count / total) * 100);
      const value = item.unit ? `${item.count}${item.unit}` : `${item.count}x`;
      return `
        <div class="legend-row">
          <span style="background: ${chartColors[index % chartColors.length]}"></span>
          <strong>${item.name}</strong>
          <em>${value} · ${percent}%</em>
        </div>
      `;
    })
    .join("");
  const hasMacroUnit = items.some((item) => item.unit);

  document.querySelector(selector).innerHTML = `
    <div class="donut-chart" style="background: conic-gradient(${segments.join(", ")})">
      <div>
        <strong>${total}</strong>
        <span>${hasMacroUnit ? "est. grams" : "orders"}</span>
      </div>
    </div>
    <div>
      <div class="pie-legend">${legend}</div>
      ${hasMacroUnit ? `<p class="chart-note">Nutrition split is estimated from dish names and should not be treated as verified nutrition data.</p>` : ""}
    </div>
  `;
}

function renderBars(selector, items) {
  const max = Math.max(...items.map((item) => item.count), 1);
  document.querySelector(selector).innerHTML = items
    .map((item) => `
      <div class="bar-row">
        <div class="bar-label">
          <span>${item.name}</span>
          <strong>${item.count}</strong>
        </div>
        <div class="bar-track">
          <div class="bar-fill" style="width: ${(item.count / max) * 100}%"></div>
        </div>
      </div>
    `)
    .join("");
}

function renderSelectedRanking() {
  if (!currentAnalysis) {
    return;
  }
  const selector = document.querySelector("#rankingSelector");
  renderPieChart("#selectedRanking", currentAnalysis[selector.value] || []);
}

function renderColumnChart(selector, items, options = {}) {
  const max = Math.max(...items.map((item) => item.count), 1);
  const filtered = options.hideEmpty ? items.filter((item) => item.count > 0) : items;
  document.querySelector(selector).innerHTML = filtered
    .map((item) => {
      const height = item.count === 0 ? 2 : Math.max((item.count / max) * 100, 12);
      return `
        <div class="column-item">
          <div class="column-value">${item.count}</div>
          <div class="column-track">
            <div class="column-fill" style="height: ${height}%"></div>
          </div>
          <span>${options.shortLabels ? item.name.slice(0, 3) : item.name}</span>
        </div>
      `;
    })
    .join("");
}

async function loadAnalysis() {
  const period = document.querySelector("#periodSelector").value;
  const budget = document.querySelector("#budgetInput").value || "6000";
  const response = await fetch(`/api/analysis?period=${period}&budget=${budget}`);
  const data = await response.json();
  currentAnalysis = data;
  renderMetrics(data.metrics);
  renderInsightCards("#budgetInsights", data.budget_insights);
  renderBudgetBurn(data.budget_burn || {});
  renderWeeklyGoal(data.weekly_goal || {});
  renderHiddenCosts(data.hidden_costs || [], data.swiggy_one_suggestion);
  renderFoodPersonality(data.food_personality, data.pattern_tags);
  renderList("#insights", data.agent_summary || data.insights);
  renderList("#recommendations", data.agent_recommendations || data.recommendations);
  renderList("#habitTriggers", data.habit_triggers);
  renderSavings("#savingsOpportunities", data.savings_opportunities);
  renderSelectedRanking();
  renderBars("#timeBuckets", data.time_buckets);
  renderColumnChart("#hourlyBreakdown", data.hourly_breakdown, { hideEmpty: true });
  renderColumnChart("#weekdayBreakdown", data.weekday_breakdown, { shortLabels: true });
}

document.querySelector("#refreshButton").addEventListener("click", loadAnalysis);
document.querySelector("#periodSelector").addEventListener("change", loadAnalysis);
document.querySelector("#budgetInput").addEventListener("change", loadAnalysis);
document.querySelector("#rankingSelector").addEventListener("change", renderSelectedRanking);
loadAnalysis();
