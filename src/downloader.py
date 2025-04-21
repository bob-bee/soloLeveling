import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from config import OUTPUT_DIR

async def save_chapter_as_pdf(chapter_number: str, url: str, format="A4"):
    """Save the chapter from the URL as a PDF in output/pdf/."""
    pdf_output_dir = os.path.join(OUTPUT_DIR, "pdf")
    os.makedirs(pdf_output_dir, exist_ok=True)
    
    pdf_path = os.path.join(pdf_output_dir, f"chapter-{chapter_number}.pdf")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            print(f"📄 Rendering: {url}")
            await page.goto(url, timeout=60000)
            await page.pdf(path=pdf_path, format=format, margin={"top": "0.5in", "bottom": "0.5in"})
            await browser.close()
            print(f"✅ Saved PDF: {pdf_path}")
    except Exception as e:
        print(f"❌ Error generating PDF for {url}: {e}")

async def process_chapter_folder(chapter_folder: Path):
    """Process each .txt file inside the chapter folder and generate PDF."""
    txt_files = list(chapter_folder.glob("*.txt"))
    for txt_file in txt_files:
        chapter_number = txt_file.stem.split("-")[-1]
        url = txt_file.read_text().strip()

        # Skip if the URL is empty or invalid
        if not url:
            print(f"⚠️ No URL found in {txt_file}. Skipping...")
            continue

        await save_chapter_as_pdf(chapter_number, url)

async def main():
    output_path = Path(OUTPUT_DIR)
    tasks = []
    
    # Creating a list of tasks to process each chapter folder asynchronously
    for chapter_folder in sorted(output_path.iterdir()):
        if chapter_folder.is_dir():
            tasks.append(process_chapter_folder(chapter_folder))

    # Running all tasks concurrently
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
