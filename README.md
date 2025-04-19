# Crypto Trading MCP (Model Context Protocol)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


A simple Model Context Protocol (MCP) server for price lookup and trading across multiple cryptocurrency exchanges.


https://github.com/user-attachments/assets/34f3a431-9370-4832-923e-ab89bf1d4913


## Requirements

- Python 3.10 or higher

## Supported Exchanges
Currently supports spot trading only.

- Upbit
- Gate.io
- Binance

More exchanges will be added in the future.

## Environment Setup

Add the authentication information required by each exchange to the environment variables. 

For example, Upbit is as follows:

```bash
UPBIT_ACCESS_KEY="your-access-key"
UPBIT_SECRET_KEY="your-secret-key"
```

## Development Guide

### Adding a New Exchange

1. Create a new exchange class inheriting from `CryptoExchange` abstract class
2. Implement required API methods
3. Write test cases
4. Register the new exchange in the factory class

### Running Tests

```bash
# Install test dependencies
uv pip install -e ".[test]"

# Run tests
pytest
```
