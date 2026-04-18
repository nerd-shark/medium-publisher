"""Configuration management for Medium Article Publisher.

This module provides configuration loading, saving, and validation functionality.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class ConfigManager:
    """Manages application configuration with load/save/validation."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize ConfigManager.
        
        Args:
            config_dir: Directory containing config files. Defaults to package config/.
        """
        if config_dir is None:
            # Default to package config directory
            package_root = Path(__file__).parent.parent
            config_dir = package_root / "config"
        
        self.config_dir = Path(config_dir)
        self.config: Dict[str, Any] = {}
        
        # User config directory (for overrides)
        self.user_config_dir = Path.home() / ".medium_publisher"
        self.user_config_dir.mkdir(exist_ok=True)
        
        self.default_config_path = self.config_dir / "default_config.yaml"
        self.user_config_path = self.user_config_dir / "config.yaml"

    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from default and user config files.
        
        Loads default config first, then overlays user config if it exists.
        
        Returns:
            Merged configuration dictionary.
            
        Raises:
            FileNotFoundError: If default config file not found.
            yaml.YAMLError: If config file is invalid YAML.
        """
        # Load default config
        if not self.default_config_path.exists():
            raise FileNotFoundError(
                f"Default config not found: {self.default_config_path}"
            )
        
        with open(self.default_config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f) or {}
        
        # Overlay user config if exists
        if self.user_config_path.exists():
            with open(self.user_config_path, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f) or {}
                self._merge_config(self.config, user_config)
        
        # Validate loaded config
        self._validate_config()
        
        return self.config

    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Save configuration to user config file.
        
        Args:
            config: Configuration to save. If None, saves current config.
            
        Raises:
            yaml.YAMLError: If config cannot be serialized to YAML.
        """
        if config is not None:
            self.config = config
        
        # Validate before saving
        self._validate_config()
        
        with open(self.user_config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(self.config, f, default_flow_style=False, sort_keys=False)

    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.
        
        Supports nested keys using dot notation (e.g., 'typing.speed_ms').
        
        Args:
            key: Configuration key (supports dot notation).
            default: Default value if key not found.
            
        Returns:
            Configuration value or default.
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by key.
        
        Supports nested keys using dot notation (e.g., 'typing.speed_ms').
        
        Args:
            key: Configuration key (supports dot notation).
            value: Value to set.
        """
        keys = key.split('.')
        config = self.config
        
        # Navigate to nested dict, creating if needed
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value

    
    def _merge_config(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> None:
        """Merge overlay config into base config (in-place).
        
        Args:
            base: Base configuration dictionary (modified in-place).
            overlay: Overlay configuration dictionary.
        """
        for key, value in overlay.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                # Recursively merge nested dicts
                self._merge_config(base[key], value)
            else:
                # Override value
                base[key] = value
    
    def _validate_config(self) -> None:
        """Validate configuration values.
        
        Validates all config sections: typing, publishing, safety, navigation, ui, assets.
        
        Raises:
            ValueError: If configuration is invalid.
        """
        # --- Typing settings ---
        base_delay = self.get('typing.base_delay_ms')
        if base_delay is not None:
            if not isinstance(base_delay, (int, float)) or base_delay <= 0:
                raise ValueError(
                    f"typing.base_delay_ms must be > 0, got {base_delay}"
                )

        variation = self.get('typing.variation_percent')
        if variation is not None:
            if not isinstance(variation, (int, float)) or variation < 0 or variation > 100:
                raise ValueError(
                    f"typing.variation_percent must be between 0 and 100, got {variation}"
                )

        typo_freq = self.get('typing.typo_frequency')
        if typo_freq is not None:
            if typo_freq not in ['low', 'medium', 'high']:
                raise ValueError(
                    f"typing.typo_frequency must be 'low', 'medium', or 'high', got {typo_freq}"
                )

        correction_ratio = self.get('typing.immediate_correction_ratio')
        if correction_ratio is not None:
            if not isinstance(correction_ratio, (int, float)) or correction_ratio < 0.0 or correction_ratio > 1.0:
                raise ValueError(
                    f"typing.immediate_correction_ratio must be between 0.0 and 1.0, got {correction_ratio}"
                )

        # --- Publishing settings ---
        publish_mode = self.get('publishing.default_mode')
        if publish_mode is not None:
            if publish_mode not in ['draft', 'public']:
                raise ValueError(
                    f"publishing.default_mode must be 'draft' or 'public', got {publish_mode}"
                )

        max_tags = self.get('publishing.max_tags')
        if max_tags is not None:
            if not isinstance(max_tags, int) or max_tags < 1 or max_tags > 5:
                raise ValueError(
                    f"publishing.max_tags must be between 1 and 5, got {max_tags}"
                )

        # --- Safety settings ---
        countdown = self.get('safety.countdown_seconds')
        if countdown is not None:
            if not isinstance(countdown, (int, float)) or countdown <= 0:
                raise ValueError(
                    f"safety.countdown_seconds must be > 0, got {countdown}"
                )

        # --- Navigation settings ---
        confidence = self.get('navigation.screen_confidence')
        if confidence is not None:
            if not isinstance(confidence, (int, float)) or confidence < 0.0 or confidence > 1.0:
                raise ValueError(
                    f"navigation.screen_confidence must be between 0.0 and 1.0, got {confidence}"
                )

        poll_interval = self.get('navigation.poll_interval_seconds')
        if poll_interval is not None:
            if not isinstance(poll_interval, (int, float)) or poll_interval <= 0:
                raise ValueError(
                    f"navigation.poll_interval_seconds must be > 0, got {poll_interval}"
                )

        login_timeout = self.get('navigation.login_timeout_seconds')
        if login_timeout is not None:
            if not isinstance(login_timeout, (int, float)) or login_timeout <= 0:
                raise ValueError(
                    f"navigation.login_timeout_seconds must be > 0, got {login_timeout}"
                )

        page_load_timeout = self.get('navigation.page_load_timeout_seconds')
        if page_load_timeout is not None:
            if not isinstance(page_load_timeout, (int, float)) or page_load_timeout <= 0:
                raise ValueError(
                    f"navigation.page_load_timeout_seconds must be > 0, got {page_load_timeout}"
                )
