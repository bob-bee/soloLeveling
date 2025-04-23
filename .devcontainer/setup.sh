from setuptools import setup, find_packages

setup(
    name="solo-leveling-downloader",
    version="1.0.0",
    description="Manga downloader and converter for Solo Leveling",
    author="bob-bee",
    author_email="geniusfaker@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Add Python dependencies here
        "requests",
        "Pillow",
        "beautifulsoup4"
    ],
    entry_points={
        "console_scripts": [
            "solo-dl=src.main:main"
        ]
    }
)
