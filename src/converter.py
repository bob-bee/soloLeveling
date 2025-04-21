import os
import asyncio

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
