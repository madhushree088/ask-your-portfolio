from pydantic import BaseModel
from typing import List


class SectorWeight(BaseModel):
    sector: str
    weight_pct: float


class AllocationResponse(BaseModel):
    allocation: List[SectorWeight]
    sources: List[str]


class HoldingPnL(BaseModel):
    ticker: str
    pnl: float
    pnl_pct: float


class PnLResponse(BaseModel):
    total_invested: float
    total_current: float
    total_pnl: float
    holdings: List[HoldingPnL]
    sources: List[str]


class GeneralResponse(BaseModel):
    answer: str
    sources: List[str]
