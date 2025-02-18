import argparse
import logging
from pathlib import Path

from gemini_parser import GeminiPDFParser


def main(args: argparse.Namespace) -> None:
    gemini_parser = GeminiPDFParser(
        api_key=args.api_key,
        model_name=args.model_name,
        num_workers=args.num_workers,
        max_page=args.max_page,
        show_progress=args.show_progress,
    )
    input_dir = Path(__file__).resolve().parents[1] / "pdfs"
    output_dir = Path(__file__).resolve().parent / "md"
    output_dir.mkdir(parents=True, exist_ok=True)
    pdfs_paths = list(input_dir.glob("*.pdf"))
    for pdf_path in pdfs_paths:
        output_path = output_dir / f"{pdf_path.stem}.md"
        gemini_parser.parse_pdf(
            file=pdf_path,
            output_file=output_path,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse PDFs using GeminiPDFParser.")
    parser.add_argument("--api_key", required=True, help="API key for GeminiPDFParser.")
    parser.add_argument("--model_name", default="gemini-2.0-flash", help="Name of the model to use.")
    parser.add_argument("--num_workers", type=int, default=4, help="Number of workers for parallel processing.")
    parser.add_argument("--max_page", type=int, default=100, help="Maximum number of pages to parse.")
    parser.add_argument("--show_progress", action="store_true", help="Show progress during parsing.")

    args = parser.parse_args()
    main(args)