# fin-infra Template Project Implementation Plan - COMPREHENSIVE EDITION

## Executive Summary

Create a **PRODUCTION-READY** `/examples` template project that demonstrates **EVERY SINGLE** fin-infra capability (20+ features across 15+ modules) with proper svc-infra backend integration.

**Goal**: Developers run `make setup && make run` and have a fully functional fintech API showcasing every fin-infra feature with real implementations, proper error handling, security, and compliance.

**Scope**: This template must demonstrate ALL capabilities listed in fin-infra's main README and documentation. This is the DEFINITIVE reference implementation.

---

## Complete Capabilities Inventory

Based on thorough research of fin-infra codebase, documentation, and API surface:

### Core Financial Data (Providers)
1. **Banking** (`fin_infra.banking`) - 2 providers
   - Plaid (OAuth-based, industry standard)
   - Teller (mTLS certificate-based, free tier)
   - Operations: Link accounts, fetch transactions, get balances, fetch identity
   
2. **Market Data** (`fin_infra.markets`) - 4 providers
   - Alpha Vantage (stocks, primary)
   - Yahoo Finance (stocks, fallback)
   - Polygon (stocks, premium)
   - CoinGecko (crypto, free tier)
   - Operations: Get quotes, historical data, company info, market cap

3. **Credit Scores** (`fin_infra.credit`) - 3 providers
   - Experian (OAuth 2.0, production-ready)
   - Equifax (coming soon)
   - TransUnion (coming soon)
   - Operations: Get score, full report, change alerts, credit factors

4. **Brokerage** (`fin_infra.brokerage`) - 3 providers
   - Alpaca (paper + live trading)
   - Interactive Brokers (research pending)
   - SnapTrade (multi-broker aggregation)
   - Operations: Get portfolio, positions, orders, execute trades

5. **Tax Data** (`fin_infra.tax`) - 3 providers
   - IRS e-File (coming soon)
   - TaxBit (crypto tax calculations)
   - Mock provider (testing)
   - Operations: Get documents, calculate liability, tax-loss harvesting

6. **Crypto Data** (`fin_infra.crypto`) - 3 providers
   - CoinGecko (market data, free tier)
   - Yahoo Finance (crypto quotes)
   - CCXT (exchange integration)
   - Operations: Get quotes, portfolio tracking, AI insights

### Financial Intelligence (Analytics & AI)
7. **Analytics** (`fin_infra.analytics`) - 7 endpoints
   - Cash flow analysis (income vs expenses, category breakdowns)
   - Savings rate calculation (3 methods: gross, net, discretionary)
   - Spending insights (patterns, anomalies, trends)
   - AI-powered advice (LLM-generated recommendations)
   - Portfolio analytics (performance, allocation, benchmarks)
   - Growth projections (Monte Carlo net worth forecasting)
   - Rebalancing (tax-optimized portfolio rebalancing)

8. **Categorization** (`fin_infra.categorization`)
   - 56 categories (MX-style taxonomy)
   - 100+ merchant rules (Starbucks, McDonald's, Uber, Netflix, Amazon)
   - Smart normalization (handles store numbers, special characters)
   - LLM-powered categorization (Google Gemini, OpenAI, Anthropic)
   - Performance: ~1000 predictions/sec, ~2.5ms latency
   - Cost: <$0.0002/transaction with caching

9. **Recurring Detection** (`fin_infra.recurring`)
   - Fixed subscriptions (Netflix, Spotify, gym)
   - Variable bills (utilities, phone with overage)
   - Irregular/annual (insurance premiums, annual subscriptions)
   - Pattern detection (frequency, amount stability)
   - Insights generation (total monthly cost, cancellation opportunities)

10. **Insights Feed** (`fin_infra.insights`)
    - Unified dashboard aggregating insights from:
      - Net worth tracking (changes, milestones, allocation shifts)
      - Budget management (overspending alerts, category warnings)
      - Goal progress (milestone achievements, deadline warnings)
      - Recurring patterns (subscription changes, trend analysis)
      - Portfolio analytics (rebalancing opportunities, risk metrics)
      - Tax optimization (estimated liabilities, deduction opportunities)
      - Crypto holdings (AI-powered analysis, market insights)
    - Priority-based sorting (high/medium/low)
    - Action items with deadlines
    - Source attribution

### Financial Planning (Goals & Budgets)
11. **Budgets** (`fin_infra.budgets`) - 8 endpoints
    - Multi-type budgets (personal, household, business, project, custom)
    - Flexible periods (weekly, biweekly, monthly, quarterly, yearly)
    - Category-based limits (groceries, dining, transportation)
    - Pre-built templates (50/30/20, Zero-Based, Envelope, Pay Yourself First)
    - Progress tracking (real-time spent vs budgeted)
    - Smart alerts (warn at 80%, alert at 100%, notify at 110%)
    - Rollover support (carry unused budget to next period)

12. **Goals** (`fin_infra.goals`) - 13 endpoints
    - Multi-type goals (savings, debt payoff, investment, net worth, income, custom)
    - Milestone tracking (checkpoint amounts with target dates)
    - Funding allocation (link multiple accounts with percentage splits)
    - Progress monitoring (real-time calculations, projected completion)
    - Flexible management (pause, resume, complete, abandon)

13. **Net Worth Tracking** (`fin_infra.net_worth`) - 4 endpoints
    - Multi-provider aggregation (banking + brokerage + crypto)
    - Asset categories (cash, investments, crypto, real estate, vehicles, other)
    - Liability categories (credit cards, mortgages, auto/student/personal loans, LOC)
    - Historical snapshots (daily with configurable retention)
    - Change detection (alert on ≥5% OR ≥$10k change)
    - svc-infra integration (jobs for daily snapshots, DB storage, cache with 1h TTL)

### Document & Compliance
14. **Documents** (`fin_infra.documents`)
    - 7 document types (tax, bank statement, receipt, invoice, contract, insurance, other)
    - OCR extraction (Tesseract 85% confidence, AWS Textract 96%)
    - AI analysis (insights, recommendations, summaries via ai-infra)
    - Secure storage (in-memory for testing, S3+SQL for production)
    - SHA-256 checksums (integrity verification)
    - Year and type filtering

15. **Security** (`fin_infra.security`)
    - Automatic PII detection (regex + context + Luhn/ABA validation)
    - Zero-config setup (`add_financial_security(app)`)
    - Compliance-ready (PCI-DSS, SOC 2, GDPR, GLBA, CCPA)
    - Provider-agnostic (works with all financial providers)
    - Key rotation support (multiple encryption keys, zero-downtime)
    - Extends svc-infra (auth/logging) without duplication

16. **Compliance** (`fin_infra.compliance`)
    - PII classification (3 tiers: high-sensitivity, personal, public)
    - Vendor ToS requirements (documented per provider)
    - Data retention policies (GLBA 5 years, FCRA 7 years)
    - Erasure workflows (right-to-delete implementation)
    - svc-infra integration (audit logging, data lifecycle)

### Utilities & Cross-Cutting
17. **Normalization** (`fin_infra.normalization`)
    - Symbol resolution (ticker ↔ CUSIP ↔ ISIN conversions)
    - Provider normalization (Yahoo `BTC-USD` → CoinGecko `bitcoin` → Alpaca `BTCUSD`)
    - Currency conversion (USD → EUR with live rates via ExchangeRate-API)
    - Metadata enrichment (ticker → company name, sector, exchange)
    - Batch operations (resolve multiple symbols efficiently)

18. **Observability** (`fin_infra.obs`)
    - Financial route classification (`|financial` suffix for metrics)
    - Integration with svc-infra observability (Prometheus, OpenTelemetry)
    - Custom metrics (provider calls, LLM costs, API latencies)
    - Grafana filtering (filter by `route=~".*\\|financial"`)

19. **Scaffolding** (`fin_infra.scaffold`)
    - CLI: `fin-infra scaffold budgets --dest-dir app/models/`
    - Generates: SQLAlchemy models, Pydantic schemas, repositories
    - Patterns: UUID primary keys, timestamps, indexes, soft-delete, multi-tenancy
    - svc-infra integration (ModelBase, SqlResource)

20. **Cashflows** (`fin_infra.cashflows`)
    - NPV (Net Present Value)
    - IRR (Internal Rate of Return)
    - XNPV, XIRR (irregular cashflows)
    - PMT, FV, PV (payment calculations)
    - Loan amortization schedules

---

## Phase 3: Main Application (EXPANDED WITH ALL CAPABILITIES)

### Complete main.py Structure (1500+ lines target)

```python
"""
Complete fintech application demonstrating ALL fin-infra + svc-infra features.

BACKEND INFRASTRUCTURE (svc-infra - REUSE, DON'T DUPLICATE):
✅ Logging (environment-aware with pick() helper)
✅ Database (SQLAlchemy 2.0 + Alembic migrations)
✅ Caching (Redis with lifecycle management)
✅ Observability (Prometheus + OpenTelemetry)
✅ Security (headers, CORS, timeouts, rate limiting)
✅ Rate Limiting (per-IP, per-user)
✅ Idempotency (in-memory or Redis-backed)
✅ Health Checks (liveness, readiness)

FINANCIAL CAPABILITIES (fin-infra - ALL 20+ FEATURES):

1. BANKING (fin_infra.banking)
   - add_banking(app, provider="plaid")
   - Endpoints: /banking/link, /banking/exchange, /banking/accounts, /banking/transactions
   - Providers: Plaid (OAuth), Teller (mTLS)
   - Security: PII filtering on responses

2. MARKET DATA (fin_infra.markets)
   - add_market_data(app, provider="alphavantage")
   - Endpoints: /market/quote/{symbol}, /market/historical/{symbol}, /market/search
   - Providers: Alpha Vantage, Yahoo Finance, Polygon
   - Caching: 60s TTL for quotes

3. CREDIT SCORES (fin_infra.credit)
   - add_credit(app, provider="experian")
   - Endpoints: /credit/score, /credit/report, /credit/factors
   - Providers: Experian (OAuth 2.0)
   - Security: High-sensitivity PII (FCRA regulated)

4. BROKERAGE (fin_infra.brokerage)
   - add_brokerage(app, provider="alpaca")
   - Endpoints: /brokerage/portfolio, /brokerage/positions, /brokerage/orders
   - Providers: Alpaca (paper/live), Interactive Brokers, SnapTrade
   - Security: SEC registered broker-dealer data

5. TAX DATA (fin_infra.tax)
   - add_tax_data(app)
   - Endpoints: /tax/documents, /tax/liability, /tax/tlh (tax-loss harvesting)
   - Providers: IRS e-File, TaxBit, Mock
   - Compliance: IRS record retention (7 years)

6. CRYPTO DATA (fin_infra.crypto)
   - add_crypto_data(app, provider="coingecko")
   - Endpoints: /crypto/quote/{symbol}, /crypto/portfolio, /crypto/insights
   - Providers: CoinGecko, Yahoo Finance, CCXT
   - AI: Portfolio insights via ai-infra CoreLLM

7. ANALYTICS (fin_infra.analytics) - 7 ENDPOINTS
   - add_analytics(app)
   - Endpoints:
     - /analytics/cash-flow - Income vs expenses with category breakdowns
     - /analytics/savings-rate - Gross/net/discretionary savings calculations
     - /analytics/spending-insights - Pattern detection, anomalies
     - /analytics/advice - AI-powered spending recommendations
     - /analytics/portfolio - Performance, allocation, benchmarks
     - /analytics/projections - Monte Carlo net worth forecasting
     - /analytics/rebalance - Tax-optimized rebalancing suggestions
   - Caching: 24h TTL for insights, 1h for real-time metrics
   - AI: LLM-generated advice via ai-infra

8. CATEGORIZATION (fin_infra.categorization)
   - add_categorization(app)
   - Endpoints: /categorize (single), /categorize/batch (multiple)
   - Rules: 100+ merchant patterns
   - Categories: 56 MX-style categories
   - LLM: Fallback for unknown merchants (Google Gemini, OpenAI)
   - Performance: ~1000 predictions/sec
   - Cost: <$0.0002/transaction with caching

9. RECURRING DETECTION (fin_infra.recurring)
   - add_recurring_detection(app)
   - Endpoints: /recurring/detect, /recurring/insights
   - Patterns: Fixed subscriptions, variable bills, irregular/annual
   - Insights: Total monthly cost, cancellation opportunities
   - Rules: Amount stability, frequency consistency

10. INSIGHTS FEED (fin_infra.insights)
    - add_insights(app)
    - Endpoints: /insights/feed, /insights/priority
    - Sources: Net worth, budgets, goals, recurring, portfolio, tax, crypto
    - Priority: High/medium/low with action items
    - Aggregation: Unified dashboard with source attribution

11. BUDGETS (fin_infra.budgets) - 8 ENDPOINTS
    - add_budgets(app)
    - Endpoints:
      - GET/POST /budgets - List and create budgets
      - GET/PATCH/DELETE /budgets/{id} - Retrieve, update, delete budget
      - GET /budgets/{id}/progress - Real-time progress tracking
      - GET /budgets/{id}/alerts - Overspending warnings (80%/100%/110%)
      - GET /budgets/templates - Pre-built templates (50/30/20, Zero-Based, etc.)
      - POST /budgets/from-template - Create from template
    - Types: Personal, household, business, project, custom
    - Periods: Weekly, biweekly, monthly, quarterly, yearly
    - Rollover: Optional carry-over of unused budget

12. GOALS (fin_infra.goals) - 13 ENDPOINTS
    - add_goals(app)
    - Endpoints:
      - GET/POST /goals - List and create goals
      - GET/PATCH/DELETE /goals/{id} - Retrieve, update, delete goal
      - GET/POST /goals/{id}/milestones - List and create milestones
      - PATCH/DELETE /goals/{id}/milestones/{mid} - Update, delete milestone
      - GET/POST /goals/{id}/funding - List and set funding sources
      - POST /goals/{id}/pause - Pause goal
      - POST /goals/{id}/resume - Resume goal
      - POST /goals/{id}/complete - Mark complete
      - POST /goals/{id}/abandon - Abandon goal
    - Types: Savings, debt payoff, investment, net worth, income, custom
    - Milestones: Checkpoint amounts with target dates
    - Funding: Multi-account allocation with percentage splits

13. NET WORTH TRACKING (fin_infra.net_worth) - 4 ENDPOINTS
    - add_net_worth_tracking(app)
    - Endpoints:
      - GET /net-worth/current - Current net worth
      - GET /net-worth/history - Historical snapshots
      - GET /net-worth/breakdown - Assets vs liabilities by category
      - POST /net-worth/snapshot - Manual snapshot creation
    - Categories: 6 asset types, 6 liability types
    - Providers: Banking + brokerage + crypto aggregation
    - Jobs: Daily automatic snapshots via svc-infra
    - Alerts: Notify on ≥5% OR ≥$10k change

14. DOCUMENTS (fin_infra.documents)
    - add_documents(app)
    - Endpoints: /documents (upload), /documents/{id} (retrieve), /documents/search
    - OCR: Tesseract or AWS Textract
    - AI: Document analysis via ai-infra
    - Storage: S3 + SQL metadata
    - Security: SHA-256 checksums, PII filtering

15. SECURITY (fin_infra.security)
    - add_financial_security(app)
    - Features:
      - Automatic PII detection and masking
      - Encryption at rest (provider tokens, SSNs)
      - Audit logging (all PII access)
      - Compliance helpers (PCI-DSS, GLBA, FCRA)
    - Zero-config: Works out of the box
    - Extends: svc-infra auth without duplication

16. COMPLIANCE (fin_infra.compliance)
    - add_compliance_tracking(app)
    - Features:
      - PII classification (auto-detect tier 1/2/3)
      - Data retention tracking (GLBA 5yr, FCRA 7yr)
      - Erasure workflows (right-to-delete)
      - Vendor ToS compliance checks
    - Integration: svc-infra data lifecycle

17. NORMALIZATION (fin_infra.normalization)
    - add_normalization(app)
    - Endpoints: /normalize/symbol, /normalize/currency, /normalize/batch
    - Operations:
      - Ticker ↔ CUSIP ↔ ISIN conversions
      - Provider-specific symbol mapping
      - Currency conversion (live rates)
      - Company metadata enrichment
    - Caching: 24h TTL for symbol data

18. OBSERVABILITY (fin_infra.obs)
    - add_observability(app, route_classifier=financial_route_classifier)
    - Features:
      - Financial route classification (|financial suffix)
      - Provider call metrics (success/failure/latency)
      - LLM cost tracking (per-user, per-feature)
      - Cache hit/miss rates
    - Integration: svc-infra Prometheus + OpenTelemetry
    - Grafana: Filter metrics by route=~".*\\|financial"

19. CASHFLOWS (fin_infra.cashflows)
    - add_cashflows(app)
    - Endpoints: /cashflows/npv, /cashflows/irr, /cashflows/pmt, /cashflows/amortization
    - Operations:
      - NPV, IRR, XNPV, XIRR
      - Payment calculations (PMT, FV, PV)
      - Loan amortization schedules
    - Use cases: Mortgage calculators, investment analysis

20. SCAFFOLDING (fin_infra.scaffold)
    - Accessed via CLI: `fin-infra scaffold budgets --dest-dir app/models/`
    - Generates: Models, schemas, repositories
    - Integration: svc-infra ModelBase, SqlResource
    - Documented in main.py comments with examples

CUSTOM ENDPOINTS:
- GET / - Service overview, capabilities list, quick links
- GET /health - Kubernetes liveness probe
- GET /features - Dynamic feature list (env-based enable/disable)
- GET /status - Detailed status with provider health checks
- GET /docs - OpenAPI documentation (ALL capabilities visible)
- GET /metrics - Prometheus metrics (financial route classification)

MIDDLEWARE STACK (svc-infra):
1. RequestIDMiddleware (X-Request-ID header)
2. CatchAllExceptionMiddleware (5xx error handling)
3. TimeoutMiddleware (handler + body read timeouts)
4. RequestSizeLimitMiddleware (10MB default)
5. SimpleRateLimitMiddleware (120 req/min per IP)
6. IdempotencyMiddleware (in-memory store)
7. InflightTrackerMiddleware (graceful shutdown)
8. SecurityHeadersMiddleware (HSTS, CSP, etc.)

STARTUP SEQUENCE:
1. Load settings (environment-aware)
2. Setup logging (DEBUG in local, INFO in prod)
3. Create FastAPI app (setup_service_api)
4. Initialize database (SQLAlchemy engine)
5. Connect cache (Redis or in-memory)
6. Wire observability (Prometheus + tracing)
7. Add security (headers, CORS)
8. Mount ALL fin-infra capabilities (20+ add_*() calls)
9. Register lifecycle events (startup/shutdown)
10. Start uvicorn server

SHUTDOWN SEQUENCE:
1. Stop accepting new requests
2. Wait for in-flight requests (graceful shutdown)
3. Close database connections
4. Close Redis connections
5. Flush metrics
6. Log shutdown complete
"""

# Implementation follows...
```

---

## Updated Success Criteria

### Feature Completeness (20+ capabilities)
- ✅ Banking (2 providers: Plaid, Teller)
- ✅ Market Data (4 providers: Alpha Vantage, Yahoo, Polygon, CoinGecko)
- ✅ Credit Scores (1 provider: Experian)
- ✅ Brokerage (1 provider: Alpaca)
- ✅ Tax Data (1 provider: Mock/TaxBit)
- ✅ Crypto Data (3 providers: CoinGecko, Yahoo, CCXT)
- ✅ Analytics (7 endpoints: cash flow, savings rate, spending insights, advice, portfolio, projections, rebalancing)
- ✅ Categorization (56 categories, 100+ rules, LLM fallback)
- ✅ Recurring Detection (3 pattern types: fixed, variable, irregular)
- ✅ Insights Feed (7 sources: net worth, budgets, goals, recurring, portfolio, tax, crypto)
- ✅ Budgets (8 endpoints: CRUD, progress, alerts, templates)
- ✅ Goals (13 endpoints: CRUD, milestones, funding, state management)
- ✅ Net Worth (4 endpoints: current, history, breakdown, manual snapshot)
- ✅ Documents (OCR + AI analysis)
- ✅ Security (PII detection, encryption, audit logging)
- ✅ Compliance (3 tiers, retention policies, erasure workflows)
- ✅ Normalization (symbol resolution, currency conversion)
- ✅ Observability (financial route classification)
- ✅ Cashflows (NPV, IRR, payment calculations, amortization)
- ✅ Scaffolding (CLI documented with examples)

### Documentation Completeness (3000+ lines target)
- ✅ README (700+ lines): ALL 20+ capabilities listed with emojis, descriptions, use cases
- ✅ QUICKSTART (250+ lines): 5-minute setup verified in clean environment
- ✅ USAGE (800+ lines): Copy-paste examples for ALL 20+ capabilities
- ✅ docs/CAPABILITIES (1000+ lines): Comprehensive reference for each capability
- ✅ docs/DATABASE (300+ lines): Model reference, migrations, schema diagrams
- ✅ docs/PROVIDERS (500+ lines): All provider configs, sandbox setup, rate limits
- ✅ docs/CLI (200+ lines): fin-infra CLI reference with examples
- ✅ docs/SECURITY (250+ lines): PII handling, encryption, compliance

### Code Quality (5000+ lines target)
- ✅ main.py (1500+ lines): ALL capabilities wired, extensive inline docs
- ✅ settings.py (400+ lines): Type-safe config for all providers
- ✅ models.py (600+ lines): 12 financial models (User, Account, Transaction, Position, Goal, Budget, Document, NetWorthSnapshot, Insight, Category, RecurringPattern, TaxDocument)
- ✅ schemas.py (800+ lines): 48+ Pydantic schemas (Base/Create/Read/Update × 12 models)
- ✅ routes.py (1000+ lines): Custom endpoints for all capabilities
- ✅ scripts (700+ lines): 5 automation scripts (test_providers, scaffold_all, quick_setup, create_tables, seed_data)

### Testing (150+ tests target)
- ✅ Unit tests (80+ tests): Models, schemas, utils, categorization rules
- ✅ Integration tests (50+ tests): API endpoints, provider mocks, E2E flows
- ✅ Acceptance tests (20+ tests): Real provider connections (sandbox mode)

---

## Estimated Effort (UPDATED)

| Phase | Files | Lines | Tests | Effort |
|-------|-------|-------|-------|--------|
| Phase 1: Project Structure | 6 | 500 | 10 | 4h |
| Phase 2: Database Models | 10 | 2,500 | 40 | 10h |
| Phase 3: Main Application | 4 | 3,500 | 60 | 20h |
| Phase 4: Documentation | 8 | 3,000 | 20 | 10h |
| Phase 5: Scripts & Automation | 5 | 700 | 20 | 6h |
| **TOTAL** | **33** | **10,200** | **150** | **50h** |

---

## Why This Scope Is Necessary

1. **Completeness**: fin-infra has 20+ capabilities. The template MUST demonstrate ALL of them to be a true reference implementation.

2. **Best Practices**: Each capability has specific patterns (caching, error handling, PII filtering, provider fallbacks). The template must show these patterns correctly.

3. **Integration**: Showing how fin-infra + svc-infra + ai-infra work together requires comprehensive examples.

4. **Documentation**: With 20+ capabilities, extensive docs are mandatory for developer understanding.

5. **Testing**: Production-ready code requires comprehensive test coverage.

6. **Reusability**: Developers will copy/paste from this template. It must be correct, complete, and production-ready.

---

## Next Steps

1. **Review and Approve**: Get stakeholder approval for this expanded scope
2. **Begin Phase 1**: Follow existing template-plans.md Phase 1 (already complete)
3. **Expand Phase 2**: Add additional models for new capabilities (Insight, Category, RecurringPattern, TaxDocument)
4. **Implement Phase 3**: Wire ALL 20+ capabilities in main.py (1500+ lines)
5. **Complete Phase 4**: Write comprehensive documentation (3000+ lines)
6. **Finish Phase 5**: Create automation scripts (5 scripts, 700+ lines)
7. **Final Verification**: Test against expanded success criteria
