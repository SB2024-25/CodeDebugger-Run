from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from models import TestCaseResult  # ✅ Import added

def run_test_cases(code: str, test_cases: list) -> list:
    results = []
    # Capture stdout safely
    local_namespace = {}
    try:
        compiled = compile(code, "<string>", "exec")
    except Exception as e:
        for case in test_cases:
            results.append(TestCaseResult(
                input=case["input"],
                expected=case["expected"],
                output="",
                passed=False,
                error=f"Code failed to compile: {str(e)}"
            ))
        return results

    for case in test_cases:
        inp = case["input"]
        expected = case["expected"]
        output = ""
        error = None
        passed = False

        # Simulate input by mocking input()
        def mock_input(prompt=""):
            return inp

        local_namespace['input'] = mock_input

        stdout_capture = StringIO()
        stderr_capture = StringIO()

        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(compiled, local_namespace)
            output = stdout_capture.getvalue().strip()
            error = stderr_capture.getvalue()
            passed = output == expected.strip()
        except Exception as e:
            error = f"Runtime error: {str(e)}"
            output = stderr_capture.getvalue() or str(e)

        results.append(TestCaseResult(
            input=inp,
            expected=expected,
            output=output,
            passed=passed,
            error=error if error else None
        ))

    return results