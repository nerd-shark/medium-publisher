# Human Typing Simulator Implementation

## Overview

The Human Typing Simulator adds realistic typing behavior including typos, corrections, variable speed, and thinking pauses to make OS-level keyboard input indistinguishable from human typing.

## Core Features

1. **Realistic Typos**: Adjacent key errors based on QWERTY layout
2. **Immediate Corrections**: Type wrong char, continue 1-3 chars, backspace to fix (70% of typos)
3. **Deferred Corrections**: Leave typo in place, fix during review pass (30% of typos)
4. **Variable Speed**: Configurable ±variation applied to base delay
5. **Thinking Pauses**: Occasional 100-500ms pauses (5% chance per character)
6. **Configurable Frequency**: Low (2%), Medium (5%), High (8%) typo rates

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
    
    # Special characters
    ' ': ['b', 'n', 'm'],
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
            "low": 0.02,
            "medium": 0.05,
            "high": 0.08
        }[typo_frequency]
        self.adjacent_keys = ADJACENT_KEYS
```

### Typo Generation

```python
def should_make_typo(self) -> bool:
    """Determine if next character should be a typo."""
    if not self.enabled:
        return False
    return random.random() < self.typo_rate

def generate_typo(self, intended_char: str) -> str:
    """Generate realistic typo using adjacent QWERTY key."""
    char_lower = intended_char.lower()
    adjacent = self.adjacent_keys.get(char_lower, [])
    
    if not adjacent:
        return intended_char
    
    typo_char = random.choice(adjacent)
    
    # Preserve case
    if intended_char.isupper():
        typo_char = typo_char.upper()
    
    return typo_char
```

### Speed Variation

```python
def get_typing_delay(self, base_delay: int) -> int:
    """Add random variation to typing delay.
    
    Args:
        base_delay: Base delay in milliseconds (from config)
    
    Returns:
        Varied delay (±variation_percent)
    """
    variation = random.uniform(-0.2, 0.2)
    return int(base_delay * (1 + variation))
```

### Thinking Pauses

```python
def get_thinking_pause(self) -> int:
    """Occasionally return longer pause (5% chance).
    
    Returns:
        Pause duration (100-500ms) or 0
    """
    if random.random() < 0.05:
        return random.randint(100, 500)
    return 0
```

### Correction Delay

```python
def get_correction_delay(self) -> int:
    """Get number of extra characters typed before noticing typo.
    
    Returns:
        Number of extra characters (1-3)
    """
    return random.randint(1, 3)
```

## Integration with ContentTyper

The `ContentTyper` uses `HumanTypingSimulator` and `OS_Input_Controller` together:

```python
class ContentTyper:
    def __init__(self, input_controller, typing_simulator, typo_tracker, config):
        self._input = input_controller          # OS_Input_Controller (pyautogui)
        self._simulator = typing_simulator       # HumanTypingSimulator
        self._tracker = typo_tracker            # DeferredTypoTracker
        self._base_delay_ms = config.get("typing.base_delay_ms", 150)
        self._immediate_ratio = config.get("typing.immediate_correction_ratio", 0.70)

    def _type_with_typos(self, text: str, allow_typos: bool = True):
        for char in text:
            # Typing delay with variation
            delay_ms = self._simulator.get_typing_delay(self._base_delay_ms)
            time.sleep(delay_ms / 1000.0)
            
            # Thinking pause
            pause = self._simulator.get_thinking_pause()
            if pause > 0:
                time.sleep(pause / 1000.0)
            
            if allow_typos and self._simulator.should_make_typo():
                typo_char = self._simulator.generate_typo(char)
                
                if random.random() < self._immediate_ratio:
                    # Immediate correction via OS_Input_Controller
                    self._input.type_character(typo_char)
                    # Type 1-3 more chars, then backspace and retype
                    # ... (correction logic)
                else:
                    # Deferred: type wrong char, record for review pass
                    self._input.type_character(typo_char)
                    self._tracker.record(...)
            else:
                # Type correct character via OS-level input
                self._input.type_character(char)
```

Key points:
- All typing goes through `OS_Input_Controller.type_character()` which calls `pyautogui.write()`
- Every keystroke checks emergency stop and focus detection before executing
- No browser page object or Playwright — pure OS-level keyboard events
- `time.sleep()` for all delays (synchronous, runs in QThread)

## Typo Simulation Flow

### Example: Typing "hello" with immediate correction

```
Intended: h e l l o
Check:    N N Y N N  (Y = make typo at position 2)
Typed:    h e k l    (k is adjacent to l, then 1 extra char typed)

Correction Flow:
1. Type 'h' via pyautogui (correct)
2. Type 'e' via pyautogui (correct)
3. Type 'k' via pyautogui (typo for 'l')
4. Type 'l' via pyautogui (1 extra char before noticing)
5. Press Backspace twice (delete 'kl')
6. Type 'l' via pyautogui (correct)
7. Type 'l' via pyautogui (correct)
8. Type 'o' via pyautogui (correct)

Final result: hello
```

### Deferred Typo Example

```
Intended: h e l l o
Check:    N N Y N N  (Y = deferred typo)
Typed:    h e k l o  (typo stays — recorded in tracker)

Later in review pass:
1. Ctrl+Home (go to top)
2. Ctrl+F → type surrounding context to find "heklo"
3. Escape (close find)
4. Backspace (delete 'k')
5. Type 'l' (correct character)
```

## Configuration

### Typo Frequency Settings

```yaml
typing:
  human_typing_enabled: true
  typo_frequency: "low"  # low, medium, high
  base_delay_ms: 150
  variation_percent: 30
  immediate_correction_ratio: 0.70  # 70% immediate, 30% deferred
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
3. **Placeholder text**: Keep markers intact
4. **Formatting markers**: Backticks, list prefixes
5. **Ctrl+F search text**: Must match exactly

## Performance Impact

### Time Overhead

**Low typos (2%)** at 150ms base delay:
- 1000 chars → ~20 typos
- Immediate (14): 14 × 7 extra keystrokes × 150ms = ~15s
- Deferred (6): 6 × review pass time (~3s each) = ~18s
- Total overhead: ~33s on a ~150s base = ~22%

**Medium typos (5%)**:
- 1000 chars → ~50 typos
- Overhead: ~80s on a ~150s base = ~53%

### Memory Usage

- O(1) constant memory for simulator
- O(n) for deferred typo tracker (n = number of deferred typos)
- QWERTY map: ~2KB static

## Testing

### Unit Tests

```python
def test_typo_generation():
    """Test typo generation uses adjacent keys."""
    simulator = HumanTypingSimulator(typo_frequency="high", enabled=True)
    
    typos = set()
    for _ in range(100):
        typo = simulator.generate_typo('e')
        typos.add(typo)
    
    expected = {'w', 'r', 'd', 's', '3', '4'}
    assert typos.issubset(expected)

def test_typo_frequency():
    """Test typo frequency matches configuration."""
    simulator = HumanTypingSimulator(typo_frequency="medium", enabled=True)
    
    typo_count = sum(1 for _ in range(1000) if simulator.should_make_typo())
    
    # Should be approximately 5% (50 typos), allow ±20% variance
    assert 40 <= typo_count <= 60

def test_typing_variation():
    """Test typing speed variation."""
    simulator = HumanTypingSimulator()
    base_delay = 150
    
    delays = [simulator.get_typing_delay(base_delay) for _ in range(100)]
    
    # Should vary within ±20% of base
    assert all(120 <= d <= 180 for d in delays)

def test_thinking_pauses():
    """Test thinking pauses occur occasionally."""
    simulator = HumanTypingSimulator()
    
    pause_count = 0
    for _ in range(1000):
        pause = simulator.get_thinking_pause()
        if pause > 0:
            pause_count += 1
            assert 100 <= pause <= 500
    
    # Should occur ~5% of time
    assert 35 <= pause_count <= 65
```

## Best Practices

1. **Use Low Frequency**: Start with "low" (2%) for most articles
2. **Disable for Code-Heavy Articles**: If article is mostly code, disable typos entirely
3. **Test First**: Test with short text before long articles
4. **Monitor Review Pass**: Watch the deferred correction pass to verify it works
5. **Adjust Timing**: If corrections look unnatural, adjust `immediate_correction_ratio`

---

**Last Updated**: 2025-03-01
