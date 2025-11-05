"""Acceptance tests for Alpaca brokerage provider.

⚠️ TRADING WARNING: These tests use paper trading mode only.
Never run with live trading credentials.

These tests make real API calls and require:
- ALPACA_PAPER_API_KEY: Alpaca paper trading API key
- ALPACA_PAPER_SECRET_KEY: Alpaca paper trading secret key

Get paper trading credentials from: https://app.alpaca.markets/paper/dashboard/overview
"""
import os
from decimal import Decimal

import pytest

from fin_infra.brokerage import easy_brokerage
from fin_infra.providers.brokerage.alpaca import AlpacaBrokerage


pytestmark = [pytest.mark.acceptance]


@pytest.mark.skipif(
    not (os.getenv("ALPACA_PAPER_API_KEY") and os.getenv("ALPACA_PAPER_SECRET_KEY")),
    reason="No Alpaca paper trading credentials in environment"
)
class TestAlpacaBrokerageAcceptance:
    """Acceptance tests for Alpaca brokerage provider (paper trading only)."""
    
    @pytest.fixture
    def broker(self):
        """Create Alpaca broker in paper mode."""
        return AlpacaBrokerage(
            api_key=os.getenv("ALPACA_PAPER_API_KEY"),
            api_secret=os.getenv("ALPACA_PAPER_SECRET_KEY"),
            mode="paper"
        )
    
    def test_get_account(self, broker):
        """Test getting account information."""
        account = broker.get_account()
        
        assert isinstance(account, dict)
        assert "id" in account
        assert "status" in account
        assert "buying_power" in account
        assert "cash" in account
        assert "portfolio_value" in account
        
        # Verify paper trading account
        assert account["status"] in ("ACTIVE", "INACTIVE")
        print(f"✓ Alpaca account: Status={account['status']}, "
              f"Buying Power=${account['buying_power']}, "
              f"Portfolio Value=${account['portfolio_value']}")
    
    def test_list_positions(self, broker):
        """Test listing positions."""
        positions = broker.positions()
        
        assert isinstance(positions, list)
        # May be empty if no positions
        print(f"✓ Alpaca positions: {len(positions)} open positions")
        
        if positions:
            pos = positions[0]
            assert "symbol" in pos
            assert "qty" in pos
            assert "side" in pos
            assert "market_value" in pos
            print(f"  Example: {pos['symbol']} - {pos['qty']} shares @ ${pos.get('current_price', 'N/A')}")
    
    def test_list_orders(self, broker):
        """Test listing orders."""
        # List all orders (including closed)
        orders = broker.list_orders(status="all", limit=10)
        
        assert isinstance(orders, list)
        print(f"✓ Alpaca orders: {len(orders)} orders in history")
        
        if orders:
            order = orders[0]
            assert "id" in order
            assert "symbol" in order
            assert "qty" in order
            assert "side" in order
            assert "type" in order
            assert "status" in order
            print(f"  Latest: {order['symbol']} - {order['side'].upper()} {order['qty']} @ {order['type']}, Status={order['status']}")
    
    def test_submit_and_cancel_order(self, broker):
        """Test submitting and canceling an order.
        
        Uses a limit order that's unlikely to fill immediately,
        so we can test order management without executing trades.
        """
        # Submit a limit order at very low price (unlikely to fill)
        order = broker.submit_order(
            symbol="AAPL",
            qty=1,
            side="buy",
            type_="limit",
            time_in_force="day",
            limit_price=1.00  # Very low price, won't fill
        )
        
        assert isinstance(order, dict)
        assert "id" in order
        assert order["symbol"] == "AAPL"
        assert order["side"] == "buy"
        assert order["type"] == "limit"
        assert order["status"] in ("new", "accepted", "pending_new")
        print(f"✓ Order submitted: ID={order['id']}, Symbol={order['symbol']}, Status={order['status']}")
        
        order_id = order["id"]
        
        # Get order details
        fetched_order = broker.get_order(order_id)
        assert fetched_order["id"] == order_id
        assert fetched_order["symbol"] == "AAPL"
        print(f"✓ Order fetched: ID={order_id}, Status={fetched_order['status']}")
        
        # Cancel the order
        broker.cancel_order(order_id)
        print(f"✓ Order canceled: ID={order_id}")
        
        # Verify cancellation
        canceled_order = broker.get_order(order_id)
        # Status may be "canceled" or "pending_cancel" depending on timing
        assert canceled_order["status"] in ("canceled", "pending_cancel")
        print(f"✓ Order status after cancel: {canceled_order['status']}")
    
    def test_get_portfolio_history(self, broker):
        """Test getting portfolio history."""
        history = broker.get_portfolio_history(period="1W", timeframe="1D")
        
        assert isinstance(history, dict)
        assert "timestamp" in history
        assert "equity" in history
        
        # May have data depending on account history
        timestamps = history.get("timestamp", [])
        print(f"✓ Portfolio history: {len(timestamps)} data points over 1 week")
        
        if timestamps:
            equity_values = history.get("equity", [])
            print(f"  Latest equity: ${equity_values[-1] if equity_values else 'N/A'}")
