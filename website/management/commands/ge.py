import ast
import json
import logging
import os

import google.generativeai as genai
from django.conf import settings
from django.core.management.base import BaseCommand

from website.views.aibot import get_gemini_api_key

logger = logging.getLogger(__name__)

REPO_PATH = settings.BASE_DIR
OUTPUT_FILE = os.path.join(REPO_PATH, "embeddings.json")

EXTENSIONS = {".py"}
GEMINI_API_KEY = get_gemini_api_key()
genai.configure(api_key=GEMINI_API_KEY)


def chunk_python_file(content: str, file_path: str):
    logger.info("Chunking file: %s", file_path)
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


class Command(BaseCommand):
    help = "Generate embeddings of the repository."

    def handle(self, *args, **kwargs):
        logger.info("Generating repository embeddings. Using repository path: %s", REPO_PATH)
        logger.info("Output will be saved to: %s", OUTPUT_FILE)
        all_embeddings = []
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("")
        try:
            processed_files = 0
            for root, dirs, files in os.walk(REPO_PATH):
                for file in files:
                    if processed_files >= 5:
                        break
                    _, ext = os.path.splitext(file)
                    if ext in EXTENSIONS:
                        full_path = os.path.join(root, file)
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        if not content.strip():
                            logger.warning("Skipping empty file: %s", full_path)
                            continue
                        chunks = chunk_python_file(content, full_path)
                        if not chunks:
                            logger.warning("No valid chunks found in file: %s", full_path)
                            continue
                        for chunk in chunks:
                            embedding = genai.embed_content(
                                model="models/text-embedding-004",
                                content=chunk["chunk"],
                                task_type="retrieval_document",
                                title=chunk["name"] or "Untitled",
                            )
                            if embedding:
                                all_embeddings.append(
                                    {
                                        "path:": full_path,
                                        "file_name": file,
                                        "content": chunk,
                                        "embedding": embedding["embedding"],
                                    }
                                )
                        processed_files += 1
                if processed_files >= 5:
                    break
        except Exception as e:
            self.stderr.write(f"Error generating embeddings: {e}")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_embeddings, f, indent=4)

        self.stdout.write(f"Saved embeddings to {OUTPUT_FILE}")
        self.stdout.write(f"Total embedded chunks: {len(all_embeddings)}")
