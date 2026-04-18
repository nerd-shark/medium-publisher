# Human Typing Simulator Implementation

## Overview

The Human Typing Simulator adds realistic typing behavior including typos, corrections, variable speed, and thinking pauses to make automation indistinguishable from human typing.

## Core Features

1. **Realistic Typos**: Adjacent key errors based on QWERTY layout
2. **Delayed Corrections**: Wait 1-3 characters before fixing typos
3. **Variable Speed**: ±20% variation in typing speed
4. **Thinking Pauses**: Occasional 100-500ms pauses
5. **Configurable Frequency**: Low (2%), Medium (5%), High (8%) typo rates

## QWERTY Keyboard Layout

### Adjacent Keys Map

```python
ADJACENT_KEYS = {
    # Top row
    'q': ['w', 'a', '1', '2'],
    'w': ['q', 'e', 's', 'a', '2', '3'],
    'e': ['w', 'r', 'd', 's', '3', '4'],
    'r': ['e', 't', 'f', 'd', '4', '5'],
    't': ['r', 'y', 'g', 'f', '5', '6'],
    'y': ['t', 'u', 'h', 'g', '6', '7'],
    'u': ['y', 'i', 'j', 'h', '7', '8'],
    'i': ['u', 'o', 'k', 'j', '8', '9'],
    'o': ['i', 'p', 'l', 'k', '9', '0'],
    'p': ['o', 'l', '0', '-'],
    
    # Home row
    'a': ['q', 'w', 's', 'z'],
    's': ['a', 'w', 'e', 'd', 'z', 'x'],
    'd': ['s', 'e', 'r', 'f', 'x', 'c'],
    'f': ['d', 'r', 't', 'g', 'c', 'v'],
    'g': ['f', 't', 'y', 'h', 'v', 'b'],
    'h': ['g', 'y', 'u', 'j', 'b', 'n'],
    'j': ['h', 'u', 'i', 'k', 'n', 'm'],
    'k': ['j', 'i', 'o', 'l', 'm'],
    'l': ['k', 'o', 'p'],
    
    # Bottom row
    'z': ['a', 's', 'x'],
    'x': ['z', 's', 'd', 'c'],
    'c': ['x', 'd', 'f', 'v'],
    'v': ['c', 'f', 'g', 'b'],
    'b': ['v', 'g', 'h', 'n'],
    'n': ['b', 'h', 'j', 'm'],
    'm': ['n', 'j', 'k'],
    
    # Numbers
    '1': ['2', 'q'],
    '2': ['1', '3', 'q', 'w'],
    '3': ['2', '4', 'w', 'e'],
    '4': ['3', '5', 'e', 'r'],
    '5': ['4', '6', 'r', 't'],
    '6': ['5', '7', 't', 'y'],
    '7': ['6', '8', 'y', 'u'],
    '8': ['7', '9', 'u', 'i'],
    '9': ['8', '0', 'i', 'o'],
    '0': ['9', '-', 'o', 'p'],
    
    # Special characters (common typos)
    ' ': ['b', 'n', 'm'],  # Space bar
    '.': [',', 'l'],
    ',': ['.', 'k', 'm'],
}
```

### Visual Layout

```
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │ 0 │ - │ = │   │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
  │ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │ [ │ ] │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
    ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
    │ A │ S │ D │ F │ G │ H │ J │ K │ L │ ; │ ' │
    └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
      ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
      │ Z │ X │ C │ V │ B │ N │ M │ , │ . │ / │
      └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
```

## Implementation

### Class Structure

```python
class HumanTypingSimulator:
    """Simulate realistic human typing behavior."""
    
    def __init__(self, typo_frequency: str = "low", enabled: bool = True):
        """Initialize simulator.
        
        Args:
            typo_frequency: "low" (2%), "medium" (5%), "high" (8%)
            enabled: Whether to simulate typos
        """
        self.enabled = enabled
        self.typo_rate = {
            "low": 0.02,     # 1 typo per 50 characters
            "medium": 0.05,  # 1 typo per 20 characters
            "high": 0.08     # 1 typo per 12.5 characters
        }[typo_frequency]
        
        # QWERTY keyboard layout
        self.adjacent_keys = ADJACENT_KEYS
```

### Typo Generation

```python
def should_make_typo(self) -> bool:
    """Determine if next character should be a typo.
    
    Returns:
        True if should make typo
    """
    if not self.enabled:
        return False
    
    return random.random() < self.typo_rate

def generate_typo(self, intended_char: str) -> str:
    """Generate realistic typo for character.
    
    Args:
        intended_char: The character user intended to type
    
    Returns:
        Adjacent key character (typo)
    """
    char_lower = intended_char.lower()
    
    # Get adjacent keys
    adjacent = self.adjacent_keys.get(char_lower, [])
    
    if not adjacent:
        # No adjacent keys defined, return same character
        return intended_char
    
    # Select random adjacent key
    typo_char = random.choice(adjacent)
    
    # Preserve case
    if intended_char.isupper():
        typo_char = typo_char.upper()
    
    return typo_char
```

### Correction Timing

```python
def get_correction_delay(self) -> int:
    """Get delay before correcting typo.
    
    Simulates human noticing typo after typing 1-3 more characters.
    
    Returns:
        Delay in milliseconds
    """
    # Type 1-3 more characters before noticing
    extra_chars = random.randint(1, 3)
    
    # Each character takes base_delay ms
    # Use average of 40ms per character
    delay = extra_chars * 40
    
    return delay
```

### Speed Variation

```python
def get_typing_delay(self, base_delay: int) -> int:
    """Add random variation to typing delay.
    
    Args:
        base_delay: Base delay in milliseconds
    
    Returns:
        Varied delay (±20%)
    """
    # Add ±20% variation
    variation = random.uniform(-0.2, 0.2)
    varied_delay = base_delay * (1 + variation)
    
    return int(varied_delay)
```

### Thinking Pauses

```python
def get_thinking_pause(self) -> int:
    """Occasionally return longer pause.
    
    Simulates human pausing to think about next sentence.
    
    Returns:
        Pause duration (100-500ms) or 0
    """
    # 5% chance of thinking pause
    if random.random() < 0.05:
        return random.randint(100, 500)
    
    return 0
```

### Overhead Calculation

```python
def calculate_overhead(self, text_length: int) -> int:
    """Calculate extra time needed for typos and corrections.
    
    Args:
        text_length: Length of text to type
    
    Returns:
        Extra seconds needed
    """
    if not self.enabled:
        return 0
    
    # Calculate expected typos
    num_typos = int(text_length * self.typo_rate)
    
    # Each typo adds:
    # 1. Wrong character (1 keystroke)
    # 2. 1-3 more characters (avg 2 keystrokes)
    # 3. Backspace to delete (avg 3 keystrokes for 3 chars)
    # 4. Correct character (1 keystroke)
    # Total: ~7 extra keystrokes per typo
    
    extra_keystrokes = num_typos * 7
    
    # Assume 40ms per keystroke
    extra_ms = extra_keystrokes * 40
    
    # Convert to seconds
    extra_seconds = extra_ms / 1000
    
    return int(extra_seconds)
```

## Typo Simulation Flow

### Example: Typing "hello"

```
Intended: h e l l o
          ↓ ↓ ↓ ↓ ↓
Check:    N N Y N N  (Y = make typo)
          ↓ ↓ ↓ ↓ ↓
Typed:    h e k l o  (k is adjacent to l)
                ↑
                typo!

Correction Flow:
1. Type 'h' (correct)
2. Type 'e' (correct)
3. Type 'k' (typo for 'l')
4. Type 'l' (continue, haven't noticed yet)
5. Type 'o' (continue, haven't noticed yet)
6. Wait 80ms (correction delay for 2 chars)
7. Press Backspace 3 times (delete 'klo')
8. Type 'l' (correct)
9. Type 'l' (correct)
10. Type 'o' (correct)

Final result: hello
```

### Detailed Timeline

```
Time (ms)  Action              Display
---------  -----------------   -------
0          Type 'h'            h
40         Type 'e'            he
80         Type 'k' (typo!)    hek
120        Type 'l'            hekl
160        Type 'o'            heklo
240        [Notice typo]       heklo
241        Backspace           hekl
242        Backspace           hek
243        Backspace           he
283        Type 'l'            hel
323        Type 'l'            hell
363        Type 'o'            hello
```

## Configuration

### Typo Frequency Settings

```yaml
typing:
  human_typing_enabled: true
  typo_frequency: "low"  # low, medium, high
```

| Setting | Rate | Typos per 100 chars | Description |
|---------|------|---------------------|-------------|
| low | 2% | 2 | Careful typing |
| medium | 5% | 5 | Normal typing |
| high | 8% | 8 | Fast/careless typing |

### When Typos Are Disabled

Typos are **never** simulated for:
1. **Code blocks**: Preserve exact syntax
2. **URLs**: Prevent broken links
3. **TODO placeholders**: Keep markers intact
4. **Special characters**: Avoid formatting issues

```python
async def type_text(self, text: str, allow_typos: bool = True):
    """Type text with optional typo simulation.
    
    Args:
        text: Text to type
        allow_typos: Whether to allow typos (False for code/URLs)
    """
    for char in text:
        if allow_typos and self.human_simulator.should_make_typo():
            # Simulate typo
            pass
        else:
            # Type correctly
            pass
```

## Performance Impact

### Time Overhead

**Low typos (2%)**:
- 1000 chars → ~20 typos
- Extra keystrokes: 20 * 7 = 140
- Extra time: 140 * 40ms = 5.6 seconds
- Overhead: ~5.6%

**Medium typos (5%)**:
- 1000 chars → ~50 typos
- Extra keystrokes: 50 * 7 = 350
- Extra time: 350 * 40ms = 14 seconds
- Overhead: ~14%

**High typos (8%)**:
- 1000 chars → ~80 typos
- Extra keystrokes: 80 * 7 = 560
- Extra time: 560 * 40ms = 22.4 seconds
- Overhead: ~22.4%

### Memory Usage

- O(1) constant memory
- QWERTY map: ~2KB
- No dynamic allocation during typing

### CPU Usage

- Minimal: Random number generation only
- No complex calculations
- Negligible impact on performance

## Testing

### Unit Tests

```python
def test_typo_generation():
    """Test typo generation uses adjacent keys."""
    simulator = HumanTypingSimulator(typo_frequency="high", enabled=True)
    
    # Test multiple times to ensure randomness
    typos = set()
    for _ in range(100):
        typo = simulator.generate_typo('e')
        typos.add(typo)
    
    # Should only generate adjacent keys
    expected = {'w', 'r', 'd', 's'}
    assert typos.issubset(expected)

def test_typo_frequency():
    """Test typo frequency matches configuration."""
    simulator = HumanTypingSimulator(typo_frequency="medium", enabled=True)
    
    # Simulate 1000 characters
    typo_count = 0
    for _ in range(1000):
        if simulator.should_make_typo():
            typo_count += 1
    
    # Should be approximately 5% (50 typos)
    # Allow ±20% variance for randomness
    assert 40 <= typo_count <= 60

def test_correction_delay():
    """Test correction delay is reasonable."""
    simulator = HumanTypingSimulator()
    
    # Test multiple times
    delays = [simulator.get_correction_delay() for _ in range(100)]
    
    # Should be between 40ms (1 char) and 120ms (3 chars)
    assert all(40 <= d <= 120 for d in delays)

def test_typing_variation():
    """Test typing speed variation."""
    simulator = HumanTypingSimulator()
    base_delay = 50
    
    # Test multiple times
    delays = [simulator.get_typing_delay(base_delay) for _ in range(100)]
    
    # Should vary ±20%
    assert all(40 <= d <= 60 for d in delays)

def test_thinking_pauses():
    """Test thinking pauses occur occasionally."""
    simulator = HumanTypingSimulator()
    
    # Test 1000 times
    pause_count = 0
    for _ in range(1000):
        pause = simulator.get_thinking_pause()
        if pause > 0:
            pause_count += 1
            assert 100 <= pause <= 500
    
    # Should occur ~5% of time (50 times)
    # Allow ±30% variance
    assert 35 <= pause_count <= 65
```

### Integration Tests

```python
async def test_realistic_typing():
    """Test complete typing with human simulation."""
    simulator = HumanTypingSimulator(typo_frequency="medium", enabled=True)
    text = "The quick brown fox jumps over the lazy dog"
    
    typed_chars = []
    corrections = []
    
    for char in text:
        if simulator.should_make_typo():
            # Type typo
            typo = simulator.generate_typo(char)
            typed_chars.append(typo)
            
            # Wait before correcting
            delay = simulator.get_correction_delay()
            await asyncio.sleep(delay / 1000)
            
            # Backspace
            typed_chars.pop()
            corrections.append(char)
        
        # Type correct character
        typed_chars.append(char)
        
        # Typing delay
        delay = simulator.get_typing_delay(40)
        await asyncio.sleep(delay / 1000)
    
    # Final text should be correct
    assert ''.join(typed_chars) == text
    
    # Should have some corrections
    assert len(corrections) > 0
```

## Troubleshooting

### Issue: Too many typos

**Symptom**: Typing seems unrealistic with excessive errors

**Solution**: Lower typo frequency to "low" (2%)

### Issue: Not enough variation

**Symptom**: Typing seems robotic despite human simulation

**Solutions**:
1. Increase base typing delay variation
2. Increase thinking pause frequency
3. Add more randomness to correction timing

### Issue: Typos in code blocks

**Symptom**: Code blocks have syntax errors

**Solution**: Ensure `allow_typos=False` for code blocks

### Issue: Performance degradation

**Symptom**: Typing becomes slower over time

**Solutions**:
1. Check for memory leaks in typo tracking
2. Verify random number generator not blocking
3. Profile code to identify bottlenecks

## Best Practices

1. **Use Low Frequency**: Start with "low" (2%) for most articles
2. **Disable for Code**: Never simulate typos in code blocks
3. **Test First**: Test with short text before long articles
4. **Monitor Logs**: Check logs for typo patterns
5. **Adjust as Needed**: Tune frequency based on results

## Future Enhancements

1. **Learning Mode**: Adapt typo patterns based on user's actual typing
2. **Fatigue Simulation**: Increase typo rate over time
3. **Context-Aware**: Different rates for different content types
4. **Personalization**: User-specific typo patterns
5. **Advanced Patterns**: Simulate common typing mistakes (double letters, transpositions)

---

**Document Version**: 1.0
**Last Updated**: 2025-03-01
**Maintained By**: Development Team
