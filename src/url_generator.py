import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import BASE_URL, OUTPUT_DIR
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

def fetch_chapter_links(base_url):
    """Fetch all chapter links from the main site page."""
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch base page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    chapter_links = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(base_url, href)
        match = re.search(r'/manga/solo-leveling-chapter-(\d+)/?$', full_url)
        if match:
            chapter_number = match.group(1)
            chapter_links.add((int(chapter_number), full_url.rstrip("/")))

    return sorted(chapter_links)

def save_links_in_folders(chapter_links, output_dir=OUTPUT_DIR):
    """Create folders for each chapter and save the link into a .txt file in output/txt/."""
    # Create the necessary directories for txt files
    txt_output_dir = os.path.join(output_dir, "txt")
    os.makedirs(txt_output_dir, exist_ok=True)

    for number, url in chapter_links:
        file_path = os.path.join(txt_output_dir, f"chapter-{number}.txt")
        with open(file_path, "w") as f:
            f.write(url)

        print(f"✅ Saved: {file_path}")

def main():
    print("🔍 Fetching chapter links from:", BASE_URL)
    chapter_links = fetch_chapter_links(BASE_URL)

    if not chapter_links:
        print("⚠️ No chapter links found.")
        return

    save_links_in_folders(chapter_links)
    print(f"\n🎉 Done! {len(chapter_links)} chapter links saved in '{os.path.join(OUTPUT_DIR, 'txt')}'.")
    
if __name__ == "__main__":
    main()
