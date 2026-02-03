from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from graph.graph_builder import app as graph_app

app = FastAPI(title="Startup Idea Evaluator")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IdeaRequest(BaseModel):
    raw_idea: str

class IdeaResponse(BaseModel):
    final_score: int
    metric_scores: dict
    swot_analysis: dict

@app.post("/evaluate", response_model=IdeaResponse)
async def evaluate_idea(request: IdeaRequest):
    try:
        # Invoke the LangGraph app
        final_state = graph_app.invoke({"raw_idea": request.raw_idea})
        
        return {
            "final_score": final_state.get("final_score", 0),
            "metric_scores": final_state.get("metric_scores", {}),
            "swot_analysis": final_state.get("swot_analysis", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
