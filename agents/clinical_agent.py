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
def clinical_trial_agent(molecule: str, country: str):
    """
    Mock Clinical Trials Agent:
    Simulates fetching active clinical trials and sponsor information
    for a given molecule in a specific country.
    Returns structured mock results with reasoning summary.
    """
    seed_str = (molecule + country).lower()
    random.seed(hash(seed_str) % 1000)
    total_trials = random.randint(3, 10)
    phases = ["Phase I", "Phase II", "Phase III"]
    sponsors = random.sample(
        ["Pfizer", "Cipla", "Sun Pharma", "GSK", "Dr. Reddy’s", "Novartis", "AstraZeneca"], 4
    )
    phase_distribution = {
        "Phase I": random.randint(1, 3),
        "Phase II": random.randint(1, 3),
        "Phase III": random.randint(1, 2),
    }
    trials = []
    for i in range(total_trials):
        trials.append({
            "trial_id": f"CT-{random.randint(100, 999)}",
            "phase": random.choice(phases),
            "sponsor": random.choice(sponsors),
            "status": random.choice(["Recruiting", "Active", "Completed"]),
        })
    reasoning = (
        f"For molecule '{molecule}' in {country}, approximately {total_trials} "
        f"ongoing or completed clinical trials were simulated. The majority are in "
        f"{max(phase_distribution, key=phase_distribution.get)}, with key sponsors including "
        f"{', '.join(sponsors[:3])}. This suggests a healthy and diverse R&D pipeline "
        f"focusing on multi-phase development efforts."
    )
    return {
        "molecule": molecule,
        "country": country,
        "total_trials": total_trials,
        "phase_distribution": phase_distribution,
        "sponsors": sponsors,
        "trial_details": trials,
        "reasoning_summary": reasoning,
        "mock": True,
    }

clinical_agent = Agent(model=model, tools=[clinical_trial_agent])