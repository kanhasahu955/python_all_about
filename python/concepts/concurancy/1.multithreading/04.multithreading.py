import requests
from threading import Thread
from time import perf_counter


class Stock(Thread):
    def __init__(self, symbol: str) -> None:
        super().__init__()
        self.symbol = symbol
        self.price = None
        self.error: str | None = None

    def run(self) -> None:
        # HTML from finance.yahoo.com/quote/... does not contain the live fin-streamer nodes
        # (they come from JS). Use the same JSON endpoint the site loads for prices.
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{self.symbol}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        }
        try:
            response = requests.get(
                url,
                params={"interval": "1d", "range": "1d"},
                headers=headers,
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
            results = payload.get("chart", {}).get("result") or []
            if not results:
                self.error = "no chart result"
                return
            meta = results[0].get("meta") or {}
            self.price = meta.get("regularMarketPrice")
            if self.price is None:
                self.error = "no regularMarketPrice"
        except requests.RequestException as exc:
            self.error = str(exc)

    def __str__(self) -> str:
        if self.error:
            return f"{self.symbol}: error — {self.error}"
        return f"{self.symbol}: {self.price}"


symbols = ["MSFT", "GOOGL", "AAPL", "META"]
threads: list[Stock] = []
start = perf_counter()
for symbol in symbols:
    thread = Stock(symbol)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

elapsed = perf_counter() - start
for thread in threads:
    print(thread)
print(f"elapsed: {elapsed:.3f}s")
