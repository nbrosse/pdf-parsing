import re
from pathlib import Path
from typing import Literal


def read_markdown_file(
        markdown_dir: Path,
        pdf_filename: str,
        method: Literal["docling", "llamaparse", "marker-pdf", "pymupdf"],
) -> list[str]:
    match method:
        case "docling" | "llamaparse":
            md_path = markdown_dir / pdf_filename.replace(".pdf", ".md")
            md_content = md_path.read_text()
            md_content_pages = md_content.split("\n---\n")
        case "marker-pdf":
            md_path = markdown_dir / pdf_filename.replace(".pdf", "") / pdf_filename.replace(".pdf", ".md")
            md_content = md_path.read_text()
            pattern = r"\n\{\d+\}-+\s\n*"
            md_content_pages = re.split(pattern, md_content)
        case "gemini":
            md_path = markdown_dir / pdf_filename.replace(".pdf", ".md")
            md_content = md_path.read_text()
            pattern = r"--- end page \d+"
            md_content_pages = re.split(pattern, md_content)
            if not md_content_pages[-1].strip():
                md_content_pages.pop()
        case "pymupdf":
            md_path = markdown_dir / pdf_filename.replace(".pdf", ".md")
            md_content = md_path.read_text()
            md_content_pages = md_content.split("\n-----\n")
            if not md_content_pages[-1].strip():
                md_content_pages.pop()
        case _:
            raise NotImplementedError(f"Method {method} not implemented")
    return md_content_pages