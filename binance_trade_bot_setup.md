# Binance Trading Bot Setup Guide

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Binance Testnet Account** (register at https://testnet.binancefuture.com/)
3. **API Keys** from Binance Testnet

## Installation

### 1. Install Required Dependencies

```bash
pip install python-binance
```

### 2. Set up Binance Testnet Account

1. Go to https://testnet.binancefuture.com/
2. Register for a new account
3. Go to API Management
4. Create new API key with futures trading permissions
5. Note down your API Key and Secret Key

### Or, 2. Set up Binance Spot Testnet Network

1. Go to https://testnet.binance.vision/
2. Authenticate using GitHub
3. Generate HMAC-SHA-256 Key
4. Note down your API Key and Secret Key

### 3. Configure API Keys(Optional)

For security, you can set environment variables:

```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_SECRET_KEY="your_secret_key_here"
```

## Usage Examples

### Basic Market Order

```bash
python main.py \
    --api-key "your_api_key" \
    --api-secret "your_secret_key" \
    --symbol BTCUSDT \
    --side BUY \
    --order-type MARKET \
    --quantity 0.001
```

### Limit Order

```bash
python main.py \
    --api-key "your_api_key" \
    --api-secret "your_secret_key" \
    --symbol BTCUSDT \
    --side BUY \
    --order-type LIMIT \
    --quantity 0.001 \
    --price 30000
```

### Stop-Limit Order

```bash
python main.py \
    --api-key "your_api_key" \
    --api-secret "your_secret_key" \
    --symbol BTCUSDT \
    --side SELL \
    --order-type STOP_LIMIT \
    --quantity 0.001 \
    --price 29000 \
    --stop-price 29500
```

### OCO Order (One-Cancels-Other)

```bash
python main.py \
    --api-key "your_api_key" \
    --api-secret "your_secret_key" \
    --symbol BTCUSDT \
    --side SELL \
    --order-type OCO \
    --quantity 0.001 \
    --price 31000 \
    --stop-price 29000 \
    --stop-limit-price 28900
```

## Information Commands

### View Account Information

```bash
python maint.py \
    --api-key "your_api_key" \
    --api-secret "your_secret_key" \
    --account-info
```


### View Open Orders

```bash
python main.py \
    --api-key "your_api_key" \
    --api-secret "your_secret_key" \
    --symbol BTCUSDT \
    --open-orders
```

### Cancel Order

```bash
python main.py \
    --api-key "your_api_key" \
    --api-secret "your_secret_key" \
    --symbol BTCUSDT \
    --cancel-order 123456789
```

## Command Line Parameters

| Parameter | Description | Required | Options |
|-----------|-------------|----------|---------|
| `--api-key` | Binance API key | Yes | String |
| `--api-secret` | Binance API secret | Yes | String |
| `--symbol` | Trading symbol |Conditional | e.g., BTCUSDT, ETHUSDT |
| `--side` | Order side | Conditional | BUY, SELL |
| `--order-type` | Order type | Conditional | MARKET, LIMIT, STOP_LIMIT, OCO |
| `--quantity` | Order quantity |Conditional| Float |
| `--price` | Limit price | Conditional | Float |
| `--stop-price` | Stop price | Conditional | Float |
| `--stop-limit-price` | Stop limit price (OCO) | Conditional | Float |
| `--testnet` | Use testnet | No | Flag (default: True) |

## Features

### Order Types Supported

1. **Market Orders**: Execute immediately at current market price
2. **Limit Orders**: Execute at specified price or better
3. **Stop-Limit Orders**: Trigger stop order when price reaches stop price
4. **OCO Orders**: One-Cancels-Other order combination

### Advanced Features

- **Comprehensive Logging**: All API calls, responses, and errors are logged
- **Error Handling**: Robust error handling for API and network issues
- **Input Validation**: Validates all user inputs before execution
- **Position Management**: View and manage open positions
- **Order Management**: Cancel, modify, and track orders
- **Account Information**: Real-time account balance and status

### Risk Management

- **Reduce Only Orders**: Close positions without opening new ones
- **Input Validation**: Prevents invalid orders
- **Testnet Environment**: Safe testing environment with fake money
- **Comprehensive Logging**: Track all trading activity

## Logging

The bot creates detailed logs in `trading_bot.log` with:
- All API requests and responses
- Order execution details
- Error messages and stack traces
- Account balance changes
- Position updates

## Error Handling

The bot handles various error scenarios:
- Network connectivity issues
- Invalid API credentials
- Insufficient balance
- Invalid order parameters
- Market closure periods
- API rate limiting

## Security Best Practices

1. **Never share API keys** in code or logs
2. **Use environment variables** for sensitive data
3. **Enable IP whitelist** in Binance API settings
4. **Use testnet** for development and testing
5. **Monitor logs** for suspicious activity
6. **Rotate API keys** regularly

## Troubleshooting

### Common Issues

1. **Invalid API credentials**
   - Verify API key and secret
   - Check API permissions
   - Ensure testnet keys for testnet

2. **Insufficient balance**
   - Check account balance
   - Verify margin requirements
   - Use smaller position sizes

3. **Invalid symbol**
   - Check symbol format (e.g., BTCUSDT)
   - Verify symbol is available on futures

4. **Network issues**
   - Check internet connection
   - Verify Binance API status
   - Check firewall settings

### Debug Mode

Enable debug logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

This will provide detailed information about all API calls and responses.

## Next Steps

1. **Test thoroughly** on testnet before live trading
2. **Implement additional strategies** (DCA, Grid trading, etc.)
3. **Add risk management** rules
4. **Create automated trading** schedules
5. **Implement backtesting** capabilities
6. **Add portfolio management** features

## Support

For issues and questions:
- Check the logs for error details
- Verify API credentials and permissions
- Ensure proper network connectivity
- Review Binance API documentation
- Test with minimal position sizes first
