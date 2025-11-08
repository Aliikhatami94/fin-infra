"""Easy builder for budget tracker.

Provides easy_budgets() function for quick BudgetTracker setup with sensible defaults.

Generic Design:
- Configures svc-infra SQL for persistence
- Configures svc-infra webhooks for alerts
- Defaults to monthly budgets with rollover enabled
- Works with any database backend (via svc-infra)
"""

from __future__ import annotations

# TODO: Implement easy_budgets() in Task 16
# - Configure DB (svc-infra SQL)
# - Configure webhooks (svc-infra)
# - Return BudgetTracker instance
