import os
import ast

def find_imports(root_dir):
    imports = set()
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    try:
                        tree = ast.parse(file.read(), filename=filename)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imports.add(alias.name.split('.')[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    imports.add(node.module.split('.')[0])
                    except Exception as e:
                        print(f"Skipped {filepath}: {e}")
    return sorted(imports)

# Example usage
project_path = "/workspaces/aws-ml-engineering-lifecycle"
packages = find_imports(project_path)
print("\n".join(packages))