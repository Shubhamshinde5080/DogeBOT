# DogeBot Test Suite

This directory contains the test suite for DogeBot components.

## Test Structure

- `test_indicators.py` - Tests for technical indicators (ATR, EMA, Bollinger Band %)
- `test_strategy.py` - Tests for grid trading strategy logic
- `test_order_mgr.py` - Tests for order management functionality
- `test_websocket.py` - Tests for WebSocket connectivity and data processing

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_indicators.py

# Run with coverage
pytest --cov=bot

# Run only unit tests
pytest -m unit

# Run integration tests
pytest -m integration
```

## Test Categories

- **Unit tests** (`@pytest.mark.unit`): Fast, isolated tests
- **Integration tests** (`@pytest.mark.integration`): Tests requiring external services
- **Slow tests** (`@pytest.mark.slow`): Tests that take longer to run
