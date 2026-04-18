"""Property-based tests for ConfigManager save/load round-trip.

Property 24: Config save/load round-trip
For any valid configuration dictionary with typing, publishing, safety,
navigation, ui, and assets settings, saving via ConfigManager.save_config()
and loading via ConfigManager.load_config() SHALL produce a dictionary
with identical values for all fields.

**Validates: Requirements 12.11, 12.12**
"""

import pytest
import tempfile
from pathlib import Path

import yaml
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from medium_publisher.core.config_manager import ConfigManager


# --- Strategies for generating valid config values ---

typing_config_strategy = st.fixed_dictionaries({
    'base_delay_ms': st.integers(min_value=1, max_value=5000),
    'variation_percent': st.integers(min_value=0, max_value=100),
    'human_typing_enabled': st.booleans(),
    'typo_frequency': st.sampled_from(['low', 'medium', 'high']),
    'immediate_correction_ratio': st.floats(
        min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False,
    ),
    'thinking_pause_min_ms': st.integers(min_value=100, max_value=5000),
    'thinking_pause_max_ms': st.integers(min_value=100, max_value=10000),
    'paragraph_pause_min_ms': st.integers(min_value=100, max_value=5000),
    'paragraph_pause_max_ms': st.integers(min_value=100, max_value=10000),
})

publishing_config_strategy = st.fixed_dictionaries({
    'default_mode': st.sampled_from(['draft', 'public']),
    'max_tags': st.integers(min_value=1, max_value=5),
})

safety_config_strategy = st.fixed_dictionaries({
    'emergency_stop_hotkey': st.sampled_from([
        'ctrl+shift+escape', 'ctrl+shift+q', 'ctrl+alt+s',
    ]),
    'countdown_seconds': st.integers(min_value=1, max_value=30),
    'focus_check_enabled': st.booleans(),
})

navigation_config_strategy = st.fixed_dictionaries({
    'screen_confidence': st.floats(
        min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False,
    ),
    'poll_interval_seconds': st.integers(min_value=1, max_value=60),
    'login_timeout_seconds': st.integers(min_value=1, max_value=600),
    'page_load_timeout_seconds': st.integers(min_value=1, max_value=120),
    'google_account_email': st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='@._-'),
        min_size=5, max_size=50,
    ),
})

ui_config_strategy = st.fixed_dictionaries({
    'always_on_top': st.booleans(),
    'remember_window_position': st.booleans(),
    'remember_last_directory': st.booleans(),
})

assets_config_strategy = st.fixed_dictionaries({
    'reference_images_dir': st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='/_-.'),
        min_size=1, max_size=100,
    ),
})

valid_config_strategy = st.fixed_dictionaries({
    'typing': typing_config_strategy,
    'publishing': publishing_config_strategy,
    'safety': safety_config_strategy,
    'navigation': navigation_config_strategy,
    'ui': ui_config_strategy,
    'assets': assets_config_strategy,
})


def _approx_equal_float(a, b, rel_tol=1e-9, abs_tol=1e-9):
    """Check approximate equality for floats after YAML round-trip."""
    if isinstance(a, float) and isinstance(b, float):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
    return a == b


def _configs_equal(original, loaded):
    """Deep compare two config dicts, handling float precision from YAML round-trip."""
    if isinstance(original, dict) and isinstance(loaded, dict):
        if set(original.keys()) != set(loaded.keys()):
            return False
        return all(_configs_equal(original[k], loaded[k]) for k in original)
    if isinstance(original, float) or isinstance(loaded, float):
        return _approx_equal_float(float(original), float(loaded))
    return original == loaded


class TestPropertyConfigRoundTrip:
    """Property 24: Config save/load round-trip.

    **Validates: Requirements 12.11, 12.12**
    """

    @given(config=valid_config_strategy)
    @settings(max_examples=100)
    def test_config_save_load_round_trip(self, config):
        """For any valid config dict, saving to YAML and loading back
        should produce identical values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            config_dir.mkdir()

            # Write the generated config as the default config
            with open(config_dir / "default_config.yaml", 'w') as f:
                yaml.safe_dump(config, f)

            # Create manager, load defaults, then save as user config
            manager = ConfigManager(config_dir=config_dir)
            manager.user_config_dir = Path(tmpdir) / "user"
            manager.user_config_dir.mkdir(exist_ok=True)
            manager.user_config_path = manager.user_config_dir / "config.yaml"

            loaded_config = manager.load_config()

            # Save the loaded config
            manager.save_config(loaded_config)

            # Load again from user config
            manager2 = ConfigManager(config_dir=config_dir)
            manager2.user_config_dir = manager.user_config_dir
            manager2.user_config_path = manager.user_config_path
            reloaded_config = manager2.load_config()

            # All fields must match
            assert _configs_equal(loaded_config, reloaded_config), (
                f"Config round-trip mismatch.\n"
                f"Original: {loaded_config}\n"
                f"Reloaded: {reloaded_config}"
            )
