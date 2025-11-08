from fastapi import FastAPI, HTTPException
from schema import IqviaIn, IqviaOut
from agents.agent import agent

app = FastAPI(title="IQVIA Mock Agent API")

@app.post("/iqvia", response_model=IqviaOut)
def iqvia_agent(payload: IqviaIn):
    try:
        query = (
            f"Generate mock IQVIA-style market insights for the "
            f"{payload.therapy_area} segment in {payload.country}. "
            f"Include estimated market size, CAGR, and key competitors."
        )
        result = agent(query)
        reasoning_summary = ""
        try:
            reasoning_summary = result.message["content"][0]["text"]
        except Exception:
            reasoning_summary = "No reasoning text returned by the model."
        return {
            "therapy_area": payload.therapy_area,
            "country": payload.country,
            "market_year": 2024,
            "market_size_usd": 55_000_000, 
            "cagr_pct": 9.8,
            "top_competitors": [
                {"company": "PharmaZen", "market_share_pct": 14.2, "estimated_revenue_usd": 7810000},
                {"company": "Healix", "market_share_pct": 11.5, "estimated_revenue_usd": 6320000},
                {"company": "Novacare", "market_share_pct": 8.9, "estimated_revenue_usd": 4900000}
            ],
            "reasoning_summary": reasoning_summary,
            "mock": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {e}")
