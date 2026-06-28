import os
import glob
from pathlib import Path
import sys

# Ensure script can find config if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from config import OUTPUT_DIR

def remove_last_panel(output_dir):
    output_path = Path(output_dir)
    if not output_path.exists():
        print(f"❌ Output directory {output_path} does not exist.")
        return

    # Find all chapter directories
    chapter_folders = sorted(output_path.glob("chapter_*"))
    
    if not chapter_folders:
        print("⚠️ No chapter folders found to clean.")
        return

    print(f"🧹 Starting cleanup across {len(chapter_folders)} chapters...")

    for folder in chapter_folders:
        images_dir = folder / "images"
        if not images_dir.exists():
            continue

        # Grab all images (matching panel_*.jpg or panel_*.png)
        panel_files = sorted(list(images_dir.glob("panel_*.*")))

        if panel_files:
            # The last element in a sorted list of panels is our target ad
            ad_panel = panel_files[-1]
            
            try:
                os.remove(ad_panel)
                print(f"🗑️ Deleted ad: {ad_panel.relative_to(output_path.parent)}")
            except Exception as e:
                print(f"❌ Failed to delete {ad_panel.name} in {folder.name}: {e}")
        else:
            print(f"ℹ️ No panels found in {folder.name}/images/")

    print("\n🎉 Cleanup complete! All trailing ad panels have been removed.")

if __name__ == "__main__":
    # Fallback to local 'output' if config isn't set up
    target_dir = OUTPUT_DIR if 'OUTPUT_DIR' in globals() else "./output"
    remove_last_panel(target_dir)