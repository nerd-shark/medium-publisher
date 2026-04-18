"""
Tests for error recovery utilities.
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, AsyncMock, patch

from medium_publisher.utils.error_recovery import (
    RetryStrategy,
    RetryPolicy,
    RecoveryState,
    ErrorRecoveryManager,
    ProgressCheckpoint
)
from medium_publisher.utils.exceptions import (
    BrowserError,
    PublishingError
)


class TestRetryStrategy:
    """Tests for RetryStrategy enum."""
    
    def test_retry_strategies_exist(self):
        """Test all retry strategies are defined."""
        assert RetryStrategy.EXPONENTIAL_BACKOFF
        assert RetryStrategy.LINEAR_BACKOFF
        assert RetryStrategy.FIXED_DELAY
    
    def test_strategy_values(self):
        """Test strategy enum values."""
        assert RetryStrategy.EXPONENTIAL_BACKOFF.value == "exponential"
        assert RetryStrategy.LINEAR_BACKOFF.value == "linear"
        assert RetryStrategy.FIXED_DELAY.value == "fixed"


class TestRetryPolicy:
    """Tests for RetryPolicy."""
    
    def test_default_policy(self):
        """Test default retry policy."""
        policy = RetryPolicy()
        
        assert policy.max_attempts == 3
        assert policy.base_delay == 2.0
        assert policy.max_delay == 60.0
        assert policy.strategy == RetryStrategy.EXPONENTIAL_BACKOFF
        assert policy.backoff_multiplier == 2.0
        assert BrowserError in policy.retryable_exceptions
    
    def test_custom_policy(self):
        """Test custom retry policy."""
        policy = RetryPolicy(
            max_attempts=5,
            base_delay=1.0,
            max_delay=30.0,
            strategy=RetryStrategy.LINEAR_BACKOFF,
            backoff_multiplier=1.5
        )
        
        assert policy.max_attempts == 5
        assert policy.base_delay == 1.0
        assert policy.max_delay == 30.0
        assert policy.strategy == RetryStrategy.LINEAR_BACKOFF
        assert policy.backoff_multiplier == 1.5
    
    def test_exponential_backoff_delay(self):
        """Test exponential backoff delay calculation."""
        policy = RetryPolicy(
            base_delay=2.0,
            backoff_multiplier=2.0,
            strategy=RetryStrategy.EXPONENTIAL_BACKOFF
        )
        
        assert policy.calculate_delay(0) == 2.0  # 2 * 2^0
        assert policy.calculate_delay(1) == 4.0  # 2 * 2^1
        assert policy.calculate_delay(2) == 8.0  # 2 * 2^2
        assert policy.calculate_delay(3) == 16.0  # 2 * 2^3
    
    def test_linear_backoff_delay(self):
        """Test linear backoff delay calculation."""
        policy = RetryPolicy(
            base_delay=2.0,
            strategy=RetryStrategy.LINEAR_BACKOFF
        )
        
        assert policy.calculate_delay(0) == 2.0  # 2 * 1
        assert policy.calculate_delay(1) == 4.0  # 2 * 2
        assert policy.calculate_delay(2) == 6.0  # 2 * 3
        assert policy.calculate_delay(3) == 8.0  # 2 * 4
    
    def test_fixed_delay(self):
        """Test fixed delay calculation."""
        policy = RetryPolicy(
            base_delay=5.0,
            strategy=RetryStrategy.FIXED_DELAY
        )
        
        assert policy.calculate_delay(0) == 5.0
        assert policy.calculate_delay(1) == 5.0
        assert policy.calculate_delay(2) == 5.0
        assert policy.calculate_delay(10) == 5.0
    
    def test_max_delay_cap(self):
        """Test delay is capped at max_delay."""
        policy = RetryPolicy(
            base_delay=10.0,
            max_delay=30.0,
            backoff_multiplier=2.0,
            strategy=RetryStrategy.EXPONENTIAL_BACKOFF
        )
        
        assert policy.calculate_delay(0) == 10.0  # 10 * 2^0 = 10
        assert policy.calculate_delay(1) == 20.0  # 10 * 2^1 = 20
        assert policy.calculate_delay(2) == 30.0  # 10 * 2^2 = 40, capped at 30
        assert policy.calculate_delay(3) == 30.0  # 10 * 2^3 = 80, capped at 30


class TestRecoveryState:
    """Tests for RecoveryState."""
    
    def test_default_recovery_state(self):
        """Test default recovery state."""
        state = RecoveryState()
        
        assert state.rate_limiter_state == {}
        assert state.version_state == {}
        assert state.progress_state == {}
        assert state.session_state == {}
        assert isinstance(state.timestamp, float)
    
    def test_recovery_state_with_data(self):
        """Test recovery state with data."""
        rate_limiter = {"chars_typed": 100, "window_start": 1234567890.0}
        version = {"current": "v2", "completed": ["v1"]}
        progress = {"step": 5, "percentage": 50}
        session = {"article_path": "/path/to/article.md"}
        
        state = RecoveryState(
            rate_limiter_state=rate_limiter,
            version_state=version,
            progress_state=progress,
            session_state=session
        )
        
        assert state.rate_limiter_state == rate_limiter
        assert state.version_state == version
        assert state.progress_state == progress
        assert state.session_state == session


class TestErrorRecoveryManager:
    """Tests for ErrorRecoveryManager."""
    
    def test_initialization(self):
        """Test error recovery manager initialization."""
        manager = ErrorRecoveryManager()
        
        assert manager.default_policy is not None
        assert manager.recovery_state is None
    
    def test_initialization_with_custom_policy(self):
        """Test initialization with custom policy."""
        policy = RetryPolicy(max_attempts=5)
        manager = ErrorRecoveryManager(default_policy=policy)
        
        assert manager.default_policy == policy
        assert manager.default_policy.max_attempts == 5
    
    @pytest.mark.asyncio
    async def test_retry_success_first_attempt(self):
        """Test retry succeeds on first attempt."""
        manager = ErrorRecoveryManager()
        
        async def successful_operation():
            return "success"
        
        result = await manager.retry_with_policy(
            successful_operation,
            operation_name="test_op"
        )
        
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_retry_success_after_failures(self):
        """Test retry succeeds after some failures."""
        manager = ErrorRecoveryManager()
        
        call_count = 0
        
        async def flaky_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise BrowserError("Temporary failure")
            return "success"
        
        result = await manager.retry_with_policy(
            flaky_operation,
            operation_name="flaky_op"
        )
        
        assert result == "success"
        assert call_count == 3
    
    @pytest.mark.asyncio
    async def test_retry_all_attempts_fail(self):
        """Test retry fails after all attempts."""
        manager = ErrorRecoveryManager()
        
        async def failing_operation():
            raise BrowserError("Permanent failure")
        
        with pytest.raises(PublishingError) as exc_info:
            await manager.retry_with_policy(
                failing_operation,
                operation_name="failing_op"
            )
        
        assert "failed after 3 attempts" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_retry_non_retryable_exception(self):
        """Test non-retryable exception is not retried."""
        manager = ErrorRecoveryManager()
        
        call_count = 0
        
        async def non_retryable_operation():
            nonlocal call_count
            call_count += 1
            raise ValueError("Non-retryable error")
        
        with pytest.raises(ValueError):
            await manager.retry_with_policy(
                non_retryable_operation,
                operation_name="non_retryable_op"
            )
        
        assert call_count == 1  # Should not retry
    
    @pytest.mark.asyncio
    async def test_retry_with_custom_policy(self):
        """Test retry with custom policy."""
        manager = ErrorRecoveryManager()
        
        policy = RetryPolicy(
            max_attempts=5,
            base_delay=0.1,
            strategy=RetryStrategy.FIXED_DELAY
        )
        
        call_count = 0
        
        async def flaky_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 4:
                raise BrowserError("Temporary failure")
            return "success"
        
        result = await manager.retry_with_policy(
            flaky_operation,
            policy=policy,
            operation_name="custom_policy_op"
        )
        
        assert result == "success"
        assert call_count == 4

    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Network tests require aiohttp integration")
    async def test_check_network_connection_success(self):
        """Test network connection check succeeds."""
        pass
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Network tests require aiohttp integration")
    async def test_check_network_connection_failure(self):
        """Test network connection check fails."""
        pass
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Network tests require aiohttp integration")
    async def test_check_network_connection_server_error(self):
        """Test network connection check with server error."""
        pass
    
    @pytest.mark.asyncio
    async def test_wait_for_network_reconnection_success(self):
        """Test waiting for network reconnection succeeds."""
        manager = ErrorRecoveryManager()
        
        call_count = 0
        
        async def mock_check():
            nonlocal call_count
            call_count += 1
            return call_count >= 2  # Succeed on second check
        
        manager.check_network_connection = mock_check
        
        result = await manager.wait_for_network_reconnection(
            max_wait_time=10.0,
            check_interval=0.1
        )
        
        assert result is True
        assert call_count >= 2
    
    @pytest.mark.asyncio
    async def test_wait_for_network_reconnection_timeout(self):
        """Test waiting for network reconnection times out."""
        manager = ErrorRecoveryManager()
        
        async def mock_check():
            return False  # Always fail
        
        manager.check_network_connection = mock_check
        
        result = await manager.wait_for_network_reconnection(
            max_wait_time=0.5,
            check_interval=0.1
        )
        
        assert result is False
    
    def test_save_recovery_state(self):
        """Test saving recovery state."""
        manager = ErrorRecoveryManager()
        
        rate_limiter = {"chars_typed": 100}
        version = {"current": "v2"}
        progress = {"step": 5}
        session = {"article_path": "/path"}
        
        manager.save_recovery_state(
            rate_limiter_state=rate_limiter,
            version_state=version,
            progress_state=progress,
            session_state=session
        )
        
        assert manager.recovery_state is not None
        assert manager.recovery_state.rate_limiter_state == rate_limiter
        assert manager.recovery_state.version_state == version
        assert manager.recovery_state.progress_state == progress
        assert manager.recovery_state.session_state == session
    
    def test_save_recovery_state_empty(self):
        """Test saving empty recovery state."""
        manager = ErrorRecoveryManager()
        
        manager.save_recovery_state()
        
        assert manager.recovery_state is not None
        assert manager.recovery_state.rate_limiter_state == {}
        assert manager.recovery_state.version_state == {}
        assert manager.recovery_state.progress_state == {}
        assert manager.recovery_state.session_state == {}
    
    def test_restore_recovery_state(self):
        """Test restoring recovery state."""
        manager = ErrorRecoveryManager()
        
        rate_limiter = {"chars_typed": 100}
        manager.save_recovery_state(rate_limiter_state=rate_limiter)
        
        restored = manager.restore_recovery_state()
        
        assert restored is not None
        assert restored.rate_limiter_state == rate_limiter
    
    def test_restore_recovery_state_none(self):
        """Test restoring when no state saved."""
        manager = ErrorRecoveryManager()
        
        restored = manager.restore_recovery_state()
        
        assert restored is None
    
    def test_clear_recovery_state(self):
        """Test clearing recovery state."""
        manager = ErrorRecoveryManager()
        
        manager.save_recovery_state(rate_limiter_state={"chars_typed": 100})
        assert manager.recovery_state is not None
        
        manager.clear_recovery_state()
        assert manager.recovery_state is None
    
    @pytest.mark.asyncio
    async def test_recover_from_browser_crash(self):
        """Test browser crash recovery."""
        manager = ErrorRecoveryManager()
        
        mock_browser = Mock()
        
        async def browser_factory():
            return mock_browser
        
        result = await manager.recover_from_browser_crash(browser_factory)
        
        assert result == mock_browser
    
    @pytest.mark.asyncio
    async def test_recover_from_browser_crash_failure(self):
        """Test browser crash recovery failure."""
        manager = ErrorRecoveryManager()
        
        async def failing_factory():
            raise Exception("Factory failed")
        
        with pytest.raises(BrowserError) as exc_info:
            await manager.recover_from_browser_crash(failing_factory)
        
        assert "Failed to recover from browser crash" in str(exc_info.value)


class TestProgressCheckpoint:
    """Tests for ProgressCheckpoint."""
    
    def test_initialization(self):
        """Test progress checkpoint initialization."""
        checkpoint = ProgressCheckpoint()
        
        assert checkpoint.checkpoints == {}
    
    def test_save_checkpoint(self):
        """Test saving checkpoint."""
        checkpoint = ProgressCheckpoint()
        
        data = {"step": 5, "article": "test.md"}
        checkpoint.save_checkpoint("checkpoint1", data)
        
        assert "checkpoint1" in checkpoint.checkpoints
        assert checkpoint.checkpoints["checkpoint1"]["step"] == 5
        assert checkpoint.checkpoints["checkpoint1"]["article"] == "test.md"
        assert "timestamp" in checkpoint.checkpoints["checkpoint1"]
    
    def test_restore_checkpoint(self):
        """Test restoring checkpoint."""
        checkpoint = ProgressCheckpoint()
        
        data = {"step": 5, "article": "test.md"}
        checkpoint.save_checkpoint("checkpoint1", data)
        
        restored = checkpoint.restore_checkpoint("checkpoint1")
        
        assert restored is not None
        assert restored["step"] == 5
        assert restored["article"] == "test.md"
        assert "timestamp" in restored
    
    def test_restore_nonexistent_checkpoint(self):
        """Test restoring nonexistent checkpoint."""
        checkpoint = ProgressCheckpoint()
        
        restored = checkpoint.restore_checkpoint("nonexistent")
        
        assert restored is None
    
    def test_clear_checkpoint(self):
        """Test clearing specific checkpoint."""
        checkpoint = ProgressCheckpoint()
        
        checkpoint.save_checkpoint("checkpoint1", {"step": 5})
        checkpoint.save_checkpoint("checkpoint2", {"step": 10})
        
        checkpoint.clear_checkpoint("checkpoint1")
        
        assert "checkpoint1" not in checkpoint.checkpoints
        assert "checkpoint2" in checkpoint.checkpoints
    
    def test_clear_nonexistent_checkpoint(self):
        """Test clearing nonexistent checkpoint."""
        checkpoint = ProgressCheckpoint()
        
        # Should not raise error
        checkpoint.clear_checkpoint("nonexistent")
    
    def test_clear_all_checkpoints(self):
        """Test clearing all checkpoints."""
        checkpoint = ProgressCheckpoint()
        
        checkpoint.save_checkpoint("checkpoint1", {"step": 5})
        checkpoint.save_checkpoint("checkpoint2", {"step": 10})
        checkpoint.save_checkpoint("checkpoint3", {"step": 15})
        
        checkpoint.clear_all_checkpoints()
        
        assert checkpoint.checkpoints == {}
    
    def test_list_checkpoints(self):
        """Test listing checkpoints."""
        checkpoint = ProgressCheckpoint()
        
        checkpoint.save_checkpoint("checkpoint1", {"step": 5})
        checkpoint.save_checkpoint("checkpoint2", {"step": 10})
        checkpoint.save_checkpoint("checkpoint3", {"step": 15})
        
        checkpoints = checkpoint.list_checkpoints()
        
        assert len(checkpoints) == 3
        assert "checkpoint1" in checkpoints
        assert "checkpoint2" in checkpoints
        assert "checkpoint3" in checkpoints
    
    def test_list_checkpoints_empty(self):
        """Test listing checkpoints when empty."""
        checkpoint = ProgressCheckpoint()
        
        checkpoints = checkpoint.list_checkpoints()
        
        assert checkpoints == []
    
    def test_multiple_saves_same_checkpoint(self):
        """Test saving same checkpoint multiple times."""
        checkpoint = ProgressCheckpoint()
        
        checkpoint.save_checkpoint("checkpoint1", {"step": 5})
        checkpoint.save_checkpoint("checkpoint1", {"step": 10})
        
        restored = checkpoint.restore_checkpoint("checkpoint1")
        
        assert restored["step"] == 10  # Should have latest value
