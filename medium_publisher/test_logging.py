"""Test script to verify logging is working correctly."""

from utils.logger import get_logger, MediumPublisherLogger

# Get logger instance
logger = get_logger("test")

# Get log file path
logger_instance = MediumPublisherLogger()
log_file = logger_instance.get_log_file_path()

print(f"Log file location: {log_file}")
print(f"Log file exists: {log_file.exists()}")

# Test different log levels
logger.debug("This is a DEBUG message")
logger.info("This is an INFO message")
logger.warning("This is a WARNING message")
logger.error("This is an ERROR message")
logger.critical("This is a CRITICAL message")

# Test exception logging
try:
    raise ValueError("Test exception for logging")
except Exception as e:
    logger.exception("Caught test exception")

print(f"\nLog messages written to: {log_file}")
print("Check the log file to verify all messages were written.")
