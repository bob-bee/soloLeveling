import os
import asyncio
<<<<<<< HEAD
from pathlib import Path

BASE_PDF_DIR = Path("/workspaces/soloLeveling/output/pdf")
BASE_HTML_DIR = Path("/workspaces/soloLeveling/output/html")

async def convert_pdf_to_html(pdf_path: Path, html_path: Path):
    """
    Convert the PDF file to a single HTML file using pdftohtml.
    """
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
        html_output_path = BASE_HTML_DIR / f"chapter-{chapter_number}.html"
        tasks.append(convert_pdf_to_html(pdf_file, html_output_path))

    # Run all conversion tasks concurrently
    await asyncio.gather(*tasks)
    tasks = []

    for pdf_file in BASE_PDF_DIR.glob("chapter-*.pdf"):
        chapter_number = pdf_file.stem.split("-")[-1]
        html_output_path = BASE_HTML_DIR / f"chapter-{chapter_number}.html"
        tasks.append(convert_pdf_to_html(pdf_file, html_output_path))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(convert_all_pdfs())
=======

# Base output folder where chapter folders are stored
BASE_OUTPUT_FOLDER = "/workspaces/soloLeveling/output"  # Modify this as needed

async def convert_pdf_to_html(pdf_path, output_dir):
    """
    Convert the PDF file to HTML format using pdftohtml from Poppler.
    """
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Path for the output HTML file
    output_html_path = os.path.join(output_dir, 'output.html')

    # Run pdftohtml command asynchronously
    process = await asyncio.create_subprocess_exec(
        'pdftohtml', pdf_path, output_html_path
    )

    await process.wait()
    print(f"Converted {pdf_path} to HTML: {output_html_path}")

async def convert_pdfs_in_chapters(base_output_folder=BASE_OUTPUT_FOLDER):
    """
    Loop through each chapter folder, find the PDF, and convert it to HTML.
    """
    tasks = []

    # Loop through chapter folders (adjust the range based on your chapters)
    for chapter_num in range(1, 200):  # Example: chapters 1 to 199
        chapter_dir = os.path.join(base_output_folder, f"chapter_{chapter_num}")
        
        # Check if the chapter folder exists and contains the correct PDF
        if os.path.exists(chapter_dir):
            pdf_path = os.path.join(chapter_dir, f"chapter-{chapter_num}.pdf")
            if os.path.exists(pdf_path):
                print(f"Processing {pdf_path}...")  # Found the PDF, now convert it
                
                # Create a folder for the converted HTML files
                html_output_dir = os.path.join(chapter_dir, "converted_html")
                
                # Add the conversion task to the list
                tasks.append(convert_pdf_to_html(pdf_path, html_output_dir))
            else:
                print(f"Chapter {chapter_num} PDF not found. Skipping...")
        else:
            print(f"Chapter {chapter_num} folder does not exist. Skipping...")

    # Run all conversion tasks concurrently
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(convert_pdfs_in_chapters())
>>>>>>> d480a3cc1e3809edc98da0cc6c6c76a1e655665d
