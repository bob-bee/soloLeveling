import os
import platform
import shutil

# === CONFIGURATION ===

# Detect platform
PLATFORM = platform.system()

# Paths to external tools
if PLATFORM == "Windows":
    WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    POPPLER_PATH = r"C:\poppler\Library\bin"
else:
    # In Codespaces/Ubuntu, wkhtmltopdf may need to be installed manually
    WKHTMLTOPDF_PATH = shutil.which("wkhtmltopdf") or "/usr/bin/wkhtmltopdf"
    POPPLER_PATH = "/usr/bin"

# Base output folder
OUTPUT_DIR = os.path.join(os.getcwd(), "output")

# Subdirectories
PDF_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "pdf")
IMAGE_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "images")
MERGED_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "merged_panels")
FINAL_PDF_PATH = os.path.join(OUTPUT_DIR, "solo_leveling_full.pdf")

# URLs and chapters
BASE_URL = "https://w66.sololevelingthemanga.com/manga/solo-leveling-chapter-{}/"
START_CHAPTER = 1
END_CHAPTER = 10

# Constants
PDF_NAME = "solo_leveling_full.pdf"
IMAGE_NAME = "solo_leveling_full.png"

# Create necessary directories
for folder in [PDF_OUTPUT_DIR, IMAGE_OUTPUT_DIR, MERGED_OUTPUT_DIR]:
    os.makedirs(folder, exist_ok=True)

# === FUNCTIONS ===
def print_config():
    print("=== Configuration ===")
    print(f"OS: {PLATFORM}")
    print(f"Output Folder: {OUTPUT_DIR}")
    print(f"Start Chapter: {START_CHAPTER}")
    print(f"End Chapter: {END_CHAPTER}")
    print(f"PDF Output Directory: {PDF_OUTPUT_DIR}")
    print(f"Image Output Directory: {IMAGE_OUTPUT_DIR}")
    print(f"Merged Panels Directory: {MERGED_OUTPUT_DIR}")
    print(f"Final PDF Path: {FINAL_PDF_PATH}")
    print(f"Base URL: {BASE_URL}")
    print(f"PDF Name: {PDF_NAME}")
    print(f"Image Name: {IMAGE_NAME}")
    print("=== External Tools ===")
    if PLATFORM == "Windows":
        print("Poppler Path: (Make sure to add Poppler to your PATH)")
    else:
        print("Poppler Path: /usr/bin")
    print(f"WKHTMLTOPDF Path: {WKHTMLTOPDF_PATH or '❌ Not found'}")
    print(f"Poppler Path: {POPPLER_PATH or '❌ Not found'}")

if __name__ == "__main__":
    print_config()
