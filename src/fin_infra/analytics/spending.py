"""Spending insights and analysis.

Provides comprehensive spending analysis with merchant breakdowns, category trends,
anomaly detection, and month-over-month comparisons.

Generic Applicability:
- Personal finance: Track spending habits and identify savings opportunities
- Business accounting: Expense analysis and budget compliance
- Wealth management: Client spending patterns and advisory insights
- Banking apps: Spending alerts and recommendations
- Budgeting tools: Category-level spending insights

Examples:
    >>> # Analyze last 30 days of spending
    >>> insights = await analyze_spending("user123", period="30d")
    >>> print(f"Top merchant: {insights.top_merchants[0]}")
    >>> print(f"Total spending: ${insights.total_spending:.2f}")
    
    >>> # Analyze specific categories only
    >>> insights = await analyze_spending("user123", categories=["Groceries", "Restaurants"])
    
    >>> # Detect spending anomalies
    >>> for anomaly in insights.anomalies:
    ...     print(f"Alert: {anomaly.category} spending is {anomaly.severity}")
"""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional

from fin_infra.analytics.models import SpendingAnomaly, SpendingInsight, TrendDirection
from fin_infra.models import Transaction


async def analyze_spending(
    user_id: str,
    *,
    period: str = "30d",
    categories: Optional[list[str]] = None,
    banking_provider=None,
    categorization_provider=None,
) -> SpendingInsight:
    """Analyze spending patterns and trends.
    
    Provides comprehensive spending insights including:
    - Top merchants by total spending
    - Category breakdown with totals and percentages
    - Spending trends (increasing, decreasing, stable)
    - Anomaly detection (unusual spending patterns)
    - Historical comparisons
    
    Args:
        user_id: User identifier
        period: Analysis period (e.g., "7d", "30d", "90d")
        categories: Filter to specific categories (None = all categories)
        banking_provider: Banking data provider (optional, for DI)
        categorization_provider: Categorization provider (optional, for DI)
    
    Returns:
        SpendingInsight with comprehensive spending analysis
    
    Raises:
        ValueError: If period format invalid
    
    Examples:
        >>> # Last 30 days of spending
        >>> insights = await analyze_spending("user123", period="30d")
        >>> insights.top_merchants[0]
        ('Amazon', 450.00)
        
        >>> # Specific categories only
        >>> insights = await analyze_spending(
        ...     "user123", 
        ...     categories=["Groceries", "Restaurants"]
        ... )
        >>> insights.category_breakdown
        {'Groceries': 320.50, 'Restaurants': 180.25}
    """
    # Parse period
    days = _parse_period(period)
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # TODO: Fetch transactions from banking provider
    # transactions = await banking_provider.get_transactions(
    #     user_id=user_id,
    #     start_date=start_date,
    #     end_date=end_date,
    # )
    
    # TODO: Categorize transactions with categorization provider
    # categorized_transactions = await _categorize_transactions(
    #     transactions, categorization_provider
    # )
    
    # Mock implementation for now
    # Simulate realistic spending data
    transactions = _generate_mock_transactions(days)
    
    # Filter expense transactions only (negative amounts)
    expense_transactions = [t for t in transactions if t.amount < 0]
    
    # Filter by categories if specified
    if categories:
        expense_transactions = [
            t for t in expense_transactions
            if _get_transaction_category(t) in categories
        ]
    
    # Calculate top merchants
    merchant_totals = defaultdict(float)
    for t in expense_transactions:
        merchant = _extract_merchant_name(t.description or "Unknown")
        merchant_totals[merchant] += abs(t.amount)
    
    top_merchants = sorted(
        merchant_totals.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]  # Top 10 merchants
    
    # Calculate category breakdown
    category_totals = defaultdict(float)
    for t in expense_transactions:
        category = _get_transaction_category(t)
        category_totals[category] += abs(t.amount)
    
    # Calculate total spending
    total_spending = sum(abs(t.amount) for t in expense_transactions)
    
    # Calculate spending trends by category
    spending_trends = await _calculate_spending_trends(
        user_id, category_totals, days, banking_provider, categorization_provider
    )
    
    # Detect anomalies
    anomalies = await _detect_spending_anomalies(
        user_id, category_totals, days, banking_provider, categorization_provider
    )
    
    return SpendingInsight(
        top_merchants=top_merchants,
        category_breakdown=dict(category_totals),
        spending_trends=spending_trends,
        anomalies=anomalies,
        period_days=days,
        total_spending=total_spending,
    )


def _parse_period(period: str) -> int:
    """Parse period string to number of days.
    
    Args:
        period: Period string like "7d", "30d", "90d"
    
    Returns:
        Number of days
    
    Raises:
        ValueError: If period format invalid
    """
    period = period.strip().lower()
    
    if not period.endswith("d"):
        raise ValueError(f"Invalid period format '{period}'. Expected format: '30d'")
    
    try:
        days = int(period[:-1])
    except ValueError:
        raise ValueError(f"Invalid period format '{period}'. Expected format: '30d'")
    
    if days <= 0:
        raise ValueError(f"Period must be positive, got {days} days")
    
    return days


def _extract_merchant_name(description: str) -> str:
    """Extract merchant name from transaction description.
    
    Args:
        description: Transaction description
    
    Returns:
        Cleaned merchant name
    """
    # Simple extraction: take first word/phrase (before common patterns)
    description = description.strip().upper()
    
    # Remove common transaction prefixes
    for prefix in ["DEBIT CARD PURCHASE", "POS", "PAYMENT TO", "TRANSFER TO"]:
        if description.startswith(prefix):
            description = description[len(prefix):].strip()
    
    # Take first meaningful part (split on common separators)
    for separator in [" - ", " #", " *", "  "]:
        if separator in description:
            description = description.split(separator)[0]
    
    # Limit length
    if len(description) > 30:
        description = description[:30]
    
    return description.strip() or "Unknown Merchant"


def _get_transaction_category(transaction: Transaction) -> str:
    """Get category for a transaction.
    
    Args:
        transaction: Transaction to categorize
    
    Returns:
        Category name
    """
    # TODO: Use categorization provider
    # For now, simple heuristic based on description
    description = (transaction.description or "").lower()
    
    # Simple keyword matching
    if any(kw in description for kw in ["grocery", "safeway", "whole foods", "trader joe"]):
        return "Groceries"
    elif any(kw in description for kw in ["restaurant", "cafe", "starbucks", "mcdonald"]):
        return "Restaurants"
    elif any(kw in description for kw in ["gas", "fuel", "shell", "chevron"]):
        return "Transportation"
    elif any(kw in description for kw in ["amazon", "target", "walmart", "retail"]):
        return "Shopping"
    elif any(kw in description for kw in ["netflix", "spotify", "hulu", "apple music"]):
        return "Entertainment"
    elif any(kw in description for kw in ["rent", "mortgage", "apartment"]):
        return "Housing"
    elif any(kw in description for kw in ["electric", "gas bill", "water", "internet"]):
        return "Utilities"
    else:
        return "Other"


async def _calculate_spending_trends(
    user_id: str,
    current_category_totals: dict[str, float],
    current_period_days: int,
    banking_provider=None,
    categorization_provider=None,
) -> dict[str, TrendDirection]:
    """Calculate spending trends by category.
    
    Compares current period to previous period to determine if spending
    is increasing, decreasing, or stable.
    
    Args:
        user_id: User identifier
        current_category_totals: Current period spending by category
        current_period_days: Number of days in current period
        banking_provider: Banking data provider (optional)
        categorization_provider: Categorization provider (optional)
    
    Returns:
        Dictionary mapping category to trend direction
    """
    # TODO: Fetch previous period data from banking provider
    # For now, mock historical comparison
    
    trends = {}
    for category, current_amount in current_category_totals.items():
        # Mock: assume previous period was 10% lower on average
        # In reality, would fetch historical data
        previous_amount = current_amount * 0.9
        
        change_percent = ((current_amount - previous_amount) / previous_amount) * 100 if previous_amount > 0 else 0
        
        # Threshold for "stable" is within 5%
        threshold = 5.0
        
        if abs(change_percent) < threshold:
            trends[category] = TrendDirection.STABLE
        elif change_percent > 0:
            trends[category] = TrendDirection.INCREASING
        else:
            trends[category] = TrendDirection.DECREASING
    
    return trends


async def _detect_spending_anomalies(
    user_id: str,
    current_category_totals: dict[str, float],
    current_period_days: int,
    banking_provider=None,
    categorization_provider=None,
) -> list[SpendingAnomaly]:
    """Detect unusual spending patterns.
    
    Identifies categories where current spending significantly deviates
    from historical averages.
    
    Args:
        user_id: User identifier
        current_category_totals: Current period spending by category
        current_period_days: Number of days in current period
        banking_provider: Banking data provider (optional)
        categorization_provider: Categorization provider (optional)
    
    Returns:
        List of detected anomalies
    """
    # TODO: Fetch historical averages from banking provider
    # For now, mock anomaly detection
    
    anomalies = []
    
    for category, current_amount in current_category_totals.items():
        # Mock: assume historical average is current amount * 0.8
        # In reality, would calculate from historical data
        average_amount = current_amount * 0.8
        
        deviation_percent = ((current_amount - average_amount) / average_amount) * 100 if average_amount > 0 else 0
        
        # Detect anomalies based on deviation
        if abs(deviation_percent) >= 50:  # Severe: 50%+ deviation
            severity = "severe"
        elif abs(deviation_percent) >= 30:  # Moderate: 30-50% deviation
            severity = "moderate"
        elif abs(deviation_percent) >= 15:  # Minor: 15-30% deviation
            severity = "minor"
        else:
            continue  # No anomaly
        
        anomalies.append(SpendingAnomaly(
            category=category,
            current_amount=current_amount,
            average_amount=average_amount,
            deviation_percent=deviation_percent,
            severity=severity,
        ))
    
    # Sort by severity (severe first)
    severity_order = {"severe": 0, "moderate": 1, "minor": 2}
    anomalies.sort(key=lambda a: severity_order.get(a.severity, 3))
    
    return anomalies


def _generate_mock_transactions(days: int) -> list[Transaction]:
    """Generate mock transactions for testing.
    
    Args:
        days: Number of days to generate transactions for
    
    Returns:
        List of mock transactions
    """
    from datetime import date
    from decimal import Decimal
    
    transactions = []
    base_date = date.today()
    
    # Generate various expense transactions
    mock_data = [
        ("AMAZON.COM", -85.00, 2),
        ("SAFEWAY GROCERIES", -120.50, 3),
        ("STARBUCKS CAFE", -5.50, 5),
        ("SHELL GAS STATION", -45.00, 7),
        ("NETFLIX SUBSCRIPTION", -15.99, 10),
        ("TARGET RETAIL", -67.30, 12),
        ("WHOLE FOODS", -95.20, 15),
        ("RESTAURANT DINNER", -75.00, 18),
        ("AMAZON.COM", -150.00, 20),
        ("SAFEWAY GROCERIES", -110.00, 22),
        ("ELECTRIC COMPANY", -85.00, 25),
        ("SPOTIFY PREMIUM", -9.99, 26),
        ("GAS STATION", -50.00, 28),
    ]
    
    for i, (description, amount, days_ago) in enumerate(mock_data):
        if days_ago <= days:  # Only include if within period
            transactions.append(Transaction(
                id=f"mock_{i}",
                account_id="mock_account",
                amount=Decimal(str(amount)),
                date=base_date - timedelta(days=days_ago),
                description=description,
            ))
    
    return transactions
