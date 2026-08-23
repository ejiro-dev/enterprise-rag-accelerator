import os
import json
from typing import List, Dict, Any
from openai import AzureOpenAI, OpenAI
from opentelemetry import trace

tracer = trace.get_tracer("enterprise.rag.engine")

class ProductionRAGEngine:
    def __init__(self):
        # Configure client (defaults to standard OpenAI or Azure OpenAI via env vars)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "mock-key"))
        self.model = os.getenv("LLM_DEPLOYMENT_NAME", "gpt-4o")

    def _mock_hybrid_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Simulates hybrid vector search with BM25 keyword matching."""
        return [
            {
                "id": "doc_001",
                "content": "Microsoft Forward Deployed Engineers (FDEs) embed with enterprise customers to build scalable cloud architectures.",
                "relevance_score": 0.94
            },
            {
                "id": "doc_002",
                "content": "Enterprise RAG solutions require strict OpenTelemetry instrumentation and input sanitization layers.",
                "relevance_score": 0.88
            }
        ]

    def query(self, user_query: str) -> Dict[str, Any]:
        with tracer.start_as_current_span("rag_retrieval_and_synthesis") as span:
            span.set_attribute("query.text", user_query)
            
            # 1. Retrieval Phase
            with tracer.start_as_current_span("vector_retrieval"):
                retrieved_docs = self._mock_hybrid_search(user_query)
                span.set_attribute("retrieval.documents_found", len(retrieved_docs))

            context_str = "\n".join([f"- {doc['content']}" for doc in retrieved_docs])

            # 2. Synthesis Phase
            system_prompt = (
                "You are an enterprise AI assistant. Answer the user query strictly using the provided context. "
                "If the context is insufficient, explicitly state that information is unavailable.\n\n"
                f"Context:\n{context_str}"
            )

            with tracer.start_as_current_span("llm_inference"):
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query}
                    ],
                    temperature=0.0,
                    max_tokens=300
                )
                
            generated_text = response.choices[0].message.content
            span.set_attribute("llm.completion_tokens", response.usage.completion_tokens)

            return {
                "answer": generated_text,
                "sources": [doc["id"] for doc in retrieved_docs],
                "telemetry": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens
                }
            }


