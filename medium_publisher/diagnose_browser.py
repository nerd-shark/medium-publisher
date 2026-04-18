"""
Diagnose browser automation issues on Windows.
"""

import sys
import subprocess

print("=" * 80)
print("Browser Automation Diagnostics")
print("=" * 80)

# Check 1: Firefox installed
print("\n1. Checking Firefox installation...")
try:
    result = subprocess.run(
        ['where', 'firefox'],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        print(f"   ✓ Firefox found: {result.stdout.strip()}")
    else:
        print("   ✗ Firefox not found in PATH")
except Exception as e:
    print(f"   ✗ Error checking Firefox: {e}")

# Check 2: GeckoDriver
print("\n2. Checking GeckoDriver...")
try:
    result = subprocess.run(
        ['where', 'geckodriver'],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        print(f"   ✓ GeckoDriver found: {result.stdout.strip()}")
    else:
        print("   ✗ GeckoDriver not found in PATH")
        print("   → Download from: https://github.com/mozilla/geckodriver/releases")
except Exception as e:
    print(f"   ✗ Error checking GeckoDriver: {e}")

# Check 3: Try launching Firefox directly
print("\n3. Testing Firefox launch (will open browser window)...")
try:
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    
    options = Options()
    # Don't use headless - we want to see if window opens
    
    print("   Attempting to launch Firefox...")
    driver = webdriver.Firefox(options=options)
    print("   ✓ Firefox launched successfully!")
    print("   → Browser window should be visible")
    
    input("   Press Enter to close browser...")
    driver.quit()
    print("   ✓ Browser closed")
    
except Exception as e:
    print(f"   ✗ Firefox launch failed: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    print("\n   Full traceback:")
    traceback.print_exc()

print("\n" + "=" * 80)
print("Diagnostics complete")
print("=" * 80)
