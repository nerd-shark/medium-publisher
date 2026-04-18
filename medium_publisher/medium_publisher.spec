# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File for Medium Article Publisher

This spec file configures PyInstaller to build a Windows executable
for the Medium Article Publisher application.

Build command:
    pyinstaller medium_publisher.spec

Output:
    dist/MediumArticlePublisher.exe
"""

import sys
from pathlib import Path

# Get the project root directory
project_root = Path('.').absolute()

# Analysis: Collect all Python files and dependencies
a = Analysis(
    ['main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # Include configuration files
        ('config/default_config.yaml', 'config'),
        ('config/selectors.yaml', 'config'),
        
        # Include documentation
        ('README.md', '.'),
        
        # Include Playwright browsers (will be downloaded separately)
        # Note: Playwright browsers are large (~300MB), users should run
        # 'playwright install chromium' after installation
    ],
    hiddenimports=[
        # PyQt6 modules
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        
        # Playwright and async
        'playwright',
        'playwright.async_api',
        'playwright._impl',
        'playwright._impl._api_structures',
        'playwright._impl._browser',
        'playwright._impl._browser_context',
        'playwright._impl._page',
        'playwright._impl._element_handle',
        'playwright._impl._frame',
        'playwright._impl._network',
        'playwright._impl._playwright',
        'playwright._impl._transport',
        'playwright._impl._connection',
        'playwright._impl._helper',
        'playwright._impl._errors',
        'asyncio',
        'asyncio.events',
        'asyncio.futures',
        'asyncio.tasks',
        'asyncio.locks',
        'asyncio.queues',
        'asyncio.streams',
        'asyncio.subprocess',
        
        # Markdown and YAML
        'markdown2',
        'yaml',
        
        # Keyring for credential storage
        'keyring',
        'keyring.backends',
        'keyring.backends.Windows',
        
        # Application modules
        'ui',
        'ui.main_window',
        'ui.settings_dialog',
        'ui.progress_widget',
        'ui.file_selector',
        'ui.log_widget',
        'core',
        'core.article_parser',
        'core.markdown_processor',
        'core.change_parser',
        'core.config_manager',
        'core.session_manager',
        'core.publishing_workflow',
        'core.version_update_workflow',
        'core.batch_publishing_workflow',
        'automation',
        'automation.playwright_controller',
        'automation.medium_editor',
        'automation.auth_handler',
        'automation.content_typer',
        'automation.rate_limiter',
        'automation.human_typing_simulator',
        'utils',
        'utils.logger',
        'utils.validators',
        'utils.exceptions',
        'utils.error_recovery',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude test modules
        'tests',
        'pytest',
        'pytest_asyncio',
        'pytest_qt',
        'pytest_cov',
        
        # Exclude development tools
        'black',
        'ruff',
        'mypy',
        
        # Exclude unnecessary modules
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
    ],
    noarchive=False,
)

# PYZ: Create Python archive
pyz = PYZ(a.pure)

# EXE: Create executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MediumArticlePublisher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI application)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # TODO: Add application icon
    version_file=None,  # TODO: Add version info file
)

# COLLECT: Collect all files for distribution
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MediumArticlePublisher',
)
