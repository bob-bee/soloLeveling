import os
import re
import csv
import sys
import asyncio
import shutil
import platform
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright

# Ensure script can find config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from config import OUTPUT_DIR

def find_browser_executable():
    """Locate an available browser executable on the system."""
    system = platform.system()
    
    # Check for Chromium (common in dev containers/Codespaces)
    chromium_path = "/usr/bin/chromium-browser"
    if os.path.exists(chromium_path):
        print(f"🧭 Using Chromium: {chromium_path}")
        return chromium_path

    # Check for Brave
    brave_path = (
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        if system == "Windows"
        else shutil.which("brave")
    )
    if brave_path and os.path.exists(brave_path):
        print(f"🦁 Using Brave: {brave_path}")
        return brave_path

    # Check for standard Google Chrome paths
    if system == "Windows":
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                print(f"🧭 Using Google Chrome: {path}")
                return path
    else:
        chrome_path = shutil.which("google-chrome") or shutil.which("chrome")
        if chrome_path:
            print(f"🧭 Using Google Chrome: {chrome_path}")
            return chrome_path

    print("⚠️ No system browser found. Playwright will default to its built-in binaries.")
    return None

async def scroll_to_bottom(page):
    """Force-scroll down the webpage to trigger lazy-loaded manga panels."""
    print("⏳ Scrolling page to trigger lazy-loaded images...")
    await page.evaluate("""
        async () => {
            await new Promise((resolve) => {
                let totalHeight = 0;
                let distance = 400; // Scroll increment
                let timer = setInterval(() => {
                    let scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;

                    if(totalHeight >= scrollHeight) {
                        clearInterval(timer);
                        resolve();
                    }
                }, 150); // Pause briefly to let panels drop in
            });
        }
    """)
    await asyncio.sleep(3) # Extra structural cushion

async def download_chapter(executable_path, chapter_num, url):
    """Download manga panels as raw images and save a full chapter backup PDF."""
    chapter_folder = Path(OUTPUT_DIR) / f"chapter_{chapter_num}"
    images_folder = chapter_folder / "images"
    images_folder.mkdir(parents=True, exist_ok=True)

    pdf_path = chapter_folder / f"chapter_{chapter_num}.pdf"

    launch_args = {}
    if executable_path:
        launch_args["executable_path"] = executable_path

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, **launch_args)
        # Emulate a large desktop screen so images load at max layout scale
        context = await browser.new_context(viewport={"width": 1200, "height": 1800})
        page = await context.new_page()

        try:
            print(f"🌐 Navigating to Chapter {chapter_num}: {url}")
            await page.goto(url, timeout=90000, wait_until="networkidle")
            
            # Counteract lazy-loading
            await scroll_to_bottom(page)

            # 1. Extraction: Pull individual structural manga image assets
            print("📸 Extracting raw panel images...")
            img_urls = await page.evaluate("""
                () => {
                    const imgs = Array.from(document.querySelectorAll('img'));
                    return imgs
                        .map(img => img.src || img.getAttribute('data-src'))
                        .filter(src => src && src.startsWith('http'));
                }
            """)
            
            # Clean and isolate actual chapter content elements (ignores layouts/avatars)
            manga_panels = [u for u in img_urls if "logo" not in u.lower() and "avatar" not in u.lower()]

            # Fetch image tags directly via page evaluation context safely
            for idx, img_url in enumerate(manga_panels, start=1):
                try:
                    img_response = await page.request.get(img_url)
                    if img_response.ok:
                        # Grab file format (jpg/png) or default safely
                        ext = "jpg" if "png" not in img_url.lower() else "png"
                        img_file = images_folder / f"panel_{idx:03d}.{ext}"
                        img_file.write_bytes(await img_response.body())
                except Exception as e:
                    continue # Keep trucking if a single background asset drops out

            print(f"📦 Saved {len(manga_panels)} raw panels to: {images_folder}")

            # 2. Backup Preservation: Output a zero-margin document capture 
            print("🖨️ Generating PDF structural map...")
            await page.pdf(
                path=str(pdf_path), 
                print_background=True, 
                width="1200px", # Wide viewport coordinates keep webtoon images unbroken
                margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
            )
            print(f"✅ Chapter {chapter_num} Complete.")

        except Exception as e:
            print(f"❌ Failed processing Chapter {chapter_num}: {e}")
        finally:
            await browser.close()

async def main():
    csv_path = Path(OUTPUT_DIR) / "chapters_list.csv"
    if not csv_path.exists():
        print(f"❌ Could not find {csv_path}. Please run url_generator.py first.")
        return

    browser_exe = find_browser_executable()
    
    # Parse records out of your compiled CSV file tracker
    chapters = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader) # Skip Header row
        for row in reader:
            if row:
                chapters.append((row[0], row[1]))

    print(f"🚀 Processing {len(chapters)} chapters sequentially to avoid rate-limits...")
    
    # Process sequentially instead of gather() because opening 10 Chrome channels 
    # simultaneously will hammer your network block and cause 403 blocks or out-of-memory errors.
    for ch_num, url in chapters:
        await download_chapter(browser_exe, ch_num, url)

if __name__ == "__main__":
    asyncio.run(main())