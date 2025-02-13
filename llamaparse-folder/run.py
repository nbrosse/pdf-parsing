from pathlib import Path

from llama_cloud_services import LlamaParse
from llama_parse import ResultType
import argparse


def main(api_key: str):
    llama_parse = LlamaParse(
        api_key=api_key,
        split_by_page=False,
        result_type=ResultType.MD,
        
    )
    input_dir = Path(__file__).resolve().parents[1] / "pdfs"
    output_dir = Path(__file__).resolve().parent / "md"
    output_dir.mkdir(exist_ok=True, parents=True)
    pdfs_paths = list(input_dir.glob("*.pdf"))
    docs = llama_parse.load_data(pdfs_paths)
    for pdf_path, doc in zip(pdfs_paths, docs):
        content = doc.text
        output_file = output_dir / f"{pdf_path.stem}.md"
        output_file.write_text(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse PDFs using LlamaParse')
    parser.add_argument('--api-key', required=True, help='LlamaParse API key')
    args = parser.parse_args()
    main(api_key=args.api_key)
