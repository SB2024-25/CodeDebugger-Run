from fastapi import FastAPI, HTTPException
from models import DebugRequest, DebugResponse
from debug_engine import debug_code

app = FastAPI(title="CodeDebugger&Run Backend")

@app.post("/debug", response_model=DebugResponse)
async def debug_endpoint(request: DebugRequest):
    try:
        result = debug_code(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.get("/")
def home():
    return {"message": "Welcome to CodeDebugger&Run! POST to /debug to analyze code."}