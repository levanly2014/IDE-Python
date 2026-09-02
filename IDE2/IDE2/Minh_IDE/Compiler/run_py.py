import subprocess
import sys
import tempfile
import os
import time
from .ast_py import ast_py


def run_py(code, input_data="", time_limit=5.0):
    syntax_error = ast_py(code)
    if syntax_error:
        return {
            "success": False,
            "output": "",
            "error": syntax_error,
            "execution_time": 0
        }

    filename = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as f:
            filename = f.name
            f.write(code)
        start_time = time.perf_counter()
        result = subprocess.run(
            [sys.executable, filename],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=time_limit  
        )
        execution_time = time.perf_counter() - start_time
        if result.returncode != 0:
            return {
                "success": False,
                "output": result.stdout,
                "error": result.stderr,
                "execution_time": execution_time
            }
        return {
            "success": True,
            "output": result.stdout,
            "error": None,
            "execution_time": execution_time
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Time Limit Exceeded",
            "execution_time": time_limit
        }

    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)
