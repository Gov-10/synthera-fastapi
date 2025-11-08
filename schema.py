from pydantic import BaseModel
from typing import Optional, List
class IqviaIn(BaseModel):
    therapy_area: str
    country: Optional[str] = None
    years_to_consider: Optional[int] = 3

class Competitor(BaseModel):
    company: str
    market_share_pct: float
    estimated_revenue_usd: float

class IqviaOut(BaseModel):
    therapy_area: str
    country: Optional[str]
    market_size_usd: float
    market_year: int
    cagr_pct: float
    top_competitors: List[Competitor]
    reasoning_summary: str
    mock: bool = True