import json
import sys
import pkgutil

def extract_imports_from_notebook(notebook_path):
    with open(notebook_path, 'r') as f:
        notebook_content = json.load(f)

    imports = set()

    for cell in notebook_content.get('cells', []):
        if cell['cell_type'] == 'code':
            for line in cell['source']:
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    import_statement = line.split()[1]
                    if '.' in import_statement:
                        import_statement = import_statement.split('.')[0]
                    imports.add(import_statement)

    return imports

def is_builtin_module(module_name):
    if module_name in sys.builtin_module_names:
        return True
    if pkgutil.find_loader(module_name) is None:
        return False
    try:
        import importlib.util
        spec = importlib.util.find_spec(module_name)
        return spec.origin is None or 'site-packages' not in spec.origin
    except ImportError:
        return False

def create_requirements_file(imports, output_path):
    with open(output_path, 'w') as f:
        for imp in sorted(imports):
            if not is_builtin_module(imp):
                if imp == 'sklearn':
                    f.write("scikit-learn\n")
                else:
                    f.write(f"{imp}\n")

notebook_path = 'test.ipynb'
output_path = 'requirements.txt'

imports = extract_imports_from_notebook(notebook_path)
create_requirements_file(imports, output_path)
