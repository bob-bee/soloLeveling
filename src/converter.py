import os
import asyncio
from pathlib import Path
from shutil import which

BASE_PDF_DIR = Path("/workspaces/soloLeveling/output/pdf")
BASE_HTML_DIR = Path("/workspaces/soloLeveling/output/html")

async def convert_pdf_to_html(pdf_path: Path, html_path: Path):
    """
    Convert the PDF file to a single HTML file using pdftohtml.
    """
    # Check if pdftohtml is installed
    if not which("pdftohtml"):
        print("❌ Error: 'pdftohtml' is not installed or not available on PATH.")
        return

    html_path.parent.mkdir(parents=True, exist_ok=True)

    # Use -s for single file output and -noframes to prevent extra splits
    process = await asyncio.create_subprocess_exec(
        'pdftohtml', '-s', '-noframes', str(pdf_path), str(html_path)
    )
    await process.wait()
    print(f"✅ Converted {pdf_path.name} → {html_path.name}")

async def convert_all_pdfs():
    """
    Convert all PDFs in the directory to HTML files.
    """
    tasks = []

    # Ensure the output directory exists
    BASE_HTML_DIR.mkdir(parents=True, exist_ok=True)

    # Iterate through all PDF files in the base directory
    for pdf_file in BASE_PDF_DIR.glob("chapter-*.pdf"):
        chapter_number = pdf_file.stem.split("-")[-1]
        html_output_path = BASE_HTML_DIR / f"chapter-{chapter_number}/chapter-{chapter_number}.html"
        tasks.append(convert_pdf_to_html(pdf_file, html_output_path))

    # Run all conversion tasks concurrently
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(convert_all_pdfs())
