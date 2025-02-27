from fastapi import FastAPI
from pydantic import BaseModel
from fact_checker import check_fact
from bias_analysis import analyse_bias

app = FastAPI()

# ✅ Define a Pydantic model for the request body
class AnalyseRequest(BaseModel):
    content: str

@app.on_event("startup")
def load_models():
    global fact_checker, bias_analyser
    fact_checker = check_fact
    bias_analyser = analyse_bias
    print("✅ Models loaded successfully!")

@app.get("/")
def home():
    return {"message": "Welcome to the AI Fake News Detector"}

# ✅ Ensure the request body is parsed correctly
@app.post("/analyse/")
def analyse_text(request: AnalyseRequest):  
    credibility = fact_checker(request.content)
    bias = bias_analyser(request.content)
    return {"credibility": credibility, "bias": bias}
