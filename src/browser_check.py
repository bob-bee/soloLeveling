import subprocess
import shutil
import sys
import os
import platform

def check_chrome(exit_on_fail=True) -> bool:
    """Check if Chrome or Chromium is installed and print its version."""
    chrome_path = "/usr/bin/chromium-browser"  # Path to Chromium installed in Codespace
    
    if chrome_path:
        try:
            result = subprocess.run([chrome_path, "--version"], capture_output=True, text=True)
            print(f"🧭 Chrome/Chromium Version: {result.stdout.strip()}")
            return True
        except Exception as e:
            print(f"⚠️ Error while checking version: {e}")
    else:
        print("❌ Chrome/Chromium is not installed or not found in PATH.")
    
    if exit_on_fail:
        sys.exit(1)
    return False

def check_brave(exit_on_fail=True) -> bool:
    """Check if Brave is installed and print its version."""
    if platform.system() == "Windows":
        brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    else:
        brave_path = shutil.which("brave")

    if brave_path and os.path.exists(brave_path):
        try:
            result = subprocess.run([brave_path, "--version"], capture_output=True, text=True)
            print(f"🦁 Brave Version: {result.stdout.strip()}")
            return True
        except Exception as e:
            print(f"⚠️ Error while checking Brave version: {e}")
    else:
        print("❌ Brave is not installed or not found in PATH.")

    if exit_on_fail:
        sys.exit(1)
    return False

if __name__ == "__main__":
    print("🔍 Checking browsers...")
    chrome_ok = check_chrome(exit_on_fail=False)
    brave_ok = check_brave(exit_on_fail=False)
    if chrome_ok:
        print("✅ Chrome/Chromium is available.")
    else:
        print("❌ Chrome/Chromium is not available.")

    if brave_ok:
        print("✅ Brave is available.")
    else:
        print("❌ Brave is not available.")

    # If neither browser is available, exit
    if not chrome_ok and not brave_ok:
        print("🚫 Neither Chrome nor Brave is available. Exiting.")
        sys.exit(1)
    else:
        print("✅ Browser check complete.")
