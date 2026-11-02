import json
import datetime
import yfinance as yf

# 監控標的清單（涵蓋 NVDA、TSLA、MU、INTC、GOOG）
TICKERS = ["NVDA", "TSLA", "MU", "INTC", "GOOG"]

def fetch_latest_data():
    results = {}
    current_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    for symbol in TICKERS:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d", interval="1d")
            
            if hist.empty:
                print(f"[警告] 無法取得 {symbol} 行情數據")
                continue
                
            latest = hist.iloc[-1]
            prev_close = hist.iloc[-2]['Close'] if len(hist) >= 2 else latest['Open']
            
            close_price = round(float(latest['Close']), 2)
            high_price = round(float(latest['High']), 2)
            low_price = round(float(latest['Low']), 2)
            prev_close_price = round(float(prev_close), 2)
            change_pct = round(((close_price - prev_close_price) / prev_close_price) * 100, 2)
            date_str = hist.index[-1].strftime("%Y-%m-%d")
            
            results[symbol] = {
                "c": close_price,
                "h": high_price,
                "l": low_price,
                "pc": prev_close_price,
                "dp": change_pct,
                "dateStr": date_str,
                "sourceName": f"Yahoo Finance 每日排程抓取 ({date_str})"
            }
            print(f"[成功] {symbol}: 收盤 ${close_price}, 漲跌 {change_pct}% ({date_str})")
        except Exception as e:
            print(f"[錯誤] 處理 {symbol} 失敗: {str(e)}")

    output_payload = {
        "updated_at": current_utc,
        "quotes": results
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output_payload, f, ensure_ascii=False, indent=2)
    print("data.json 輸出完成。")

if __name__ == "__main__":
    fetch_latest_data()
