import ast


def is_code_allowed(code):
    """
    Checks if the given code uses any module or function that is not allowed.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise Exception(e)

    allowed_names = set(allowed_builtins)
    imported_modules = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_name = alias.name.split('.')[0]
                if module_name not in allowed_modules:
                    return False, f'the module {module_name} is not allowed'
                imported_modules.add(module_name)
        elif isinstance(node, ast.ImportFrom):
            if node.module not in allowed_modules:
                return False, f'the module {node.module} is not allowed'
            imported_modules.add(node.module)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id not in allowed_names:
                    return False, f'the function {node.func.id} is not allowed'
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr not in allowed_names:
                    module_name = node.func.value.id
                    if module_name in imported_modules:
                        continue
                    return False, f'the function {node.func.attr} is not allowed'
    return True, 'passed'


ALLOWED_MODULES = ['time', 'math']
ALLOWED_BUILTINS = ['print', 'len', 'range']

code1 = "import time; time.sleep(5)"
code2 = "import os; os.system('rm -rf /')"
code3 = "time print('Hello'); time.sleep(5); os.system('rm -rf /')"

print(is_code_allowed(code1, ALLOWED_MODULES, ALLOWED_BUILTINS))  # True
print(is_code_allowed(code2, ALLOWED_MODULES, ALLOWED_BUILTINS))  # False
print(is_code_allowed(code3, ALLOWED_MODULES, ALLOWED_BUILTINS))  # False
