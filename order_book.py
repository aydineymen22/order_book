import asyncio
import websockets
import requests
import json
import time

symbol = "BTCUSDT"
depth_levels = 5
bids = {}
asks = {}
last_update_id = None

# --- ANSI color codes ---
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def apply_updates(book, updates):
    for price, qty in updates:
        p, q = float(price), float(qty)
        if q == 0.0:
            book.pop(p, None)
        else:
            book[p] = q

def top_depth(levels=depth_levels):
    top_bids = sorted(bids.items(), key=lambda x: -x[0])[:levels]
    top_asks = sorted(asks.items(), key=lambda x: x[0])[:levels]
    return top_bids, top_asks

def get_snapshot():
    global bids, asks, last_update_id
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=1000"
    snapshot = requests.get(url).json()
    last_update_id = snapshot["lastUpdateId"]
    bids.update({float(p): float(q) for p, q in snapshot["bids"]})
    asks.update({float(p): float(q) for p, q in snapshot["asks"]})
    print(f"Got snapshot with lastUpdateId = {last_update_id}")

async def stream_depth():
    global last_update_id
    uri = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@depth@100ms"
    last_print = 0

    async with websockets.connect(uri) as ws:
        async for msg in ws:
            data = json.loads(msg)
            apply_updates(bids, data["b"])
            apply_updates(asks, data["a"])

            now = time.time()
            if now - last_print >= 1:
                top_bids, top_asks = top_depth()
                
                print("\033c", end="")

                print(f"===== {symbol} Order Book Top {depth_levels} =====")
                
                print(f"{GREEN}Bids (Price | Quantity){RESET}")
                for price, qty in top_bids:
                    print(f"{GREEN}{price:10.2f} | {qty:10.4f}{RESET}")
                
                print(f"{RED}Asks (Price | Quantity){RESET}")
                for price, qty in top_asks:
                    print(f"{RED}{price:10.2f} | {qty:10.4f}{RESET}")
                
                last_print = now

def main():
    get_snapshot()
    asyncio.run(stream_depth())

if __name__ == "__main__":
    main()
