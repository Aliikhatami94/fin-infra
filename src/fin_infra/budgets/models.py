"""Pydantic models for budget management.

This module defines the data models for budgets, categories, progress tracking,
alerts, and templates. All models are generic and application-agnostic.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class BudgetType(str, Enum):
    """Budget type classification.
    
    Generic across applications:
    - personal: Individual budget (personal finance apps)
    - household: Shared family budget (household management)
    - business: Company/department budget (business accounting)
    - project: Project-specific budget (project management)
    - custom: User-defined budget type
    """

    PERSONAL = "personal"
    HOUSEHOLD = "household"
    BUSINESS = "business"
    PROJECT = "project"
    CUSTOM = "custom"


class BudgetPeriod(str, Enum):
    """Budget period for tracking cycles.
    
    Supports various budgeting frequencies:
    - weekly: 7 days (short-term tracking)
    - biweekly: 14 days (paycheck cycles)
    - monthly: 30 days (most common)
    - quarterly: 90 days (business planning)
    - yearly: 365 days (annual budgets)
    """

    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


# TODO: Define remaining models in Task 12
# - Budget
# - BudgetCategory
# - BudgetProgress
# - BudgetAlert
# - BudgetTemplate
