import re
from pathlib import Path
from typing import Literal

import streamlit as st
import os
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(layout="wide")

# Define the paths to your PDF and Markdown folders
repo_folder = Path(__file__).resolve().parents[1]
pdf_folder = repo_folder / "pdfs"

pdf_pages = {
    "2023-conocophillips-aim-presentation-1-7.pdf": 7,
    "deloitte-tech-risk-sector-banking.pdf": 2,
    "dttl-tax-technology-report-2023.pdf": 17,
    "gx-iif-open-data.pdf": 32,
    "life-sciences-smart-manufacturing-services-peak-matrix-assessment-2023.pdf": 15,
    "XC9500_CPLD_Family-1-4.pdf": 4
}

pdfs_files = os.listdir(str(pdf_folder))


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
        case "gemini" | "mistral":
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

@st.cache_data
def read_pdf_file(pdf_path: Path) -> bytes:
    return pdf_path.read_bytes()


st.title("PDF and Markdown Viewer")

method = st.selectbox("Choose method", options=["docling", "llamaparse", "marker-pdf", "pymupdf", "gemini", "mistral"])
markdown_folder = repo_folder / f"{method}-folder" / "md"
filename = st.selectbox("Choose filename", options=pdfs_files)
num_pages_file = pdf_pages[filename]
page = st.selectbox("Choose page", options=list(range(1, num_pages_file + 1)))
pdf_content = read_pdf_file(pdf_folder / filename)
md_content_pages = read_markdown_file(
    pdf_filename=filename,
    markdown_dir=markdown_folder,
    method=method,
)

if len(md_content_pages) != num_pages_file:
    st.warning(f"Number of markdown pages {len(md_content_pages)} does not match the number of pdf pages {num_pages_file}")

if filename:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("PDF Viewer")
        pdf_viewer(pdf_content, width="90%", pages_to_render=[page])

    with col2:
        st.subheader("Markdown Content")
        st.markdown(md_content_pages[page - 1])
        st.divider()
        st.subheader("Raw text Content")
        st.text(md_content_pages[page - 1])