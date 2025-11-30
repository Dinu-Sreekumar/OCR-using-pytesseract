# OCR Streamlit Application

A Python-based Optical Character Recognition (OCR) application built with Streamlit and Tesseract. This app allows users to upload images, extract text, and download the results as both plain text and searchable PDF files.

## Demo

![OCR App Interface](assets/OCR%20UI.png)

[Watch Demo Video](assets/OCR%20demo.mp4)

## Features

- **Image Upload**: Supports PNG, JPG, and JPEG formats.
- **Text Extraction**: Uses Tesseract OCR to extract text from images.
- **PDF Generation**: Converts images to searchable PDF documents.
- **OS Detection**: Automatically configures Tesseract path for Windows users.
- **User-Friendly Interface**: Built with Streamlit for a clean and responsive UI.

## Prerequisites

1.  **Python 3.7+**
2.  **Tesseract OCR Engine**:
    - **Windows**: Download and install from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki).
        - **Important**: The application expects Tesseract to be installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`.
    - **Linux**: `sudo apt install tesseract-ocr`
    - **macOS**: `brew install tesseract`

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/macOS
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

2.  Open your browser (usually at `http://localhost:8501`).

3.  Upload an image and click **Extract Text & Generate PDF**.

## Project Structure

- `app.py`: Main application file containing UI and OCR logic.
- `requirements.txt`: List of Python dependencies.
- `.gitignore`: Specifies files to be ignored by Git.

## Troubleshooting

- **Tesseract Not Found**: Ensure Tesseract is installed and the path in `app.py` matches your installation path. On Windows, the default is set to `C:\Program Files\Tesseract-OCR\tesseract.exe`.

## Author

- **Dinu Sreekumar**: [LinkedIn](https://www.linkedin.com/in/dinu-sreekumar)
