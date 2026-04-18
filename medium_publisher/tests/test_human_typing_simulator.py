"""
Tests for HumanTypingSimulator

Tests typo generation, timing variations, and overhead calculations.
"""

import pytest
from medium_publisher.automation.human_typing_simulator import HumanTypingSimulator


class TestHumanTypingSimulatorInitialization:
    """Test simulator initialization."""
    
    def test_init_default_values(self):
        """Test initialization with default values."""
        simulator = HumanTypingSimulator()
        
        assert simulator.enabled is True
        assert simulator.typo_rate == 0.02  # Default "low"
    
    def test_init_low_frequency(self):
        """Test initialization with low typo frequency."""
        simulator = HumanTypingSimulator(typo_frequency="low")
        
        assert simulator.typo_rate == 0.02
    
    def test_init_medium_frequency(self):
        """Test initialization with medium typo frequency."""
        simulator = HumanTypingSimulator(typo_frequency="medium")
        
        assert simulator.typo_rate == 0.05
    
    def test_init_high_frequency(self):
        """Test initialization with high typo frequency."""
        simulator = HumanTypingSimulator(typo_frequency="high")
        
        assert simulator.typo_rate == 0.08
    
    def test_init_disabled(self):
        """Test initialization with typos disabled."""
        simulator = HumanTypingSimulator(enabled=False)
        
        assert simulator.enabled is False
    
    def test_init_invalid_frequency_defaults_to_low(self):
        """Test initialization with invalid frequency defaults to low."""
        simulator = HumanTypingSimulator(typo_frequency="invalid")
        
        assert simulator.typo_rate == 0.02


class TestShouldMakeTypo:
    """Test typo decision logic."""
    
    def test_should_make_typo_disabled(self):
        """Test that typos are never made when disabled."""
        simulator = HumanTypingSimulator(enabled=False)
        
        # Test 100 times to ensure it's always False
        results = [simulator.should_make_typo() for _ in range(100)]
        
        assert all(result is False for result in results)
    
    def test_should_make_typo_enabled_returns_boolean(self):
        """Test that should_make_typo returns boolean when enabled."""
        simulator = HumanTypingSimulator(enabled=True)
        
        result = simulator.should_make_typo()
        
        assert isinstance(result, bool)
    
    def test_should_make_typo_probability_low(self):
        """Test that typo probability is approximately 2% for low frequency."""
        simulator = HumanTypingSimulator(typo_frequency="low", enabled=True)
        
        # Test 10000 times to get statistical significance
        results = [simulator.should_make_typo() for _ in range(10000)]
        typo_count = sum(results)
        typo_rate = typo_count / 10000
        
        # Allow 1% margin of error (1% to 3%)
        assert 0.01 <= typo_rate <= 0.03
    
    def test_should_make_typo_probability_medium(self):
        """Test that typo probability is approximately 5% for medium frequency."""
        simulator = HumanTypingSimulator(typo_frequency="medium", enabled=True)
        
        # Test 10000 times
        results = [simulator.should_make_typo() for _ in range(10000)]
        typo_count = sum(results)
        typo_rate = typo_count / 10000
        
        # Allow 1.5% margin of error (3.5% to 6.5%)
        assert 0.035 <= typo_rate <= 0.065


class TestGenerateTypo:
    """Test typo generation logic."""

    
    def test_generate_typo_returns_adjacent_key(self):
        """Test that generate_typo returns an adjacent key."""
        simulator = HumanTypingSimulator()
        
        # Test with 'a' which has adjacent keys ['q', 's', 'w', 'z']
        typo = simulator.generate_typo('a')
        
        assert typo in ['q', 's', 'w', 'z']
    
    def test_generate_typo_preserves_uppercase(self):
        """Test that generate_typo preserves uppercase."""
        simulator = HumanTypingSimulator()
        
        # Test with uppercase 'A'
        typo = simulator.generate_typo('A')
        
        # Should be uppercase version of adjacent key
        assert typo in ['Q', 'S', 'W', 'Z']
        assert typo.isupper()
    
    def test_generate_typo_lowercase(self):
        """Test that generate_typo returns lowercase for lowercase input."""
        simulator = HumanTypingSimulator()
        
        typo = simulator.generate_typo('e')
        
        assert typo in ['w', 'r', 'd', 's']
        assert typo.islower()
    
    def test_generate_typo_no_adjacent_keys(self):
        """Test that generate_typo returns original char if no adjacent keys."""
        simulator = HumanTypingSimulator()
        
        # Test with character not in ADJACENT_KEYS
        typo = simulator.generate_typo('!')
        
        assert typo == '!'
    
    def test_generate_typo_numbers(self):
        """Test that generate_typo works with numbers."""
        simulator = HumanTypingSimulator()
        
        # Test with '5' which has adjacent keys ['4', '6', 'r', 't']
        typo = simulator.generate_typo('5')
        
        assert typo in ['4', '6', 'r', 't']
    
    def test_generate_typo_randomness(self):
        """Test that generate_typo produces different results."""
        simulator = HumanTypingSimulator()
        
        # Generate 100 typos for 'a'
        typos = [simulator.generate_typo('a') for _ in range(100)]
        
        # Should have at least 2 different typos (very high probability)
        unique_typos = set(typos)
        assert len(unique_typos) >= 2


class TestGetCorrectionDelay:
    """Test correction delay logic."""
    
    def test_get_correction_delay_range(self):
        """Test that correction delay is between 1 and 3."""
        simulator = HumanTypingSimulator()
        
        # Test 100 times
        delays = [simulator.get_correction_delay() for _ in range(100)]
        
        assert all(1 <= delay <= 3 for delay in delays)
    
    def test_get_correction_delay_variety(self):
        """Test that correction delay produces different values."""
        simulator = HumanTypingSimulator()
        
        # Test 100 times
        delays = [simulator.get_correction_delay() for _ in range(100)]
        unique_delays = set(delays)
        
        # Should have at least 2 different values
        assert len(unique_delays) >= 2


class TestGetTypingDelay:
    """Test typing delay variation logic."""
    
    def test_get_typing_delay_within_range(self):
        """Test that typing delay is within ±20% of base."""
        simulator = HumanTypingSimulator()
        base_delay = 100
        
        # Test 100 times
        delays = [simulator.get_typing_delay(base_delay) for _ in range(100)]
        
        # All delays should be within 80-120ms (±20% of 100ms)
        assert all(80 <= delay <= 120 for delay in delays)
    
    def test_get_typing_delay_minimum_1ms(self):
        """Test that typing delay is at least 1ms."""
        simulator = HumanTypingSimulator()
        
        # Test with very small base delay
        delay = simulator.get_typing_delay(1)
        
        assert delay >= 1
    
    def test_get_typing_delay_variety(self):
        """Test that typing delay produces different values."""
        simulator = HumanTypingSimulator()
        
        # Test 100 times with base 50ms
        delays = [simulator.get_typing_delay(50) for _ in range(100)]
        unique_delays = set(delays)
        
        # Should have many different values
        assert len(unique_delays) >= 10


class TestGetThinkingPause:
    """Test thinking pause logic."""

    
    def test_get_thinking_pause_mostly_zero(self):
        """Test that thinking pause is 0 most of the time (90%)."""
        simulator = HumanTypingSimulator()
        
        # Test 1000 times
        pauses = [simulator.get_thinking_pause() for _ in range(1000)]
        zero_count = sum(1 for p in pauses if p == 0)
        zero_rate = zero_count / 1000
        
        # Should be approximately 90% zeros (allow 5% margin: 85%-95%)
        assert 0.85 <= zero_rate <= 0.95
    
    def test_get_thinking_pause_range(self):
        """Test that thinking pause is in range 100-500ms when not zero."""
        simulator = HumanTypingSimulator()
        
        # Test 1000 times and collect non-zero pauses
        pauses = [simulator.get_thinking_pause() for _ in range(1000)]
        non_zero_pauses = [p for p in pauses if p > 0]
        
        # All non-zero pauses should be 100-500ms
        assert all(100 <= p <= 500 for p in non_zero_pauses)
    
    def test_get_thinking_pause_variety(self):
        """Test that thinking pause produces different values."""
        simulator = HumanTypingSimulator()
        
        # Test 1000 times and collect non-zero pauses
        pauses = [simulator.get_thinking_pause() for _ in range(1000)]
        non_zero_pauses = [p for p in pauses if p > 0]
        unique_pauses = set(non_zero_pauses)
        
        # Should have many different pause values
        assert len(unique_pauses) >= 10


class TestCalculateOverhead:
    """Test overhead calculation logic."""
    
    def test_calculate_overhead_disabled(self):
        """Test that overhead is 0 when disabled."""
        simulator = HumanTypingSimulator(enabled=False)
        
        overhead = simulator.calculate_overhead(1000)
        
        assert overhead == 0
    
    def test_calculate_overhead_low_frequency(self):
        """Test overhead calculation with low typo frequency."""
        simulator = HumanTypingSimulator(typo_frequency="low")
        
        # 1000 chars * 2% = 20 typos * 4 overhead = 80 extra chars
        overhead = simulator.calculate_overhead(1000)
        
        assert overhead == 80
    
    def test_calculate_overhead_medium_frequency(self):
        """Test overhead calculation with medium typo frequency."""
        simulator = HumanTypingSimulator(typo_frequency="medium")
        
        # 1000 chars * 5% = 50 typos * 4 overhead = 200 extra chars
        overhead = simulator.calculate_overhead(1000)
        
        assert overhead == 200
    
    def test_calculate_overhead_high_frequency(self):
        """Test overhead calculation with high typo frequency."""
        simulator = HumanTypingSimulator(typo_frequency="high")
        
        # 1000 chars * 8% = 80 typos * 4 overhead = 320 extra chars
        overhead = simulator.calculate_overhead(1000)
        
        assert overhead == 320
    
    def test_calculate_overhead_small_text(self):
        """Test overhead calculation with small text."""
        simulator = HumanTypingSimulator(typo_frequency="low")
        
        # 50 chars * 2% = 1 typo * 4 overhead = 4 extra chars
        overhead = simulator.calculate_overhead(50)
        
        assert overhead == 4
    
    def test_calculate_overhead_zero_length(self):
        """Test overhead calculation with zero length text."""
        simulator = HumanTypingSimulator(typo_frequency="low")
        
        overhead = simulator.calculate_overhead(0)
        
        assert overhead == 0


class TestAdjacentKeysMap:
    """Test ADJACENT_KEYS map completeness."""
    
    def test_adjacent_keys_all_lowercase_letters(self):
        """Test that all lowercase letters have adjacent keys."""
        simulator = HumanTypingSimulator()
        
        for char in 'abcdefghijklmnopqrstuvwxyz':
            assert char in simulator.ADJACENT_KEYS
            assert len(simulator.ADJACENT_KEYS[char]) > 0
    
    def test_adjacent_keys_all_numbers(self):
        """Test that all numbers have adjacent keys."""
        simulator = HumanTypingSimulator()
        
        for char in '0123456789':
            assert char in simulator.ADJACENT_KEYS
            assert len(simulator.ADJACENT_KEYS[char]) > 0
    
    def test_adjacent_keys_symmetry(self):
        """Test that adjacent key relationships are mostly symmetric."""
        simulator = HumanTypingSimulator()
        
        # Check a few key relationships
        # If 'a' is adjacent to 'q', then 'q' should be adjacent to 'a'
        assert 'q' in simulator.ADJACENT_KEYS['a']
        assert 'a' in simulator.ADJACENT_KEYS['q']
        
        assert 's' in simulator.ADJACENT_KEYS['a']
        assert 'a' in simulator.ADJACENT_KEYS['s']



class TestHumanTypingSimulatorEdgeCases:
    """Test edge cases for HumanTypingSimulator."""
    
    def test_generate_typo_all_letters(self):
        """Test generate_typo works for all letters."""
        simulator = HumanTypingSimulator()
        
        # Test all lowercase letters
        for char in 'abcdefghijklmnopqrstuvwxyz':
            typo = simulator.generate_typo(char)
            assert isinstance(typo, str)
            assert len(typo) == 1
    
    def test_generate_typo_all_numbers(self):
        """Test generate_typo works for all numbers."""
        simulator = HumanTypingSimulator()
        
        # Test all numbers
        for char in '0123456789':
            typo = simulator.generate_typo(char)
            assert isinstance(typo, str)
            assert len(typo) == 1
    
    def test_generate_typo_special_characters(self):
        """Test generate_typo with special characters."""
        simulator = HumanTypingSimulator()
        
        # Special characters not in ADJACENT_KEYS should return original
        for char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~`':
            typo = simulator.generate_typo(char)
            assert typo == char
    
    def test_calculate_overhead_various_lengths(self):
        """Test overhead calculation with various text lengths."""
        simulator = HumanTypingSimulator(typo_frequency="medium")
        
        # Test different lengths
        test_cases = [
            (100, 20),   # 100 * 0.05 * 4 = 20
            (500, 100),  # 500 * 0.05 * 4 = 100
            (1500, 300), # 1500 * 0.05 * 4 = 300
        ]
        
        for text_length, expected_overhead in test_cases:
            overhead = simulator.calculate_overhead(text_length)
            assert overhead == expected_overhead
    
    def test_get_typing_delay_zero_base(self):
        """Test get_typing_delay with zero base delay."""
        simulator = HumanTypingSimulator()
        
        # Even with 0 base, should return at least 1ms
        delay = simulator.get_typing_delay(0)
        assert delay >= 1
    
    def test_get_typing_delay_large_base(self):
        """Test get_typing_delay with large base delay."""
        simulator = HumanTypingSimulator()
        
        # Test with 1000ms base
        delay = simulator.get_typing_delay(1000)
        
        # Should be within ±20% (800-1200ms)
        assert 800 <= delay <= 1200
    
    def test_should_make_typo_high_frequency(self):
        """Test typo probability for high frequency."""
        simulator = HumanTypingSimulator(typo_frequency="high", enabled=True)
        
        # Test 10000 times
        results = [simulator.should_make_typo() for _ in range(10000)]
        typo_count = sum(results)
        typo_rate = typo_count / 10000
        
        # Should be approximately 8% (allow 2% margin: 6%-10%)
        assert 0.06 <= typo_rate <= 0.10
    
    def test_get_correction_delay_distribution(self):
        """Test correction delay has even distribution."""
        simulator = HumanTypingSimulator()
        
        # Test 1000 times
        delays = [simulator.get_correction_delay() for _ in range(1000)]
        
        # Count occurrences of each value
        count_1 = delays.count(1)
        count_2 = delays.count(2)
        count_3 = delays.count(3)
        
        # Each should appear roughly 1/3 of the time (allow 10% margin)
        assert 250 <= count_1 <= 450
        assert 250 <= count_2 <= 450
        assert 250 <= count_3 <= 450
