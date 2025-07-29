from pydantic import BaseModel
from typing import List, Optional

class DebugRequest(BaseModel):
    code: str
    test_cases: Optional[List[dict]] = None  # [{"input": "...", "expected": "..."}, ...]

class TestCaseResult(BaseModel):
    input: str
    expected: str
    output: str
    passed: bool
    error: Optional[str] = None

class BugReport(BaseModel):
    line: int
    type: str  # "syntax", "logic", "style", "runtime"
    message: str
    suggestion: str

class DebugResponse(BaseModel):
    success: bool
    syntax_error: Optional[str] = None
    ast_analysis: List[str]
    linter_issues: List[str]
    test_results: List[TestCaseResult]
    bug_explanations: List[BugReport]
    ai_suggestions: str