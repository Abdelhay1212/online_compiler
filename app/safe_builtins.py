import ast
from typing import Tuple

ALLOWED_MODULES = [
    'math', 'random', 'string', 'datetime', 'time', 'calendar', 'json',
    'collections', 'itertools', 'functools', 're', 'struct', 'decimal',
    'fractions', 'multiprocessing', 'queue', 'statistics', 'operator', 'copy',
    'pprint', 'enum', 'heapq', 'bisect', 'types', 'array', 'textwrap', 'uuid',
    'hashlib', 'base64', 'pathlib', 'weakref', 'abc', 'collections.abc', 'secrets'
]

ALLOWED_BUILTINS = [
    'print', 'len', 'range', 'str', 'int', 'float', 'list', 'tuple', 'dict',
    'set', 'input', 'strip', 'lower', 'upper', 'replace', 'split', 'join', 'append',
    'insert', 'remove', 'sort', 'reverse', 'index', 'count', 'keys', 'values', 'items',
    'get', 'update',
]


def is_code_allowed(code: str) -> Tuple[bool, str]:
    """
    Checks if the given code uses any module or function that is not allowed.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise Exception(e)

    allowed_names = set(ALLOWED_BUILTINS)
    imported_modules = set()
    defined_functions = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_name = alias.name.split('.')[0]
                if module_name not in ALLOWED_MODULES:
                    return False, f'the module {module_name} is not allowed'
                imported_modules.add(module_name)
        elif isinstance(node, ast.ImportFrom):
            if node.module not in ALLOWED_MODULES:
                return False, f'the module {node.module} is not allowed'
            imported_modules.add(node.module)
        elif isinstance(node, ast.FunctionDef):
            defined_functions.add(node.name)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id not in allowed_names and node.func.id not in defined_functions:
                    return False, f'the function {node.func.id} is not allowed'
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr not in allowed_names:
                    module_name = node.func.value.id if isinstance(
                        node.func.value, ast.Name) else None
                    if module_name not in imported_modules:
                        return False, f'the function {node.func.attr} is not allowed'

    return True, 'passed'
