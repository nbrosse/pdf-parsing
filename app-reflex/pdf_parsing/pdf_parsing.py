from pathlib import Path

import reflex as rx
from reflex import State

from pdf_parsing.md_files import read_markdown_file

PDF_PAGES = {
    "2023-conocophillips-aim-presentation-1-7.pdf": 7,
    "deloitte-tech-risk-sector-banking.pdf": 2,
    "dttl-tax-technology-report-2023.pdf": 17,
    "gx-iif-open-data.pdf": 32,
    "life-sciences-smart-manufacturing-services-peak-matrix-assessment-2023.pdf": 15,
    "XC9500_CPLD_Family-1-4.pdf": 4
}

FILES = list(PDF_PAGES.keys())

METHODS = ["docling", "llamaparse", "marker-pdf", "pymupdf", "gemini"]


class AppState(State):
    method: str = "docling"
    filename: str = FILES[0]

    page_number: str = "1"

    @rx.var
    def md_content_pages(self) -> list[str]:
        return read_markdown_file(
            Path(f"../{self.method}-folder/md/"),
            self.filename,
            self.method
        )

    def set_filename(self, value: str):
        self.set_page_number("1")
        self.filename = value

    def set_page_number(self, value: str):
        self.page_number = value

    @rx.var
    def num_pages_file(self) -> int:
        return PDF_PAGES.get(self.filename)

    @rx.var
    def page_options(self) -> list[str]:
        return [str(i) for i in range(1, self.num_pages_file + 1)]

    @rx.var(cache=False)
    def url_pdf(self) -> str:
        return f"pdf/{self.filename}#page={self.page_number}"

    @rx.var
    def page(self) -> int:
        return int(self.page_number)

    def decrement_page(self):
        self.set_page_number(str(self.page - 1))

    def increment_page(self):
        self.set_page_number(str(self.page + 1))


def pdf_viewer_component():
    # Reflex doesn't have a built-in PDF viewer, so this is a placeholder
    return rx.el.object(
        data=AppState.url_pdf,
        width="50vw",
        height="100vh",
        type="application/pdf",
        key=f"{AppState.filename}-{AppState.page_number}"
    )


def markdown_viewer_component():
    return rx.vstack(
        rx.tabs(
        rx.tabs.list(
            rx.tabs.trigger("Markdown Content", value="tab1"),
            rx.tabs.trigger("Raw Text Content", value="tab2"),
        ),
        rx.tabs.content(
            rx.vstack(
                rx.markdown(
                    AppState.md_content_pages[AppState.page - 1],
                    width="100%",
                ),
                spacing="3",
                width="50vw",
            ),
            value="tab1"
        ),
        rx.tabs.content(
            rx.vstack(
                rx.vstack(
                    rx.foreach(
                        AppState.md_content_pages[AppState.page - 1].split("\n"),
                        lambda x: rx.text(x)
                    ),
                    spacing="1",
                ),

                spacing="3",
                width="50vw",
            ),
            value="tab2"
        ),
        width="50vw",
        default_value="tab1",
    ),
        rx.hstack(
            rx.cond(
                AppState.page - 1 != 0,
                rx.icon_button(
                    "arrow-left",
                    on_click=AppState.decrement_page
                )
            ),
            rx.cond(
                AppState.page != AppState.num_pages_file,
                rx.icon_button(
                    "arrow-right",
                    on_click=AppState.increment_page
                )
            ),
            justify_content="space-evenly",
            width="100%"
        ),
    )


def index():
    return rx.vstack(
        rx.heading("PDF and Markdown Viewer", size="8"),
        rx.select(
            METHODS,
            value=AppState.method,
            on_change=AppState.set_method,
            label="Choose method",
        ),
        rx.select(
            FILES,
            value=AppState.filename,
            on_change=AppState.set_filename,
            label="Choose filename",
        ),
        rx.select(
            AppState.page_options,
            value=AppState.page_number,
            on_change=AppState.set_page_number,
            label="Choose page",
        ),
        rx.hstack(
            pdf_viewer_component(),
            markdown_viewer_component(),
            spacing="1",
            width="100%",
        ),
        padding="20px",
        width="100%",
    )


app = rx.App()
app.add_page(index)
