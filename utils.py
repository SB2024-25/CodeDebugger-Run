import ast
import io
import tokenize

def has_syntax_error(code: str) -> tuple[bool, str]:
    try:
        compile(code, "<string>", "exec")
        return False, ""
    except SyntaxError as e:
        return True, f"SyntaxError at line {e.lineno}: {e.msg}"

def analyze_ast(code: str) -> list:
    issues = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.If) and isinstance(node.test, ast.Constant):
                if isinstance(node.test.value, bool):
                    issues.append(f"Redundant condition at line {node.lineno}: Always evaluates to {node.test.value}")
            elif isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and node.func.id == 'input':
                    issues.append(f"Potential security issue: Use of 'input()' at line {node.lineno}")
    except Exception as e:
        issues.append(f"AST parsing error: {str(e)}")
    return issues