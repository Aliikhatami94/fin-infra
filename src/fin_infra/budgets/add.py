"""FastAPI integration for budget management.

Provides add_budgets() helper to mount budget endpoints with svc-infra dual routers.

Endpoints:
- POST /budgets: Create budget
- GET /budgets: List budgets
- GET /budgets/{id}: Get budget
- PATCH /budgets/{id}: Update budget
- DELETE /budgets/{id}: Delete budget
- GET /budgets/{id}/progress: Get budget progress
- GET /budgets/templates: List templates
- POST /budgets/from-template: Create from template

Generic Design:
- Uses svc-infra user_router (authentication required)
- Caches budget queries (5 minute TTL)
- Registers scoped docs with add_prefixed_docs()
- Works with any budget type
"""

from __future__ import annotations

# TODO: Implement add_budgets() in Task 17
# - Use svc-infra user_router (MANDATORY)
# - Mount 8 endpoints
# - Apply caching decorators
# - Call add_prefixed_docs()
# - Store on app.state.budgets
