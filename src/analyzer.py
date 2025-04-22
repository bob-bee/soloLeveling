import os
from pathlib import Path
from bs4 import BeautifulSoup  # Requires `beautifulsoup4` installed

BASE_HTML_DIR = Path("/workspaces/soloLeveling/output/html")
BASE_TEXT_DIR = Path("/workspaces/soloLeveling/output/text")

def analyze_html_and_update_text(chapter_number: str):
    """
    Analyze the HTML file and update the corresponding text file with extracted data.
    """
    # Paths for the HTML and text files
    html_file_path = BASE_HTML_DIR / f"chapter-{chapter_number}/chapter-{chapter_number}.html"
    text_file_path = BASE_TEXT_DIR / f"chapter-{chapter_number}.txt"

    # Check if the HTML file exists
    if not html_file_path.exists():
        print(f"❌ HTML file not found: {html_file_path}")
        return

    # Check if the text file exists
    if not text_file_path.exists():
        print(f"⚠️ Text file not found: {text_file_path}. Creating a new one.")
        text_file_path.parent.mkdir(parents=True, exist_ok=True)
        text_file_path.touch()

    # Parse the HTML file
    with open(html_file_path, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")

    # Extract relevant data
    body = soup.body
    dimensions = f"Width: {body.get('width', 'unknown')}, Height: {body.get('height', 'unknown')}" if body else "Dimensions: unknown"
    css_selectors = [tag.name for tag in soup.find_all()]

    # Update the text file
    with open(text_file_path, "a", encoding="utf-8") as text_file:
        text_file.write("\n--- HTML Analysis ---\n")
        text_file.write(f"Dimensions: {dimensions}\n")
        text_file.write(f"CSS Selectors: {', '.join(css_selectors)}\n")

    print(f"✏️ Updated text file: {text_file_path}")

def analyze_all_html_files():
    """
    Analyze all HTML files in the output/html directory and update corresponding text files.
    """
    # Iterate through all HTML files in the base directory
    for html_folder in BASE_HTML_DIR.glob("chapter-*"):
        chapter_number = html_folder.name.split("-")[-1]
        html_file_path = html_folder / f"chapter-{chapter_number}.html"

        if html_file_path.exists():
            analyze_html_and_update_text(chapter_number)
        else:
            print(f"⚠️ HTML file not found for chapter {chapter_number}: {html_file_path}")

if __name__ == "__main__":
    analyze_all_html_files()