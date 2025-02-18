# Run MinerU

Installation: See the [Installation of MinerU](https://mineru.readthedocs.io/en/latest/user_guide/install/install.html) documentation for detailed instructions.

## Setup and Execution

1.  **Synchronize Dependencies:**

    ```bash
    uv sync
    ```

    *   This command synchronizes your project's dependencies using `uv`, ensuring all required packages are installed based on your project's configuration file (e.g., `pyproject.toml`, `requirements.txt`). It's similar to running `pip install -r requirements.txt` but typically faster.

2.  **Download Pre-trained Models (if necessary):**

    ```bash
    uv run download_models_hf.py
    ```

3.  **Run MinerU's `magic-pdf` Tool:**

    ```bash
    uv run magic-pdf -p ../pdfs/ -o md/
    ```

    *   This command executes the `magic-pdf` script, which is the core tool for processing PDF files in MinerU.
    *   `-p ../pdfs/`: Specifies the input directory containing the PDF files. The relative path `../pdfs/` indicates that the `pdfs` directory is located one level up from the current working directory.
    *   `-o md/`: Specifies the output directory where the processed Markdown files will be saved. The relative path `md/` indicates that the `md` directory is located in the current working directory.