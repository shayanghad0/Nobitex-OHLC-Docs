#!/usr/bin/env python3
"""
Nobitex OHLC data fetcher.

Usage:
    python main.py -symbol BTCIRT -timeframe 4h -candles 35

This script fetches OHLC (Open, High, Low, Close, Volume) data from Nobitex API
and exports it to a JSON file named as:
    {symbol}-{jalali_date}-{time}.json
where jalali_date is in format YYYY/MM/DD and time is HH:MM:SS.
"""

import argparse
import json
import requests
import datetime
import sys
import re

# ---------- Jalali (Solar Hijri) calendar conversion ----------
# Based on an algorithm commonly used in Python.
# Returns (jy, jm, jd) from Gregorian (gy, gm, gd)
def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if gy > 1600:
        gy2 = gy - 1600
    else:
        gy2 = gy - 621
    days = gy2 * 365 + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400)
    days += g_d_m[gm - 1] + gd
    if gm > 2 and ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        days += 1
    days -= 78  # days until March 21, year 1 (Farvardin 1)
    jy = 1
    jm = 1
    jd = 1
    while True:
        jy += 1
        if (jy - 1) % 4 == 3:
            days_in_year = 366
        else:
            days_in_year = 365
        if days > days_in_year:
            days -= days_in_year
        else:
            break
    months = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
    if (jy - 1) % 4 == 3:
        months[11] = 30
    for i in range(12):
        if days > months[i]:
            days -= months[i]
        else:
            jm = i + 1
            jd = days
            break
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
    # Normalize: remove spaces, lowercase
    tf = tf.strip().lower()
    # Map known formats
    mapping = {
        '1m': '1',
        '5m': '5',
        '15m': '15',
        '30m': '30',
        '1h': '60',
        '3h': '180',
        '4h': '240',
        '6h': '360',
        '12h': '720',
        'd': 'D',
        '1d': '1D',
        '2d': '2D',
        '3d': '3D'
    }
    if tf in mapping:
        return mapping[tf]
    # If numeric like "60" (minutes) or "D" directly, accept
    if tf in ['1', '5', '15', '30', '60', '180', '240', '360', '720', 'D', '1D', '2D', '3D']:
        return tf
    # Try to parse as number of minutes (e.g., "240")
    if tf.isdigit():
        return tf
    # Not recognized
    print(f"Error: Unrecognized timeframe '{tf}'.", file=sys.stderr)
    print("Supported: 1m, 5m, 15m, 30m, 1h, 3h, 4h, 6h, 12h, D, 2D, 3D", file=sys.stderr)
    sys.exit(1)

# ---------- Main ----------
def main():
    args = parse_args()
    symbol = args.symbol.upper()
    timeframe = args.timeframe
    candles = args.candles

    # Validate candles
    if candles < 1:
        print("Error: candles must be positive.", file=sys.stderr)
        sys.exit(1)
    if candles > 500:
        print("Warning: API returns at most 500 candles. Requesting more may result in only 500.", file=sys.stderr)

    # Map timeframe
    resolution = map_timeframe(timeframe)

    # Get current time (Unix timestamp)
    to_timestamp = int(datetime.datetime.now().timestamp())

    # Build URL
    base_url = "https://apiv2.nobitex.ir/market/udf/history"
    params = {
        "symbol": symbol,
        "resolution": resolution,
        "to": to_timestamp,
        "countback": candles
    }

    # Make request
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

    # Check response status
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

    # Extract OHLC data
    # Note: API returns lists of numbers
    t_list = data.get("t", [])
    o_list = data.get("o", [])
    h_list = data.get("h", [])
    l_list = data.get("l", [])
    c_list = data.get("c", [])
    v_list = data.get("v", [])

    # Ensure all lists have same length
    length = len(t_list)
    if not (len(o_list) == len(h_list) == len(l_list) == len(c_list) == len(v_list) == length):
        print("Error: Inconsistent data lengths from API.", file=sys.stderr)
        sys.exit(1)

    # Build output dictionary with descriptive keys
    output = {
        "time": t_list,
        "open": o_list,
        "high": h_list,
        "low": l_list,
        "close": c_list,
        "volume": v_list
    }

    # Prepare filename with Jalali date and time
    now = datetime.datetime.now()
    gy, gm, gd = now.year, now.month, now.day
    jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
    # Format date: YYYY/MM/DD (with leading zeros for month/day)
    jdate_str = f"{jy:04d}/{jm:02d}/{jd:02d}"
    # Format time: HH:MM:SS
    jtime_str = now.strftime("%H:%M:%S")

    # Sanitize filename: replace ':' with '-' to avoid issues on Windows
    # But the spec says hh:mm:ss, so we keep colon; it's usually fine.
    filename = f"{symbol}-{jdate_str}-{jtime_str}.json"

    # Write JSON file
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Data exported to {filename}")
    except IOError as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()