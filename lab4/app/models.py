from pydantic import BaseModel, Field
from typing import Optional

class SummarizeRequest(BaseModel):
    # Enforces that text is non-empty and required
    text: str = Field(..., min_length=1, description="The text to summarize.")
    # Optional field with a default value of 100
    max_length: Optional[int] = Field(default=100, gt=0)

class SummarizeResponse(BaseModel):
    summary: str
    model: str
    truncated: bool
