"""
Property-based tests for HumanTypingSimulator.

Feature: medium-keyboard-publisher
Properties 13, 14, 15, 16, 18

Validates: Requirements 5.1, 5.3, 5.4, 5.6, 5.15
"""

from hypothesis import given, settings, strategies as st

from medium_publisher.automation.human_typing_simulator import HumanTypingSimulator


class TestTypingSpeedBounds:
    """Property 13: Typing speed variation stays within ±30% bounds.

    **Validates: Requirements 5.1**

    For any base delay value, every value returned by
    get_typing_delay(base_delay) SHALL be within
    [base_delay * 0.7, base_delay * 1.3] (min 1ms).
    """

    @given(base_delay=st.integers(min_value=1, max_value=5000))
    @settings(max_examples=200)
    def test_delay_within_bounds(self, base_delay: int) -> None:
        """get_typing_delay returns value within ±30% of base_delay (min 1ms)."""
        sim = HumanTypingSimulator()
        delay = sim.get_typing_delay(base_delay)

        lower = max(1, int(base_delay * 0.7))
        upper = int(base_delay * 1.3)

        assert delay >= lower, (
            f"Delay {delay} below lower bound {lower} for base_delay={base_delay}"
        )
        assert delay <= upper, (
            f"Delay {delay} above upper bound {upper} for base_delay={base_delay}"
        )

    @given(base_delay=st.just(0))
    @settings(max_examples=10)
    def test_zero_base_delay_returns_at_least_one(self, base_delay: int) -> None:
        """get_typing_delay with base_delay=0 returns at least 1ms."""
        sim = HumanTypingSimulator()
        delay = sim.get_typing_delay(base_delay)
        assert delay >= 1


class TestTypoGenerationAdjacentKey:
    """Property 14: Typo generation produces adjacent QWERTY key.

    **Validates: Requirements 5.4**

    For any character that has entries in ADJACENT_KEYS,
    generate_typo(char) SHALL return one of the adjacent keys,
    preserving case.
    """

    @given(char=st.sampled_from(sorted(HumanTypingSimulator.ADJACENT_KEYS.keys())))
    @settings(max_examples=200)
    def test_typo_is_adjacent_key_lowercase(self, char: str) -> None:
        """generate_typo returns an adjacent key for lowercase chars."""
        sim = HumanTypingSimulator()
        typo = sim.generate_typo(char)

        adjacent = HumanTypingSimulator.ADJACENT_KEYS[char]
        assert typo in adjacent, (
            f"Typo '{typo}' not in adjacent keys {adjacent} for '{char}'"
        )

    @given(char=st.sampled_from(sorted(HumanTypingSimulator.ADJACENT_KEYS.keys())))
    @settings(max_examples=200)
    def test_typo_preserves_uppercase(self, char: str) -> None:
        """generate_typo preserves case when input is uppercase."""
        sim = HumanTypingSimulator()
        upper_char = char.upper()
        typo = sim.generate_typo(upper_char)

        adjacent_lower = HumanTypingSimulator.ADJACENT_KEYS[char]
        adjacent_upper = [k.upper() for k in adjacent_lower]

        if upper_char != char:  # Only check case for alpha chars
            assert typo in adjacent_upper, (
                f"Typo '{typo}' not in uppercase adjacent keys "
                f"{adjacent_upper} for '{upper_char}'"
            )


class TestTypoFrequency:
    """Property 15: Typo frequency approximates configured rate.

    **Validates: Requirements 5.3**

    For any typo frequency setting (low=2%, medium=5%, high=8%),
    over ≥1000 calls, the proportion of should_make_typo() returning
    True SHALL be within ±2 percentage points.
    """

    @given(freq=st.sampled_from(["low", "medium", "high"]))
    @settings(max_examples=30)
    def test_typo_rate_within_tolerance(self, freq: str) -> None:
        """should_make_typo rate approximates configured frequency ±2pp."""
        sim = HumanTypingSimulator(typo_frequency=freq)
        expected_rate = sim.typo_rates[freq]

        num_calls = 5000
        typo_count = sum(1 for _ in range(num_calls) if sim.should_make_typo())
        actual_rate = typo_count / num_calls

        tolerance = 0.02
        assert abs(actual_rate - expected_rate) <= tolerance, (
            f"Frequency '{freq}': expected ~{expected_rate:.2%}, "
            f"got {actual_rate:.2%} (tolerance ±{tolerance:.0%})"
        )


class TestCorrectionDelay:
    """Property 16: Immediate correction delay is 1-3 characters.

    **Validates: Requirements 5.6**

    For any call to get_correction_delay(), the returned value
    SHALL be in [1, 3].
    """

    @given(st.integers(min_value=1, max_value=500))
    @settings(max_examples=200)
    def test_correction_delay_in_range(self, _iteration: int) -> None:
        """get_correction_delay always returns value in [1, 3]."""
        sim = HumanTypingSimulator()
        delay = sim.get_correction_delay()

        assert 1 <= delay <= 3, (
            f"Correction delay {delay} outside [1, 3]"
        )


class TestEstimatedTypingOverhead:
    """Property 18: Estimated typing time accounts for all overhead.

    **Validates: Requirements 5.15**

    For any article length and typing config, calculate_overhead()
    should return >= 0 and scale with text length and typo rate.
    """

    @given(
        text_length=st.integers(min_value=0, max_value=100000),
        freq=st.sampled_from(["low", "medium", "high"]),
    )
    @settings(max_examples=200)
    def test_overhead_non_negative(self, text_length: int, freq: str) -> None:
        """calculate_overhead returns non-negative value."""
        sim = HumanTypingSimulator(typo_frequency=freq)
        overhead = sim.calculate_overhead(text_length)
        assert overhead >= 0

    @given(
        text_length=st.integers(min_value=100, max_value=100000),
        freq=st.sampled_from(["low", "medium", "high"]),
    )
    @settings(max_examples=200)
    def test_overhead_scales_with_length(self, text_length: int, freq: str) -> None:
        """Longer text produces equal or greater overhead."""
        sim = HumanTypingSimulator(typo_frequency=freq)
        overhead = sim.calculate_overhead(text_length)
        half_overhead = sim.calculate_overhead(text_length // 2)
        assert overhead >= half_overhead

    @given(text_length=st.integers(min_value=100, max_value=100000))
    @settings(max_examples=100)
    def test_higher_typo_rate_means_more_overhead(self, text_length: int) -> None:
        """Higher typo frequency produces equal or greater overhead."""
        low = HumanTypingSimulator(typo_frequency="low")
        high = HumanTypingSimulator(typo_frequency="high")
        assert high.calculate_overhead(text_length) >= low.calculate_overhead(text_length)

    @given(text_length=st.integers(min_value=0, max_value=100000))
    @settings(max_examples=100)
    def test_disabled_simulator_zero_overhead(self, text_length: int) -> None:
        """Disabled simulator returns zero overhead."""
        sim = HumanTypingSimulator(enabled=False)
        assert sim.calculate_overhead(text_length) == 0
