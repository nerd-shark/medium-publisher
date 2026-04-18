"""
Platform abstraction layer for multi-platform publishing.

This package provides a unified interface for publishing to different platforms
(Medium, Substack, etc.) using the Strategy Pattern.
"""

from .platform_interface import PlatformInterface
from .platform_factory import PlatformFactory

__all__ = ["PlatformInterface", "PlatformFactory"]
