"""Budget alerts and notifications.

Detects overspending, approaching limits, and unusual spending patterns.
Integrates with svc-infra webhooks for alert delivery.

Alert Types:
- Overspending: Spent > budgeted amount
- Approaching limit: Spent > 80% of budgeted
- Unusual spending: Spike in category (compared to historical average)

Generic Design:
- Configurable thresholds per category
- Works with all budget types
- Integrates with svc-infra webhooks for notifications
"""

from __future__ import annotations

# TODO: Implement check_budget_alerts() function in Task 14
