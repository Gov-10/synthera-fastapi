from strands import Agent,tool
from strands.models.gemini import GeminiModel
import requests
import os
import environ
from dotenv import load_dotenv
import random
load_dotenv()
env = environ.Env()
environ.Env.read_env()
model= GeminiModel(
    client_args= {
        "api_key": os.getenv("GEMINI_API_KEY")
    }, 
    model_id= "gemini-2.5-flash", 
    params= {
        "temperature" : 0.4, 
        "max_output_tokens": 2048, 
        "top_p" : 0.9, 
        "top_k" : 40
    }
)
@tool
def iqvia_agent(therapy_area:str, country: str):
    """
    Mock IQVIA Insights Agent:
    Simulates fetching market data for a given therapy area and country.
    Returns structured mock results with reasoning text.
    """
    seed_str = (therapy_area + country).lower()
    random.seed(hash(seed_str) % 1000)
    market_size = random.randint(10, 80) * 1_000_000
    cagr = round(random.uniform(4.0, 15.0), 2)
    competitors = random.sample(
        ["PharmaZen", "Novacare", "Healix", "Medilife", "BioCore", "AstraThera", "CureOn"],
        5
    )
    comp_list = []
    base = 100
    for c in competitors:
        share = round(random.uniform(5, 25), 2)
        base -= share
        comp_list.append({
            "company": c,
            "market_share_pct": share,
            "estimated_revenue_usd": round(market_size * (share / 100), 2)
        })
    reasoning = (
        f"In the {therapy_area} segment of {country}, the simulated data suggests a total "
        f"market size of approximately ${market_size/1_000_000:.1f}M, growing at a "
        f"{cagr}% compound annual growth rate. Key players include "
        f"{', '.join([c['company'] for c in comp_list[:3]])}, with a competitive "
        f"landscape characterized by mid-tier dominance and steady volume expansion."
    )
    return {
        "therapy_area": therapy_area,
        "country": country,
        "market_year": 2024,
        "market_size_usd": market_size,
        "cagr_pct": cagr,
        "top_competitors": comp_list,
        "reasoning_summary": reasoning,
        "mock": True,
    }



agent = Agent(model=model, tools=[iqvia_agent])