import os
from pathlib import Path
import sys
from PIL import Image

# Ensure script can find config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from config import OUTPUT_DIR

def merge_chapter_panels(output_dir):
    output_path = Path(output_dir)
    chapter_folders = sorted(output_path.glob("chapter_*"))
    
    if not chapter_folders:
        print("⚠️ No chapter folders found to merge.")
        return

    print(f"🎨 Stitching panels for {len(chapter_folders)} chapters...")

    for folder in chapter_folders:
        images_dir = folder / "images"
        if not images_dir.exists():
            continue

        # Fetch all cleaned panel images
        panel_files = sorted(list(images_dir.glob("panel_*.*")))
        if not panel_files:
            continue

        print(f"🔄 Processing {folder.name} ({len(panel_files)} panels)...")

        # Load images safely and compute scaling target base width
        images = [Image.open(p) for p in panel_files]
        
        # Use the widest panel's width as the standard matrix frame 
        # (prevents narrow images from getting blurry while keeping layout consistent)
        target_width = max(img.width for img in images)

        resized_images = []
        total_height = 0

        for img in images:
            # Maintain aspect ratio while matching target uniform width
            if img.width != target_width:
                scale_factor = target_width / img.width
                new_height = int(img.height * scale_factor)
                # Use Resampling.LANCZOS for crystal-clear manga text scaling
                img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
            
            resized_images.append(img)
            total_height += img.height

        # Create the unified long vertical canvas asset canvas
        stitched_canvas = Image.new("RGB", (target_width, total_height))

        # Paste panels sequentially downwards
        current_y = 0
        for img in resized_images:
            stitched_canvas.paste(img, (0, current_y))
            current_y += img.height

        # Save output options: Save as an ultra-long PNG image 
        # or convert directly to a single-page scrolling PDF backup
        merged_output_dir = folder / "merged"
        merged_output_dir.mkdir(exist_ok=True)
        
        final_image_path = merged_output_dir / f"{folder.name}_seamless.png"
        final_pdf_path = merged_output_dir / f"{folder.name}_scrollable.pdf"

        # Save high-quality master assets
        stitched_canvas.save(final_image_path, "PNG")
        stitched_canvas.save(final_pdf_path, "PDF", resolution=100.0)

        print(f"✅ Generated seamless view maps: {final_pdf_path.name}")

    print("\n🎉 All chapters have been stitched together seamlessly!")

if __name__ == "__main__":
    target_dir = OUTPUT_DIR if 'OUTPUT_DIR' in globals() else "./output"
    merge_chapter_panels(target_dir)