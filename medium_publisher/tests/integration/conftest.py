"""
Integration test configuration and fixtures.

This module provides shared fixtures and configuration for integration tests.
Integration tests interact with real browsers and external services.
"""

import os
import pytest
from pathlib import Path
from typing import Optional

# Integration test marker
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (requires --integration flag)"
    )

def pytest_collection_modifyitems(config, items):
    """Skip integration tests unless --integration flag is provided."""
    if not config.getoption("--integration"):
        skip_integration = pytest.mark.skip(reason="need --integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)

def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests"
    )
    parser.addoption(
        "--medium-email",
        action="store",
        default=None,
        help="Medium account email for testing"
    )
    parser.addoption(
        "--medium-password",
        action="store",
        default=None,
        help="Medium account password for testing"
    )

@pytest.fixture(scope="session")
def test_credentials(request):
    """
    Get test account credentials from environment or command line.
    
    Returns:
        dict: Credentials with 'email' and 'password' keys
    """
    email = request.config.getoption("--medium-email") or os.getenv("MEDIUM_TEST_EMAIL")
    password = request.config.getoption("--medium-password") or os.getenv("MEDIUM_TEST_PASSWORD")
    
    if not email or not password:
        pytest.skip("Test credentials not provided. Set MEDIUM_TEST_EMAIL and MEDIUM_TEST_PASSWORD environment variables.")
    
    return {
        "email": email,
        "password": password
    }

@pytest.fixture(scope="session")
def test_config():
    """
    Get test configuration.
    
    Returns:
        dict: Test configuration
    """
    return {
        "typing": {
            "speed_ms": 10,  # Fast typing for tests
            "paragraph_delay_ms": 50,
            "max_chars_per_minute": 35,
            "human_typing_enabled": True,
            "typo_frequency": "low"
        },
        "publishing": {
            "default_mode": "draft",
            "auto_add_tags": True,
            "max_tags": 5
        },
        "browser": {
            "headless": False,  # Visible for debugging
            "timeout_seconds": 30
        }
    }

@pytest.fixture
def test_article_path(tmp_path):
    """
    Create a test markdown article.
    
    Returns:
        Path: Path to test article
    """
    article_content = """---
title: Test Article for Integration Testing
subtitle: This is a test subtitle
tags:
  - testing
  - automation
  - medium
---

# Introduction

This is a test article for integration testing.

## Section 1

This section contains **bold text** and *italic text*.

## Section 2

This section contains a code block:

```python
def hello_world():
    print("Hello, World!")
```

## Conclusion

This is the conclusion of the test article.
"""
    
    article_path = tmp_path / "test_article.md"
    article_path.write_text(article_content)
    return article_path

@pytest.fixture
def test_article_v2_path(tmp_path):
    """
    Create a test markdown article version 2.
    
    Returns:
        Path: Path to test article v2
    """
    article_content = """---
title: Test Article for Integration Testing
subtitle: This is an updated test subtitle
tags:
  - testing
  - automation
  - medium
  - updated
---

# Introduction

This is an updated test article for integration testing.

## Section 1

This section contains **bold text**, *italic text*, and `inline code`.

## New Section

This is a new section added in version 2.

## Section 2

This section contains an updated code block:

```python
def hello_world():
    print("Hello, World!")
    print("This is version 2!")
```

## Conclusion

This is the updated conclusion of the test article.
"""
    
    article_path = tmp_path / "test_article_v2.md"
    article_path.write_text(article_content)
    return article_path
