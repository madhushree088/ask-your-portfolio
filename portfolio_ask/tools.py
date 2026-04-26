"""
Deterministic financial calculations.
The LLM is never asked to compute numbers — these functions handle all math.
"""
from portfolio_ask.models import AllocationResponse, PnLResponse, SectorWeight, HoldingPnL


def compute_sector_allocation(holdings: list[dict]) -> AllocationResponse:
    """Compute portfolio weight per sector."""
    sector_values: dict[str, float] = {}
    total = 0.0

    for h in holdings:
        value = h["quantity"] * h["current_price"]
        sector_values[h["sector"]] = sector_values.get(h["sector"], 0) + value
        total += value

    allocation = [
        SectorWeight(sector=s, weight_pct=round(v / total * 100, 2))
        for s, v in sorted(sector_values.items(), key=lambda x: -x[1])
    ]
    return AllocationResponse(allocation=allocation, sources=["portfolio.json"])


def compute_pnl(holdings: list[dict]) -> PnLResponse:
    """Compute P&L for each holding and overall."""
    total_invested = 0.0
    total_current = 0.0
    breakdown = []

    for h in holdings:
        invested = h["quantity"] * h["avg_cost"]
        current = h["quantity"] * h["current_price"]
        pnl = current - invested
        pnl_pct = (pnl / invested) * 100

        total_invested += invested
        total_current += current
        breakdown.append(HoldingPnL(
            ticker=h["ticker"],
            pnl=round(pnl, 2),
            pnl_pct=round(pnl_pct, 2)
        ))

    return PnLResponse(
        total_invested=round(total_invested, 2),
        total_current=round(total_current, 2),
        total_pnl=round(total_current - total_invested, 2),
        holdings=breakdown,
        sources=["portfolio.json"]
    )
