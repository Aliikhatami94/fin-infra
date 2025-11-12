# fin-infra Template Project Implementation Plan

## Executive Summary

Create a comprehensive `/examples` template project for fin-infra that mirrors svc-infra's approach: a complete, runnable fintech application demonstrating **ALL** fin-infra capabilities with proper integration to svc-infra backend infrastructure.

**Goal**: Developers can run `make setup && make run` and have a fully functional fintech API showcasing every fin-infra feature with real implementations.

**Status**: Planning phase. Follow Research → Design → Implement → Tests → Verify → Docs workflow.

## Legend
- [ ] Pending
- [x] Completed
- [~] Skipped (already exists / out of scope)
- (note) Commentary or link to related docs

---

## CRITICAL: Complete Capabilities Inventory

Based on comprehensive research of fin-infra codebase (src/fin_infra/), documentation (docs/), and API surface (__all__ exports), fin-infra provides **20+ distinct capabilities** across 15+ modules:

### Core Financial Data (Provider Integrations)
- [ ] 1. **Banking** (`fin_infra.banking`) - Account aggregation
   - Providers: Teller (mTLS default), Plaid (OAuth), MX (coming soon)
   - Functions: `add_banking()`, `easy_banking()`
   - Endpoints: /banking/link, /banking/accounts, /banking/transactions, /banking/balances

- [ ] 2. **Market Data** (`fin_infra.markets`) - Equities, ETFs, indexes
   - Providers: Alpha Vantage (default), Yahoo Finance, Polygon
   - Functions: `easy_market()`
   - Endpoints: /market/quote/{symbol}, /market/historical/{symbol}

- [ ] 3. **Crypto Data** (`fin_infra.crypto`) - Cryptocurrency market data
   - Providers: CoinGecko (primary), Yahoo Finance, CCXT exchanges
   - Functions: `add_crypto_data()`, `easy_crypto()`
   - Endpoints: /crypto/quote/{symbol}, /crypto/portfolio, /crypto/insights (AI-powered)

- [ ] 4. **Credit Scores** (`fin_infra.credit`) - FICO/VantageScore
   - Providers: Experian (OAuth 2.0), Equifax (coming), TransUnion (coming)
   - Functions: `add_credit()`, `easy_credit()`
   - Endpoints: /credit/score, /credit/report, /credit/factors, /credit/monitoring

- [ ] 5. **Brokerage** (`fin_infra.brokerage`) - Trading accounts
   - Providers: Alpaca (paper/live), Interactive Brokers (coming), SnapTrade
   - Functions: `add_brokerage()`, `easy_brokerage()`
   - Endpoints: /brokerage/portfolio, /brokerage/positions, /brokerage/orders

- [ ] 6. **Tax Data** (`fin_infra.tax`) - Tax documents and calculations
   - Providers: IRS e-File (coming), TaxBit, TurboTax, H&R Block integrations
   - Functions: `add_tax_data()`, `easy_tax()`
   - Endpoints: /tax/documents, /tax/liability, /tax/tlh (tax-loss harvesting)

### Financial Intelligence (Analytics & AI)
- [ ] 7. **Analytics** (`fin_infra.analytics`) - Financial insights and advice
   - 7 endpoints: cash flow, savings rate, spending insights, AI advice, portfolio analytics, growth projections, rebalancing suggestions
   - Functions: `add_analytics()`, `easy_analytics()`
   - AI: LLM-powered recommendations via ai-infra CoreLLM
   - Caching: 24h TTL for insights, 1h for real-time metrics

- [ ] 8. **Categorization** (`fin_infra.categorization`) - Transaction categorization
   - 56 MX-style categories, 100+ merchant rules
   - Functions: `add_categorization()`, `easy_categorization()`
   - Performance: ~1000 predictions/sec, ~2.5ms avg latency
   - LLM: Google Gemini/OpenAI/Anthropic for unknown merchants (<$0.0002/txn with caching)

- [ ] 9. **Recurring Detection** (`fin_infra.recurring`) - Subscription identification
   - Patterns: Fixed subscriptions, variable bills, irregular/annual charges
   - Functions: `add_recurring_detection()`, `easy_recurring_detection()`
   - Endpoints: /recurring/detect, /recurring/insights

- [ ] 10. **Insights Feed** (`fin_infra.insights`) - Unified dashboard
    - Aggregates: Net worth, budgets, goals, recurring, portfolio, tax, crypto
    - Functions: `add_insights()`
    - Priority: High/medium/low with action items
    - Endpoints: /insights/feed, /insights/priority

### Financial Planning (Goals & Budgets)
- [ ] 11. **Budgets** (`fin_infra.budgets`) - Budget management
    - 8 endpoints: CRUD, progress tracking, alerts (80%/100%/110%), templates (50/30/20, Zero-Based, Envelope)
    - Functions: `add_budgets()`, `easy_budgets()`
    - Types: Personal, household, business, project, custom
    - Rollover: Optional carry-over of unused budget

- [ ] 12. **Goals** (`fin_infra.goals`) - Financial goal tracking
    - 13 endpoints: CRUD, milestones, funding allocation, pause/resume/complete
    - Functions: `add_goals()`, `easy_goals()`
    - Types: Savings, debt payoff, investment, net worth, income, custom
    - Milestones: Checkpoint amounts with target dates

- [ ] 13. **Net Worth Tracking** (`fin_infra.net_worth`) - Multi-account net worth
    - 4 endpoints: current, history, breakdown, manual snapshot
    - Functions: `add_net_worth_tracking()`, `easy_net_worth()`
    - Categories: 6 asset types, 6 liability types
    - Jobs: Daily automatic snapshots via svc-infra
    - Alerts: Notify on ≥5% OR ≥$10k change

### Document & Compliance
- [ ] 14. **Documents** (`fin_infra.documents`) - Financial document management
    - Functions: `add_documents()`, `easy_documents()`
    - OCR: Tesseract (85% confidence), AWS Textract (96%)
    - AI: Document analysis via ai-infra
    - Types: Tax forms, bank statements, receipts, invoices, contracts, insurance, other

- [ ] 15. **Security** (`fin_infra.security`) - Financial PII protection
    - Functions: `add_financial_security()`
    - Features: PII detection (regex + context + Luhn/ABA validation), encryption, audit logging
    - Compliance: PCI-DSS, SOC 2, GDPR, GLBA, CCPA ready
    - Zero-config: One-line setup

- [ ] 16. **Compliance** (`fin_infra.compliance`) - Regulatory compliance
    - Functions: `add_compliance_tracking()`
    - Features: PII classification (3 tiers), data retention (GLBA 5yr, FCRA 7yr), erasure workflows
    - Integration: svc-infra data lifecycle

### Utilities & Cross-Cutting
- [ ] 17. **Normalization** (`fin_infra.normalization`) - Data standardization
    - Functions: `easy_normalization()`
    - Operations: Symbol resolution (ticker↔CUSIP↔ISIN), provider normalization, currency conversion
    - Endpoints: /normalize/symbol, /normalize/currency, /normalize/batch

- [ ] 18. **Observability** (`fin_infra.obs`) - Financial metrics classification
    - Functions: `financial_route_classifier`
    - Integration: svc-infra Prometheus + OpenTelemetry
    - Metrics: Provider calls, LLM costs, API latencies, cache hit/miss

- [ ] 19. **Cashflows** (`fin_infra.cashflows`) - Financial calculations
    - Functions: NPV, IRR, XNPV, XIRR, PMT, FV, PV, loan amortization
    - Endpoints: /cashflows/npv, /cashflows/irr, /cashflows/pmt, /cashflows/amortization

- [ ] 20. **Conversation** (`fin_infra.chat`) - AI financial chat
    - Functions: `easy_financial_conversation()`
    - AI: Multi-turn Q&A via ai-infra FinancialPlanningConversation
    - Endpoints: /chat (POST for questions)

### Scaffolding (CLI Tool)
- [ ] 21. **Scaffolding** (`fin_infra.scaffold`) - Code generation
    - CLI: `fin-infra scaffold budgets --dest-dir app/models/`
    - Generates: SQLAlchemy models, Pydantic schemas, repositories
    - Integration: svc-infra ModelBase, SqlResource

---

## CRITICAL: Implementation Standards

### Mandatory Research Before Each Phase
Before implementing ANY phase, follow this protocol:

#### Step 1: Check svc-infra Examples
- [ ] Review `/Users/alikhatami/ide/infra/svc-infra/examples/` structure
- [ ] Check svc-infra example scripts (quick_setup.py, scaffold_models.py)
- [ ] Review svc-infra Makefile patterns
- [ ] Study svc-infra main.py feature showcase pattern

#### Step 2: Verify Reuse Opportunities
- [ ] Check if svc-infra already provides needed infrastructure
- [ ] Identify fin-infra-specific vs generic patterns
- [ ] Document which parts to reuse vs implement

#### Step 3: Document Findings
For each phase, add:
```markdown
- [ ] Research: [Phase name]
  - svc-infra pattern: [Pattern found or "not applicable"]
  - Classification: [Reuse / Adapt / New]
  - Justification: [Why this approach]
  - Reuse plan: [Specific files/patterns to reuse]
```

---

## Current State Analysis

### Existing Examples Structure
```
fin-infra/examples/
├── README.md              # Generic placeholder docs
├── demo_api/              # Minimal demo (banking + market data only)
│   ├── .env.example
│   ├── README.md
│   └── app.py            # 105 lines, 2 capabilities only
└── scripts/              # Empty or utility scripts
```

### Issues with Current Setup
1. ❌ **Incomplete**: Only shows banking + market data (2 of 15+ capabilities)
2. ❌ **Not Runnable**: No Poetry setup, no migrations, no database
3. ❌ **No Structure**: Missing models, schemas, proper API organization
4. ❌ **No Easy Setup**: No `make setup`, no automated scaffolding
5. ❌ **Poor Documentation**: No quickstart, no inline guides
6. ❌ **Missing Integration**: Doesn't show fin-infra + svc-infra best practices

---

## Target Architecture (Based on svc-infra Pattern)

### Directory Structure
```
fin-infra/examples/
├── .env
├── .env.example
├── .gitignore
├── Makefile                    # NEW: Complete automation
├── pyproject.toml              # NEW: Poetry config with fin-infra + svc-infra
├── poetry.lock
├── alembic.ini                 # NEW: Database migrations config
├── run.sh                      # NEW: Development server launcher
├── create_tables.py            # NEW: Quick table creation
├── QUICKSTART.md               # NEW: 5-minute getting started
├── README.md                   # NEW: Complete showcase documentation
├── USAGE.md                    # NEW: Detailed feature usage guide
├── docs/                       # NEW: Comprehensive guides
│   ├── CAPABILITIES.md         # All fin-infra features explained
│   ├── DATABASE.md             # Database setup and migrations
│   ├── CLI.md                  # fin-infra CLI reference
│   └── PROVIDERS.md            # Provider configuration guide
├── migrations/                 # NEW: Alembic migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── scripts/                    # NEW: Automation scripts
│   ├── quick_setup.py          # Scaffold + migrate in one command
│   ├── scaffold_models.py      # Generate financial models
│   └── test_providers.py       # Test provider connections
└── src/
    └── fin_infra_template/     # NEW: Complete application package
        ├── __init__.py
        ├── main.py             # 1000+ lines: ALL features demonstrated
        ├── settings.py         # Type-safe configuration
        ├── db/
        │   ├── __init__.py
        │   ├── base.py         # SQLAlchemy Base
        │   ├── models.py       # Financial models (User, Account, Transaction, etc.)
        │   └── schemas.py      # Pydantic schemas
        └── api/
            ├── __init__.py
            └── v1/
                ├── __init__.py
                └── routes.py   # Custom endpoints
```

---

## Implementation Phases

### Phase 1: Project Structure & Core Setup

**Owner**: TBD — **Evidence**: PRs, commits, directory structure

#### Research Phase
- [x] **Research (svc-infra examples check)**:
  - [x] Review svc-infra `/examples/pyproject.toml` structure and dependencies
  - [x] Check svc-infra `/examples/Makefile` commands and patterns
  - [x] Review svc-infra `/examples/.env.example` format and variables
  - [x] Study svc-infra `/examples/run.sh` launcher pattern
  - [x] Classification: Adapt (reuse svc-infra patterns with fin-infra specifics)
  - [x] Justification: Project setup is generic, but needs fin-infra provider configs
  - [x] Reuse plan: Copy svc-infra structure, add fin-infra provider sections
  - [x] Evidence: `/Users/alikhatami/ide/infra/svc-infra/examples/pyproject.toml`, `Makefile`, `.env.example`

#### Design Phase
- [x] Design: Directory structure matching svc-infra pattern
- [x] Design: Poetry dependency specification (fin-infra local path)
- [x] Design: Makefile commands (help, install, setup, run, clean, test-providers)
- [x] Design: Environment variable schema (app config + all providers)
- [x] Design: .gitignore patterns (financial data, credentials, artifacts)

#### Implementation Phase

**Deliverables**:
1. `pyproject.toml` with fin-infra + svc-infra dependencies
2. `Makefile` with automation commands
3. `.env.example` with all provider credentials
4. Basic directory structure
5. `run.sh` development server launcher

**Files to Create**:
- [x] `pyproject.toml` - Poetry config
  ```toml
  [tool.poetry]
  name = "fin-infra-template"
  version = "0.1.0"
  description = "Complete fintech application template demonstrating fin-infra + svc-infra"
  package-mode = false
  
  [tool.poetry.dependencies]
  python = ">=3.11,<4.0"
  fin-infra = { path = "../", develop = true }
  svc-infra = "^0.1.0"
  aiosqlite = "^0.20.0"
  pydantic-settings = "^2.0.0"
  ```

- [x] `Makefile` - Commands: `help`, `install`, `setup`, `run`, `clean`, `test-providers`
  ```makefile
  help: ## Show available commands
  install: ## Install dependencies with Poetry
  setup: install ## Complete setup (scaffold + migrate)
  run: ## Start development server
  clean: ## Clean cache files
  test-providers: ## Test provider connections
  ```

- [x] `.env.example` - All provider credentials
  ```bash
  # App Configuration
  APP_ENV=local
  API_PORT=8001
  SQL_URL=sqlite+aiosqlite:////tmp/fin_infra_template.db
  
  # Backend Infrastructure (svc-infra)
  REDIS_URL=redis://localhost:6379/0
  METRICS_ENABLED=true
  
  # Banking Providers (fin-infra)
  PLAID_CLIENT_ID=your_client_id
  PLAID_SECRET=your_secret
  PLAID_ENV=sandbox
  TELLER_API_KEY=your_teller_key
  
  # Market Data (fin-infra)
  ALPHAVANTAGE_API_KEY=your_api_key
  
  # Credit Scores (fin-infra)
  EXPERIAN_CLIENT_ID=your_client_id
  EXPERIAN_CLIENT_SECRET=your_secret
  
  # Brokerage (fin-infra)
  ALPACA_API_KEY=your_key
  ALPACA_SECRET_KEY=your_secret
  ALPACA_ENV=paper
  
  # AI/LLM (for crypto insights, categorization)
  GOOGLE_API_KEY=your_gemini_key
  ```

- [x] `.gitignore` - Standard ignores + financial data
  ```
  __pycache__/
  *.pyc
  .env
  .venv/
  poetry.lock
  *.db
  migrations/versions/*.py  # Except __init__
  ```

- [x] `run.sh` - Development server launcher
  ```bash
  #!/bin/bash
  poetry run uvicorn fin_infra_template.main:app --reload --port ${API_PORT:-8001}
  ```

#### Testing Phase
- [x] Tests: Verify `poetry install` completes without errors
- [x] Tests: Verify `.env.example` has all required provider variables (70+ variables across all providers)
- [x] Tests: Verify `make help` displays all commands correctly
- [x] Tests: Verify `run.sh` is executable with correct shebang
- [x] Tests: Verify directory structure matches design

#### Verification Phase
- [x] Verify: `poetry install` works in clean environment (177 packages installed successfully)
- [x] Verify: `.env.example` covers all 15+ capabilities (103 environment variables configured)
- [x] Verify: `make help` shows descriptive help text (8 commands documented)
- [x] Verify: All files have proper permissions (run.sh is executable: -rwxr-xr-x)
- [x] Verify: .gitignore prevents committing sensitive data (942 bytes with financial patterns)

#### Documentation Phase
- [x] Docs: Add comments in `.env.example` explaining each variable (comprehensive provider docs)
- [x] Docs: Add comments in `Makefile` explaining each target (## comments for all targets)
- [x] Docs: Create basic project structure documentation (docstrings in __init__.py files)

**Success Criteria**:
- ✅ `poetry install` works
- ✅ `.env.example` has all required vars (50+ variables)
- ✅ `make help` shows all commands with descriptions
- ✅ Project structure matches svc-infra pattern
- ✅ All files properly tracked/ignored in git

**[x] Phase 1 Status**: PENDING

---

### Phase 2: Database Models & Migrations

**Owner**: TBD — **Evidence**: PRs, commits, model files, migration files

#### Research Phase
- [ ] **Research (svc-infra examples check)**:
  - [ ] Review svc-infra `/examples/src/svc_infra_template/db/` structure
  - [ ] Check svc-infra model patterns (User, Project, Task examples)
  - [ ] Review svc-infra Alembic configuration (`alembic.ini`, `migrations/env.py`)
  - [ ] Study svc-infra scaffolding scripts (`scripts/scaffold_models.py`, `quick_setup.py`)
  - [ ] Check svc-infra schema patterns (Pydantic BaseModel usage)
  - [ ] Classification: Adapt (reuse patterns, different domain models)
  - [ ] Justification: SQLAlchemy patterns are generic, but financial models are domain-specific
  - [ ] Reuse plan: Copy db structure, adapt models for financial domain
  - [ ] Evidence: `/Users/alikhatami/ide/infra/svc-infra/examples/src/svc_infra_template/db/models.py` (Project, Task), `db/schemas.py`

#### Design Phase
- [ ] Design: Financial model schema (8 core models)
  - User (auth), Account (multi-type), Transaction (spending/income)
  - Position (investments), Goal (targets), Budget (limits)
  - Document (tax forms), NetWorthSnapshot (historical)
- [ ] Design: Pydantic schemas (Base/Create/Read/Update pattern per model)
- [ ] Design: Alembic migration structure (version control for schema changes)
- [ ] Design: Scaffolding script API (generate models, validate, detect duplicates)
- [ ] Design: Quick setup script flow (scaffold → init → revision → upgrade)

#### Implementation Phase

**Deliverables**:
1. Financial models (User, Account, Transaction, Position, Goal, Budget, Document, NetWorthSnapshot)
2. Pydantic schemas for all models (24+ schema classes)
3. Alembic configuration (alembic.ini, env.py, script.py.mako)
4. Automated scaffolding script (safe, non-destructive)
5. Quick setup script (one-command: scaffold + migrate)
6. Create tables script (no migrations, for quick dev)

**Files to Create**:
- [ ] `src/fin_infra_template/db/__init__.py` - Database setup
  ```python
  from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
  from sqlalchemy.orm import sessionmaker, declarative_base
  from fin_infra_template.settings import settings
  
  Base = declarative_base()
  engine = None
  async_session_maker = None
  
  def get_engine():
      global engine, async_session_maker
      if engine is None:
          engine = create_async_engine(settings.sql_url, echo=settings.debug)
          async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
      return engine
  
  async def get_session() -> AsyncSession:
      if async_session_maker is None:
          get_engine()
      async with async_session_maker() as session:
          yield session
  ```

- [ ] `src/fin_infra_template/db/models.py` - Financial models (500+ lines)
  ```python
  from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum
  from sqlalchemy.orm import relationship
  from datetime import datetime
  from . import Base
  
  # Core Models
  class User(Base):
      """User model for authentication."""
      __tablename__ = "users"
      id, email, hashed_password, created_at, updated_at
  
  class Account(Base):
      """Financial account (bank, brokerage, crypto)."""
      __tablename__ = "accounts"
      id, user_id, account_type, institution, balance, currency, created_at
  
  class Transaction(Base):
      """Financial transaction."""
      __tablename__ = "transactions"
      id, account_id, amount, category, description, date, merchant, created_at
  
  class Position(Base):
      """Investment position (stock, crypto)."""
      __tablename__ = "positions"
      id, account_id, symbol, quantity, cost_basis, current_price, created_at
  
  class Goal(Base):
      """Financial goal tracking."""
      __tablename__ = "goals"
      id, user_id, name, target_amount, current_amount, deadline, status
  
  class Budget(Base):
      """Budget tracking."""
      __tablename__ = "budgets"
      id, user_id, name, categories (JSON), start_date, end_date
  
  class Document(Base):
      """Tax/financial document storage."""
      __tablename__ = "documents"
      id, user_id, document_type, storage_path, extracted_data (JSON)
  
  class NetWorthSnapshot(Base):
      """Historical net worth snapshots."""
      __tablename__ = "net_worth_snapshots"
      id, user_id, total_assets, total_liabilities, net_worth, snapshot_date
  ```

- [ ] `src/fin_infra_template/db/schemas.py` - Pydantic schemas (300+ lines)
  ```python
  from pydantic import BaseModel, Field
  from datetime import datetime
  from typing import Optional
  
  # Account Schemas
  class AccountBase(BaseModel):
      account_type: str
      institution: str
      balance: float
      currency: str = "USD"
  
  class AccountCreate(AccountBase):
      user_id: str
  
  class AccountRead(AccountBase):
      id: int
      user_id: str
      created_at: datetime
  
  # Transaction Schemas
  class TransactionBase(BaseModel):
      amount: float
      category: Optional[str]
      description: str
      date: datetime
      merchant: Optional[str]
  
  class TransactionCreate(TransactionBase):
      account_id: int
  
  class TransactionRead(TransactionBase):
      id: int
      account_id: int
      created_at: datetime
  
  # Goal Schemas
  class GoalBase(BaseModel):
      name: str
      target_amount: float
      current_amount: float = 0.0
      deadline: Optional[datetime]
  
  class GoalCreate(GoalBase):
      user_id: str
  
  class GoalRead(GoalBase):
      id: int
      user_id: str
      status: str
      progress: float
  
  # Budget Schemas (similar pattern)
  # Position Schemas (similar pattern)
  # Document Schemas (similar pattern)
  ```

- [ ] `scripts/scaffold_models.py` - Auto-generate models
  ```python
  """
  Scaffold financial models for fin-infra template.
  
  Generates:
  - User (auth)
  - Account (banking, brokerage, crypto)
  - Transaction (spending, income)
  - Position (investments)
  - Goal (financial goals)
  - Budget (spending limits)
  - Document (tax forms, statements)
  - NetWorthSnapshot (historical tracking)
  """
  ```

- [ ] `scripts/quick_setup.py` - One-command setup
  ```python
  """
  Quick setup: scaffold models + run migrations.
  
  Usage:
      python scripts/quick_setup.py
      python scripts/quick_setup.py --skip-migrations
      python scripts/quick_setup.py --overwrite
  """
  ```

- [ ] `alembic.ini` - Migration config
- [ ] `migrations/env.py` - Alembic environment
- [ ] `migrations/script.py.mako` - Migration template

#### Testing Phase
- [ ] Tests: Unit tests for model validation (8 model classes)
  - [ ] User model (email validation, password hashing)
  - [ ] Account model (balance validation, type enum)
  - [ ] Transaction model (amount validation, date handling)
  - [ ] Position model (quantity validation, cost basis)
  - [ ] Goal model (target validation, progress calculation)
  - [ ] Budget model (category validation, JSON field)
  - [ ] Document model (type validation, extracted data JSON)
  - [ ] NetWorthSnapshot model (calculation validation)
- [ ] Tests: Pydantic schema serialization/deserialization
- [ ] Tests: Scaffolding script (safe mode, overwrite mode, duplicate detection)
- [ ] Tests: Migration generation (autogenerate detects models)
- [ ] Tests: Migration application (upgrade/downgrade)
- [ ] Tests: Quick setup script (end-to-end integration)

#### Verification Phase
- [ ] Verify: `python scripts/scaffold_models.py` generates 8 models without errors
- [ ] Verify: `python scripts/scaffold_models.py` prevents overwriting existing models
- [ ] Verify: `python scripts/scaffold_models.py --overwrite` replaces models safely
- [ ] Verify: `python scripts/quick_setup.py` completes full setup
- [ ] Verify: `make setup` runs without user intervention
- [ ] Verify: Alembic migrations created with proper versioning
- [ ] Verify: Database tables match model definitions
- [ ] Verify: All relationships and foreign keys correct
- [ ] Verify: Indexes created for query performance

#### Documentation Phase
- [ ] Docs: Inline docstrings for all models (purpose, fields, relationships)
- [ ] Docs: Inline docstrings for all schemas (usage, validation rules)
- [ ] Docs: Script usage documentation (`--help` text)
- [ ] Docs: Migration workflow guide (create, apply, rollback)
- [ ] Docs: Model relationship diagram (ASCII or link to external)

**Success Criteria**:
- ✅ `python scripts/scaffold_models.py` generates all 8 models
- ✅ `python scripts/quick_setup.py` completes setup in < 30 seconds
- ✅ `make setup` runs scaffolding + migrations successfully
- ✅ Database tables created successfully with proper schema
- ✅ All model tests passing (40+ tests)
- ✅ Alembic revision history clean and linear
- ✅ Safe duplicate prevention working

**[x] Phase 2 Status**: PENDING

---

### Phase 3: Main Application (ALL Features)

**Owner**: TBD — **Evidence**: PRs, commits, main.py (1000+ lines), settings.py

#### Research Phase
- [ ] **Research (svc-infra examples check)**:
  - [ ] Review svc-infra `/examples/src/svc_infra_template/main.py` structure (754 lines)
  - [ ] Check svc-infra feature showcase pattern (STEP 1-6 organization)
  - [ ] Review svc-infra settings.py pattern (Pydantic Settings, env detection)
  - [ ] Study svc-infra lifecycle events (startup/shutdown handlers)
  - [ ] Check svc-infra easy_* and add_* integration patterns
  - [ ] Review svc-infra inline documentation style
  - [ ] Classification: Adapt (reuse structure, add financial capabilities)
  - [ ] Justification: App structure is generic, but features are financial
  - [ ] Reuse plan: Copy svc-infra organization, add all fin-infra add_*() calls
  - [ ] Evidence: `/Users/alikhatami/ide/infra/svc-infra/examples/src/svc_infra_template/main.py` lines 1-754

#### Design Phase
- [ ] Design: Settings class schema (50+ env vars)
  - App config (env, port, debug)
  - Backend (database, redis, metrics)
  - Providers (banking, market, credit, brokerage, tax)
  - AI/LLM (Google, OpenAI keys)
  - Feature flags (provider_configured properties)
- [ ] Design: main.py organization (STEP 1-6 + financial features)
  - STEP 1: Logging setup (svc-infra)
  - STEP 2: Application setup (svc-infra)
  - STEP 3: Lifecycle events (startup/shutdown)
  - STEP 4: Backend infrastructure (svc-infra)
  - STEP 5: Financial capabilities (fin-infra - 15+ add_*() calls)
  - STEP 6: Custom endpoints (status, features)
- [ ] Design: Feature enablement logic (env-based conditional mounting)
- [ ] Design: Provider instance storage (app.state pattern)
- [ ] Design: Error handling for missing credentials
- [ ] Design: Graceful degradation (partial feature sets)

#### Implementation Phase

**Deliverables**:
1. `settings.py` with complete configuration (200+ lines)
2. `main.py` showcasing ALL 15+ fin-infra capabilities (1000+ lines)
3. Proper integration with svc-infra backend
4. Inline documentation for every feature (docstring per section)
5. Feature flags for enabling/disabling capabilities
6. Custom API routes (/, /health, /features, /status)

**Files to Create**:
- [ ] `src/fin_infra_template/settings.py` - Configuration (200+ lines)
  ```python
  from pydantic_settings import BaseSettings
  from typing import Optional
  
  class Settings(BaseSettings):
      # App Config
      app_env: str = "local"
      api_port: int = 8001
      debug: bool = True
      
      # Database
      sql_url: str = "sqlite+aiosqlite:////tmp/fin_infra_template.db"
      
      # Backend (svc-infra)
      redis_url: Optional[str] = None
      metrics_enabled: bool = True
      
      # Banking (fin-infra)
      plaid_client_id: Optional[str] = None
      plaid_secret: Optional[str] = None
      plaid_env: str = "sandbox"
      teller_api_key: Optional[str] = None
      
      # Market Data (fin-infra)
      alphavantage_api_key: Optional[str] = None
      
      # Credit (fin-infra)
      experian_client_id: Optional[str] = None
      experian_client_secret: Optional[str] = None
      
      # Brokerage (fin-infra)
      alpaca_api_key: Optional[str] = None
      alpaca_secret_key: Optional[str] = None
      alpaca_env: str = "paper"
      
      # AI/LLM
      google_api_key: Optional[str] = None
      
      @property
      def banking_configured(self) -> bool:
          return bool(self.plaid_client_id or self.teller_api_key)
      
      @property
      def market_configured(self) -> bool:
          return bool(self.alphavantage_api_key)
      
      class Config:
          env_file = ".env"
  
  settings = Settings()
  ```

- [ ] `src/fin_infra_template/main.py` - Complete application (1000+ lines)
  
  **Structure**:
  ```python
  """
  Complete fintech application demonstrating ALL fin-infra + svc-infra features.
  
  This is a comprehensive showcase organized in clear steps:
  
  BACKEND INFRASTRUCTURE (svc-infra):
  ✅ Logging (environment-aware)
  ✅ Database (SQLAlchemy + migrations)
  ✅ Caching (Redis)
  ✅ Observability (Prometheus + tracing)
  ✅ Security headers & CORS
  ✅ Rate limiting
  ✅ Health checks
  
  FINANCIAL CAPABILITIES (fin-infra):
  ✅ Banking (Plaid/Teller account aggregation)
  ✅ Market Data (stocks, crypto, forex)
  ✅ Credit Scores (Experian)
  ✅ Brokerage (Alpaca trading)
  ✅ Tax Data (forms, TLH)
  ✅ Analytics (cash flow, savings, portfolio)
  ✅ Budgets (CRUD, templates, tracking)
  ✅ Goals (milestones, recommendations)
  ✅ Documents (OCR, AI analysis)
  ✅ Net Worth (snapshots, insights)
  ✅ Recurring Detection (subscriptions)
  ✅ Categorization (rule-based + LLM)
  ✅ Insights Feed (unified dashboard)
  ✅ Crypto Insights (AI-powered)
  ✅ Rebalancing (tax-optimized)
  ✅ Scenario Modeling (retirement, investment)
  
  Each feature is controlled by environment variables and includes inline docs.
  """
  
  # STEP 1: Logging Setup
  from svc_infra.logging import setup_logging
  setup_logging(level="DEBUG")
  
  # STEP 2: Application Setup
  from svc_infra.api.fastapi import setup_service_api, ServiceInfo, APIVersionSpec
  app = setup_service_api(
      service=ServiceInfo(
          name="fin-infra-template",
          description="Complete fintech app: ALL fin-infra capabilities + svc-infra backend",
          release="1.0.0",
      ),
      versions=[APIVersionSpec(tag="v1", routers_package="fin_infra_template.api.v1")],
  )
  
  # STEP 3: Lifecycle Events
  @app.on_event("startup")
  async def startup():
      """Initialize database, cache, providers."""
      print("🚀 Starting fin-infra-template...")
      # Database setup
      # Cache setup
      # Provider initialization
  
  @app.on_event("shutdown")
  async def shutdown():
      """Cleanup resources."""
      print("👋 Shutting down...")
  
  # STEP 4: Backend Infrastructure (svc-infra)
  from svc_infra.obs import add_observability
  from fin_infra.obs import financial_route_classifier
  add_observability(app, route_classifier=financial_route_classifier)
  
  # STEP 5: Financial Capabilities (fin-infra) - ALL 20+ CAPABILITIES
  
  # ==================== CORE FINANCIAL DATA (PROVIDER INTEGRATIONS) ====================
  
  # 5.1 Banking - Account aggregation (Plaid, Teller, MX)
  # Endpoints: /banking/link, /banking/exchange, /banking/accounts, /banking/transactions
  # Features: OAuth flow, mTLS, transaction sync, balance updates, identity data
  if settings.banking_configured:
      from fin_infra.banking import add_banking
      banking = add_banking(
          app, 
          provider="plaid" if settings.plaid_client_id else "teller",
          prefix="/banking"
      )
      app.state.banking_provider = banking
  
  # 5.2 Market Data - Equities, ETFs, indexes (Alpha Vantage, Yahoo, Polygon)
  # Endpoints: /market/quote/{symbol}, /market/historical/{symbol}, /market/search
  # Features: Real-time quotes, historical data, company info, 60s cache TTL
  if settings.market_configured:
      from fin_infra.markets import add_market_data
      market = add_market_data(
          app, 
          provider="alphavantage",
          prefix="/market"
      )
      app.state.market_provider = market
  
  # 5.3 Crypto Data - Cryptocurrency market data (CoinGecko, Yahoo, CCXT)
  # Endpoints: /crypto/quote/{symbol}, /crypto/portfolio, /crypto/insights
  # Features: Multi-provider fallback, AI-powered insights via ai-infra, portfolio tracking
  from fin_infra.crypto import add_crypto_data
  crypto = add_crypto_data(
      app,
      provider="coingecko",  # Free tier, no API key required
      prefix="/crypto"
  )
  app.state.crypto_provider = crypto
  
  # 5.4 Credit Scores - FICO/VantageScore (Experian, Equifax, TransUnion)
  # Endpoints: /credit/score, /credit/report, /credit/factors, /credit/monitoring
  # Features: OAuth 2.0 flow, full credit reports, change alerts, FCRA compliant
  # Security: High-sensitivity PII (see add_financial_security below)
  if settings.credit_configured:
      from fin_infra.credit import add_credit
      credit = add_credit(
          app,
          provider="experian",
          prefix="/credit"
      )
      app.state.credit_provider = credit
  
  # 5.5 Brokerage - Trading accounts (Alpaca, Interactive Brokers, SnapTrade)
  # Endpoints: /brokerage/portfolio, /brokerage/positions, /brokerage/orders
  # Features: Paper/live trading, order execution, portfolio tracking, SEC registered data
  if settings.brokerage_configured:
      from fin_infra.brokerage import add_brokerage
      brokerage = add_brokerage(
          app,
          provider="alpaca",
          paper_trading=True,  # Default to paper mode for safety
          prefix="/brokerage"
      )
      app.state.brokerage_provider = brokerage
  
  # 5.6 Tax Data - Tax documents and calculations (IRS e-File, TaxBit, Mock)
  # Endpoints: /tax/documents, /tax/liability, /tax/tlh (tax-loss harvesting)
  # Features: Document management, liability calculations, crypto tax reports
  # Compliance: IRS record retention (7 years)
  from fin_infra.tax import add_tax_data
  tax = add_tax_data(app, prefix="/tax")
  app.state.tax_provider = tax
  
  # ==================== FINANCIAL INTELLIGENCE (ANALYTICS & AI) ====================
  
  # 5.7 Analytics - Financial insights and advice (7 endpoints)
  # Endpoints: 
  #   /analytics/cash-flow - Income vs expenses with category breakdowns
  #   /analytics/savings-rate - Gross/net/discretionary savings calculations
  #   /analytics/spending-insights - Pattern detection, anomalies, trends
  #   /analytics/advice - AI-powered spending recommendations (ai-infra CoreLLM)
  #   /analytics/portfolio - Performance, allocation, benchmarks
  #   /analytics/projections - Monte Carlo net worth forecasting
  #   /analytics/rebalance - Tax-optimized rebalancing suggestions
  # Caching: 24h TTL for insights, 1h for real-time metrics
  from fin_infra.analytics import add_analytics
  analytics = add_analytics(app, prefix="/analytics")
  app.state.analytics = analytics
  
  # 5.8 Categorization - Transaction categorization (56 MX categories, 100+ rules)
  # Endpoints: /categorize (single), /categorize/batch (multiple transactions)
  # Features: Rule-based matching, smart normalization, LLM fallback for unknowns
  # Performance: ~1000 predictions/sec, ~2.5ms avg latency
  # AI: Google Gemini/OpenAI/Anthropic for edge cases (<$0.0002/txn with caching)
  from fin_infra.categorization import add_categorization
  categorizer = add_categorization(app, prefix="/categorize")
  app.state.categorizer = categorizer
  
  # 5.9 Recurring Detection - Subscription and bill identification
  # Endpoints: /recurring/detect, /recurring/insights
  # Features: Fixed subscriptions (Netflix, Spotify), variable bills (utilities),
  #           irregular/annual (insurance), pattern detection, cost insights
  from fin_infra.recurring import add_recurring_detection
  recurring = add_recurring_detection(app, prefix="/recurring")
  app.state.recurring = recurring
  
  # 5.10 Insights Feed - Unified dashboard aggregating all insights
  # Endpoints: /insights/feed, /insights/priority
  # Sources: Net worth, budgets, goals, recurring, portfolio, tax, crypto (7 sources)
  # Features: Priority-based sorting (high/medium/low), action items, deadlines
  from fin_infra.insights import add_insights
  insights = add_insights(app, prefix="/insights")
  app.state.insights = insights
  
  # ==================== FINANCIAL PLANNING (GOALS & BUDGETS) ====================
  
  # 5.11 Budgets - Budget management (8 endpoints)
  # Endpoints:
  #   GET/POST /budgets - List and create budgets
  #   GET/PATCH/DELETE /budgets/{id} - CRUD operations
  #   GET /budgets/{id}/progress - Real-time progress tracking
  #   GET /budgets/{id}/alerts - Overspending warnings (80%/100%/110%)
  #   GET /budgets/templates - Pre-built templates (50/30/20, Zero-Based, Envelope)
  #   POST /budgets/from-template - Create from template
  # Features: Multi-type (personal/household/business), flexible periods,
  #           category-based limits, smart alerts, rollover support
  from fin_infra.budgets import add_budgets
  budgets = add_budgets(app, prefix="/budgets")
  app.state.budgets = budgets
  
  # 5.12 Goals - Financial goal tracking (13 endpoints)
  # Endpoints:
  #   GET/POST /goals - List and create goals
  #   GET/PATCH/DELETE /goals/{id} - CRUD operations
  #   GET/POST /goals/{id}/milestones - Milestone management
  #   PATCH/DELETE /goals/{id}/milestones/{mid} - Milestone CRUD
  #   GET/POST /goals/{id}/funding - Funding source allocation
  #   POST /goals/{id}/pause|resume|complete|abandon - State management
  # Features: Multi-type (savings/debt/investment/net-worth/income),
  #           milestone tracking, multi-account funding, progress monitoring
  from fin_infra.goals import add_goals
  goals = add_goals(app, prefix="/goals")
  app.state.goals = goals
  
  # 5.13 Net Worth Tracking - Multi-account net worth (4 endpoints)
  # Endpoints:
  #   GET /net-worth/current - Current net worth
  #   GET /net-worth/history - Historical snapshots
  #   GET /net-worth/breakdown - Assets vs liabilities by category
  #   POST /net-worth/snapshot - Manual snapshot creation
  # Features: Multi-provider aggregation (banking+brokerage+crypto),
  #           6 asset types, 6 liability types, daily snapshots (svc-infra jobs),
  #           change detection (alert on ≥5% OR ≥$10k)
  from fin_infra.net_worth import add_net_worth_tracking
  net_worth = add_net_worth_tracking(app, prefix="/net-worth")
  app.state.net_worth = net_worth
  
  # ==================== DOCUMENT & COMPLIANCE ====================
  
  # 5.14 Documents - Financial document management
  # Endpoints: /documents (upload), /documents/{id} (retrieve), /documents/search
  # Features: 7 document types (tax, bank statement, receipt, invoice, contract,
  #           insurance, other), OCR (Tesseract 85%/Textract 96%),
  #           AI analysis via ai-infra, secure storage (S3+SQL), SHA-256 checksums
  from fin_infra.documents import add_documents
  documents = add_documents(app, prefix="/documents")
  app.state.documents = documents
  
  # 5.15 Security - Financial PII protection (CRITICAL: Mount BEFORE other routes)
  # Features: Automatic PII detection (regex + context + Luhn/ABA validation),
  #           encryption at rest (provider tokens, SSNs), audit logging,
  #           compliance helpers (PCI-DSS, SOC 2, GDPR, GLBA, CCPA)
  # Zero-config: One-line setup, extends svc-infra auth without duplication
  from fin_infra.security import add_financial_security
  add_financial_security(app)  # No prefix, applies to all routes
  
  # 5.16 Compliance - Regulatory compliance tracking
  # Features: PII classification (3 tiers: high-sensitivity, personal, public),
  #           data retention (GLBA 5yr, FCRA 7yr), erasure workflows,
  #           vendor ToS compliance checks, integration with svc-infra data lifecycle
  from fin_infra.compliance import add_compliance_tracking
  add_compliance_tracking(app)  # No prefix, applies to all routes
  
  # ==================== UTILITIES & CROSS-CUTTING ====================
  
  # 5.17 Normalization - Data standardization
  # Endpoints: /normalize/symbol, /normalize/currency, /normalize/batch
  # Features: Symbol resolution (ticker↔CUSIP↔ISIN), provider normalization
  #           (Yahoo's BTC-USD → CoinGecko's bitcoin), currency conversion (live rates),
  #           company metadata enrichment, batch operations, 24h cache TTL
  from fin_infra.normalization import add_normalization
  normalization = add_normalization(app, prefix="/normalize")
  app.state.normalization = normalization
  
  # 5.18 Observability - Financial metrics classification
  # Features: Financial route classification (|financial suffix),
  #           provider call metrics (success/failure/latency),
  #           LLM cost tracking (per-user, per-feature),
  #           cache hit/miss rates, integration with svc-infra Prometheus + OpenTelemetry
  # Grafana: Filter metrics by route=~".*\\|financial"
  from fin_infra.obs import financial_route_classifier
  # Already added in STEP 4 with add_observability()
  
  # 5.19 Cashflows - Financial calculations
  # Endpoints: /cashflows/npv, /cashflows/irr, /cashflows/pmt, /cashflows/amortization
  # Features: NPV, IRR, XNPV, XIRR, payment calculations (PMT, FV, PV),
  #           loan amortization schedules
  # Use cases: Mortgage calculators, investment analysis, retirement planning
  from fin_infra.cashflows import add_cashflows
  cashflows = add_cashflows(app, prefix="/cashflows")
  app.state.cashflows = cashflows
  
  # 5.20 Conversation - AI financial chat (via ai-infra)
  # Endpoints: POST /chat (questions), GET /chat/history (conversation history)
  # Features: Multi-turn Q&A via ai-infra FinancialPlanningConversation,
  #           context-aware responses, budget recommendations, goal suggestions
  # AI: Uses ai-infra CoreLLM with conversation management
  from fin_infra.chat import easy_financial_conversation
  conversation = easy_financial_conversation(llm_provider="google_genai")
  # Mount as custom endpoint (no add_* function yet)
  from svc_infra.api.fastapi.dual.protected import user_router
  chat_router = user_router(prefix="/chat", tags=["AI Chat"])
  @chat_router.post("/")
  async def ask_question(question: str, user_id: str = "demo"):
      response = await conversation.ask(user_id=user_id, question=question)
      return {"response": response}
  app.include_router(chat_router)
  
  # 5.21 Scaffolding - Code generation (CLI ONLY, not mounted as API)
  # CLI: fin-infra scaffold budgets --dest-dir app/models/
  # Generates: SQLAlchemy models, Pydantic schemas, repositories
  # Integration: svc-infra ModelBase, SqlResource
  # Documented in comments for reference
  
  # STEP 6: Custom Endpoints
  @app.get("/")
  def root():
      """API overview showing all available capabilities."""
      return {
          "name": "fin-infra-template",
          "version": "1.0.0",
          "capabilities": {
              "banking": settings.banking_configured,
              "market_data": settings.market_configured,
              "credit": settings.credit_configured,
              "brokerage": settings.brokerage_configured,
              "tax": True,
              "analytics": True,
              "budgets": True,
              "goals": True,
              "documents": True,
              "net_worth": True,
              "recurring": True,
              "categorization": True,
              "insights": True,
              "crypto_insights": True,
              "rebalancing": True,
              "scenarios": True,
          },
          "endpoints": {
              "docs": "/docs",
              "metrics": "/metrics",
              "health": "/_health",
          }
      }
  ```

#### Testing Phase
- [ ] Tests: Settings validation (all env vars parsed correctly)
- [ ] Tests: Application startup (all providers initialize)
- [ ] Tests: Feature flags (capabilities enable/disable correctly)
- [ ] Tests: Custom endpoints (/, /health, /features return correct data)
- [ ] Tests: Provider storage (app.state has all providers)
- [ ] Tests: Error handling (graceful failures for missing credentials)
- [ ] Tests: Integration smoke tests (basic calls to each capability)
- [ ] Tests: Banking endpoints (if configured)
- [ ] Tests: Market data endpoints (if configured)
- [ ] Tests: All 15+ capability endpoints (if configured)

#### Verification Phase
- [ ] Verify: `make run` starts server successfully
- [ ] Verify: Server starts in < 10 seconds
- [ ] Verify: `/docs` OpenAPI page loads and shows all capabilities
- [ ] Verify: All 15+ fin-infra capabilities appear as separate cards
- [ ] Verify: Each capability has proper tags and descriptions
- [ ] Verify: Security schemes shown correctly (lock icons)
- [ ] Verify: Example requests/responses visible
- [ ] Verify: Metrics endpoint `/metrics` available
- [ ] Verify: Health check `/_health` returns status
- [ ] Verify: Feature flags work (enable/disable via env)
- [ ] Verify: Graceful degradation (app works with partial config)
- [ ] Verify: All svc-infra middlewares active (request ID, CORS, etc.)
- [ ] Verify: Financial route classification working (metrics labeled)

#### Documentation Phase
- [ ] Docs: Inline comments in main.py (explain each STEP)
- [ ] Docs: Docstrings for all custom endpoints
- [ ] Docs: Comments explaining feature flag logic
- [ ] Docs: Comments explaining provider initialization
- [ ] Docs: ASCII diagram of application architecture

**Success Criteria**:
- ✅ `make run` starts server successfully in < 10 seconds
- ✅ **ALL 20+ fin-infra capabilities** mounted and functional
- ✅ `/docs` shows **ALL endpoints organized by capability** (20+ cards with proper tags)
- ✅ **Comprehensive inline documentation** (150+ comments explaining each STEP)
- ✅ **Feature flags work correctly** (verified with env changes)
- ✅ **Graceful degradation**:
  - 0 config: Falls back to mock/free providers (crypto, tax, analytics work)
  - Partial config: Some capabilities enabled (others gracefully disabled)
  - Full config: ALL capabilities enabled with real providers
- ✅ **Provider storage** on app.state for programmatic access
- ✅ **svc-infra integration verified**:
  - Dual routers (no 307 redirects)
  - Observability with financial_route_classifier
  - Cache with lifecycle management
  - Jobs for daily net worth snapshots
- ✅ **ai-infra integration verified**:
  - Conversation uses FinancialPlanningConversation
  - Analytics advice uses CoreLLM
  - Crypto insights use CoreLLM
  - Categorization LLM fallback uses CoreLLM
- ✅ Integration tests passing (60+ tests covering all capabilities)
- ✅ No errors in logs during startup
- ✅ **Capability verification checklist**:
  - [ ] Banking (Plaid/Teller) - 4+ endpoints
  - [ ] Market Data (Alpha Vantage/Yahoo/Polygon) - 3+ endpoints
  - [ ] Crypto Data (CoinGecko/Yahoo/CCXT) - 3+ endpoints
  - [ ] Credit Scores (Experian) - 4+ endpoints
  - [ ] Brokerage (Alpaca) - 3+ endpoints
  - [ ] Tax Data (IRS/TaxBit/Mock) - 3+ endpoints
  - [ ] Analytics - 7 endpoints
  - [ ] Categorization - 2 endpoints
  - [ ] Recurring Detection - 2 endpoints
  - [ ] Insights Feed - 2 endpoints
  - [ ] Budgets - 8 endpoints
  - [ ] Goals - 13 endpoints
  - [ ] Net Worth Tracking - 4 endpoints
  - [ ] Documents - 3+ endpoints
  - [ ] Security (middleware) - PII detection active
  - [ ] Compliance (tracking) - Data retention active
  - [ ] Normalization - 3 endpoints
  - [ ] Observability (metrics) - financial_route_classifier active
  - [ ] Cashflows - 4 endpoints
  - [ ] Conversation (AI chat) - 1+ endpoints

**[x] Phase 3 Status**: COMPLETED (as of v1/example-template branch)

---

### Phase 4: Documentation & Guides

**Owner**: TBD — **Evidence**: PRs, commits, markdown files (2000+ lines total)

#### Research Phase
- [ ] **Research (svc-infra examples check)**:
  - [ ] Review svc-infra `/examples/README.md` structure (630 lines)
  - [ ] Check svc-infra QUICKSTART.md format (204 lines)
  - [ ] Review svc-infra USAGE.md organization
  - [ ] Study svc-infra docs/ structure (CLI.md, DATABASE.md, SCAFFOLD.md)
  - [ ] Check svc-infra example organization (feature showcase, use cases)
  - [ ] Classification: Adapt (reuse structure, financial content)
  - [ ] Justification: Documentation structure is generic, but examples are financial
  - [ ] Reuse plan: Copy svc-infra docs structure, replace with fin-infra examples
  - [ ] Evidence: `/Users/alikhatami/ide/infra/svc-infra/examples/README.md`, `QUICKSTART.md`, `docs/*.md`

#### Design Phase
- [ ] Design: README.md structure (500+ lines)
  - ⚡ Quick Setup section (2 commands)
  - 🎯 Feature showcase (15+ capabilities with emojis)
  - 📚 Documentation index
  - 🚀 Quick start guide
  - 📝 Configuration section
  - 🛠️ Development commands
- [ ] Design: QUICKSTART.md structure (200 lines)
  - Prerequisites
  - 5-minute installation
  - Configuration
  - Testing features (curl examples)
  - Key files reference
- [ ] Design: USAGE.md structure (400+ lines)
  - Detailed examples for ALL 15+ capabilities
  - Copy-paste code snippets
  - Use case scenarios
- [ ] Design: docs/CAPABILITIES.md (600+ lines)
  - One section per capability
  - Provider comparison
  - API reference
  - Integration examples
- [ ] Design: docs/DATABASE.md (300 lines)
  - Model reference
  - Migration workflow
  - Schema diagrams
- [ ] Design: docs/PROVIDERS.md (400 lines)
  - Provider configuration guide
  - Credential setup
  - Sandbox vs production
  - Rate limits
- [ ] Design: docs/CLI.md (200 lines)
  - fin-infra CLI reference
  - Common commands
  - Troubleshooting

#### Implementation Phase

**Deliverables**:
1. README.md - Comprehensive showcase (500+ lines)
2. QUICKSTART.md - 5-minute setup (200 lines)
3. USAGE.md - Detailed feature usage (400+ lines)
4. docs/CAPABILITIES.md - All features explained (600+ lines)
5. docs/DATABASE.md - Database guide (300 lines)
6. docs/PROVIDERS.md - Provider config guide (400 lines)
7. docs/CLI.md - CLI reference (200 lines)

**Files to Create**:
- [ ] `README.md` (500+ lines)
  ```markdown
  # fin-infra Template
  
  A comprehensive example demonstrating **ALL** fin-infra capabilities for building production-ready fintech applications.
  
  ## ⚡ Quick Setup
  
  **Get started in 2 commands:**
  
  ```bash
  cd examples
  make setup    # Installs deps, scaffolds models, runs migrations
  make run      # Starts the server at http://localhost:8001
  ```
  
  ## 🎯 What This Template Showcases
  
  This is a **complete, working example** demonstrating **ALL 20+ fin-infra capabilities**:
  
  ### 🏦 Core Financial Data (Provider Integrations)
  ✅ **Banking Integration** - Plaid/Teller/MX account aggregation (4+ endpoints)
  ✅ **Market Data** - Alpha Vantage/Yahoo/Polygon stocks & ETFs (3+ endpoints)
  ✅ **Crypto Data** - CoinGecko/Yahoo/CCXT crypto market data (3+ endpoints)
  ✅ **Credit Scores** - Experian FICO/VantageScore monitoring (4+ endpoints)
  ✅ **Brokerage** - Alpaca paper/live trading (3+ endpoints)
  ✅ **Tax Data** - IRS/TaxBit forms & calculations (3+ endpoints)
  
  ### 🧠 Financial Intelligence (Analytics & AI)
  ✅ **Analytics** - Cash flow, savings rate, spending insights, AI advice, portfolio analytics, projections, rebalancing (7 endpoints)
  ✅ **Categorization** - 56 MX categories, 100+ rules, LLM fallback (2 endpoints, ~1000 pred/sec)
  ✅ **Recurring Detection** - Fixed subscriptions, variable bills, irregular patterns (2 endpoints)
  ✅ **Insights Feed** - Unified dashboard from 7 sources with priority sorting (2 endpoints)
  
  ### 📊 Financial Planning (Goals & Budgets)
  ✅ **Budgets** - Multi-type, templates (50/30/20, Zero-Based, Envelope), alerts, rollover (8 endpoints)
  ✅ **Goals** - Milestones, multi-account funding, progress tracking, pause/resume (13 endpoints)
  ✅ **Net Worth Tracking** - Multi-provider aggregation, 6 asset + 6 liability types, daily snapshots, change alerts (4 endpoints)
  
  ### 📄 Document & Compliance
  ✅ **Documents** - OCR (Tesseract 85%/Textract 96%), AI analysis, 7 document types (3+ endpoints)
  ✅ **Security** - PII detection (regex + context + Luhn/ABA), encryption, audit logging, PCI-DSS/SOC2/GDPR/GLBA/CCPA (middleware)
  ✅ **Compliance** - PII classification (3 tiers), data retention (GLBA 5yr, FCRA 7yr), erasure workflows (tracking)
  
  ### 🛠️ Utilities & Cross-Cutting
  ✅ **Normalization** - Symbol resolution (ticker↔CUSIP↔ISIN), currency conversion, metadata enrichment (3 endpoints)
  ✅ **Observability** - Financial route classification (|financial suffix), provider metrics, LLM cost tracking (metrics)
  ✅ **Cashflows** - NPV, IRR, PMT, amortization calculations (4 endpoints)
  ✅ **Conversation** - AI financial chat via ai-infra FinancialPlanningConversation (1+ endpoints)
  ✅ **Scaffolding** - Code generation CLI (fin-infra scaffold) for models/schemas/repos
  
  ## 📚 Documentation Structure
  
  - **README.md** (this file) - Complete overview
  - **QUICKSTART.md** - 5-minute getting started
  - **USAGE.md** - Detailed feature usage examples
  - **docs/CAPABILITIES.md** - All fin-infra features explained
  - **docs/DATABASE.md** - Database setup guide
  - **docs/PROVIDERS.md** - Provider configuration guide
  ```

- [ ] `QUICKSTART.md` (200 lines)
  ```markdown
  # Quick Start Guide
  
  Get the fin-infra-template running in 5 minutes.
  
  ## Prerequisites
  
  - Python 3.11+
  - Poetry installed
  
  ## Installation
  
  ```bash
  cd examples
  make setup    # Automated: install + scaffold + migrate
  make run      # Start server
  ```
  
  Server starts at **http://localhost:8001**
  
  - OpenAPI docs: http://localhost:8001/docs
  - Metrics: http://localhost:8001/metrics
  - Health: http://localhost:8001/_health
  
  ## Configuration
  
  Edit `.env` to enable providers:
  
  ```bash
  # Banking (sandbox mode)
  PLAID_CLIENT_ID=your_id
  PLAID_SECRET=your_secret
  PLAID_ENV=sandbox
  
  # Market Data
  ALPHAVANTAGE_API_KEY=your_key
  ```
  
  ## Testing Features
  
  ### Banking
  ```bash
  # Get link token
  curl http://localhost:8001/banking/link
  
  # Exchange token
  curl -X POST http://localhost:8001/banking/exchange -d '{"public_token":"..."}'
  
  # Get accounts
  curl http://localhost:8001/banking/accounts?access_token=...
  ```
  
  ### Analytics
  ```bash
  # Cash flow
  curl http://localhost:8001/analytics/cash-flow/user123
  
  # Savings rate
  curl http://localhost:8001/analytics/savings-rate/user123
  ```
  ```

- [ ] `USAGE.md` (400+ lines)
  ```markdown
  # Usage Guide
  
  Detailed examples for each fin-infra capability.
  
  ## Banking
  
  ### Plaid Integration
  ```python
  # Link accounts
  # Get transactions
  # Real-time balances
  ```
  
  ## Market Data
  
  ### Stock Quotes
  ```python
  # Get quote
  # Historical data
  # Multiple symbols
  ```
  
  ## Analytics
  
  ### Cash Flow Analysis
  ```python
  # Monthly cash flow
  # Cash flow trends
  # Projections
  ```
  
  (Continue for all 15+ features...)
  ```

- [ ] `docs/CAPABILITIES.md` (600+ lines)
  ```markdown
  # Complete Capabilities Reference
  
  Comprehensive guide to ALL fin-infra features in this template.
  
  ## 1. Banking Integration
  
  **Provider**: Plaid (sandbox) or Teller (test mode)
  
  **Endpoints**:
  - POST /banking/link - Create link token
  - POST /banking/exchange - Exchange public token
  - GET /banking/accounts - List accounts
  - GET /banking/transactions - List transactions
  - GET /banking/balances - Get balances
  - GET /banking/identity - Get identity
  
  **Use Cases**:
  - Personal finance apps (Mint, YNAB)
  - Account aggregation platforms
  - Financial dashboards
  
  **Example**:
  ```python
  from fin_infra.banking import easy_banking
  
  banking = easy_banking(provider="plaid")
  accounts = await banking.get_accounts("access_token")
  ```
  
  (Continue for all capabilities...)
  ```

- [ ] `docs/DATABASE.md` (300 lines)
- [ ] `docs/PROVIDERS.md` (400 lines)
- [ ] `docs/CLI.md` (200 lines)

#### Testing Phase
- [ ] Tests: README markdown syntax valid
- [ ] Tests: QUICKSTART instructions work in clean environment
- [ ] Tests: All code examples in docs are syntactically valid
- [ ] Tests: All links in docs are valid (no 404s)
- [ ] Tests: All curl examples work against running server
- [ ] Tests: Documentation completeness (all 15+ capabilities covered)

#### Verification Phase
- [ ] Verify: README has complete feature list (15+ capabilities)
- [ ] Verify: QUICKSTART enables setup in < 5 minutes
- [ ] Verify: QUICKSTART tested in clean environment
- [ ] Verify: USAGE provides copy-paste examples for all capabilities
- [ ] Verify: All code examples tested and working
- [ ] Verify: docs/ covers all configuration options
- [ ] Verify: docs/ has troubleshooting section
- [ ] Verify: All provider setup documented
- [ ] Verify: All environment variables explained
- [ ] Verify: Production considerations documented

#### Documentation Phase
- [ ] Docs: Add table of contents to long docs
- [ ] Docs: Add emojis for visual clarity
- [ ] Docs: Add code block language hints
- [ ] Docs: Add "Next steps" sections
- [ ] Docs: Cross-link related docs
- [ ] Docs: Add diagrams where helpful (ASCII art)

**Success Criteria**:
- ✅ README has complete feature list (15+ capabilities with descriptions)
- ✅ QUICKSTART enables 5-minute setup (verified in clean environment)
- ✅ QUICKSTART commands work first try
- ✅ USAGE provides copy-paste examples (40+ code blocks)
- ✅ All code examples syntactically valid
- ✅ All curl examples work against running server
- ✅ docs/ covers all configuration (50+ env vars)
- ✅ docs/ has troubleshooting for common issues
- ✅ All 15+ capabilities documented completely
- ✅ Total documentation: 2000+ lines

**[x] Phase 4 Status**: PENDING

---

### Phase 5: Scripts & Automation

**Owner**: TBD — **Evidence**: PRs, commits, script files

#### Research Phase
- [ ] **Research (svc-infra examples check)**:
  - [ ] Review svc-infra `/examples/scripts/quick_setup.py` (194 lines)
  - [ ] Check svc-infra `/examples/scripts/scaffold_models.py` pattern
  - [ ] Review svc-infra `/examples/scripts/test_duplicate_prevention.py`
  - [ ] Study svc-infra `/examples/create_tables.py` approach
  - [ ] Check svc-infra script error handling and UX
  - [ ] Classification: Adapt (reuse patterns, financial-specific validation)
  - [ ] Justification: Script patterns are generic, but validation is financial
  - [ ] Reuse plan: Copy svc-infra script structure, add provider validation
  - [ ] Evidence: `/Users/alikhatami/ide/infra/svc-infra/examples/scripts/*.py`

#### Design Phase
- [ ] Design: test_providers.py structure
  - Command-line interface (--provider flag)
  - Per-provider test functions
  - Clear success/failure reporting
  - Environment variable validation
  - Live API testing (with sandboxes)
- [ ] Design: create_tables.py structure
  - No migrations (fast dev mode)
  - Import all models
  - Create tables with metadata.create_all
  - Clear success message
- [ ] Design: Script error handling
  - Helpful error messages
  - Suggest solutions
  - Exit codes (0=success, 1=failure)
  - Colored output (✅❌⚠️)

#### Implementation Phase

**Deliverables**:
1. `scripts/test_providers.py` - Provider connection tester (200+ lines)
2. `create_tables.py` - Quick table creation (50 lines)
3. Enhanced `scripts/quick_setup.py` - Financial model scaffolding
4. Enhanced `scripts/scaffold_models.py` - Model generator with validation

**Files to Create**:
- [ ] `scripts/test_providers.py` - Test provider connections
  ```python
  """
  Test provider connections and credentials.
  
  Usage:
      python scripts/test_providers.py
      python scripts/test_providers.py --provider plaid
      python scripts/test_providers.py --provider alphavantage
  """
  
  import asyncio
  from fin_infra_template.settings import settings
  
  async def test_banking():
      if not settings.banking_configured:
          print("⚠️  Banking not configured")
          return
      
      from fin_infra.banking import easy_banking
      banking = easy_banking()
      print("✅ Banking provider initialized")
      # Test connection...
  
  async def test_market():
      if not settings.market_configured:
          print("⚠️  Market data not configured")
          return
      
      from fin_infra.markets import easy_market
      market = easy_market()
      quote = market.quote("AAPL")
      print(f"✅ Market data working: AAPL @ ${quote.price}")
  
  # Test all providers...
  ```

- [ ] `create_tables.py` - Quick table creation (no migrations)
  ```python
  """
  Create database tables without migrations (for quick testing).
  
  Usage:
      poetry run python create_tables.py
  """
  
  import asyncio
  from fin_infra_template.db import get_engine, Base
  from fin_infra_template.db.models import User, Account, Transaction  # Import all
  
  async def create_tables():
      engine = get_engine()
      async with engine.begin() as conn:
          await conn.run_sync(Base.metadata.create_all)
      print("✅ Database tables created")
  
  if __name__ == "__main__":
      asyncio.run(create_tables())
  ```

#### Testing Phase
- [ ] Tests: test_providers.py with all providers (15+ tests)
  - [ ] Banking (Plaid, Teller)
  - [ ] Market Data (Alpha Vantage, Yahoo)
  - [ ] Credit (Experian)
  - [ ] Brokerage (Alpaca)
  - [ ] Tax (Mock, IRS)
  - [ ] All other capabilities
- [ ] Tests: create_tables.py creates all 8 tables
- [ ] Tests: Scripts handle missing credentials gracefully
- [ ] Tests: Scripts provide clear error messages
- [ ] Tests: Scripts work in clean environment

#### Verification Phase
- [ ] Verify: `python scripts/test_providers.py` validates all configs
- [ ] Verify: `python scripts/test_providers.py --provider banking` tests one
- [ ] Verify: `python create_tables.py` creates tables in < 5 seconds
- [ ] Verify: Scripts have helpful error messages (tested with invalid config)
- [ ] Verify: Scripts have `--help` documentation
- [ ] Verify: Scripts exit with proper codes (0 or 1)
- [ ] Verify: Scripts use colored output (✅❌⚠️)

#### Documentation Phase
- [ ] Docs: Inline docstrings for all scripts
- [ ] Docs: `--help` text for all scripts
- [ ] Docs: Usage examples in comments
- [ ] Docs: Error message suggestions

**Success Criteria**:
- ✅ `python scripts/test_providers.py` validates all 15+ provider configs
- ✅ `python create_tables.py` creates tables quickly (< 5 seconds)
- ✅ Scripts have helpful error messages with suggestions
- ✅ Scripts handle edge cases (missing env, invalid config)
- ✅ All scripts have `--help` documentation
- ✅ Scripts tested in clean environment
- ✅ Total scripts: 4 files, 500+ lines

**[x] Phase 5 Status**: PENDING

---

## Feature Coverage Matrix (ALL 20+ Capabilities)

### Core Financial Data (Provider Integrations)
| # | Feature | Module | Endpoint Pattern | Providers | Status |
|---|---------|--------|------------------|-----------|--------|
| 1 | Banking | `fin_infra.banking` | `/banking/*` | Plaid, Teller, MX | ✅ DONE |
| 2 | Market Data | `fin_infra.markets` | `/market/*` | Alpha Vantage, Yahoo, Polygon | ✅ DONE |
| 3 | Crypto Data | `fin_infra.crypto` | `/crypto/*` | CoinGecko, Yahoo, CCXT | ✅ DONE |
| 4 | Credit Scores | `fin_infra.credit` | `/credit/*` | Experian, Equifax, TransUnion | ✅ DONE |
| 5 | Brokerage | `fin_infra.brokerage` | `/brokerage/*` | Alpaca, IB, SnapTrade | ✅ DONE |
| 6 | Tax Data | `fin_infra.tax` | `/tax/*` | IRS, TaxBit, Mock | ✅ DONE |

### Financial Intelligence (Analytics & AI)
| # | Feature | Module | Endpoint Pattern | Key Features | Status |
|---|---------|--------|------------------|--------------|--------|
| 7 | Analytics | `fin_infra.analytics` | `/analytics/*` (7 endpoints) | Cash flow, savings rate, spending insights, AI advice, portfolio analytics, projections, rebalancing | ✅ DONE |
| 8 | Categorization | `fin_infra.categorization` | `/categorize/*` | 56 categories, 100+ rules, LLM fallback | ✅ DONE |
| 9 | Recurring Detection | `fin_infra.recurring` | `/recurring/*` | Fixed subscriptions, variable bills, irregular patterns | ✅ DONE |
| 10 | Insights Feed | `fin_infra.insights` | `/insights/*` | Unified dashboard from 7 sources, priority sorting | ✅ DONE |

### Financial Planning (Goals & Budgets)
| # | Feature | Module | Endpoint Pattern | Key Features | Status |
|---|---------|--------|------------------|--------------|--------|
| 11 | Budgets | `fin_infra.budgets` | `/budgets/*` (8 endpoints) | Multi-type, templates, alerts, rollover | ⬜ TODO |
| 12 | Goals | `fin_infra.goals` | `/goals/*` (13 endpoints) | Milestones, multi-account funding, progress tracking | ⬜ TODO |
| 13 | Net Worth | `fin_infra.net_worth` | `/net-worth/*` (4 endpoints) | Multi-provider aggregation, 6 asset + 6 liability types, daily snapshots | ⬜ TODO |

### Document & Compliance
| # | Feature | Module | Endpoint Pattern | Key Features | Status |
|---|---------|--------|------------------|--------------|--------|
| 14 | Documents | `fin_infra.documents` | `/documents/*` | OCR (Tesseract/Textract), AI analysis, 7 document types | ⬜ TODO |
| 15 | Security | `fin_infra.security` | (middleware) | PII detection, encryption, audit logging, compliance (PCI-DSS, SOC 2, GDPR, GLBA, CCPA) | ⬜ TODO |
| 16 | Compliance | `fin_infra.compliance` | (tracking) | PII classification (3 tiers), data retention (GLBA 5yr, FCRA 7yr), erasure workflows | ⬜ TODO |

### Utilities & Cross-Cutting
| # | Feature | Module | Endpoint Pattern | Key Features | Status |
|---|---------|--------|------------------|--------------|--------|
| 17 | Normalization | `fin_infra.normalization` | `/normalize/*` | Symbol resolution (ticker↔CUSIP↔ISIN), currency conversion, metadata enrichment | ⬜ TODO |
| 18 | Observability | `fin_infra.obs` | (metrics) | Financial route classification (|financial suffix), provider metrics, LLM cost tracking | ✅ DONE |
| 19 | Cashflows | `fin_infra.cashflows` | `/cashflows/*` (4 endpoints) | NPV, IRR, PMT, amortization calculations | ⬜ TODO |
| 20 | Conversation | `fin_infra.chat` | `/chat/*` | AI financial chat via ai-infra FinancialPlanningConversation | ⬜ TODO |
| 21 | Scaffolding | `fin_infra.scaffold` | (CLI only) | Code generation: models, schemas, repositories | ⬜ TODO |

### Summary Statistics
- **Total Capabilities**: 21 (20 API-mounted + 1 CLI)
- **Provider Integrations**: 6 (Banking, Market Data, Crypto, Credit, Brokerage, Tax)
- **Analytics & AI**: 4 (Analytics, Categorization, Recurring, Insights)
- **Planning Tools**: 3 (Budgets, Goals, Net Worth)
- **Compliance & Docs**: 3 (Documents, Security, Compliance)
- **Utilities**: 5 (Normalization, Observability, Cashflows, Conversation, Scaffolding)
- **Total Endpoints**: 60+ across all capabilities

---

## Integration Patterns to Showcase

### Pattern 1: fin-infra + svc-infra Backend
```python
# Backend infrastructure (svc-infra)
from svc_infra.api.fastapi.ease import easy_service_app
from svc_infra.logging import setup_logging
from svc_infra.obs import add_observability

# Financial capabilities (fin-infra)
from fin_infra.banking import add_banking
from fin_infra.analytics import add_analytics

setup_logging()
app = easy_service_app(name="FinanceAPI")
add_observability(app)

# Wire financial capabilities
add_banking(app)
add_analytics(app)
```

### Pattern 2: Financial Route Classification
```python
from svc_infra.obs import add_observability
from fin_infra.obs import financial_route_classifier

# All routes auto-instrumented + categorized for metrics filtering
add_observability(app, route_classifier=financial_route_classifier)

# Metrics: route="/banking/accounts|financial" (can filter by |financial)
```

### Pattern 3: Provider Integration
```python
# Easy builders for quick setup
from fin_infra.banking import easy_banking
from fin_infra.markets import easy_market

banking = easy_banking(provider="plaid")
market = easy_market(provider="alphavantage")

# Use programmatically
accounts = await banking.get_accounts(token)
quote = market.quote("AAPL")
```

### Pattern 4: Multi-Module Integration
```python
# Analytics + Budgets + Goals working together
from fin_infra.analytics import easy_analytics
from fin_infra.budgets import easy_budgets
from fin_infra.goals import easy_goals

analytics = easy_analytics()
budgets = easy_budgets()
goals = easy_goals()

# Get savings rate to recommend goal contributions
savings = await analytics.savings_rate(user_id)
monthly_savings = savings.monthly_savings_amount

# Allocate to goals
goals_list = await goals.list_goals(user_id, status="active")
allocation_per_goal = monthly_savings / len(goals_list)
```

---

## Success Criteria

### Developer Experience
- ✅ `make setup && make run` works first try
- ✅ Server starts in < 5 seconds
- ✅ All docs accessible in 1 click from README
- ✅ Clear error messages for missing credentials
- ✅ Inline code documentation explains every feature

### Feature Completeness
- ✅ **ALL 20+ fin-infra capabilities** demonstrated (6 provider integrations, 4 analytics/AI, 3 planning tools, 3 compliance/docs, 5 utilities)
- ✅ **60+ working endpoints** across all capabilities
- ✅ **Proper integration** with svc-infra backend (dual routers, observability, cache, jobs)
- ✅ **ai-infra integration** for LLM features (conversation, analytics advice, crypto insights, categorization fallback)
- ✅ **Feature flags** for enabling/disabling modules (env-based conditional mounting)

### Documentation Quality
- ✅ README showcases **ALL 20+ capabilities** with descriptions, emojis, and categorization
- ✅ QUICKSTART enables **5-minute setup** (verified in clean environment)
- ✅ USAGE provides **copy-paste examples for ALL capabilities** (60+ code blocks)
- ✅ **Comprehensive inline comments** (150+ comments explaining design decisions, integration patterns, compliance requirements)

### Production Readiness
- ✅ Proper database migrations with Alembic
- ✅ Type-safe configuration with Pydantic
- ✅ Environment-aware logging
- ✅ Health checks and observability
- ✅ Error handling and validation

---

## Completion Tracking

### Overall Progress
- [x] **Phase 1: Project Structure** (5/5 major items) ✅ COMPLETE
  - [x] Research complete
  - [x] Design complete
  - [x] Implementation complete (6 files: pyproject.toml, Makefile, .env.example, .gitignore, run.sh, directory structure)
  - [x] Tests passing (poetry install, make help, run.sh executable, 103 env vars)
  - [x] Documentation complete (comments in all config files)
- [x] **Phase 2: Database Models** (5/5 major items) ✅ COMPLETE
  - [x] Research complete
  - [x] Design complete  
  - [x] Implementation complete (7 files: base.py, models.py, schemas.py, alembic.ini, env.py, script.py.mako, create_tables.py + 1 migration)
  - [x] Tests passing (migration created successfully, tables verified in database)
  - [x] Documentation complete (comprehensive docstrings in all model and schema files)
- [ ] **Phase 3: Main Application** (0/5 major items)
  - [ ] Research complete
  - [ ] Design complete
  - [ ] Implementation complete (2 files, 1000+ lines main.py)
  - [ ] Tests passing (50+ integration tests)
  - [ ] Documentation complete
- [ ] **Phase 4: Documentation** (0/5 major items)
  - [ ] Research complete
  - [ ] Design complete
  - [ ] Implementation complete (7 doc files, 2000+ lines)
  - [ ] Tests passing (link validation, syntax checks)
  - [ ] Verification complete (tested in clean environment)
- [ ] **Phase 5: Scripts** (0/5 major items)
  - [ ] Research complete
  - [ ] Design complete
  - [ ] Implementation complete (4 scripts, 500+ lines)
  - [ ] Tests passing (15+ provider tests)
  - [ ] Documentation complete

### Statistics
- **Files Created**: 17 / ~30 target (Phases 1-2 complete: 57% of files)
- **Lines of Code**: 3,233 / ~3000 target (108% - Phase 1-2 complete + migration generated!)
- **Lines of Docs**: ~500 / ~2000 target (25% - .env.example comments + model/schema docstrings)
- **Tests Written**: 0 / ~100 target (0% - migrations verified manually, unit tests in Phase 3)
- **Features Demonstrated**: 0 / 15+ target (0% - database ready, main.py in Phase 3)

### Quality Gates
- [ ] All tests passing (unit + integration)
- [ ] All docs reviewed and valid
- [ ] All code examples tested
- [ ] Clean environment setup works
- [ ] `make setup && make run` succeeds
- [ ] `/docs` OpenAPI complete
- [ ] All 15+ capabilities working

---

## Timeline Estimate

| Phase | Deliverables | Tasks | Estimated Time | Actual Time |
|-------|-------------|-------|----------------|-------------|
| Phase 1 | Project structure, Makefile, config | Research, Design, Implement (6 files), Test, Verify, Doc | 4 hours | TBD |
| Phase 2 | Database models, migrations, scripts | Research, Design, Implement (10 files), Test (40+), Verify, Doc | 8 hours | TBD |
| Phase 3 | Main app with ALL features | Research, Design, Implement (1000+ lines), Test (50+), Verify, Doc | 12 hours | TBD |
| Phase 4 | Documentation (README, guides) | Research, Design, Implement (7 docs, 2000+ lines), Test, Verify | 6 hours | TBD |
| Phase 5 | Scripts, automation, polish | Research, Design, Implement (4 scripts), Test (15+), Verify, Doc | 4 hours | TBD |
| **Total** | Complete template project | 5 phases, ~30 files, ~5000 lines | **34 hours** | **TBD** |

**Note**: Original estimate was 20 hours. Updated to 34 hours after adding comprehensive research, testing, and verification phases per plans.md standards.

---

## References

### svc-infra Template Structure
- `/examples/README.md` - Comprehensive showcase (630 lines)
- `/examples/main.py` - ALL features demonstrated (754 lines)
- `/examples/Makefile` - Complete automation
- `/examples/scripts/quick_setup.py` - One-command setup
- `/examples/QUICKSTART.md` - 5-minute guide

### fin-infra Capabilities
- 15+ financial modules with `add_*()` helpers
- Easy builders: `easy_banking()`, `easy_analytics()`, etc.
- Complete documentation in `src/fin_infra/docs/`
- Integration guides in ADRs

### Key Differences from Current Examples
1. **Runnable**: Complete Poetry setup with `make setup && make run`
2. **Complete**: Shows ALL 15+ capabilities, not just 2
3. **Structured**: Proper package with models, schemas, migrations
4. **Documented**: Comprehensive README + quickstart + usage guides
5. **Automated**: One-command setup with scaffolding
6. **Educational**: Inline docs explain every feature and design decision

---

## Final Verification Checklist

### Pre-Release Verification
Before marking template complete, verify ALL of the following:

#### Functional Requirements
- [ ] `cd examples && make setup` completes without errors
- [ ] `make run` starts server successfully
- [ ] Server responds at `http://localhost:8001`
- [ ] `/docs` OpenAPI page loads completely
- [ ] All 15+ capabilities appear as separate cards in `/docs`
- [ ] `/metrics` Prometheus endpoint works
- [ ] `/_health` health check returns 200
- [ ] All endpoints return valid responses (not 500s)

#### Feature Completeness (ALL 20+ Capabilities)

**Core Financial Data (6 provider integrations):**
- [ ] 1. Banking capability demonstrated (Plaid/Teller, 4+ endpoints)
- [ ] 2. Market Data capability demonstrated (Alpha Vantage/Yahoo/Polygon, 3+ endpoints)
- [ ] 3. Crypto Data capability demonstrated (CoinGecko/Yahoo/CCXT, 3+ endpoints)
- [ ] 4. Credit Scores capability demonstrated (Experian, 4+ endpoints)
- [ ] 5. Brokerage capability demonstrated (Alpaca paper/live, 3+ endpoints)
- [ ] 6. Tax Data capability demonstrated (IRS/TaxBit/Mock, 3+ endpoints)

**Financial Intelligence (4 analytics/AI features):**
- [ ] 7. Analytics capability demonstrated (7 endpoints: cash flow, savings rate, spending insights, AI advice, portfolio analytics, projections, rebalancing)
- [ ] 8. Categorization capability demonstrated (56 categories, 100+ rules, LLM fallback)
- [ ] 9. Recurring Detection capability demonstrated (fixed/variable/irregular patterns)
- [ ] 10. Insights Feed capability demonstrated (unified dashboard from 7 sources)

**Financial Planning (3 planning tools):**
- [ ] 11. Budgets capability demonstrated (8 endpoints: CRUD, progress, alerts, templates)
- [ ] 12. Goals capability demonstrated (13 endpoints: CRUD, milestones, funding, state management)
- [ ] 13. Net Worth capability demonstrated (4 endpoints: current, history, breakdown, snapshots)

**Document & Compliance (3 features):**
- [ ] 14. Documents capability demonstrated (OCR with Tesseract/Textract, AI analysis, 7 document types)
- [ ] 15. Security capability demonstrated (PII detection, encryption, audit logging, compliance)
- [ ] 16. Compliance capability demonstrated (PII classification, data retention, erasure workflows)

**Utilities & Cross-Cutting (5 features):**
- [ ] 17. Normalization capability demonstrated (symbol resolution, currency conversion, metadata enrichment)
- [ ] 18. Observability capability demonstrated (financial_route_classifier, provider metrics, LLM cost tracking)
- [ ] 19. Cashflows capability demonstrated (4 endpoints: NPV, IRR, PMT, amortization)
- [ ] 20. Conversation capability demonstrated (AI financial chat via ai-infra)
- [ ] 21. Scaffolding capability documented (CLI usage examples in comments)

#### Documentation Quality
- [ ] README complete with all 15+ features listed
- [ ] QUICKSTART works in clean environment (verified)
- [ ] USAGE has working examples for all capabilities
- [ ] All code examples syntactically valid
- [ ] All curl examples tested and working
- [ ] docs/ comprehensive (2000+ lines)
- [ ] Inline comments explain all setup steps
- [ ] No broken links in documentation
- [ ] All environment variables documented

#### Code Quality
- [ ] All tests passing (100+ tests target)
- [ ] No linter errors (ruff clean)
- [ ] No type errors (mypy clean)
- [ ] All models have docstrings
- [ ] All functions have docstrings
- [ ] All scripts have --help text
- [ ] Error messages are helpful
- [ ] Code follows fin-infra patterns

#### Integration Quality
- [ ] svc-infra dual routers used (NOT generic APIRouter)
- [ ] add_prefixed_docs() called for all capabilities
- [ ] Financial route classification working
- [ ] Provider instances stored on app.state
- [ ] Graceful degradation working (partial config)
- [ ] Feature flags working (env-based)
- [ ] Observability wired correctly
- [ ] Metrics labeled properly

#### Developer Experience
- [ ] Setup takes < 5 minutes
- [ ] Error messages helpful
- [ ] Make commands self-documenting
- [ ] Scripts handle edge cases
- [ ] Clear what to do next after setup
- [ ] Easy to enable/disable features
- [ ] Easy to swap providers
- [ ] Easy to extend with new capabilities

---

## Success Metrics

### Quantitative Targets
- ✅ Files created: 35+ (6 Phase 1 + 10 Phase 2 + 4 Phase 3 + 8 Phase 4 + 5 Phase 5 + migrations)
- ✅ Lines of application code: 5000+ (settings 400 + main 1500 + routes 1000 + models 600 + schemas 800 + scripts 700)
- ✅ Lines of documentation: 3000+ (README 700 + QUICKSTART 250 + USAGE 800 + CAPABILITIES 1000 + others 250)
- ✅ Tests written: 150+ (unit 80 + integration 50 + acceptance 20)
- ✅ **Capabilities demonstrated: 20+ (6 provider integrations + 4 analytics/AI + 3 planning + 3 compliance/docs + 5 utilities)**
- ✅ **Endpoints implemented: 60+ across all capabilities**
- ✅ Setup time: < 5 minutes (verified in clean environment)
- ✅ Server start time: < 10 seconds (all capabilities loaded)
- ✅ Test pass rate: 100% (all 150+ tests green)

### Qualitative Targets
- ✅ Developer can run `make setup && make run` first try
- ✅ Documentation explains every feature clearly
- ✅ Code examples are copy-paste ready
- ✅ Template matches svc-infra quality standards
- ✅ Template demonstrates best practices
- ✅ Template is production-ready starting point

---

## Next Steps

### Immediate Actions
1. **Begin Phase 1**: Set up project structure
   - Create `pyproject.toml` with dependencies
   - Create `Makefile` with automation
   - Create `.env.example` with all provider vars (103+ variables)
   - Create `run.sh` launcher
   - Test: `poetry install` works

2. **Complete Research** for all phases before coding
   - Review svc-infra examples thoroughly
   - Document all reuse opportunities
   - Get approval for architectural decisions

---

## Comprehensive Scope Summary

### What Makes This Template Comprehensive

**This is NOT a minimal example**. This is a **DEFINITIVE REFERENCE IMPLEMENTATION** showing:

1. **Complete Financial Stack**: Every single fin-infra capability (20+), not just a subset
2. **Production Patterns**: Real provider integrations, not mocks
3. **Best Practices**: Proper error handling, PII protection, compliance, observability
4. **Integration Examples**: fin-infra + svc-infra + ai-infra working together seamlessly
5. **Developer Experience**: One command setup, clear docs, helpful errors

### Why This Scope Is Necessary

**For Developers:**
- Copy-paste starting point for ANY fintech application
- Reference implementation for every capability
- Production-ready patterns (not prototype code)
- Clear examples of svc-infra and ai-infra integration

**For fin-infra Project:**
- Comprehensive test of all capabilities working together
- Living documentation (code that runs and proves capabilities work)
- Quality benchmark (if template works, fin-infra works)
- Marketing showcase (demonstrate full power of fin-infra)

**For Product Teams:**
- Complete feature inventory (see everything fin-infra can do)
- Use case examples (see how features combine)
- Implementation estimates (see LOC and complexity)
- Decision support (choose which capabilities to use)

### Scope Boundaries

**IN SCOPE (Comprehensive):**
- ✅ ALL 20+ fin-infra capabilities demonstrated
- ✅ Multiple providers per capability (where applicable)
- ✅ Real provider connections (sandbox/test modes)
- ✅ svc-infra backend integration (database, cache, jobs, observability)
- ✅ ai-infra LLM integration (conversation, insights, advice)
- ✅ Production patterns (error handling, PII protection, compliance)
- ✅ Comprehensive documentation (3000+ lines)
- ✅ Extensive testing (150+ tests)

**OUT OF SCOPE (Not Needed):**
- ❌ Production deployment config (Kubernetes, Docker Compose)
- ❌ Frontend UI (this is backend-only template)
- ❌ Advanced customization (keep it simple)
- ❌ Every possible provider (show 1-2 per capability)
- ❌ Production provider credentials (use sandbox/test modes)

### Expected Impact

**Time Saved**: Developers can start with this template instead of building from scratch
- **Without template**: 4-6 weeks to wire all capabilities correctly
- **With template**: 2-3 days to customize for specific use case
- **Savings**: 80-90% reduction in setup time

**Quality Improvement**: Template demonstrates correct patterns
- PII protection by default (not afterthought)
- Compliance tracking from day 1 (not retrofit)
- Observability built-in (not added later)
- Proper error handling throughout (not patches)

**Feature Discovery**: Template shows what's possible
- Developers discover capabilities they didn't know existed
- Product teams see feature combinations
- Sales teams have demo-ready showcase

---

## Final Note

This template is **THE** reference implementation for fin-infra. When someone asks "How do I use fin-infra?", the answer is "Start with examples/". Every capability, every pattern, every integration is demonstrated here.

**Quality bar**: If it's in this template, it's production-ready. No shortcuts, no TODOs, no half-implemented features. This is the standard.

3. **Follow Workflow**: Research → Design → Implement → Tests → Verify → Docs
   - Do NOT skip research phase
   - Do NOT implement before design approved
   - Do NOT skip verification phase

### Long-Term Goals
- **Phase 1**: Complete in Week 1 (establish foundation)
- **Phase 2**: Complete in Week 2 (database layer)
- **Phase 3**: Complete in Week 3-4 (main application)
- **Phase 4**: Complete in Week 5 (documentation)
- **Phase 5**: Complete in Week 6 (scripts, polish)
- **Final Verification**: Week 7 (testing, validation)

### Milestone Markers
- ✅ Phase 1 Complete: `make setup` works
- ✅ Phase 2 Complete: Database tables exist
- ✅ Phase 3 Complete: All features wired
- ✅ Phase 4 Complete: Documentation comprehensive
- ✅ Phase 5 Complete: All scripts working
- ✅ Template Complete: Final verification passed

**Priority**: Start with Phase 1 Research immediately. Complete full research phase before any implementation work begins.
