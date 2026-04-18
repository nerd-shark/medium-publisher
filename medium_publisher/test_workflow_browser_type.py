"""Test browser type parameter in PublishingWorkflow."""

from core.publishing_workflow import PublishingWorkflow
from core.session_manager import SessionManager

# Test 1: Default browser type (chromium)
print("Test 1: PublishingWorkflow with default browser type")
config = {"browser": {"headless": False, "timeout_seconds": 30}}
session_manager = SessionManager()
workflow1 = PublishingWorkflow(config, session_manager)
print(f"  browser_type = {workflow1.browser_type}")
assert workflow1.browser_type == "chromium", "Default should be chromium"
print("  ✓ PASS")

# Test 2: Firefox browser type
print("\nTest 2: PublishingWorkflow with firefox browser type")
workflow2 = PublishingWorkflow(config, session_manager, browser_type="firefox")
print(f"  browser_type = {workflow2.browser_type}")
assert workflow2.browser_type == "firefox", "Should be firefox"
print("  ✓ PASS")

# Test 3: Chromium browser type (explicit)
print("\nTest 3: PublishingWorkflow with chromium browser type (explicit)")
workflow3 = PublishingWorkflow(config, session_manager, browser_type="chromium")
print(f"  browser_type = {workflow3.browser_type}")
assert workflow3.browser_type == "chromium", "Should be chromium"
print("  ✓ PASS")

print("\n✅ All workflow tests passed!")
