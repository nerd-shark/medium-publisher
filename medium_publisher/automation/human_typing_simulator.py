"""
Human Typing Simulator

Simulates realistic human typing patterns including typos, corrections, and timing variations.
"""

import random
from typing import Dict, List


class HumanTypingSimulator:
    """Simulates human-like typing behavior with typos and timing variations."""
    
    # QWERTY keyboard layout map for adjacent key typos
    ADJACENT_KEYS: Dict[str, List[str]] = {
        'a': ['q', 's', 'w', 'z'],
        'b': ['v', 'g', 'h', 'n'],
        'c': ['x', 'd', 'f', 'v'],
        'd': ['s', 'e', 'f', 'c', 'x'],
        'e': ['w', 'r', 'd', 's'],
        'f': ['d', 'r', 'g', 'c', 'v'],
        'g': ['f', 't', 'h', 'b', 'v'],
        'h': ['g', 'y', 'j', 'n', 'b'],
        'i': ['u', 'o', 'k', 'j'],
        'j': ['h', 'u', 'k', 'n', 'm'],
        'k': ['j', 'i', 'l', 'm'],
        'l': ['k', 'o', 'p'],
        'm': ['n', 'j', 'k'],
        'n': ['b', 'h', 'j', 'm'],
        'o': ['i', 'p', 'l', 'k'],
        'p': ['o', 'l'],
        'q': ['w', 'a'],
        'r': ['e', 't', 'f', 'd'],
        's': ['a', 'w', 'd', 'x', 'z'],
        't': ['r', 'y', 'g', 'f'],
        'u': ['y', 'i', 'j', 'h'],
        'v': ['c', 'f', 'g', 'b'],
        'w': ['q', 'e', 's', 'a'],
        'x': ['z', 's', 'd', 'c'],
        'y': ['t', 'u', 'h', 'g'],
        'z': ['a', 's', 'x'],
        '1': ['2', 'q'],
        '2': ['1', '3', 'q', 'w'],
        '3': ['2', '4', 'w', 'e'],
        '4': ['3', '5', 'e', 'r'],
        '5': ['4', '6', 'r', 't'],
        '6': ['5', '7', 't', 'y'],
        '7': ['6', '8', 'y', 'u'],
        '8': ['7', '9', 'u', 'i'],
        '9': ['8', '0', 'i', 'o'],
        '0': ['9', 'o', 'p'],
    }
    
    def __init__(self, typo_frequency: str = "low", enabled: bool = True):
        """
        Initialize typing simulator.
        
        Args:
            typo_frequency: "low" (2%), "medium" (5%), "high" (8%)
            enabled: Whether to simulate typos
        """
        self.enabled = enabled
        self.typo_rates = {
            "none": 0.0,
            "low": 0.02,
            "medium": 0.05,
            "high": 0.08
        }
        self.typo_rate = self.typo_rates.get(typo_frequency, 0.02)

    
    def should_make_typo(self) -> bool:
        """
        Determine if next character should be a typo.
        
        Returns:
            True if typo should be made, False otherwise
        """
        if not self.enabled:
            return False
        return random.random() < self.typo_rate
    
    def generate_typo(self, intended_char: str) -> str:
        """
        Generate realistic typo for character (adjacent key).
        
        Args:
            intended_char: The character user intended to type
            
        Returns:
            Adjacent key character as typo, or intended char if no adjacent keys
        """
        char_lower = intended_char.lower()
        
        # Get adjacent keys for this character
        adjacent = self.ADJACENT_KEYS.get(char_lower, [])
        
        if not adjacent:
            # No adjacent keys defined, return intended character
            return intended_char
        
        # Select random adjacent key
        typo_char = random.choice(adjacent)
        
        # Preserve case if original was uppercase
        if intended_char.isupper():
            return typo_char.upper()
        
        return typo_char
    
    def get_correction_delay(self) -> int:
        """
        Get delay before correcting typo (1-3 chars).
        
        Returns:
            Number of additional characters to type before correcting (1-3)
        """
        return random.randint(1, 3)
    
    def get_typing_delay(self, base_delay: int) -> int:
        """
        Add random variation to typing delay (±20%).
        
        Args:
            base_delay: Base delay in milliseconds
            
        Returns:
            Delay with ±20% random variation
        """
        variation = random.uniform(-0.20, 0.20)
        varied_delay = base_delay * (1 + variation)
        return max(1, int(varied_delay))  # Ensure at least 1ms
    
    def get_thinking_pause(self) -> int:
        """
        Occasionally return longer pause (100-500ms).
        
        Returns:
            0 for no pause (90% of time), or 100-500ms pause (10% of time)
        """
        if random.random() < 0.05:  # 5% chance of thinking pause
            return random.randint(100, 400)
        return 0
    
    def calculate_overhead(self, text_length: int) -> int:
        """
        Calculate extra time needed for typos and corrections.
        
        Args:
            text_length: Length of text to type
            
        Returns:
            Additional characters needed for typos and corrections
        """
        if not self.enabled:
            return 0
        
        # Expected number of typos
        expected_typos = int(text_length * self.typo_rate)
        
        # Each typo adds approximately 4 keystrokes:
        # - 1 typo character
        # - 1-3 additional characters before noticing (avg 2)
        # - 2-4 backspaces to delete (avg 3)
        # - 2-4 correct characters to retype (avg 3)
        # Total: ~4 extra keystrokes per typo
        overhead_per_typo = 4
        
        return expected_typos * overhead_per_typo
