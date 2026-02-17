from fastapi import FastAPI, HTTPException, Depends
from app.models import SummarizeRequest, SummarizeResponse
from app.summarizer import process_summary, SummarizationError
from app.auth import require_auth

app = FastAPI(title="Summarization Service", version="0.1.0")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(
    request: SummarizeRequest,
    _: None = Depends(require_auth),
):
    try:
        result = process_summary(request.text, request.max_length)
        return result
    except SummarizationError as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": f"Internal Server Error: {str(e)}"})
