# order_book
# Live Order Book Terminal Visualizer

This Python script connects to the Binance exchange to visualize the live order book for a given cryptocurrency trading pair. It prints the top bids and asks in the terminal with colored formatting for easy readability.

---

## Features

* Fetches initial order book snapshot using Binance REST API.
* Receives live incremental updates via Binance WebSocket (`@depth@100ms`).
* Displays top bids and asks in the terminal with color coding.
* Updates the display every second, clearing the terminal for a live visualization effect.
* Adjustable number of top levels to display (`depth_levels`).

---

## Requirements

* Python 3.8+
* Libraries:

  ```bash
  pip install requests websockets
  ```

---

## Files

* `order_book.py` : Main script for live order book visualization in terminal.

---

## Usage

1. Open `order_book.py` in your editor.
2. Optionally, change the `symbol` variable to a different trading pair (default is `BTCUSDT`).
3. Run the script:

   ```bash
   python order_book.py
   ```
4. The terminal will display the top bids and asks every second, with bids in green and asks in red.

---

## How It Works

1. **REST Snapshot:** Fetches the full current order book via REST API to initialize `bids` and `asks`.
2. **WebSocket Updates:** Connects to Binance WebSocket for incremental updates and updates the local order book accordingly.
3. **Top Depth Extraction:** The `top_depth()` function sorts bids in descending order and asks in ascending order, selecting the top `depth_levels` entries.
4. **Terminal Display:** Prints bids (green) and asks (red) with aligned columns and clears the terminal each second for a real-time effect.

---

## Customization

* `depth_levels` : Number of top levels displayed (default: 5).
* ANSI color codes (`GREEN`, `RED`) can be modified for different terminal color preferences.
* Update interval can be adjusted by changing the `if now - last_print >= 1` condition.

---

## Notes

* This script is intended for **learning and visualization purposes** only.
* Terminal must support ANSI escape codes for colored output.
* Frequent WebSocket messages from Binance are throttled in display by showing only top levels and updating once per second.

---

## License

MIT License
