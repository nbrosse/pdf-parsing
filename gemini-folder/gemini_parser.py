import base64
import re
from io import BytesIO
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types
from pypdf import PdfReader, PdfWriter
from utils import run_jobs, asyncio_run

nest_asyncio_err = "cannot be called from a running event loop"
nest_asyncio_msg = "The event loop is already running. Add `import nest_asyncio; nest_asyncio.apply()` to your code to fix this issue."


PDF_PARSING_PROMPT = """
You are a specialized document transcription assistant converting PDF documents to Markdown format.
Your primary goal is to create an accurate, complete, and well-structured Markdown representation.

<instructions>
1. Language and Content:
   - MAINTAIN the original document language throughout ALL content
   - ALL elements (headings, tables, descriptions) must use source language
   - Preserve language-specific formatting and punctuation
   - Do NOT translate any content

2. Text Content:
   - Convert all text to proper Markdown syntax
   - Use appropriate heading levels (# ## ###)
   - Preserve emphasis (bold, italic, underline)
   - Convert bullet points to Markdown lists (-, *, +)
   - Maintain original document structure and hierarchy

3. Visual Elements (CRITICAL):
   a. Tables:
      - MUST represent ALL data cells accurately in original language
      - Use proper Markdown table syntax |---|
      - Include header rows
      - Add caption above table: [Table X: Description] in document language
      
   b. Charts/Graphs:
      - Create detailed tabular representation of ALL data points
      - Include X/Y axis labels and units in original language
      - List ALL data series names as written
      - Add caption: [Graph X: Description] in document language
      
   c. Images/Figures:
      - Format as: ![Figure X: Detailed description](image_reference)
      - Describe key visual elements in original language
      - Include measurements/scales if present
      - Note any text or labels within images

4. Quality Requirements:
   - NO content may be omitted
   - Verify all numerical values are preserved
   - Double-check table column/row counts match original
   - Ensure all labels and legends are included
   - Maintain document language consistently throughout

5. Structure Check:
   - Begin each section with clear heading
   - Use consistent list formatting
   - Add blank lines between elements
   - Preserve original content order
   - Verify language consistency across sections
</instructions>
"""


def _get_pdf_medadata(reader: PdfReader) -> dict[str, Any]:
    nb_pages = reader.get_num_pages()
    initial_page = reader.pages[0]
    width = initial_page.mediabox.width
    height = initial_page.mediabox.height
    if width > height:
        format = "landscape"
    else:
        format = "portrait"
    return {"nb_pages": nb_pages, "format": format}


def _postprocess_markdown_output(response: str) -> str:
    pattern = r"```markdown\s*(.*?)```"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return response


class GeminiPDFParser:

    def __init__(
            self,
            api_key: str,
            model_name: str = "gemini-2.0-flash",
            num_workers: int = 4,
            max_page: int = 100,
            show_progress: bool = True,
    ) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.max_page = max_page
        self.num_workers = num_workers
        self.show_progress = show_progress

    def parse_pdf(
        self,
        file: str | Path,
        output_file: str | Path,
    ) -> None:
        try:
            return asyncio_run(self.aparse_pdf(file, output_file))
        except RuntimeError as e:
            if nest_asyncio_err in str(e):
                raise RuntimeError(nest_asyncio_msg)
            else:
                raise e

    async def _aparse_page(
        self,
        reader: PdfReader,
        page_num: int,
    ):
        page = reader.pages[page_num]
        writer = PdfWriter()
        writer.add_page(page)
        with BytesIO() as bytes_stream:
            writer.write(bytes_stream)
            bytes_stream.seek(0)
            page_content = bytes_stream.read()
        # page_data = base64.standard_b64encode(page_content).decode("utf-8")
        return await self.client.aio.models.generate_content(
            model=self.model_name,
            contents = [
                types.Part.from_bytes(
                    data=page_content,
                    mime_type="application/pdf",
                ),
                PDF_PARSING_PROMPT,
            ]
        )

    async def aparse_pdf(
        self,
        file: str | Path,
        output_file: str | Path,
    ) -> None:
        file = Path(file)
        output_file = Path(output_file)
        if not file.exists():
            raise FileNotFoundError(f"File {str(file)} does not exist")
        if file.suffix != ".pdf":
            raise ValueError(f"File {str(file)} is not a PDF")
        reader = PdfReader(str(file))
        metadata = _get_pdf_medadata(reader=reader)
        nb_pages = metadata["nb_pages"]
        if nb_pages > self.max_page:
            raise Exception(f"Number of pages {nb_pages} exceeds the maximum number of pages {self.max_page}")
        metadata["filename"] = file.name
        jobs = [
            self._aparse_page(
                reader=reader,
                page_num=page_num,
            ) for page_num in range(nb_pages)
        ]
        try:
            results = await run_jobs(
                jobs,
                workers=self.num_workers,
                desc=f"Parsing file {file.name}",
                show_progress=self.show_progress,
            )
            results = [_postprocess_markdown_output(r.text) for r in results]
            transcription = "".join([f"{r}\n\n--- end page {i + 1}\n\n" for i, r in enumerate(results)])
            output_file.write_text(transcription)
        except RuntimeError as e:
            if nest_asyncio_err in str(e):
                raise RuntimeError(nest_asyncio_msg)
            else:
                raise e
