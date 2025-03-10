import argparse
from pathlib import Path

from mistralai import Mistral, OCRResponse, DocumentURLChunk, SDKError
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type
from tqdm import tqdm


def replace_images_in_markdown(markdown_str: str, images_dict: dict) -> str:
    for img_name, base64_str in images_dict.items():
        markdown_str = markdown_str.replace(
            f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})"
        )
    return markdown_str


def get_combined_markdown(pdf_response: OCRResponse) -> str:
    markdowns: list[str] = []
    for page in pdf_response.pages:
        page_number = page.index
        image_data = {}
        for img in page.images:
            image_data[img.id] = img.image_base64
        markdowns.append(replace_images_in_markdown(page.markdown, image_data))
        markdowns.append(f"\n\n--- end page {page_number + 1}\n\n")
    return "".join(markdowns)


@retry(wait=wait_fixed(10), stop=stop_after_attempt(10), retry=retry_if_exception_type(SDKError))
def parse_pdf(
        client: Mistral,
        pdf_path: Path,
        output_path: Path,
) -> None:
    uploaded_pdf = client.files.upload(
        file={
            "file_name": pdf_path.name,
            "content": pdf_path.read_bytes(),
        },
        purpose="ocr",
    )
    signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)
    pdf_response = client.ocr.process(
        model="mistral-ocr-latest",
        document=DocumentURLChunk(document_url=signed_url.url),
        include_image_base64=True,
    )
    combined_markdown = get_combined_markdown(pdf_response)
    output_path.write_text(combined_markdown)


def main(args: argparse.Namespace):
    api_key = args.api_key
    client = Mistral(api_key=api_key)
    input_dir = Path(__file__).resolve().parents[1] / "pdfs"
    output_dir = Path(__file__).resolve().parent / "md"
    output_dir.mkdir(parents=True, exist_ok=True)
    pdfs_paths = list(input_dir.glob("*.pdf"))
    for pdf_path in tqdm(pdfs_paths, desc="Parsing pdfs"):
        output_path = output_dir / f"{pdf_path.stem}.md"
        parse_pdf(
            client=client,
            pdf_path=pdf_path,
            output_path=output_path,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse PDFs using Mistral OCR.")
    parser.add_argument("--api_key", required=True, type=str, help="API key for Mistral.")
    args = parser.parse_args()
    main(args)