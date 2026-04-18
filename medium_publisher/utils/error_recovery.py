"""
Error recovery utilities for Medium Article Publisher.

Provides retry logic, network reconnection, browser crash recovery,
and state preservation across retries.
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Callable, Any, Optional, Dict
from enum import Enum

from .logger import get_logger
from .exceptions import (
    BrowserError,
    AuthenticationError,
    PublishingError
)


class RetryStrategy(Enum):
    """Retry strategy types."""
    EXPONENTIAL_BACKOFF = "exponential"
    LINEAR_BACKOFF = "linear"
    FIXED_DELAY = "fixed"


@dataclass
class RetryPolicy:
    """
    Retry policy configuration.
    
    Attributes:
        max_attempts: Maximum number of retry attempts
        base_delay: Base delay in seconds between retries
        max_delay: Maximum delay in seconds
        strategy: Retry strategy (exponential, linear, fixed)
        backoff_multiplier: Multiplier for exponential backoff
        retryable_exceptions: Tuple of exception types to retry
    """
    max_attempts: int = 3
    base_delay: float = 2.0
    max_delay: float = 60.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    backoff_multiplier: float = 2.0
    retryable_exceptions: tuple = (BrowserError, ConnectionError, TimeoutError)
    
    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for given attempt number.
        
        Args:
            attempt: Current attempt number (0-indexed)
            
        Returns:
            Delay in seconds
        """
        if self.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            delay = self.base_delay * (self.backoff_multiplier ** attempt)
        elif self.strategy == RetryStrategy.LINEAR_BACKOFF:
            delay = self.base_delay * (attempt + 1)
        else:  # FIXED_DELAY
            delay = self.base_delay
        
        return min(delay, self.max_delay)


@dataclass
class RecoveryState:
    """
    State to preserve across retries and recovery.
    
    Attributes:
        rate_limiter_state: Rate limiter state (chars_typed, window_start)
        version_state: Version tracking state (current, completed)
        progress_state: Progress tracking (step, percentage)
        session_state: Session metadata
        timestamp: When state was saved
    """
    rate_limiter_state: Dict[str, Any] = field(default_factory=dict)
    version_state: Dict[str, Any] = field(default_factory=dict)
    progress_state: Dict[str, Any] = field(default_factory=dict)
    session_state: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class ErrorRecoveryManager:
    """
    Manages error recovery, retries, and state preservation.
    
    Provides:
    - Retry logic with configurable policies
    - Network reconnection handling
    - Browser crash recovery
    - State preservation across retries
    """
    
    def __init__(self, default_policy: Optional[RetryPolicy] = None):
        """
        Initialize error recovery manager.
        
        Args:
            default_policy: Default retry policy (uses defaults if None)
        """
        self.logger = get_logger("ErrorRecoveryManager")
        self.default_policy = default_policy or RetryPolicy()
        self.recovery_state: Optional[RecoveryState] = None
    
    async def retry_with_policy(
        self,
        operation: Callable,
        *args,
        policy: Optional[RetryPolicy] = None,
        operation_name: str = "operation",
        **kwargs
    ) -> Any:
        """
        Retry an operation with specified policy.
        
        Args:
            operation: Async function to retry
            *args: Positional arguments for operation
            policy: Retry policy (uses default if None)
            operation_name: Name for logging
            **kwargs: Keyword arguments for operation
            
        Returns:
            Result of operation
            
        Raises:
            Exception: If all retries fail
        """
        policy = policy or self.default_policy
        last_error = None
        
        for attempt in range(policy.max_attempts):
            try:
                self.logger.info(
                    f"Attempting {operation_name} "
                    f"(attempt {attempt + 1}/{policy.max_attempts})"
                )
                
                result = await operation(*args, **kwargs)
                
                if attempt > 0:
                    self.logger.info(
                        f"{operation_name} succeeded on attempt {attempt + 1}"
                    )
                
                return result
                
            except policy.retryable_exceptions as e:
                last_error = e
                self.logger.warning(
                    f"{operation_name} failed on attempt {attempt + 1}: {e}"
                )
                
                if attempt < policy.max_attempts - 1:
                    delay = policy.calculate_delay(attempt)
                    self.logger.info(f"Retrying in {delay:.1f} seconds...")
                    await asyncio.sleep(delay)
            
            except Exception as e:
                # Non-retryable exception
                self.logger.error(
                    f"{operation_name} failed with non-retryable error: {e}"
                )
                raise
        
        # All retries failed
        self.logger.error(
            f"{operation_name} failed after {policy.max_attempts} attempts"
        )
        raise PublishingError(
            f"{operation_name} failed after {policy.max_attempts} attempts: {last_error}"
        ) from last_error

    
    async def check_network_connection(
        self,
        test_url: str = "https://medium.com",
        timeout: float = 10.0
    ) -> bool:
        """
        Check if network connection is available.
        
        Args:
            test_url: URL to test connection
            timeout: Timeout in seconds
            
        Returns:
            True if connection available, False otherwise
        """
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(test_url, timeout=timeout) as response:
                    return response.status < 500
                    
        except Exception as e:
            self.logger.warning(f"Network connection check failed: {e}")
            return False
    
    async def wait_for_network_reconnection(
        self,
        max_wait_time: float = 300.0,
        check_interval: float = 5.0
    ) -> bool:
        """
        Wait for network reconnection.
        
        Args:
            max_wait_time: Maximum time to wait in seconds
            check_interval: Interval between checks in seconds
            
        Returns:
            True if reconnected, False if timeout
        """
        self.logger.info("Waiting for network reconnection...")
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            if await self.check_network_connection():
                elapsed = time.time() - start_time
                self.logger.info(f"Network reconnected after {elapsed:.1f} seconds")
                return True
            
            self.logger.debug(
                f"Network still unavailable, checking again in {check_interval}s..."
            )
            await asyncio.sleep(check_interval)
        
        self.logger.error(f"Network reconnection timeout after {max_wait_time}s")
        return False
    
    def save_recovery_state(
        self,
        rate_limiter_state: Optional[Dict[str, Any]] = None,
        version_state: Optional[Dict[str, Any]] = None,
        progress_state: Optional[Dict[str, Any]] = None,
        session_state: Optional[Dict[str, Any]] = None
    ):
        """
        Save state for recovery.
        
        Args:
            rate_limiter_state: Rate limiter state
            version_state: Version tracking state
            progress_state: Progress tracking state
            session_state: Session metadata
        """
        self.recovery_state = RecoveryState(
            rate_limiter_state=rate_limiter_state or {},
            version_state=version_state or {},
            progress_state=progress_state or {},
            session_state=session_state or {},
            timestamp=time.time()
        )
        
        self.logger.info("Recovery state saved")
    
    def restore_recovery_state(self) -> Optional[RecoveryState]:
        """
        Restore saved recovery state.
        
        Returns:
            RecoveryState if available, None otherwise
        """
        if self.recovery_state:
            age = time.time() - self.recovery_state.timestamp
            self.logger.info(f"Restoring recovery state (age: {age:.1f}s)")
            return self.recovery_state
        
        self.logger.warning("No recovery state available")
        return None
    
    def clear_recovery_state(self):
        """Clear saved recovery state."""
        self.recovery_state = None
        self.logger.info("Recovery state cleared")
    
    async def recover_from_browser_crash(
        self,
        browser_factory: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Recover from browser crash by reinitializing.
        
        Args:
            browser_factory: Function to create new browser instance
            *args: Positional arguments for factory
            **kwargs: Keyword arguments for factory
            
        Returns:
            New browser instance
            
        Raises:
            BrowserError: If recovery fails
        """
        self.logger.warning("Attempting browser crash recovery...")
        
        try:
            # Wait a bit before reinitializing
            await asyncio.sleep(2.0)
            
            # Create new browser instance
            browser = await browser_factory(*args, **kwargs)
            
            self.logger.info("Browser crash recovery successful")
            return browser
            
        except Exception as e:
            self.logger.error(f"Browser crash recovery failed: {e}")
            raise BrowserError(f"Failed to recover from browser crash: {e}") from e


class ProgressCheckpoint:
    """
    Manages progress checkpoints for resume capability.
    
    Allows saving progress before major operations and resuming from
    last checkpoint on failure.
    """
    
    def __init__(self):
        """Initialize progress checkpoint manager."""
        self.logger = get_logger("ProgressCheckpoint")
        self.checkpoints: Dict[str, Dict[str, Any]] = {}
    
    def save_checkpoint(
        self,
        checkpoint_id: str,
        data: Dict[str, Any]
    ):
        """
        Save a progress checkpoint.
        
        Args:
            checkpoint_id: Unique identifier for checkpoint
            data: Checkpoint data to save
        """
        self.checkpoints[checkpoint_id] = {
            **data,
            "timestamp": time.time()
        }
        
        self.logger.info(f"Checkpoint saved: {checkpoint_id}")
    
    def restore_checkpoint(
        self,
        checkpoint_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Restore a progress checkpoint.
        
        Args:
            checkpoint_id: Checkpoint identifier
            
        Returns:
            Checkpoint data if exists, None otherwise
        """
        if checkpoint_id in self.checkpoints:
            data = self.checkpoints[checkpoint_id]
            age = time.time() - data["timestamp"]
            self.logger.info(
                f"Checkpoint restored: {checkpoint_id} (age: {age:.1f}s)"
            )
            return data
        
        self.logger.warning(f"Checkpoint not found: {checkpoint_id}")
        return None
    
    def clear_checkpoint(self, checkpoint_id: str):
        """
        Clear a specific checkpoint.
        
        Args:
            checkpoint_id: Checkpoint identifier
        """
        if checkpoint_id in self.checkpoints:
            del self.checkpoints[checkpoint_id]
            self.logger.info(f"Checkpoint cleared: {checkpoint_id}")
    
    def clear_all_checkpoints(self):
        """Clear all checkpoints."""
        count = len(self.checkpoints)
        self.checkpoints.clear()
        self.logger.info(f"All checkpoints cleared ({count} total)")
    
    def list_checkpoints(self) -> list:
        """
        List all checkpoint IDs.
        
        Returns:
            List of checkpoint IDs
        """
        return list(self.checkpoints.keys())
