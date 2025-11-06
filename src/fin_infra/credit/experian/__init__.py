"""Experian credit bureau integration.

This package implements real Experian API integration with:
- OAuth 2.0 authentication
- Credit score and report endpoints
- Response parsing to fin_infra models
- Error handling and retries
- FCRA compliance logging

Architecture:
    auth.py - OAuth token management
    client.py - HTTP client for Experian API
    parser.py - Response parsing to Pydantic models
    provider.py - CreditProvider implementation

Example:
    >>> from fin_infra.credit.experian import ExperianProvider
    >>> provider = ExperianProvider(api_key="...", environment="sandbox")
    >>> score = await provider.get_credit_score("user123")
"""

from fin_infra.credit.experian.provider import ExperianProvider

__all__ = ["ExperianProvider"]
