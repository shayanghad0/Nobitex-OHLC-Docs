#!/usr/bin/env python3
"""
Nobitex OHLC data fetcher.

Usage:
    python main.py -symbol BTCIRT -timeframe 4h -candles 35

Exports JSON: {symbol}-{jalali_date}-{time}.json (with safe characters).
"""

import argparse
import json
import requests
import datetime
import sys
import re

# ---------- Reliable Jalali (Solar Hijri) conversion ----------
def gregorian_to_jalali(gy, gm, gd):
    """
    Convert Gregorian date to Jalali (Solar Hijri) date.
    Returns (jy, jm, jd) as integers.
    Algorithm from: https://github.com/babakataie/jalali-python
    """
    # Normalize to days since 0001-01-01 (Gregorian)
    g_days = 0
    for y in range(1, gy):
        g_days += 366 if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0) else 365
    month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for m in range(1, gm):
        g_days += month_days[m]
        if m == 2 and ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
            g_days += 1
    g_days += gd

    # Days from 1 Farvardin 1 (622-03-21 Gregorian) = g_days - offset
    # Offset: days from 0001-01-01 to 622-03-21
    offset = 0
    for y in range(1, 622):
        offset += 366 if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0) else 365
    offset += 31 + 28 + 21  # days up to March 21, 622
    # Actually March 21 is day 80 of year (31+28+21)
    jalali_days = g_days - offset

    if jalali_days <= 0:
        # Handle years before 622, but we don't need that here
        return 0, 0, 0

    # Calculate Jalali year
    jy = 1
    while True:
        # Jalali leap years are years that (year-1)%4 == 3
        days_in_year = 366 if (jy - 1) % 4 == 3 else 365
        if jalali_days > days_in_year:
            jalali_days -= days_in_year
            jy += 1
        else:
            break

    # Calculate Jalali month and day
    months = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
    if (jy - 1) % 4 == 3:
        months[11] = 30
    jm = 1
    for days_in_month in months:
        if jalali_days > days_in_month:
            jalali_days -= days_in_month
            jm += 1
        else:
            break
    jd = jalali_days

    return jy, jm, jd

# ---------- Command line argument parsing ----------
def parse_args():
    parser = argparse.ArgumentParser(description='Fetch OHLC data from Nobitex API.')
    parser.add_argument('-symbol', required=True, help='Trading symbol, e.g., BTCIRT, BTCUSDT')
    parser.add_argument('-timeframe', required=True, help='Timeframe: e.g., 1m, 5m, 15m, 30m, 1h, 3h, 4h, 6h, 12h, D, 2D, 3D')
    parser.add_argument('-candles', required=True, type=int, help='Number of candles to fetch (max 500)')
    return parser.parse_args()

# ---------- Map user timeframe to API resolution ----------
def map_timeframe(tf):
    tf = tf.strip().lower()
    mapping = {
        '1m': '1', '5m': '5', '15m': '15', '30m': '30',
        '1h': '60', '3h': '180', '4h': '240', '6h': '360', '12h': '720',
        'd': 'D', '1d': '1D', '2d': '2D', '3d': '3D'
    }
    if tf in mapping:
        return mapping[tf]
    if tf in ['1', '5', '15', '30', '60', '180', '240', '360', '720', 'D', '1D', '2D', '3D']:
        return tf
    if tf.isdigit():
        return tf
    print(f"Error: Unrecognized timeframe '{tf}'.", file=sys.stderr)
    print("Supported: 1m, 5m, 15m, 30m, 1h, 3h, 4h, 6h, 12h, D, 2D, 3D", file=sys.stderr)
    sys.exit(1)

# ---------- Main ----------
def main():
    args = parse_args()
    symbol = args.symbol.upper()
    timeframe = args.timeframe
    candles = args.candles

    if candles < 1:
        print("Error: candles must be positive.", file=sys.stderr)
        sys.exit(1)
    if candles > 500:
        print("Warning: API returns at most 500 candles. Requesting more may result in only 500.", file=sys.stderr)

    resolution = map_timeframe(timeframe)

    # Current time as Unix timestamp
    to_timestamp = int(datetime.datetime.now().timestamp())

    # Build URL
    base_url = "https://apiv2.nobitex.ir/market/udf/history"
    params = {
        "symbol": symbol,
        "resolution": resolution,
        "to": to_timestamp,
        "countback": candles
    }

    headers = {
        "Accept": "application/json",
        "User-Agent": "TraderBot/OHLC-Fetcher-1.0"
    }

    try:
        resp = requests.get(base_url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    status = data.get("s")

    if status == "error":
        errmsg = data.get("errmsg", "Unknown error")
        print(f"API error: {errmsg}", file=sys.stderr)
        sys.exit(1)
    elif status == "no_data":
        print("No data found for the given parameters.", file=sys.stderr)
        sys.exit(1)
    elif status != "ok":
        print(f"Unexpected response status: {status}", file=sys.stderr)
        sys.exit(1)

    t_list = data.get("t", [])
    o_list = data.get("o", [])
    h_list = data.get("h", [])
    l_list = data.get("l", [])
    c_list = data.get("c", [])
    v_list = data.get("v", [])

    length = len(t_list)
    if not (len(o_list) == len(h_list) == len(l_list) == len(c_list) == len(v_list) == length):
        print("Error: Inconsistent data lengths from API.", file=sys.stderr)
        sys.exit(1)

    output = {
        "time": t_list,
        "open": o_list,
        "high": h_list,
        "low": l_list,
        "close": c_list,
        "volume": v_list
    }

    # Generate filename with Jalali date and time, sanitized for filesystem
    now = datetime.datetime.now()
    jy, jm, jd = gregorian_to_jalali(now.year, now.month, now.day)
    # Format: YYYY/MM/DD but replace '/' with '-' for safety
    jdate_str = f"{jy:04d}-{jm:02d}-{jd:02d}"   # now safe
    # Time: HH:MM:SS, replace ':' with '-'
    jtime_str = now.strftime("%H-%M-%S")

    filename = f"{symbol}-{jdate_str}-{jtime_str}.json"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Data exported to {filename}")
    except IOError as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()