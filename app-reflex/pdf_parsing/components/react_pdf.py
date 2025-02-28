import reflex as rx


class PdfDocument(rx.Component):
    """PDF Document component from react-pdf"""

    library = "react-pdf"
    tag = "Document"
    lib_dependencies: list[str] = ["pdfjs-dist@4.8.69"]
    file: rx.Var[str]
    on_load_success: rx.EventHandler[lambda num_pages: [num_pages]]

    def add_imports(self):
        return {
            "react-pdf": [rx.ImportVar(tag="pdfjs")], "": [
                'react-pdf/dist/Page/TextLayer.css',
                'react-pdf/dist/Page/AnnotationLayer.css'
            ]
        }
    def add_custom_code(self) -> list[str]:
        return [
            """

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();
        """
        ]

class PdfPage(rx.Component):
    """Page component from react-pdf."""

    library = "react-pdf"
    tag = "Page"

    page_number: rx.Var[int]