import os
import sys
import asyncio
from pathlib import Path

# Add project root directory to path mapping array
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import optimized pipeline modules
from src.url_generator import main as run_url_generator
from src.downloader import main as run_downloader
from src.cleanChapters import remove_last_panel
from src.mergePanels import merge_chapter_panels
from config import OUTPUT_DIR

def generate_viewer_html():
    """Dynamically drops the infinite scroll HTML viewer layout directly inside output folder."""
    viewer_path = Path(OUTPUT_DIR) / "viewer.html"
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solo Leveling Infinity Viewer</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #0b0c10; color: #c5a059; font-family: sans-serif; overflow-x: hidden; }
        #toolbar { position: fixed; top: 0; left: 0; width: 100%; background: rgba(11, 12, 16, 0.95); border-bottom: 2px solid #1f2833; display: flex; align-items: center; justify-content: center; gap: 20px; padding: 12px; z-index: 1000; }
        select, button { background: #1f2833; color: #45f3ff; border: 1px solid #45f3ff; padding: 8px 16px; font-weight: bold; border-radius: 4px; cursor: pointer; }
        select:hover, button:hover { background: #45f3ff; color: #1f2833; }
        #manga-container { margin-top: 70px; display: flex; flex-direction: column; align-items: center; width: 100%; }
        .manga-strip { width: 100%; max-width: 800px; height: auto; display: block; box-shadow: 0 0 30px rgba(0,0,0,0.8); }
        #status-msg { margin: 100px auto; font-size: 18px; color: #66fcf1; text-align: center; }
    </style>
</head>
<body>
    <div id="toolbar">
        <select id="chapter-select" onchange="loadChapter(this.value)">
            <option value="">-- Choose Chapter --</option>
        </select>
        <button id="play-btn" onclick="toggleAutoScroll()">▶ Auto Scroll</button>
        <input type="range" id="speed-slider" min="1" max="10" value="3" onchange="updateSpeed()">
    </div>
    <div id="manga-container">
        <div id="status-msg">Select a chapter to begin...</div>
    </div>
    <script>
        let scrollInterval = null, isScrolling = false, scrollSpeed = 3;
        const selectMenu = document.getElementById('chapter-select');
        
        // Dynamically looks for chapters 1 to 10 inside directory
        for (let i = 1; i <= 10; i++) {
            const opt = document.createElement('option');
            opt.value = `chapter_${i}/merged/chapter_${i}_seamless.png`;
            opt.innerHTML = `Chapter ${i}`;
            selectMenu.appendChild(opt);
        }

        function loadChapter(imagePath) {
            const container = document.getElementById('manga-container');
            if (!imagePath) { container.innerHTML = '<div id="status-msg">Select a chapter to begin...</div>'; return; }
            const img = new Image();
            img.className = 'manga-strip';
            img.src = imagePath;
            img.onload = () => { container.innerHTML = ''; container.appendChild(img); window.scrollTo({top: 0}); };
            img.onerror = () => { container.innerHTML = '<div id="status-msg" style="color:red;">❌ Chapter image not found. Run processing steps!</div>'; };
        }

        function toggleAutoScroll() {
            const btn = document.getElementById('play-btn');
            if (isScrolling) {
                clearInterval(scrollInterval);
                btn.innerHTML = "▶ Auto Scroll";
            } else {
                scrollInterval = setInterval(() => { window.scrollBy(0, scrollSpeed); }, 30);
                btn.innerHTML = "⏸ Pause";
            }
            isScrolling = !isScrolling;
        }

        function updateSpeed() {
            scrollSpeed = parseInt(document.getElementById('speed-slider').value);
            if (isScrolling) { toggleAutoScroll(); toggleAutoScroll(); }
        }
    </script>
</body>
</html>
"""
    with open(viewer_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"🖥️  Webtoon Canvas Engine deployed at: {viewer_path}")


def main():
    print("⚡ Entering Shadow Monarch Data Pipeline Framework...")
    print("====================================================")

    # Step 1: Scrape & Build targets inside your chapters_list.csv file tracking loop
    print("\n🔗 [STAGE 1/5]: Scraping host domains for chapters tracking array...")
    run_url_generator()

    # Step 2: Trigger Headless Playwright/Chrome browser engine elements sequentially
    print("\n⬇️  [STAGE 2/5]: Initializing browser viewport downloads...")
    asyncio.run(run_downloader())

    # Step 3: Parse chapter images array blocks and target trailing advertisement banners
    print("\n🧹 [STAGE 3/5]: Running image correction matrix and dropping trailing promotional ads...")
    remove_last_panel(OUTPUT_DIR)

    # Step 4: Scale asset ratios using Pillow engine and stitch panels vertically
    print("\n🎨 [STAGE 4/5]: Running continuous image stitching scripts...")
    merge_chapter_panels(OUTPUT_DIR)

    # Step 5: Output local custom interactive interface architecture framework maps
    print("\n⚙️  [STAGE 5/5]: Exporting static interface distribution layout files...")
    generate_viewer_html()

    print("\n====================================================")
    print("🎉 PIPELINE RUN COMPLETE!")
    print(f"💡 Open '{Path(OUTPUT_DIR)/'viewer.html'}' in any modern web browser to read.")

if __name__ == "__main__":
    main()