"""Credit score monitoring providers.

Providers for credit bureaus (Experian, Equifax, TransUnion):
- ExperianProvider: Experian credit reports and scores
- easy_credit(): One-liner to create configured credit provider
- add_credit_monitoring(): FastAPI helper to wire credit routes

FCRA Compliance:
- All credit pulls must have permissible purpose
- Log all credit report accesses (see fin_infra.compliance)
- Provide adverse action notices if applicable

Cost Optimization:
- Use svc-infra.cache with 24h TTL to minimize bureau API costs
- Bureau pulls cost ~$0.50-$2.00 each; caching saves 95% of costs

Example:
    >>> from fin_infra.credit import easy_credit
    >>> 
    >>> # Zero config (uses EXPERIAN_API_KEY from env)
    >>> credit = easy_credit()
    >>> score = credit.get_credit_score("user123")
    >>> 
    >>> # Explicit provider
    >>> credit = easy_credit(provider="experian", api_key="...")
    >>> report = credit.get_credit_report("user123")
"""

from datetime import date
from decimal import Decimal
from typing import Literal

from fin_infra.models.credit import (
    CreditAccount,
    CreditInquiry,
    CreditReport,
    CreditScore,
    PublicRecord,
)
from fin_infra.providers.base import CreditProvider
from fin_infra.settings import Settings


class ExperianProvider(CreditProvider):
    """Experian credit bureau provider (mock implementation).
    
    v1 Implementation:
    - Mock data for development/testing
    - Real Experian API integration deferred to v2 (requires API key)
    
    Args:
        api_key: Experian API key (optional, from env)
        environment: "sandbox" or "production" (default: sandbox)
        **config: Additional configuration
        
    Environment Variables:
        EXPERIAN_API_KEY: API key for Experian API
        EXPERIAN_CLIENT_ID: Client ID (if required)
        EXPERIAN_ENVIRONMENT: "sandbox" or "production" (default: sandbox)
        
    Example:
        >>> provider = ExperianProvider(api_key="...", environment="sandbox")
        >>> score = provider.get_credit_score("user123")
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        environment: Literal["sandbox", "production"] = "sandbox",
        **config,
    ):
        self.api_key = api_key
        self.environment = environment
        self.config = config

    def get_credit_score(self, user_id: str, **kwargs) -> CreditScore:
        """Retrieve current credit score for a user.
        
        v1: Returns mock data (FICO 8 score 735 with sample factors).
        v2: Will integrate with real Experian API.
        
        Args:
            user_id: User identifier
            **kwargs: Additional parameters (ignored in v1)
            
        Returns:
            CreditScore with score, model, bureau, factors
            
        Example:
            >>> provider = ExperianProvider()
            >>> score = provider.get_credit_score("user123")
            >>> print(score.score)  # 735
        """
        # v1: Mock data
        return CreditScore(
            user_id=user_id,
            score=735,
            score_model="FICO 8",
            bureau="experian",
            score_date=date.today(),
            factors=[
                "Credit card utilization is high (35%)",
                "No recent late payments",
                "Average age of accounts is good (8 years)",
                "Credit mix is diverse",
                "Recent hard inquiry detected",
            ],
            change=15,  # +15 points since last pull
        )

    def get_credit_report(self, user_id: str, **kwargs) -> CreditReport:
        """Retrieve full credit report for a user.
        
        v1: Returns mock data (sample accounts, inquiries, no public records).
        v2: Will integrate with real Experian API.
        
        Args:
            user_id: User identifier
            **kwargs: Additional parameters (ignored in v1)
            
        Returns:
            CreditReport with score, accounts, inquiries, public records
            
        Example:
            >>> provider = ExperianProvider()
            >>> report = provider.get_credit_report("user123")
            >>> print(len(report.accounts))  # 3
        """
        # v1: Mock data
        score = self.get_credit_score(user_id)

        accounts = [
            CreditAccount(
                account_id="acc_cc_chase",
                account_type="credit_card",
                creditor_name="Chase Bank",
                account_status="open",
                balance=Decimal("3500.00"),
                credit_limit=Decimal("10000.00"),
                payment_status="current",
                opened_date=date(2018, 3, 15),
                last_payment_date=date(2025, 1, 1),
                monthly_payment=Decimal("150.00"),
            ),
            CreditAccount(
                account_id="acc_auto_ford",
                account_type="auto_loan",
                creditor_name="Ford Motor Credit",
                account_status="open",
                balance=Decimal("12000.00"),
                credit_limit=None,
                payment_status="current",
                opened_date=date(2022, 6, 1),
                last_payment_date=date(2025, 1, 1),
                monthly_payment=Decimal("450.00"),
            ),
            CreditAccount(
                account_id="acc_student_navient",
                account_type="student_loan",
                creditor_name="Navient",
                account_status="open",
                balance=Decimal("25000.00"),
                credit_limit=None,
                payment_status="current",
                opened_date=date(2015, 9, 1),
                last_payment_date=date(2025, 1, 1),
                monthly_payment=Decimal("300.00"),
            ),
        ]

        inquiries = [
            CreditInquiry(
                inquiry_id="inq_chase_2025",
                inquiry_type="hard",
                inquirer_name="Chase Bank",
                inquiry_date=date(2025, 1, 1),
                purpose="credit_card_application",
            ),
            CreditInquiry(
                inquiry_id="inq_ford_2024",
                inquiry_type="hard",
                inquirer_name="Ford Motor Credit",
                inquiry_date=date(2024, 12, 15),
                purpose="auto_loan",
            ),
        ]

        return CreditReport(
            user_id=user_id,
            bureau="experian",
            report_date=date.today(),
            score=score,
            accounts=accounts,
            inquiries=inquiries,
            public_records=[],
            consumer_statements=[],
        )

    def subscribe_to_changes(self, user_id: str, webhook_url: str, **kwargs) -> str:
        """Subscribe to credit score change notifications.
        
        v1: Returns mock subscription ID (no real webhook integration).
        v2: Will integrate with Experian webhook API.
        
        Args:
            user_id: User identifier
            webhook_url: URL to receive webhook notifications
            **kwargs: Additional parameters (ignored in v1)
            
        Returns:
            Subscription ID
            
        Example:
            >>> provider = ExperianProvider()
            >>> sub_id = provider.subscribe_to_changes("user123", "https://api.example.com/webhooks")
            >>> print(sub_id)  # "sub_mock_user123"
        """
        # v1: Mock subscription
        return f"sub_mock_{user_id}"


def easy_credit(
    provider: str | CreditProvider = "experian", **config
) -> CreditProvider:
    """Create configured credit provider with environment variable auto-detection.
    
    Zero-config builder for credit monitoring. Automatically reads configuration
    from environment variables.
    
    Args:
        provider: Bureau name or CreditProvider instance
            - "experian" (default): Experian provider
            - "equifax": Equifax provider (future)
            - "transunion": TransUnion provider (future)
            - CreditProvider instance: Use directly
        **config: Optional configuration overrides
            - api_key: API key (overrides env)
            - environment: "sandbox" or "production" (overrides env)
            
    Returns:
        Configured CreditProvider instance
        
    Environment Variables:
        EXPERIAN_API_KEY: API key for Experian API
        EXPERIAN_CLIENT_ID: Client ID (if required)
        EXPERIAN_ENVIRONMENT: "sandbox" or "production" (default: sandbox)
        
    Examples:
        >>> # Zero config (uses EXPERIAN_API_KEY from env)
        >>> credit = easy_credit()
        >>> score = credit.get_credit_score("user123")
        
        >>> # Explicit provider
        >>> credit = easy_credit(provider="experian", api_key="...")
        >>> report = credit.get_credit_report("user123")
        
        >>> # Custom provider instance
        >>> custom_provider = ExperianProvider(api_key="...", environment="production")
        >>> credit = easy_credit(provider=custom_provider)
    """
    # If provider is already a CreditProvider instance, return it
    if isinstance(provider, CreditProvider):
        return provider

    # Load settings from environment
    settings = Settings()

    # Provider factory
    if provider == "experian":
        # Auto-detect from env or use config overrides
        api_key = config.pop("api_key", getattr(settings, "experian_api_key", None))
        environment = config.pop(
            "environment", getattr(settings, "experian_environment", "sandbox")
        )
        return ExperianProvider(api_key=api_key, environment=environment, **config)
    elif provider == "equifax":
        raise NotImplementedError("Equifax provider not implemented yet (v2)")
    elif provider == "transunion":
        raise NotImplementedError("TransUnion provider not implemented yet (v2)")
    else:
        raise ValueError(f"Unknown credit provider: {provider}")


__all__ = [
    "ExperianProvider",
    "easy_credit",
]
