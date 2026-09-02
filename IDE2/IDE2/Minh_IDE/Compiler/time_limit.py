import ast
import math


def calculate_execution_time(code):
    try:
        tree = ast.parse(code)
        node_count = sum(1 for _ in ast.walk(tree))
        base_timeout = 600.0
        complexity_bonus = (node_count / 100) * 1.0
        total_timeout = base_timeout + complexity_bonus
        return int(math.ceil(total_timeout))
    except Exception:
        return 600 