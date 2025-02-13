import logging
from pathlib import Path

from docling.document_converter import DocumentConverter
from docling_core.types.doc import ImageRefMode

logging.basicConfig(level=logging.INFO)


def main():
    doc_converter = DocumentConverter()
    input_dir = Path(__file__).resolve().parents[1] / "pdfs"
    output_dir = Path(__file__).resolve().parent / "md"
    output_dir.mkdir(parents=True, exist_ok=True)
    pdfs_paths = input_dir.glob("*.pdf")
    docs = doc_converter.convert_all(pdfs_paths)
    for doc in docs:
        doc_filename = doc.input.file.stem
        num_pages = doc.document.num_pages()
        contents = [doc.document.export_to_markdown(image_mode=ImageRefMode.PLACEHOLDER, page_no=p) for p in range(1, num_pages + 1)]
        content = "\n---\n".join(contents)
        output_file = output_dir / f"{doc_filename}.md"
        output_file.write_text(content)


if __name__ == "__main__":
    main()
