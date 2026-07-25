# Nobitex OHLC Data Fetcher

This Python script retrieves **Open, High, Low, Close, and Volume** (OHLC) candle data from the [Nobitex Market API](https://apidocs.nobitex.ir/) and exports it as a JSON file.

## Features
- Fetches up to 500 candles per request.
- Supports all timeframes (1m, 5m, 15m, 30m, 1h, 3h, 4h, 6h, 12h, D, 2D, 3D).
- Outputs a list of candle objects with **time in milliseconds** (Unix timestamp × 1000).
- Filename includes the symbol, Jalali date, and time (safe for all OSes).

## Usage

```bash
python main.py -symbol <SYMBOL> -timeframe <TIMEFRAME> -candles <COUNT>
```

### Example
```bash
python main.py -symbol BTCIRT -timeframe 4h -candles 35
```

This will generate a file like `BTCIRT-1405-05-02-17-48-27.json` containing the OHLC data.

### Output Format
```json
[
  {
    "time": 1784853000000,
    "open": 12620000001.0,
    "high": 12729722030.0,
    "low": 12590378778.0,
    "close": 12703672179.0,
    "volume": 0.62346164
  },
  ...
]
```

## Documentation
- [OHLC API Docs (Nobitex)](https://apidocs.nobitex.ir/market_data/%D8%AF%D8%B1%DB%8C%D8%A7%D9%81%D8%AA-%D8%AF%D8%A7%D8%AF%D9%87-%D9%87%D8%A7%DB%8C-ohlc)
- [Old API Docs (UDF Format)](https://old-apidocs.nobitex.ir/#ohlc)
- [Local API Docs](API%20Docs.md)

## Requirements
- Python 3.6+
- `requests` library (install with `pip install requests`)

## Notes
- The API limits responses to 500 candles per request.
- Candles are returned in reverse chronological order (newest first).
