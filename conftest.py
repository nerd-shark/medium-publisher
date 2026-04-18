"""Root conftest.py — adds medium_publisher/ to sys.path so bare imports
(e.g. ``from utils.exceptions import ...``) used inside the package resolve
correctly when tests are collected from the workspace root.
"""

import sys
from pathlib import Path

_pkg_dir = Path(__file__).resolve().parent / "medium_publisher"
if str(_pkg_dir) not in sys.path:
    sys.path.insert(0, str(_pkg_dir))
