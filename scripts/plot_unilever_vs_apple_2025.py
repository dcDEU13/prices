"""Plot Apple and Unilever's adjusted-price changes during 2025."""

from pathlib import Path
from datetime import date

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from prices import load_prices

ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = ROOT / "figures"
OUTPUT = FIGURES_DIR / "unilever_vs_apple_2025.png"

STOCKS = {
    "AAPL": ("Apple", "#2563eb"),
    "ULVR.L": ("Unilever", "#9333ea"),
}


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 6.5), constrained_layout=True)

    for ticker, (company, color) in STOCKS.items():
        prices = load_prices(ticker).loc["2025-01-01":"2025-12-31"]
        adjusted_close = prices["Adj Close"]
        percent_change = (adjusted_close / adjusted_close.iloc[0] - 1) * 100
        ax.plot(
            prices.index,
            percent_change,
            label=f"{company} ({ticker})",
            color=color,
            linewidth=1.8,
        )

    ax.axhline(0, color="#6b7280", linewidth=0.8)
    ax.set_title("Apple vs Unilever in 2025", fontsize=16, fontweight="bold")
    ax.set_ylabel("Change in adjusted close since first 2025 trading day (%)")
    ax.set_xlabel("Date")
    ax.set_xlim(date(2025, 1, 1), date(2025, 12, 31))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.grid(True, color="#d1d5db", linewidth=0.7, alpha=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.text(
        0.5,
        -0.02,
        "Adjusted close indexed to each stock's first available 2025 trading day; "
        "each series uses its own trading dates. Source: repository Yahoo Finance data.",
        ha="center",
        fontsize=9,
        color="#4b5563",
    )
    fig.savefig(OUTPUT, dpi=180, bbox_inches="tight", facecolor="white")
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
