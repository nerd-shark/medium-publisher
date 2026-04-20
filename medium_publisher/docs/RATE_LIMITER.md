# Typing Speed Control

## Overview

The Medium Keyboard Publisher controls typing speed through configurable delays between keystrokes. There is no external rate limiter or sliding window algorithm — speed is governed by `base_delay_ms` and `variation_percent` in the configuration.

## How Typing Speed Works

### Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `base_delay_ms` | 150 | Milliseconds between each keystroke |
| `variation_percent` | 30 | Random ±% variation applied to base delay |

### Effective Speed

With default settings (150ms base, 30% variation):
- **Minimum delay**: 150 × 0.70 = 105ms per character
- **Maximum delay**: 150 × 1.30 = 195ms per character
- **Average**: ~150ms per character → ~6.7 characters/second → ~400 chars/minute

### Speed Calculation

The `HumanTypingSimulator.get_typing_delay()` method applies variation:

```python
def get_typing_delay(self, base_delay: int) -> int:
    """Add random variation to typing delay.
    
    Args:
        base_delay: Base delay in milliseconds (from config)
    
    Returns:
        Varied delay in milliseconds
    """
    variation = random.uniform(
        -self.variation_percent / 100,
        self.variation_percent / 100
    )
    return int(base_delay * (1 + variation))
```

## Time Estimation

### Formula

```python
def estimate_typing_time(total_chars: int, base_delay_ms: int, typo_rate: float) -> int:
    """Estimate total typing time in seconds.
    
    Args:
        total_chars: Number of characters to type
        base_delay_ms: Base delay between keystrokes (ms)
        typo_rate: Typo frequency (0.0-0.08)
    
    Returns:
        Estimated time in seconds
    """
    # Base typing time
    base_time_ms = total_chars * base_delay_ms
    
    # Typo overhead: each typo adds ~7 extra keystrokes
    num_typos = int(total_chars * typo_rate)
    typo_overhead_ms = num_typos * 7 * base_delay_ms
    
    # Thinking pauses: ~5% of characters trigger a 100-500ms pause
    pause_chars = int(total_chars * 0.05)
    avg_pause_ms = 300  # average of 100-500ms
    pause_overhead_ms = pause_chars * avg_pause_ms
    
    total_ms = base_time_ms + typo_overhead_ms + pause_overhead_ms
    return int(total_ms / 1000)
```

### Example Calculations

**1000 characters, default settings (150ms), low typos (2%)**:
```
Base time:      1000 × 150ms = 150,000ms = 150s
Typo overhead:  20 typos × 7 × 150ms = 21,000ms = 21s
Thinking:       50 pauses × 300ms = 15,000ms = 15s
Total:          ~186 seconds ≈ 3.1 minutes
```

**5000 characters, default settings, medium typos (5%)**:
```
Base time:      5000 × 150ms = 750,000ms = 750s
Typo overhead:  250 typos × 7 × 150ms = 262,500ms = 262s
Thinking:       250 pauses × 300ms = 75,000ms = 75s
Total:          ~1087 seconds ≈ 18.1 minutes
```

**1000 characters, fast settings (80ms), no typos**:
```
Base time:      1000 × 80ms = 80,000ms = 80s
Typo overhead:  0
Thinking:       50 pauses × 300ms = 15,000ms = 15s
Total:          ~95 seconds ≈ 1.6 minutes
```

## Integration with ContentTyper

The `ContentTyper` class uses the typing delay on every character:

```python
class ContentTyper:
    def __init__(self, input_controller, typing_simulator, typo_tracker, config):
        self._base_delay_ms = config.get("typing.base_delay_ms", 150)
        # ...

    def _type_with_typos(self, text: str, allow_typos: bool = True):
        for char in text:
            # Get varied delay from simulator
            delay_ms = self._simulator.get_typing_delay(self._base_delay_ms)
            time.sleep(delay_ms / 1000.0)
            
            # Optional thinking pause
            pause = self._simulator.get_thinking_pause()
            if pause > 0:
                time.sleep(pause / 1000.0)
            
            # Type the character via OS-level input
            self._input.type_character(char)
```

## Configuring Speed

### In Settings Dialog

1. Open Settings → Typing
2. Adjust "Base Delay (ms)" slider or input
3. Adjust "Variation (%)" for randomness
4. Save

### In config.yaml

```yaml
typing:
  base_delay_ms: 150        # Milliseconds between keystrokes
  variation_percent: 30      # ±30% random variation
  human_typing_enabled: true # Enable typo simulation
  typo_frequency: "low"     # low (2%), medium (5%), high (8%)
```

### Speed Presets

| Preset | base_delay_ms | Effective Speed | Use Case |
|--------|--------------|-----------------|----------|
| Fast | 50-80 | ~12-20 chars/sec | Testing, short articles |
| Normal | 120-180 | ~5-8 chars/sec | Standard publishing |
| Careful | 200-300 | ~3-5 chars/sec | Maximum realism |

## Why No Hard Rate Limit?

The application uses OS-level keyboard input (pyautogui) to type into the browser. Since this produces real keystrokes indistinguishable from human typing, there is no need for an artificial rate limit. The typing speed is controlled purely by the delay between keystrokes, which the user can configure to their preference.

## Additional Timing Factors

Beyond the base delay, these factors affect total typing time:

1. **Thinking pauses**: 5% chance of 100-500ms pause per character
2. **Typo correction**: Each typo adds ~7 extra keystrokes at base delay
3. **Formatting shortcuts**: Brief delays for Ctrl+B, Ctrl+I, etc.
4. **Paragraph breaks**: Small delay between content blocks
5. **Review pass**: Deferred typo corrections at end (Ctrl+F → fix each)

## Monitoring Progress

The UI displays:
- **Elapsed time**: How long typing has been running
- **Estimated remaining**: Based on characters left × average delay
- **Block progress**: "Block N of M" counter
- **Characters typed**: Running count

---

**Last Updated**: 2025-03-01
