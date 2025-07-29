# debug_engine.py
"""
Core debugging engine for CodeDebugger&Run.
Performs syntax check, AST analysis, linting, test execution, and AI-powered explanations.
"""
import subprocess
import os
from typing import List

# Import your AI explanation module (e.g., gemini_ai, mistral_ai, or perplexity_ai)
from gemini_ai import get_ai_explanation  # Change this to use mistral_ai or perplexity_ai

# Import models
from models import DebugResponse, BugReport, TestCaseResult

# Import utilities
from utils import has_syntax_error, analyze_ast
from test_runner import run_test_cases


def collect_linter_issues(code: str, filename="temp_code.py") -> List[str]:
    """
    Runs flake8 and pylint on the code and returns style/logic issues.
    """
    # Write code to a temporary file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    issues = []

    # Run flake8
    try:
        result = subprocess.run(
            ["flake8", filename],
            capture_output=True,
            text=True,
            timeout=10,
            encoding="utf-8"
        )
        if result.stdout:
            for line in result.stdout.splitlines():
                issues.append(f"Style: {line}")
    except FileNotFoundError:
        issues.append("Linter: flake8 not installed. Run 'pip install flake8'")
    except Exception as e:
        issues.append(f"Linter error (flake8): {str(e)}")

    # Run pylint
    try:
        result = subprocess.run(
            ["pylint", filename, "--errors-only"],
            capture_output=True,
            text=True,
            timeout=15,
            encoding="utf-8"
        )
        if result.stdout:
            for line in result.stdout.splitlines():
                if "********" not in line and line.strip():
                    issues.append(f"Logic/Design: {line}")
    except FileNotFoundError:
        issues.append("Linter: pylint not installed. Run 'pip install pylint'")
    except Exception as e:
        issues.append(f"Linter error (pylint): {str(e)}")

    # Clean up
    try:
        os.remove(filename)
    except:
        pass

    return issues


def debug_code(request_data) -> DebugResponse:
    """
    Main debugging function.
    Takes user code and test cases, returns full debug report with AI explanations.
    """
    code = request_data.code
    test_cases = request_data.test_cases or []

    # Step 1: Check for syntax errors
    has_syntax, syntax_msg = has_syntax_error(code)
    if has_syntax:
        ai_suggestion = get_ai_explanation(f"Syntax Error: {syntax_msg}")
        return DebugResponse(
            success=False,
            syntax_error=syntax_msg,
            ast_analysis=[],
            linter_issues=[],
            test_results=[],
            bug_explanations=[
                BugReport(line=0, type="syntax", message=syntax_msg, suggestion=ai_suggestion)
            ],
            ai_suggestions=ai_suggestion
        )

    # Step 2: AST Analysis
    ast_issues = analyze_ast(code)

    # Step 3: Linter Issues
    linter_issues = collect_linter_issues(code)

    # Step 4: Run Test Cases
    test_results = run_test_cases(code, test_cases)

    # Step 5: Compile bug summary for AI
    bug_summary = "\n".join(
        [f"AST: {issue}" for issue in ast_issues] +
        [f"Linter: {issue}" for issue in linter_issues] +
        [
            f"Test Fail: Input '{t.input}' → Expected '{t.expected}', Got '{t.output}'"
            for t in test_results if not t.passed
        ]
    )

    if not bug_summary.strip():
        bug_summary = "No bugs found. The code appears correct and passes all tests."

    # Step 6: Get AI Explanation from Gemini (or Mistral/Perplexity)
    ai_suggestions = get_ai_explanation(bug_summary)

    # Step 7: Format bug reports
    bug_reports = []
    for issue in ast_issues:
        bug_reports.append(BugReport(line=0, type="logic", message=issue, suggestion=ai_suggestions))
    for issue in linter_issues:
        bug_reports.append(BugReport(line=0, type="style", message=issue, suggestion="Follow PEP8 and best practices."))

    # Check if all tests passed
    all_tests_passed = all(t.passed for t in test_results) if test_results else True
    success = all_tests_passed and not ast_issues and not linter_issues

    return DebugResponse(
        success=success,
        syntax_error=None,
        ast_analysis=ast_issues,
        linter_issues=linter_issues,
        test_results=test_results,
        bug_explanations=bug_reports,
        ai_suggestions=ai_suggestions
    )