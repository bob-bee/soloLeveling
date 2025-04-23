# src/main.py

from src import url_generator, downloader, converter

def main():
    print("🚀 Starting data pipeline...")

    print("🔗 Generating URLs...")
    urls = url_generator.generate_urls()

    print("⬇️  Downloading content...")
    downloader.download_all(urls)

    print("🔄 Converting downloaded content...")
    converter.convert_all()

    print("✅ All done!")

if __name__ == "__main__":
    main()
