# Credit Score Monitoring

**Provider**: Experian, Equifax (future), TransUnion (future)  
**Status**: ✅ v1 Complete (mock implementation)  
**Regulation**: FCRA (Fair Credit Reporting Act)

## Overview

Credit score monitoring enables fintech applications to:
- Retrieve user credit scores (FICO, VantageScore)
- Access full credit reports (accounts, inquiries, payment history)
- Subscribe to score change notifications
- Display credit insights (factors, utilization, etc.)

**Use cases**: Credit Karma, Credit Sesame, Mint, personal finance apps

## Quick Start

### Zero-Config Usage

```python
from fin_infra.credit import easy_credit

# Uses EXPERIAN_API_KEY from environment
credit = easy_credit()
score = credit.get_credit_score("user123")

print(f"Score: {score.score} ({score.score_model})")
print(f"Change: {score.change:+d} points")
```

### FastAPI Integration

```python
from fastapi import FastAPI
from fin_infra.credit.add import add_credit_monitoring

app = FastAPI()

# Wire credit routes (GET /credit/score, /credit/report, etc.)
credit = add_credit_monitoring(app, provider="experian")

# Routes available:
# GET /credit/score?user_id=user123
# GET /credit/report?user_id=user123
# POST /credit/subscribe?user_id=user123&webhook_url=...
```

### Full Credit Report

```python
from fin_infra.credit import easy_credit

credit = easy_credit()
report = credit.get_credit_report("user123")

print(f"Score: {report.score.score}")
print(f"Accounts: {len(report.accounts)}")
print(f"Inquiries: {len(report.inquiries)}")

# Access account details
for account in report.accounts:
    print(f"{account.creditor_name}: ${account.balance}")
```

## Data Models

### CreditScore

```python
from fin_infra.models.credit import CreditScore

score = CreditScore(
    user_id="user123",
    score=735,
    score_model="FICO 8",
    bureau="experian",
    score_date=date.today(),
    factors=[
        "Credit card utilization is high (35%)",
        "No recent late payments",
        "Average age of accounts is good (8 years)",
    ],
    change=15  # +15 points since last pull
)
```

**Fields**:
- `score` (int): Credit score 300-850
- `score_model` (str): "FICO 8", "VantageScore 3.0", etc.
- `bureau` (str): "experian", "equifax", "transunion"
- `factors` (list[str]): Factors affecting score
- `change` (int | None): Change since last pull

### CreditReport

```python
from fin_infra.models.credit import CreditReport

report = CreditReport(
    user_id="user123",
    bureau="experian",
    report_date=date.today(),
    score=score,
    accounts=[...],           # List of CreditAccount
    inquiries=[...],          # List of CreditInquiry
    public_records=[...],     # List of PublicRecord
    consumer_statements=[...] # Disputes, etc.
)
```

### CreditAccount (Tradeline)

```python
from fin_infra.models.credit import CreditAccount

account = CreditAccount(
    account_id="acc123",
    account_type="credit_card",  # or "mortgage", "auto_loan", "student_loan"
    creditor_name="Chase Bank",
    account_status="open",
    balance=Decimal("5000.00"),
    credit_limit=Decimal("10000.00"),
    payment_status="current",    # or "30_days_late", "60_days_late", etc.
    opened_date=date(2020, 1, 1),
    last_payment_date=date(2025, 1, 1),
)
```

### CreditInquiry (Hard/Soft Pulls)

```python
from fin_infra.models.credit import CreditInquiry

inquiry = CreditInquiry(
    inquiry_id="inq123",
    inquiry_type="hard",         # or "soft"
    inquirer_name="Chase Bank",
    inquiry_date=date(2025, 1, 1),
    purpose="credit_card_application"  # Optional
)
```

## Bureau Comparison

| Feature | Experian (v1) | Equifax (v2) | TransUnion (v2) |
|---------|---------------|--------------|-----------------|
| **Credit Scores** | ✅ FICO 8 | ⏸️ FICO 8, VantageScore | ⏸️ FICO 8, VantageScore |
| **Credit Reports** | ✅ Mock data | ⏸️ Full reports | ⏸️ Full reports |
| **Sandbox** | ✅ Free tier | ⏸️ Enterprise | ⏸️ Enterprise |
| **Webhooks** | ⏸️ v2 | ⏸️ v2 | ⏸️ v2 |
| **Cost** | ~$0.50-$2.00/pull | ~$0.50-$2.00/pull | ~$0.50-$2.00/pull |
| **API Docs** | [Experian Connect](https://developer.experian.com/) | [Equifax API](https://www.equifax.com/business/api/) | [TransUnion API](https://www.transunion.com/business/products-services/apis) |

**v1 Note**: v1 implements Experian with mock data only. Real API integration requires API key and is deferred to v2.

## Environment Variables

### Experian

```bash
# API credentials (get from https://developer.experian.com/)
EXPERIAN_API_KEY=your_api_key_here
EXPERIAN_CLIENT_ID=your_client_id_here  # If required
EXPERIAN_ENVIRONMENT=sandbox  # or "production"
```

## Integration with svc-infra

### Caching (Reduce Bureau Costs)

**Problem**: Bureau pulls cost ~$0.50-$2.00 each. Without caching, costs scale linearly with user requests.

**Solution**: Use `svc-infra.cache` with 24h TTL (industry standard for credit monitoring):

```python
from svc_infra.cache import cache_read, cache_write, resource
from fin_infra.credit import easy_credit

credit = easy_credit()

# Define credit resource with 24-hour TTL
credit_resource = resource("credit_score", id_param="user_id")

@credit_resource.cache_read(ttl=86400)  # 24 hours
async def get_credit_score_cached(user_id: str):
    # Fetch from bureau (expensive - ~$0.50-$2.00)
    score = credit.get_credit_score(user_id)
    return score

# Invalidate cache on user request or webhook notification
@credit_resource.cache_write()
async def refresh_credit_score(user_id: str):
    # Force fresh pull
    score = credit.get_credit_score(user_id)
    return score
```

**Cost savings**: With 24h caching, a user checking their score 10 times/day costs **1 pull/day** instead of **10 pulls/day** (90% savings).

### Webhooks (Score Change Notifications)

**v2 Integration** (not implemented in v1):

```python
from svc_infra.webhooks import add_webhooks, webhook_event
from fastapi import FastAPI

app = FastAPI()

# Wire webhooks
add_webhooks(app, events=["credit.score_changed"])

# Emit event when bureau notifies us of score change
await webhook_event(
    app,
    "credit.score_changed",
    {
        "user_id": "user123",
        "old_score": 720,
        "new_score": 735,
        "change": +15,
        "bureau": "experian"
    }
)
```

Users can subscribe to webhooks at `POST /credit/subscribe` endpoint.

### Compliance Event Logging (FCRA)

**FCRA requirement**: All credit report accesses must be logged with permissible purpose.

```python
from fin_infra.compliance import log_compliance_event

# Log every credit report access
log_compliance_event(
    app,
    "credit.report_accessed",
    {
        "user_id": user_id,
        "bureau": "experian",
        "purpose": "consumer_disclosure",  # FCRA permissible purpose
        "timestamp": datetime.utcnow().isoformat(),
    }
)
```

**Permissible purposes** (FCRA §604):
- Consumer disclosure (user requesting their own report)
- Credit transaction (loan application)
- Employment purposes (with user consent)
- Account review (existing creditor)
- Collection activity

**Important**: fin-infra does NOT enforce permissible purpose in v1. Production apps MUST implement consent workflows and purpose tracking.

## FCRA Compliance Notes

### Legal Requirements

1. **User Consent**: Users must consent to credit pulls
2. **Permissible Purpose**: All pulls must have valid FCRA purpose
3. **Adverse Action Notices**: If credit decision is based on report, notify user
4. **Data Retention**: Credit reports must be retained per state laws
5. **Security**: PII must be encrypted at rest and in transit

### Implementation Checklist

- [ ] User consent workflow (checkbox, signature, etc.)
- [ ] Permissible purpose tracking (log all accesses)
- [ ] Adverse action notice generation (if applicable)
- [ ] Data retention policy (see ADR-0011, docs/compliance.md)
- [ ] PII encryption (use svc-infra.security)
- [ ] Access logging (use fin_infra.compliance)

### Recommended Reading

- [FTC: Fair Credit Reporting Act](https://www.ftc.gov/legal-library/browse/statutes/fair-credit-reporting-act)
- [CFPB: Credit Reporting](https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores/)
- [ADR-0011: Compliance Posture](./adr/0011-compliance-posture.md)
- [Compliance Guide](./compliance.md)

**Disclaimer**: This documentation is NOT legal advice. Consult with legal counsel before deploying credit monitoring in production.

## API Reference

### easy_credit()

```python
def easy_credit(provider: str | CreditProvider = "experian", **config) -> CreditProvider
```

**Create configured credit provider with environment variable auto-detection.**

**Args**:
- `provider` (str | CreditProvider): Bureau name or CreditProvider instance
  - `"experian"` (default): Experian provider
  - `"equifax"`: Equifax provider (future)
  - `"transunion"`: TransUnion provider (future)
  - `CreditProvider` instance: Use directly
- `**config`: Optional configuration overrides
  - `api_key` (str): API key (overrides env)
  - `environment` (str): "sandbox" or "production" (overrides env)

**Returns**: Configured `CreditProvider` instance

**Environment Variables**:
- `EXPERIAN_API_KEY`: API key for Experian API
- `EXPERIAN_CLIENT_ID`: Client ID (if required)
- `EXPERIAN_ENVIRONMENT`: "sandbox" or "production" (default: sandbox)

**Examples**:

```python
# Zero config (uses EXPERIAN_API_KEY from env)
credit = easy_credit()

# Explicit provider
credit = easy_credit(provider="experian", api_key="...", environment="production")

# Custom provider instance
custom_provider = ExperianProvider(api_key="...", environment="production")
credit = easy_credit(provider=custom_provider)
```

### add_credit_monitoring()

```python
def add_credit_monitoring(
    app: FastAPI,
    *,
    provider: str | CreditProvider | None = None,
    prefix: str = "/credit",
    cache_ttl: int = 86400,
    **config
) -> CreditProvider
```

**Wire credit monitoring routes to FastAPI app.**

**Mounts routes**:
- `GET {prefix}/score` - Get current credit score (cached)
- `GET {prefix}/report` - Get full credit report (cached)
- `POST {prefix}/subscribe` - Subscribe to score change webhooks
- `GET {prefix}/history` - Get score history (future)

**Args**:
- `app` (FastAPI): FastAPI application
- `provider` (str | CreditProvider | None): Bureau name or CreditProvider instance (default: "experian")
- `prefix` (str): Route prefix (default: "/credit")
- `cache_ttl` (int): Cache TTL in seconds (default: 86400 = 24h)
- `**config`: Additional configuration passed to easy_credit()

**Returns**: Configured `CreditProvider` instance

**Example**:

```python
from fastapi import FastAPI
from fin_infra.credit.add import add_credit_monitoring

app = FastAPI()
credit = add_credit_monitoring(app, provider="experian")

# Routes available:
# GET /credit/score?user_id=user123
# GET /credit/report?user_id=user123
# POST /credit/subscribe?user_id=user123&webhook_url=...
```

## Testing

### Unit Tests

```bash
# Run credit tests
poetry run pytest tests/unit/test_credit.py -v

# All 22 tests pass with mock data
```

### Acceptance Tests

**v1**: No acceptance tests (requires real Experian API key)

**v2**: Will add acceptance tests with sandbox credentials

```bash
# Future: Run acceptance tests with sandbox credentials
EXPERIAN_API_KEY=sandbox_key poetry run pytest tests/acceptance/test_credit_experian_acceptance.py -v
```

## v1 Implementation Status

### Completed ✅

- [x] ADR-0012: Credit monitoring architecture
- [x] Data models: CreditScore, CreditReport, CreditAccount, CreditInquiry, PublicRecord
- [x] ExperianProvider (mock implementation)
- [x] easy_credit() one-liner
- [x] add_credit_monitoring() FastAPI helper
- [x] Unit tests (22 tests, all passing)
- [x] Documentation (this file)

### Deferred to v2 ⏸️

- [ ] Real Experian API integration (requires API key)
- [ ] svc-infra.cache integration (24h TTL)
- [ ] svc-infra.webhooks integration (score change notifications)
- [ ] Compliance event logging (FCRA permissible purpose)
- [ ] svc-infra dual routers (user_router for auth)
- [ ] svc-infra scoped docs (landing page card)
- [ ] Equifax provider
- [ ] TransUnion provider
- [ ] Acceptance tests (sandbox credentials)
- [ ] Score history tracking
- [ ] Dispute management

## Related Documentation

- [ADR-0012: Credit Monitoring Architecture](./adr/0012-credit-monitoring.md)
- [ADR-0011: Compliance Posture](./adr/0011-compliance-posture.md)
- [Compliance Guide](./compliance.md)
- [svc-infra Cache](../../svc-infra/docs/cache.md)
- [svc-infra Webhooks](../../svc-infra/docs/webhooks.md)

## Support

**Experian API**: https://developer.experian.com/  
**FCRA Guidance**: https://www.ftc.gov/legal-library/browse/statutes/fair-credit-reporting-act  
**Issues**: Report issues on GitHub

---

**Note**: v1 uses mock data only. Real bureau integration requires API keys and legal review before production deployment.
