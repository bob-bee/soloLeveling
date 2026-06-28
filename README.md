# Solo Leveling Ad-Free Webtoon Processor

A robust web scraping and automation pipeline designed to extract *Solo Leveling* chapters from webtoon aggregators, strip out annoying trailing advertisement panels, seamlessly stitch the long vertical layouts, and compile them into a beautiful, interactive, self-hosted web viewer.

---

## 📂 Project Architecture & Components

```text
.
├── output/                  # Generated assets and web viewer
│   ├── chapter_X/           # Raw downloaded panels and backups per chapter
│   ├── chapters_list.csv    # Scraped target URLs from the generator
│   └── viewer.html          # Custom, auto-scrolling browser interface
├── src/                     # Core execution source code
│   ├── config.py            # Global variables, base paths, and configuration
│   ├── url_generator.py     # Stage 1: Scrapes index pages to extract chapter URLs
│   ├── downloader.py        # Stage 2: Headless Playwright engine (handles lazy-loading)
│   ├── cleanChapters.py     # Stage 3: Dynamic optimization (removes trailing ad panels)
│   ├── mergePanels.py       # Stage 4: Pillow canvas stitcher (makes vertical strips)
│   └── main.py              # Orchestration: Executes the entire pipeline sequentially
├── README.md                # Documentation and guide
└── requirements.txt         # Virtual environment dependencies

```

### Script Directory Reference (`src/`)

* **`main.py`**: The central brain. Run this to automatically execute Stages 1 through 4 in sequence and deploy the web viewer.
* **`config.py`**: Houses directory declarations (`OUTPUT_DIR`) and the `BASE_URL` target.
* **`url_generator.py`**: Parses the target site using `BeautifulSoup4` and `re` matching patterns, generating `output/chapters_list.csv`.
* **`downloader.py`**: Launches an automated browser context (`Playwright`), mimics a human scrolling down to defeat lazy-loading, downloads raw images (`.jpg`/`.png`), and outputs a basic PDF backup layout.
* **`cleanChapters.py`**: Scans the sorted image directories and dynamically trims the absolute final panel (`panel_XYZ`) from each folder to remove ads.
* **`mergePanels.py`**: Uses `Pillow` (PIL) to scale all panels to a uniform resolution width and stitch them top-to-bottom into an ultra-long, seamless image asset.

*(Note: Legacy files like `converter.py`, `analyzer.py`, and `merge.py` are preserved legacy structures from older EPUB generation formats).*

---

## 🛠️ Step-by-Step Installation & Commands

Follow these commands in your terminal to set up your virtual environment, satisfy dependencies, and manage the pipeline.

### 1. Initialize and Activate Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate

```

### 2. Install Project Dependencies

```bash
pip install -r requirements.txt
# If requirements.txt is empty, run:
pip install requests beautifulsoup4 pillow playwright

```

### 3. Install Playwright Web Engines & Fix Linux 26.04 Bypasses

Playwright might complain about explicit system mapping if you are on a very new Linux environment. Use this override command to force a compatible Chromium installation:

```bash
PLAYWRIGHT_HOST_PLATFORM_OVERRIDE=ubuntu24.04-x64 python3 -m playwright install chromium

```

*Alternatively, ensure your system's native Chromium or Brave build is mapped (the downloader will automatically search for `/usr/bin/chromium-browser` or `brave` as a backup).*

### 4. Run the Entire Automated Pipeline

To run everything sequentially (URL Extraction ➡️ Image Download ➡️ Ad Cleanup ➡️ Panel Stitching ➡️ Viewer Deployment), execute:

```bash
python3 src/main.py

```

---

## 🔍 Independent Sub-Module Execution (Debugging)

If your network drops, a specific chapter breaks, or you want to fix a single component without re-downloading gigabytes of image files, you can run stages completely independently:

* **To re-extract URLs to CSV:**
```bash
python3 src/url_generator.py

```


* **To restart downloading missing raw panels:**
```bash
python3 src/downloader.py

```


* **To re-run the ad cleanup filter:**
```bash
python3 src/cleanChapters.py

```


* **To force-restitch raw panels into seamless images:**
```bash
python3 src/mergePanels.py

```



---

## 🖥️ Reading the Manga

Once `main.py` finishes running, it outputs a self-contained local application entrypoint at `output/viewer.html`.

1. Simply navigate to your `output/` directory in your file explorer.
2. Double-click **`viewer.html`** to open it in Chrome, Brave, or Firefox.
3. Select a chapter from the top dropdown, set your speed slider, and tap **`Auto Scroll`** (or hit `Spacebar`) for a smooth, hands-free, infinite-scrolling reading experience!

```

```