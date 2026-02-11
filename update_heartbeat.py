import yfinance as yf
from datetime import datetime
import re

# 监控标的（可自行增删）
symbols = {
    '上证指数': '000001.SS',
    '恒生指数': '^HSI',
    '标普500': '^GSPC'
}

lines = []
for name, sym in symbols.items():
    ticker = yf.Ticker(sym)
    hist = ticker.history(period="1d")
    if not hist.empty:
        price = hist['Close'].iloc[-1]
        change = price - hist['Open'].iloc[-1]
        pct = change / hist['Open'].iloc[-1] * 100
        lines.append(f"| {name} | {price:.2f} | {change:+.2f} | {pct:+.2f}% |")
    else:
        lines.append(f"| {name} | N/A | N/A | N/A |")

table = "| 名称 | 价格 | 涨跌 | 涨跌幅 |\n|------|------|------|--------|\n"
table += "\n".join(lines)

with open("HEARTBEAT.md", "r", encoding="utf-8") as f:
    content = f.read()

today = datetime.now().strftime("%Y-%m-%d %H:%M")
new_content = re.sub(r'{{ date }}', today, content)
new_content = re.sub(r'{{ content }}', table, new_content)

with open("HEARTBEAT.md", "w", encoding="utf-8") as f:
    f.write(new_content)
