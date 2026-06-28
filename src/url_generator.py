import os
import re
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys

# Ensure script can find config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from config import BASE_URL, OUTPUT_DIR

def fetch_chapter_links(base_url):
    """Fetch all chapter links from the main site page."""
    try:
        # Spoof a real modern browser to bypass client side filters / blocks
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch base page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    chapter_links = set()

    print("Parsing page links...")
    
    # 1. Grab links from any href attribute on the page
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(base_url, href)
        
        # Flex regex to match anywhere inside the URL string
        match = re.search(r'read-solo-leveling-manga-chapter-(\d+(?:\.\d+)?)-online', full_url)
        if match:
            chapter_number = match.group(1)
            chapter_links.add((float(chapter_number), full_url.rstrip("/")))

    # 2. If BeautifulSoup failed because of Javascript grid loading, look for fallback strings inside <script> blocks
    if not chapter_links:
        print("⚠️ Grid hidden by JavaScript. Attempting to extract from page scripts...")
        script_links = re.findall(r'https://onlinesololevelingmanga\.com/read-solo-leveling-manga-chapter-\d+(?:\.\d+)?-online/?', response.text)
        for url in script_links:
            match = re.search(r'read-solo-leveling-manga-chapter-(\d+(?:\.\d+)?)-online', url)
            if match:
                chapter_number = match.group(1)
                chapter_links.add((float(chapter_number), url.rstrip("/")))

    # Sort numerically by chapter number
    return sorted(list(chapter_links), key=lambda x: x[0])

def save_links_to_csv(chapter_links, output_dir=OUTPUT_DIR):
    """Save the links into a structured CSV file inside the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "chapters_list.csv")
    
    with open(csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        # Headers for your downstream PDF/image compiler
        writer.writerow(["Chapter Number", "URL"])
        
        for number, url in chapter_links:
            # Drop trailing decimals for clean integers (e.g., 2.0 -> 2)
            display_num = int(number) if number.is_integer() else number
            writer.writerow([display_num, url])
            
    print(f"✅ Saved CSV to: {csv_path}")

def main():
    print("🔍 Fetching chapter links from:", BASE_URL)
    chapter_links = fetch_chapter_links(BASE_URL)

    if not chapter_links:
        print("\n❌ Extraction failed. The landing page might be fully locked down by JS.")
        print("💡 QUICK FIX: Change your BASE_URL in config.py to a chapter page instead (e.g. the chapter-0 link), since individual chapters usually contain a static sidebar drop-down menu with all other chapters!")
        return

    save_links_to_csv(chapter_links)
    print(f"\n🎉 Done! {len(chapter_links)} chapter links compiled successfully.")
    
if __name__ == "__main__":
    main()