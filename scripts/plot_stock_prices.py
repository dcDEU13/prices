"""Plot the three repository stocks as percent changes since 2024."""

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from prices import TICKERS, load_prices

ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = ROOT / "figures"
OUTPUT = FIGURES_DIR / "stock_prices_since_2024.png"

STOCKS = {
    "AAPL": ("Apple", "#2563eb"),
    "NVDA": ("NVIDIA", "#16a34a"),
    "ULVR.L": ("Unilever", "#9333ea"),
}


def main() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 6.5), constrained_layout=True)

    for ticker in TICKERS:
        company, color = STOCKS[ticker]
        prices = load_prices(ticker)
        prices = prices.loc[prices.index >= "2024-01-01"]
        adjusted_close = prices["Adj Close"]
        percent_change = (adjusted_close / adjusted_close.iloc[0] - 1) * 100
        ax.plot(
            prices.index,
            percent_change,
            label=f"{company} ({ticker})",
            color=color,
            linewidth=1.6,
        )

    ax.axhline(0, color="#6b7280", linewidth=0.8)
    ax.set_title("Stock Price Change Since 2024", fontsize=16, fontweight="bold")
    ax.set_ylabel("Change in adjusted close (%)")
    ax.set_xlabel("Date")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.grid(True, color="#d1d5db", linewidth=0.7, alpha=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.text(
        0.5,
        -0.02,
        "Each series is indexed to its first available trading day on or after 1 Jan 2024. "
        "Adjusted close; source: repository Yahoo Finance data.",
        ha="center",
        fontsize=9,
        color="#4b5563",
    )
    fig.savefig(OUTPUT, dpi=180, bbox_inches="tight", facecolor="white")
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
