# Running the Streamlit App

These instructions explain how to run the Streamlit application.

1.  **Set up your environment (using UV):**

    ```bash
    uv sync
    ```
    This command synchronizes your environment dependencies, ensuring you have all the necessary packages installed (as defined in your project's `pyproject.toml` file).

2.  **Run the Streamlit App:**

    ```bash
    uv run streamlit run streamlit_app.py
    ```

    This command launches the Streamlit application using the `streamlit run` command.  `streamlit_app.py` is assumed to be the main file containing your Streamlit code.

3.  **Accessing the App:**

    After running the command above, Streamlit will typically print a message in your terminal indicating the local URL where the app is running (usually something like `http://localhost:8501`).  It should also automatically open a new tab in your default web browser at that address. If it doesn't open automatically, copy the URL from the terminal and paste it into your browser.

**Important Notes:**

*   **Parsing Tool Availability:**  The application focuses on showcasing these parsing tools: `docling`, `llamaparser`, `gemini`, `marker-pdf`, and `pymupdf`.

*   **`minerU` Exclusion:**  The `minerU` parser is *not* included in this application's UI. This is primarily because its output is challenging to split by page, and its table output is in HTML format, making it difficult to integrate seamlessly with the other parsers within the Streamlit application's design.
