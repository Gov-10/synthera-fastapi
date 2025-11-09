from fastapi import FastAPI, HTTPException
from schema import IqviaIn, IqviaOut, ClinicalIn, ClinicalOut
from agents.agent import agent
from agents.clinical_agent import clinical_agent
import random

app = FastAPI(title="Synthera Mock Agents (MOCK DATA ONLY)")

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


@app.post("/clinical_agent",response_model= ClinicalOut)
def clinical_route(payload: ClinicalIn):
    try:
        query = f"Generate mock data for Clinical Trials, Sponsor profiles, Trial Phase Distributions for {payload.molecule} in {payload.country}"
        result = clinical_agent(query)
        reasoning_summary = ""
        try:
            reasoning_summary = result.message["content"][0]["text"]
        except Exception:
            reasoning_summary = "No reasoning text returned by the model."
        random.seed(hash((payload.molecule + payload.country).lower()) % 1000)
        total_trials = random.randint(3, 10)
        phase_distribution = {
            "Phase I": random.randint(1, 3),
            "Phase II": random.randint(1, 3),
            "Phase III": random.randint(1, 2)
        }
        sponsors = random.sample(
            ["Pfizer", "Cipla", "Sun Pharma", "GSK", "Dr. Reddy’s", "Novartis", "AstraZeneca"],
            4
        )
        trials = [
            {
                "trial_id": f"CT-{random.randint(100, 999)}",
                "phase": random.choice(["Phase I", "Phase II", "Phase III"]),
                "sponsor": random.choice(sponsors),
                "status": random.choice(["Recruiting", "Active", "Completed"])
            }
            for _ in range(total_trials)
        ]
        return {
            "molecule": payload.molecule, 
            "country": payload.country, 
            "total_trials" : total_trials, 
            "phase_distribution": phase_distribution,
            "sponsors": sponsors,
            "trial_details": trials,
            "reasoning_summary": reasoning_summary,
            "mock": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {e}")



