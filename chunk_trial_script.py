import ast


def chunk_python_file(content: str, file_path: str):
    tree = ast.parse(content)
    lines = content.splitlines()
    chunks = []
    covered_lines = set()

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if hasattr(node, "decorator_list") and node.decorator_list:
                decorator_lines = [decorator.lineno for decorator in node.decorator_list]
                start_line = min(decorator_lines) - 1
            else:
                start_line = node.lineno - 1
            end_line = node.end_lineno
            for i in range(start_line, end_line):
                covered_lines.add(i)
            code_chunk = "\n".join(lines[start_line:end_line])
            chunks.append(
                {
                    "type": "class" if isinstance(node, ast.ClassDef) else "function",
                    "name": getattr(node, "name", None),
                    "chunk": code_chunk,
                    "file": file_path,
                    "start_line": start_line + 1,
                    "end_line": end_line,
                }
            )
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            start_line = node.lineno - 1
            end_line = node.end_lineno if node.end_lineno else node.lineno
            for i in range(start_line, end_line):
                covered_lines.add(i)
            code_chunk = "\n".join(lines[start_line:end_line])
            chunks.append(
                {
                    "type": "import",
                    "name": str(code_chunk).strip(),
                    "chunk": code_chunk,
                    "file": file_path,
                    "start_line": start_line + 1,
                    "end_line": end_line,
                }
            )

    module_lines = [lines[i] for i in range(len(lines)) if i not in covered_lines and lines[i].strip() != ""]
    if module_lines:
        chunks.append(
            {
                "type": "module",
                "name": None,
                "chunk": "\n".join(module_lines),
                "file": file_path,
                "start_line": None,
                "end_line": None,
            }
        )

    return chunks


code_sample = '''
"""Module docstring. It does somethig"""

import os

# Module-level variable
x = 42

@decorator
def funct():
    """Function docstring."""
    # Function comment
    pass

class myclass:
    """Class docstring."""
    def method(self):
        pass
'''

final_chunks = chunk_python_file(code_sample, "sample.py")
for chunk in final_chunks:
    print(f"Type: {chunk['type']}")
    print(f"Name: {chunk['name']}")
    print(f"Chunk:\n{chunk['chunk']}")
    print("-" * 40)

# processed_files = 0
# for root, dirs, files in os.walk("blt"):
#     for file in files:
#         _, ext = os.path.splitext(file)
#         if ext in {".py"}:
#             full_path = os.path.join(root, file)
#             with open(full_path, "r", encoding="utf-8") as f:
#                 print(f"Processing file: {full_path}")
#                 content = f.read()
#             final_chunks = chunk_python_file(content, full_path)
#             for chunk in final_chunks:
#                 print(f"Type: {chunk['type']}")
#                 print(f"Name: {chunk['name']}")
#                 print(f"Chunk:\n{chunk['chunk']}")
#                 print("-" * 40)
#             processed_files += 1
#             if processed_files >= 5:
#                 break
#     if processed_files >= 5:
#         break
