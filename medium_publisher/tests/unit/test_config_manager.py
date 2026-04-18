"""Unit tests for ConfigManager."""

import pytest
import tempfile
from pathlib import Path
import yaml

from medium_publisher.core.config_manager import ConfigManager


@pytest.fixture
def default_config():
    """Return a valid default config matching the new schema."""
    return {
        'typing': {
            'base_delay_ms': 200,
            'variation_percent': 30,
            'human_typing_enabled': True,
            'typo_frequency': 'low',
            'immediate_correction_ratio': 0.70,
            'thinking_pause_min_ms': 500,
            'thinking_pause_max_ms': 2000,
            'paragraph_pause_min_ms': 1000,
            'paragraph_pause_max_ms': 3000,
        },
        'publishing': {
            'default_mode': 'draft',
            'max_tags': 5,
        },
        'safety': {
            'emergency_stop_hotkey': 'ctrl+shift+escape',
            'countdown_seconds': 3,
            'focus_check_enabled': True,
        },
        'navigation': {
            'screen_confidence': 0.8,
            'poll_interval_seconds': 2,
            'login_timeout_seconds': 300,
            'page_load_timeout_seconds': 30,
            'google_account_email': 'user@example.com',
        },
        'ui': {
            'always_on_top': True,
            'remember_window_position': True,
            'remember_last_directory': True,
        },
        'assets': {
            'reference_images_dir': 'assets/medium/',
        },
    }


@pytest.fixture
def temp_config_dir(default_config):
    """Create temporary config directory with new schema defaults."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir) / "config"
        config_dir.mkdir()

        with open(config_dir / "default_config.yaml", 'w') as f:
            yaml.safe_dump(default_config, f)

        yield config_dir


class TestConfigManager:
    """Test ConfigManager functionality."""

    def test_init(self, temp_config_dir):
        """Test ConfigManager initialization."""
        manager = ConfigManager(config_dir=temp_config_dir)
        assert manager.config_dir == temp_config_dir
        assert manager.config == {}

    def test_load_config(self, temp_config_dir):
        """Test loading configuration."""
        manager = ConfigManager(config_dir=temp_config_dir)
        manager.user_config_dir = temp_config_dir / "user"
        manager.user_config_dir.mkdir(exist_ok=True)
        manager.user_config_path = manager.user_config_dir / "config.yaml"

        config = manager.load_config()

        assert config['typing']['base_delay_ms'] == 200
        assert config['typing']['variation_percent'] == 30
        assert config['typing']['typo_frequency'] == 'low'
        assert config['typing']['immediate_correction_ratio'] == 0.70
        assert config['publishing']['default_mode'] == 'draft'
        assert config['safety']['countdown_seconds'] == 3
        assert config['navigation']['screen_confidence'] == 0.8
        assert config['ui']['always_on_top'] is True
        assert config['assets']['reference_images_dir'] == 'assets/medium/'

    def test_get_config_value(self, temp_config_dir):
        """Test getting config values with dot notation."""
        manager = ConfigManager(config_dir=temp_config_dir)
        manager.user_config_dir = temp_config_dir / "user"
        manager.user_config_dir.mkdir(exist_ok=True)
        manager.user_config_path = manager.user_config_dir / "config.yaml"

        manager.load_config()

        assert manager.get('typing.base_delay_ms') == 200
        assert manager.get('safety.countdown_seconds') == 3
        assert manager.get('navigation.screen_confidence') == 0.8
        assert manager.get('nonexistent.key', 'default') == 'default'

    def test_set_config_value(self, temp_config_dir):
        """Test setting config values with dot notation."""
        manager = ConfigManager(config_dir=temp_config_dir)
        manager.user_config_dir = temp_config_dir / "user"
        manager.user_config_dir.mkdir(exist_ok=True)
        manager.user_config_path = manager.user_config_dir / "config.yaml"
        manager.load_config()

        manager.set('typing.base_delay_ms', 150)
        assert manager.get('typing.base_delay_ms') == 150

        manager.set('new.nested.key', 'value')
        assert manager.get('new.nested.key') == 'value'

    def test_save_config(self, temp_config_dir):
        """Test saving configuration."""
        manager = ConfigManager(config_dir=temp_config_dir)
        manager.user_config_dir = temp_config_dir / "user"
        manager.user_config_dir.mkdir(exist_ok=True)
        manager.user_config_path = manager.user_config_dir / "config.yaml"
        manager.load_config()

        manager.set('typing.base_delay_ms', 150)
        manager.save_config()

        assert manager.user_config_path.exists()

        manager2 = ConfigManager(config_dir=temp_config_dir)
        manager2.user_config_dir = manager.user_config_dir
        manager2.user_config_path = manager.user_config_path
        manager2.load_config()
        assert manager2.get('typing.base_delay_ms') == 150

    def test_merge_config(self, temp_config_dir):
        """Test config merging."""
        manager = ConfigManager(config_dir=temp_config_dir)

        base = {'a': 1, 'b': {'c': 2, 'd': 3}}
        overlay = {'b': {'c': 99}, 'e': 4}

        manager._merge_config(base, overlay)

        assert base['a'] == 1
        assert base['b']['c'] == 99
        assert base['b']['d'] == 3
        assert base['e'] == 4

    def test_missing_default_config(self, temp_config_dir):
        """Test error when default config missing."""
        (temp_config_dir / "default_config.yaml").unlink()

        manager = ConfigManager(config_dir=temp_config_dir)
        with pytest.raises(FileNotFoundError, match="Default config not found"):
            manager.load_config()


class TestConfigValidation:
    """Test config validation for new schema fields."""

    def test_validate_base_delay_invalid(self, temp_config_dir):
        """Test validation rejects base_delay_ms <= 0."""
        manager = ConfigManager(config_dir=temp_config_dir)
        manager.user_config_dir = temp_config_dir / "user"
        manager.user_config_dir.mkdir(exist_ok=True)
        manager.user_config_path = manager.user_config_dir / "config.yaml"
        manager.load_config()

        manager.set('typing.base_delay_ms', 0)
        with pytest.raises(ValueError, match="typing.base_delay_ms must be > 0"):
            manager._validate_config()

        manager.set('typing.base_delay_ms', -10)
        with pytest.raises(ValueError, match="typing.base_delay_ms must be > 0"):
            manager._validate_config()

    def test_validate_variation_percent_bounds(self, temp_config_dir):
        """Test validation rejects variation_percent outside 0-100."""
        manager = ConfigManager(config_dir=temp_config_dir)
        manager.user_config_dir = temp_config_dir / "user"
        manager.user_config_dir.mkdir(exist_ok=True)
        manager.user_config_path = manager.user_config_dir / "config.yaml"
        manager.load_config()

        manager.set('typing.variation_percent', -1)
        with pytest.raises(ValueError, match="typing.variation_percent must be between 0 and 100"):
            manager._validate_config()

        manager.set('typing.variation_percent', 101)
        with pytest.raises(ValueError, match="typing.variation_percent must be between 0 and 100"):
            manager._validate_config()

    def test_validate_typo_frequency(self, temp_config_dir):
        """Test validation rejects invalid typo_frequency."""
        manager = ConfigManager(config_dir=temp_config_dir)
        manager.user_config_dir = temp_config_dir / "user"
        manager.user_config_dir.mkdir(exist_ok=True)
        manager.user_config_path = manager.user_config_dir / "config.yaml"
        manager.load_config()

        manager.set('typing.typo_frequency', 'invalid')
        with pytest.raises(ValueError, match="typing.typo_frequency must be"):
            manager._validate_config()

    def test_validate_immediate_correction_ratio(self, temp_config_dir):
        """Test validation rejects correction ratio outside 0.0-1.0."""
        manager = ConfigManager(config_dir=temp_config_dir)
        manager.user_config_dir = temp_config_dir / "user"
        manager.user_config_dir.mkdir(exist_ok=True)
        manager.user_config_path = manager.user_config_dir / "config.yaml"
        manager.load_config()

        manager.set('typing.immediate_correction_ratio', 1.5)
        with pytest.raises(ValueError, match="typing.immediate_correction_ratio must be between 0.0 and 1.0"):
            manager._validate_config()

        manager.set('typing.immediate_correction_ratio', -0.1)
        with pytest.raises(ValueError, match="typing.immediate_correction_ratio must be between 0.0 and 1.0"):
            manager._validate_config()

    def test_validate_publish_mode(self, temp_config_dir):
        """Test validation rejects invalid publish mode."""
        manager = ConfigManager(config_dir=temp_config_dir)
        manager.user_config_dir = temp_config_dir / "user"
        manager.user_config_dir.mkdir(exist_ok=True)
        manager.user_config_path = manager.user_config_dir / "config.yaml"
        manager.load_config()

        manager.set('publishing.default_mode', 'invalid')
        with pytest.raises(ValueError, match="publishing.default_mode must be"):
            manager._validate_config()

    def test_validate_max_tags(self, temp_config_dir):
        """Test validation rejects max_tags outside 1-5."""
        manager = ConfigManager(config_dir=temp_config_dir)
        manager.user_config_dir = temp_config_dir / "user"
        manager.user_config_dir.mkdir(exist_ok=True)
        manager.user_config_path = manager.user_config_dir / "config.yaml"
        manager.load_config()

        manager.set('publishing.max_tags', 10)
        with pytest.raises(ValueError, match="publishing.max_tags must be between 1 and 5"):
            manager._validate_config()

    def test_validate_countdown_seconds(self, temp_config_dir):
        """Test validation rejects countdown_seconds <= 0."""
        manager = ConfigManager(config_dir=temp_config_dir)
        manager.user_config_dir = temp_config_dir / "user"
        manager.user_config_dir.mkdir(exist_ok=True)
        manager.user_config_path = manager.user_config_dir / "config.yaml"
        manager.load_config()

        manager.set('safety.countdown_seconds', 0)
        with pytest.raises(ValueError, match="safety.countdown_seconds must be > 0"):
            manager._validate_config()

    def test_validate_screen_confidence(self, temp_config_dir):
        """Test validation rejects screen_confidence outside 0.0-1.0."""
        manager = ConfigManager(config_dir=temp_config_dir)
        manager.user_config_dir = temp_config_dir / "user"
        manager.user_config_dir.mkdir(exist_ok=True)
        manager.user_config_path = manager.user_config_dir / "config.yaml"
        manager.load_config()

        manager.set('navigation.screen_confidence', 1.5)
        with pytest.raises(ValueError, match="navigation.screen_confidence must be between 0.0 and 1.0"):
            manager._validate_config()

        manager.set('navigation.screen_confidence', -0.1)
        with pytest.raises(ValueError, match="navigation.screen_confidence must be between 0.0 and 1.0"):
            manager._validate_config()

    def test_validate_valid_config_passes(self, temp_config_dir):
        """Test that a valid config passes validation without errors."""
        manager = ConfigManager(config_dir=temp_config_dir)
        manager.user_config_dir = temp_config_dir / "user"
        manager.user_config_dir.mkdir(exist_ok=True)
        manager.user_config_path = manager.user_config_dir / "config.yaml"
        manager.load_config()

        # Should not raise
        manager._validate_config()
