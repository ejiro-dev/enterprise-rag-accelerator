# Enterprise RAG Solution Accelerator

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-Enabled-F5A800.svg?logo=opentelemetry)](https://opentelemetry.io/)
[![Zero-Trust](https://img.shields.io/badge/Security-Zero--Trust_Guardrails-blue.svg)](ARCH_DIAGRAM.md)

Production-ready Reference Architecture for Enterprise Retrieval-Augmented Generation (RAG) workloads. Built for Forward Deployed Engineering (FDE) scenarios requiring high reliability, sub-200ms hybrid retrieval, and automated quality evaluation harnesses.

---

## Core Capabilities

* **Hybrid Search Engine:** Dense vector embeddings coupled with sparse BM25 retrieval for high-precision context extraction.
* **Zero-Trust Guardrails:** Pre-retrieval regular expression and payload filtering to block prompt injection before model inference.
* **Built-in Observability:** Native OpenTelemetry instrumentation for distributed request tracing and token-usage telemetry.
* **Automated Evaluation Harness:** Deterministic benchmark suite to score answer relevancy and flag hallucination risks.

---

## Quickstart

```bash
# Clone the repository
git clone [https://github.com/ejiro-dev/enterprise-rag-accelerator.git](https://github.com/ejiro-dev/enterprise-rag-accelerator.git)
cd enterprise-rag-accelerator

# Run full stack with Docker Compose
docker-compose up --build

