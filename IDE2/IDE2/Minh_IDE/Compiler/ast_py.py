import ast

def ast_py(code):
    try:
        ast.parse(code)
        return 

    except SyntaxError as e:
        return {
            "type": type(e).__name__,                  
            "error": e.msg,
            "line": e.lineno,
            "column": e.offset,
            "text": e.text.strip() if e.text else ""
        }
