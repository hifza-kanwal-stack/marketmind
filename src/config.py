import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("CRITICAL: OPENAI_API_KEY environment variable is missing!")
    
    PLANNER_MODEL = os.getenv("PLANNER_MODEL", "gpt-4o")
    RESEARCHER_MODEL = os.getenv("RESEARCHER_MODEL", "gpt-4o-mini")
    SYNTHESIS_MODEL = os.getenv("SYNTHESIS_MODEL", "gpt-4o")
    QC_MODEL = os.getenv("QC_MODEL", "gpt-4o-mini")
    
    MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "12"))
    MAX_TOOL_CALLS = int(os.getenv("MAX_TOOL_CALLS", "30"))
    BUDGET_CEILING_USD = float(os.getenv("BUDGET_CEILING_USD", "2.00"))

settings = Settings()
