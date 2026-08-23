import re
from fastapi import HTTPException, status

PROMPT_INJECTION_PATTERNS = [
    r"(?i)ignore\s+(previous|all)\s+instructions",
    r"(?i)system\s+override",
    r"(?i)you\s+are\s+now\s+dan",
    r"(?i)reveal\s+(system\s+prompt|api\s+key|internal\s+state)",
    r"(?i)sudo\s+mode",
]

def sanitize_and_guard_input(user_query: str) -> str:
    """Zero-Trust input validation and prompt-injection detection."""
    clean_query = user_query.strip()
    
    if len(clean_query) < 3 or len(clean_query) > 2000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload constraint violation: Query length must be between 3 and 2000 characters."
        )
        
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, clean_query):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Security Violation: Hostile prompt injection heuristic triggered."
            )
            
    return clean_query
  
