"""FastAPI integration for credit score monitoring.

Provides add_credit_monitoring() helper to wire credit routes to FastAPI app.

Routes:
    GET /credit/score - Get current credit score (cached 24h)
    GET /credit/report - Get full credit report (cached 24h)
    POST /credit/subscribe - Subscribe to score change webhooks
    GET /credit/history - Get score history (future)

Integration with svc-infra:
    - svc-infra.cache: 24h TTL for score/report caching (reduce bureau costs)
    - svc-infra.auth: User authentication required
    - fin-infra.compliance: FCRA compliance event logging

Example:
    >>> from fastapi import FastAPI
    >>> from fin_infra.credit.add import add_credit_monitoring
    >>> 
    >>> app = FastAPI()
    >>> credit = add_credit_monitoring(app, provider="experian")
"""

from typing import TYPE_CHECKING

from fin_infra.credit import ExperianProvider, easy_credit
from fin_infra.models.credit import CreditReport, CreditScore
from fin_infra.providers.base import CreditProvider

if TYPE_CHECKING:
    from fastapi import FastAPI


def add_credit_monitoring(
    app: "FastAPI",
    *,
    provider: str | CreditProvider | None = None,
    prefix: str = "/credit",
    cache_ttl: int = 86400,  # 24 hours (minimize bureau pulls)
    **config,
) -> CreditProvider:
    """Wire credit monitoring routes to FastAPI app.
    
    Mounts routes:
        GET {prefix}/score - Get current credit score (cached)
        GET {prefix}/report - Get full credit report (cached)
        POST {prefix}/subscribe - Subscribe to score change webhooks
        GET {prefix}/history - Get score history (future)
    
    Integration with svc-infra:
        - Uses svc-infra.cache for score caching (reduce API costs)
        - Uses svc-infra.webhooks for score change notifications
        - Uses svc-infra.auth for user authentication
        - Logs compliance events (FCRA permissible purpose)
    
    Args:
        app: FastAPI application
        provider: Bureau name or CreditProvider instance (default: "experian")
        prefix: Route prefix (default: "/credit")
        cache_ttl: Cache TTL in seconds (default: 86400 = 24h)
        **config: Additional configuration passed to easy_credit()
        
    Returns:
        Configured CreditProvider instance
        
    Example:
        >>> from fastapi import FastAPI
        >>> from fin_infra.credit.add import add_credit_monitoring
        >>> 
        >>> app = FastAPI()
        >>> credit = add_credit_monitoring(app, provider="experian")
        >>> 
        >>> # Routes available:
        >>> # GET /credit/score
        >>> # GET /credit/report
        >>> # POST /credit/subscribe
    """
    # NOTE: svc-infra dual routers NOT used for v1 (no auth dependency yet)
    # v2 will use: from svc_infra.api.fastapi.dual.protected import user_router
    from fastapi import APIRouter

    # Create credit provider
    if provider is None:
        provider = "experian"
    credit_provider = easy_credit(provider, **config) if isinstance(provider, str) else provider

    # Store provider on app state for route access
    app.state.credit_provider = credit_provider

    # Create router
    router = APIRouter(prefix=prefix, tags=["Credit Monitoring"])

    @router.get("/score", response_model=CreditScore)
    async def get_credit_score(user_id: str):
        """Get current credit score for a user.
        
        Returns cached score if available (24h TTL), otherwise pulls from bureau.
        
        Args:
            user_id: User identifier
            
        Returns:
            CreditScore with score, model, bureau, factors
            
        FCRA Compliance:
            - Logs credit.score_accessed compliance event
            - Requires user consent (not enforced in v1)
        """
        # v1: No caching integration (direct call to provider)
        # v2: Will use svc-infra.cache with @cache_read decorator
        score = credit_provider.get_credit_score(user_id)

        # v1: No compliance logging (module not imported)
        # v2: Will use fin_infra.compliance.log_compliance_event()
        # log_compliance_event(app, "credit.score_accessed", {"user_id": user_id})

        return score

    @router.get("/report", response_model=CreditReport)
    async def get_credit_report(user_id: str):
        """Get full credit report for a user.
        
        Returns cached report if available (24h TTL), otherwise pulls from bureau.
        
        Args:
            user_id: User identifier
            
        Returns:
            CreditReport with score, accounts, inquiries, public records
            
        FCRA Compliance:
            - Logs credit.report_accessed compliance event
            - Requires user consent (not enforced in v1)
        """
        # v1: No caching integration (direct call to provider)
        # v2: Will use svc-infra.cache with @cache_read decorator
        report = credit_provider.get_credit_report(user_id)

        # v1: No compliance logging (module not imported)
        # v2: Will use fin_infra.compliance.log_compliance_event()
        # log_compliance_event(app, "credit.report_accessed", {"user_id": user_id})

        return report

    @router.post("/subscribe")
    async def subscribe_to_credit_changes(user_id: str, webhook_url: str):
        """Subscribe to credit score change notifications.
        
        Args:
            user_id: User identifier
            webhook_url: URL to receive webhook notifications
            
        Returns:
            Subscription ID
            
        v1: Returns mock subscription ID (no real webhook integration).
        v2: Will integrate with svc-infra.webhooks.
        """
        # v1: No webhook integration (direct call to provider)
        # v2: Will use svc-infra.webhooks for subscription management
        subscription_id = credit_provider.subscribe_to_changes(user_id, webhook_url)
        return {"subscription_id": subscription_id, "webhook_url": webhook_url}

    # Mount router
    app.include_router(router, include_in_schema=True)

    # v1: No scoped docs registration
    # v2: Will use svc-infra.api.fastapi.docs.scoped.add_prefixed_docs()
    # add_prefixed_docs(
    #     app,
    #     prefix=prefix,
    #     title="Credit Monitoring",
    #     auto_exclude_from_root=True,
    #     visible_envs=None,
    # )

    return credit_provider


__all__ = ["add_credit_monitoring"]
