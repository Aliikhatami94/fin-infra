# Production Readiness Punch List (v1 Framework Release)

Comprehensive checklist for making fin-infra production‑ready. Each section follows: Research → Design → Implement → Tests → Verify → Docs. We will not implement until reviewed; existing functionality will be reused (skipped) when discovered during research.

## Legend
- [ ] Pending
- [x] Completed
- [~] Skipped (already exists / out of scope)
(note) Commentary or link to ADR / PR.

⸻

## Must‑have (Ship with v1)

### A0. Acceptance Harness & CI Promotion Gate (new)
- [x] Design: Acceptance env contract (ports, env, seed keys, base URL). (ADR‑0001 — docs/acceptance.md)
- [x] Implement: docker-compose.test.yml + Makefile targets (accept/up/wait/seed/down).
	- Files: docker-compose.test.yml, Makefile
- [x] Implement: minimal acceptance app and first smoke test.
	- Files: tests/acceptance/app.py, tests/acceptance/test_smoke_ping.py, tests/acceptance/conftest.py
- [x] Implement: wait-for helper (Makefile curl loop) and tester container.
- [x] Verify: CI job to run acceptance matrix and teardown.
	- Files: .github/workflows/acceptance.yml
- [x] Docs: docs/acceptance.md and docs/acceptance-matrix.md updated for tester and profiles.
- [x] Supply-chain: generate SBOM and image scan (Trivy) with severity gate; upload SBOM as artifact. (acceptance.yml)
- [x] Provenance: sign SBOM artifact (cosign keyless) — best-effort for v1. (acceptance.yml)
- [~] Backend matrix: run acceptance against in‑memory + Redis (cache) profiles. (Reuse svc‑infra caching; Redis profile coverage is handled in svc‑infra contexts.)

### 0. Backfill Coverage for Base Modules (current repo)

Owner: TBD — Evidence: PRs, tests, CI runs
- Core: settings.py (timeouts/retries provided by svc‑infra; no local http wrapper)
- [~] Research: ensure pydantic‑settings (networking concerns covered in svc‑infra).
- [~] Skipped: unit tests for HTTP timeouts/retries (covered by svc‑infra).
- [ ] Docs: quickstart for settings (link to svc‑infra for timeouts/retries & caching).
- Providers skeletons:
	- Market: providers/market/yahoo.py (proto) → swap to chosen vendor(s) below.
	- Crypto: providers/market/ccxt_crypto.py (proto)
	- Banking: providers/banking/plaid_client.py (proto) → replace with default pick.
	- Brokerage: providers/brokerage/alpaca.py (paper trading)

### 1. Provider Registry & Interfaces (plug‑and‑play)
- [ ] Research: ABCs for BankingProvider, MarketDataProvider, CryptoDataProvider, BrokerageProvider.
- [ ] Design: provider registry with entry‑points + YAML mapping. (ADR‑0002)
- [ ] Implement: fin_infra/providers/base.py ABCs + registry.py loader (resolve("banking:teller")).
- [ ] Tests: dynamic import, fallback on missing providers, feature flags.
- [ ] Docs: docs/providers.md with examples + configuration table.

### 2. Banking / Account Aggregation (default: Teller)
- [ ] Research: free dev tier limits, token exchange, accounts/transactions endpoints.
- [ ] Design: auth flow contracts; token storage interface; PII boundary. (ADR‑0003)
- [ ] Implement: providers/banking/teller_client.py with typed DTOs; sandbox seed.
- [ ] Tests: integration (mocked HTTP) + acceptance: link‑token stub → accounts list → transactions list.
- [ ] Verify: acceptance profile banking=teller green.
- [ ] Docs: docs/banking.md (env vars, limits, migration path to Plaid/MX later).

### 3. Equities/FX Market Data (default: Alpha Vantage)
- [ ] Research: free tier + throttling; endpoint coverage (quote, OHLC, FX).
- [ ] Design: rate‑aware adapter with backoff. (ADR‑0004) Caching is via svc‑infra if/when endpoints are made async.
- [ ] Implement: providers/market/alpha_vantage.py (quotes, time series daily/intraday, FX). (Optionally adopt svc‑infra caching if migrating to async.)
- [ ] Tests: unit for symbol normalization; acceptance: price fetch burst obeys limits.
- [ ] Verify: acceptance profile market=alpha_vantage green.
- [ ] Docs: docs/market-data.md (quotas, caching guidance, fallbacks).

### 4. Crypto Market Data (default: CoinGecko)
- [ ] Research: free plan quotas; mapping symbol → CoinGecko id; vs CCXT.
- [ ] Design: id mapping store; normalize by asset{type, symbol, exchange?}. (ADR‑0005)
- [ ] Implement: providers/crypto/coingecko.py (spot prices, metadata) + optional ccxt candles.
- [ ] Tests: id resolution edge cases (e.g., BTC, WBTC, BTC.B), OHLC sanity.
- [ ] Verify: acceptance profile crypto=coingecko green.
- [ ] Docs: docs/crypto-data.md.

### 5. Brokerage (default: Alpaca Paper Trading)
- [ ] Research: orders, positions, clock; paper trading free.
- [ ] Design: order idempotency + replay safety; clock‑guard + risk checks. (ADR‑0006)
- [ ] Implement: providers/brokerage/alpaca.py (submit_order, positions) with idempotency key + server replay detection.
- [ ] Tests: unit for order param validation; acceptance: buy/sell happy path + duplicate submission → one order.
- [ ] Verify: acceptance profile brokerage=alpaca_paper green.
- [ ] Docs: docs/brokerage.md (keys, paper vs live, risk notes).

### 6. Caching, Rate Limits & Retries (cross‑cutting)
- [~] Skipped: Reuse svc‑infra for caching, rate limiting, timeouts & retries. No local cache/http/retry modules in fin‑infra; adopt svc‑infra decorators only if/when migrating providers to async.

### 7. Data Normalization: Symbols, Currencies, Time
- [ ] Research: symbol clashes (e.g., BTI across regions), ISO‑4217, crypto tickers.
- [ ] Design: canonical InstrumentKey (namespace:symbol) + FX normalization + tz handling. (ADR‑0008)
- [ ] Implement: fin_infra/normalize.py (instrument key, currency → decimal places, timezone utils, trading calendar shim).
- [ ] Tests: round‑trips across providers; FX conversions sanity.
- [ ] Docs: docs/normalization.md.

### 8. Security, Secrets & PII boundaries
- [~] Skipped: Reuse svc‑infra security/auth/logging scaffolding where applicable. Fin‑infra is a library; defer service‑level security concerns (PII boundaries, signed cookies, auth) to svc‑infra.

### 9. Observability & SLOs
- [ ] Research: metrics/logging libraries.
- [ ] Design: SLI/SLOs for provider calls (availability %, p95 latency); error budget math. (ADR‑0010)
- [ ] Implement: Prometheus middleware for any demo API; provider call metrics (provider_request_total{provider,endpoint,status}; latency histogram).
- [ ] Tests: metrics presence; failure paths increment properly.
- [ ] Verify: dashboard JSON, alert samples (Grafana + Alertmanager). (docs/ops.md)

### 10. Demo API & SDK Surface (optional but helpful)
- [ ] Research: FastAPI scaffolding for demo endpoints.
- [ ] Design: minimal endpoints: /banking/accounts, /market/quote, /crypto/ticker, /brokerage/submit-order.
- [ ] Implement: api/fastapi/add.py helper + demo app under examples/demo_api.
- [ ] Tests: openapi present; CORS preflight; simple auth key.
- [ ] Docs: docs/api.md quickstart.

### 11. DX & Quality Gates
- [ ] Research: CI pipeline steps & gaps.
- [ ] Design: gating order (ruff, mypy, pytest, SBOM, SAST stub), version bump + changelog.
- [ ] Implement: CI workflow templates under dx/ + .github/workflows/ci.yml.
- [ ] Tests: dx helpers unit tests.
- [ ] Docs: docs/contributing.md and release process.

### 12. Legal/Compliance Posture (v1 lightweight)
- [ ] Research: vendor ToS (no data resale; attribution); storage policy for PII and tokens.
- [ ] Design: data map + retention notes; toggle to disable sensitive modules.
- [ ] Implement: compliance notes page + code comments marking PII boundaries.
- [ ] Docs: docs/compliance.md (not a substitute for legal review).

⸻

## Nice‑to‑have (Fast Follows)

### 13. Multi‑Broker Aggregation (read‑only)
- [ ] Research: SnapTrade pricing and coverage.
- [ ] Design: BrokerageAggregatorProvider + account/positions sync cadence.
- [ ] Implement: providers/brokerage/snaptrade.py (read‑only holdings, transactions).
- [ ] Tests: diff‑merge holdings; symbol normalization across brokers.
- [ ] Docs: enablement + limits.

### 14. Portfolio Analytics & Optimization
- [ ] Research: PyPortfolioOpt, QuantStats, Empyrical, Statsmodels.
- [ ] Design: analytics module surface (returns, risk, factor-ish metrics; frontier/HRP optional).
- [ ] Implement: analytics/portfolio.py + examples.
- [ ] Tests: reproducibility (seeded), unit for metrics.
- [ ] Docs: docs/analytics.md.

### 15. Statements & OCR (import)
- [ ] Research: CoinGecko/CCXT statement gaps; Ocrolus/Veryfi vs Tesseract.
- [ ] Design: document ingestion pipeline; schema for transactions.
- [ ] Implement: imports/statements/* + pluggable parser interface.
- [ ] Tests: sample PDFs; redaction.
- [ ] Docs: docs/imports.md.

### 16. Identity/KYC (Stripe Identity)
- [ ] Research: free allowances; required verifications.
- [ ] Design: provider interface IdentityProvider.
- [ ] Implement: providers/identity/stripe_identity.py (start/verify/status).
- [ ] Tests: mocked integration; rate limits.
- [ ] Docs: docs/identity.md.

### 17. Payments
- [ ] Research: Stripe ACH/Card; regional alt‑rails.
- [ ] Design: payment adapter + webhook verification.
- [ ] Implement: providers/payments/stripe.py.
- [ ] Tests: idempotency, webhook signature.
- [ ] Docs: docs/payments.md.

### 18. Feature Flags & Experiments
- [ ] Research: flag store options.
- [ ] Design: FlagService + evaluation order; experiment allocation.
- [ ] Implement: flags/service.py + decorator.
- [ ] Tests: rollout stability.
- [ ] Docs: docs/flags.md.

### 19. Internationalization & Trading Calendars
- [ ] Research: market calendars (NYSE, NASDAQ, LSE, crypto 24/7).
- [ ] Design: calendar abstraction; localized formatting.
- [ ] Implement: calendars/* + i18n helpers.
- [ ] Tests: open/closed behavior, holiday rules.
- [ ] Docs: docs/time-and-calendars.md.

⸻

## Quick Wins (Implement Early)

### 20. Immediate Enhancements
- [ ] Implement: per‑provider rate‑limit headers surfaced to callers. (Optional if svc‑infra layer used.)
- [ ] Implement: common error model (Problem+JSON) + error codes registry.
- [ ] Implement: order idempotency key middleware (brokerage).
- [ ] Implement: provider health‑check endpoints for demo API.
- [ ] Implement: symbol lookup endpoint (/symbols/search?q=). (Caching, if needed, via svc‑infra.)
- [ ] Implement: CLI utilities (fin‑infra):
	- keys verify, demo run, providers ls. (Remove cache‑warm; rely on svc‑infra if needed.)

⸻

## Tracking & Ordering

Prioritize Must‑have top→bottom. Interleave Quick Wins if they unlock infrastructure (e.g., retries/backoff before Alpha Vantage adapter if not using svc‑infra). Each section requires: Research complete → Design approved → Implementation + Tests → Verify → Docs.

## Notes / Decisions Log

Record ADRs for: provider registry, Alpha Vantage rate/backoff strategy (caching via svc‑infra if adopted), CoinGecko id mapping, order idempotency semantics, symbol normalization, SLOs/metrics taxonomy, PII/secret boundaries, CI gates.

⸻

## Global Verification & Finalization
- Run full pytest suite after each major category completion.
- Re‑run flaky markers (x3) to ensure stability.
- Update this checklist with PR links & skip markers (~) for existing features.
- Produce release readiness report summarizing completed items.
- Tag version & generate changelog.

Updated: Initial production‑readiness plan for fin‑infra aligned to provider defaults (Teller, Alpha Vantage, CoinGecko, Alpaca paper).
