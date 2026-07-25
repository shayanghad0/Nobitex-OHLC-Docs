# Nobitex OHLC Data Fetcher

A Python script to fetch OHLC (Open, High, Low, Close, Volume) candlestick data from the [Nobitex](https://nobitex.ir) exchange API and export it as a JSON file.

The exported JSON is a **list of candle objects**, with timestamps in **milliseconds** – compatible with many charting and analysis tools.

---

## Features

- Fetch up to **500 candles** per request (API limit).
- Supports all Nobitex **resolutions** (minutes, hours, days).
- Outputs JSON as a clean array of objects, each with:
  - `time` (Unix timestamp in **milliseconds**)
  - `open`, `high`, `low`, `close`, `volume`
- File naming uses **Jalali (Solar Hijri) date** and current time, e.g.  
  `BTCIRT-1405-05-02-17-48-27.json`
- Optional **output directory** (absolute or relative) – the directory is created if missing.
- Safe file names for Windows, Linux, macOS.

---

## Requirements

- Python 3.6+
- `requests` library

Install `requests` if not already installed:

```bash
pip install requests
```

---

## Usage

```bash
python main.py -symbol SYMBOL -timeframe TIMEFRAME -candles COUNT [-output DIR]
```

### Arguments

| Argument   | Required | Description                                                                                 |
|------------|----------|---------------------------------------------------------------------------------------------|
| `-symbol`  | ✅ Yes   | Trading symbol, e.g., `BTCIRT`, `ETHUSDT`, `BTCUSDT`. See full list below.                 |
| `-timeframe` | ✅ Yes | Candle interval. Supported values: `1m`, `5m`, `15m`, `30m`, `1h`, `3h`, `4h`, `6h`, `12h`, `D`, `2D`, `3D`. |
| `-candles` | ✅ Yes   | Number of candles to fetch (1–500).                                                         |
| `-output`  | ❌ No    | Output directory path (absolute or relative). Defaults to current directory.                |

### Valid Symbol List

The full list is available in the [Nobitex API documentation](https://nobitex.ir). Common ones include:

- **IRT pairs**: `BTCIRT`, `ETHIRT`, `USDTIRT`, `LTCIRT`, `XRPIRT`, `BNBIRT`, `DOGEIRT`, `TRXIRT`, `ADAIRT`, `SOLIRT`, `TONIRT`, `ARBIT`, `APTIRT`, `NEARIRT`, `FILIRT`, `XMRIRT`, etc.
- **USDT pairs**: `BTCUSDT`, `ETHUSDT`, `LTCUSDT`, `XRPUSDT`, `BNBUSDT`, `DOGEUSDT`, `SOLUSDT`, `ARBUSDT`, `TONUSDT`, `NEARUSDT`, `FILUSDT`, `XMRUSDT`, etc.

---

## Examples

### Basic fetch

Save `BTCIRT` 4‑hour candles (10 candles) in the current folder:

```bash
python main.py -symbol BTCIRT -timeframe 4h -candles 10
```

Output file: `BTCIRT-1405-05-02-17-48-27.json`

### Specify output directory (absolute)

```bash
python main.py -symbol BTCUSDT -timeframe 1h -candles 50 -output C:\Users\Shayan\Desktop\price_data
```

### Relative output directory

```bash
python main.py -symbol ETHIRT -timeframe D -candles 30 -output ..\data
```

---

## Output Format

The JSON file contains a **list** of objects. Each object represents one candle:

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

- `time` – Unix timestamp in **milliseconds** (13 digits).
- All numeric values are floats or integers (no string quotes).

---

## How It Works

1. The script builds a request to the Nobitex public API endpoint:  
   `https://apiv2.nobitex.ir/market/udf/history`
2. It sends the `symbol`, `resolution`, and `countback` parameters (or `to` and `from` for pagination; here we use `countback` for simplicity).
3. The response is parsed; if `s` is `"ok"`, the OHLC arrays are extracted.
4. Each candle is formatted as a dictionary and collected into a list.
5. The file name is generated using the current Jalali date (converted from Gregorian) and time, replacing `:` and `/` with `-` for filesystem safety.
6. If an output directory is given, it is created (if missing) and the file is saved there.

---

## Error Handling

- **API errors** – e.g., invalid symbol or resolution → script exits with an error message.
- **No data** – if the API returns `s: "no_data"`, the script exits.
- **Network issues** – a descriptive error is printed.
- **File system errors** – e.g., permission denied or invalid path → script exits.

---

## Notes

- The Nobitex API limits each request to **500 candles**. If `-candles` exceeds 500, the script will still request 500 (the API caps it automatically), but it’s better to keep it within the limit.
- The public API does **not** require an API key.
- Rate limit: **60 requests per minute** (per IP).
- Minute candles before March 2023 (start of year 1401) are not available.

---

## License

This script is provided “as is” without warranty of any kind. You may use and modify it freely for personal or commercial use.
