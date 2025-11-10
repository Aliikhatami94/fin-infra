"""
Goals module for financial goal tracking and management.

Provides comprehensive goal management with milestone tracking,
funding allocation, and progress monitoring.
"""

from fin_infra.goals.management import (
    FinancialGoalTracker,
    GoalProgressReport,
    GoalValidation,
    calculate_debt_free_goal,
    calculate_home_purchase_goal,
    calculate_retirement_goal,
    calculate_wealth_milestone,
)
from fin_infra.goals.models import (
    FundingSource,
    Goal,
    GoalProgress,
    GoalStatus,
    GoalType,
    Milestone,
)

__all__ = [
    # Tracker and validation (from management.py)
    "FinancialGoalTracker",
    "GoalProgressReport",
    "GoalValidation",
    "calculate_debt_free_goal",
    "calculate_home_purchase_goal",
    "calculate_retirement_goal",
    "calculate_wealth_milestone",
    # Enhanced models (from models.py)
    "FundingSource",
    "Goal",
    "GoalProgress",
    "GoalStatus",
    "GoalType",
    "Milestone",
]
