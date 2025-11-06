"""Data normalization module for financial symbols and currencies."""

from fin_infra.normalization.currency_converter import (
    CurrencyConverter,
    CurrencyNotSupportedError,
)
from fin_infra.normalization.models import (
    CurrencyConversionResult,
    ExchangeRate,
    SymbolMetadata,
)
from fin_infra.normalization.symbol_resolver import (
    SymbolNotFoundError,
    SymbolResolver,
)

__all__ = [
    "SymbolResolver",
    "CurrencyConverter",
    "easy_normalization",
    "SymbolMetadata",
    "ExchangeRate",
    "CurrencyConversionResult",
    "SymbolNotFoundError",
    "CurrencyNotSupportedError",
]


# Singleton instances (initialized lazily)
_resolver_instance: SymbolResolver | None = None
_converter_instance: CurrencyConverter | None = None


def easy_normalization(
    api_key: str | None = None,
) -> tuple[SymbolResolver, CurrencyConverter]:
    """
    Get configured symbol resolver and currency converter (one-liner setup).

    Returns singleton instances on subsequent calls for efficiency.

    Args:
        api_key: Optional API key for exchangerate-api.io (paid tier)

    Returns:
        Tuple of (SymbolResolver, CurrencyConverter)

    Example:
        >>> from fin_infra.normalization import easy_normalization
        >>> resolver, converter = easy_normalization()
        >>> ticker = await resolver.to_ticker("037833100")  # CUSIP → AAPL
        >>> eur = await converter.convert(100, "USD", "EUR")  # 92.0
    """
    global _resolver_instance, _converter_instance

    if _resolver_instance is None:
        _resolver_instance = SymbolResolver()

    if _converter_instance is None:
        _converter_instance = CurrencyConverter(api_key=api_key)

    return _resolver_instance, _converter_instance
