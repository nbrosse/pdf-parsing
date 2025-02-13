from pathlib import Path
import pymupdf4llm


def main():
    input_dir = Path(__file__).resolve().parents[1] / "pdfs"
    output_dir = Path(__file__).resolve().parent / "md"
    output_dir.mkdir(parents=True, exist_ok=True)
    pdfs_paths = input_dir.glob("*.pdf")
    for pdf_path in pdfs_paths:
        md_text = pymupdf4llm.to_markdown(pdf_path)
        md_path = output_dir / f"{pdf_path.stem}.md"
        md_path.write_text(md_text)


if __name__ == "__main__":
    main()


