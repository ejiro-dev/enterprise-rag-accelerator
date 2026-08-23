from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.guardrails import sanitize_and_guard_input
from app.rag_engine import ProductionRAGEngine

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Enterprise RAG Solution Accelerator",
    version="1.0.0",
    description="Production-ready FDE blueprint with OpenTelemetry, Rate Limiting, and Input Guardrails."
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

FastAPIInstrumentor.instrument_app(app)
rag_engine = ProductionRAGEngine()

class QueryRequest(BaseModel):
    query: str = Field(..., example="What are the security requirements for enterprise FDE deployments?")

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
    telemetry: dict

@app.get("/healthz", status_code=200)
async def health_check():
    return {"status": "healthy", "service": "enterprise-rag-accelerator"}

@app.post("/api/v1/query", response_model=QueryResponse)
@limiter.limit("20/minute")
async def execute_query(request: Request, payload: QueryRequest):
    sanitized_query = sanitize_and_guard_input(payload.query)
    result = rag_engine.query(sanitized_query)
    return result
  
