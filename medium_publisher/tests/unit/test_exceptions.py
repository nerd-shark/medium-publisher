"""
Unit tests for custom exceptions module.
"""

import pytest
from medium_publisher.utils.exceptions import (
    PublishingError,
    AuthenticationError,
    BrowserError,
    ContentError,
    FileError,
)


class TestPublishingError:
    """Tests for PublishingError base exception."""
    
    def test_init_with_message_only(self):
        """Test initialization with message only."""
        error = PublishingError("Test error")
        assert error.message == "Test error"
        assert error.details == {}
        assert str(error) == "Test error"
    
    def test_init_with_message_and_details(self):
        """Test initialization with message and details."""
        details = {"file": "test.md", "line": 42}
        error = PublishingError("Test error", details)
        assert error.message == "Test error"
        assert error.details == details
        assert "file=test.md" in str(error)
        assert "line=42" in str(error)
    
    def test_str_representation_no_details(self):
        """Test string representation without details."""
        error = PublishingError("Simple error")
        assert str(error) == "Simple error"
    
    def test_str_representation_with_details(self):
        """Test string representation with details."""
        error = PublishingError("Error occurred", {"code": 500, "url": "https://example.com"})
        result = str(error)
        assert "Error occurred" in result
        assert "code=500" in result
        assert "url=https://example.com" in result
    
    def test_inheritance_from_exception(self):
        """Test that PublishingError inherits from Exception."""
        error = PublishingError("Test")
        assert isinstance(error, Exception)
    
    def test_can_be_raised(self):
        """Test that PublishingError can be raised."""
        with pytest.raises(PublishingError) as exc_info:
            raise PublishingError("Test error")
        assert str(exc_info.value) == "Test error"
    
    def test_can_be_caught_as_exception(self):
        """Test that PublishingError can be caught as Exception."""
        try:
            raise PublishingError("Test error")
        except Exception as e:
            assert isinstance(e, PublishingError)
            assert str(e) == "Test error"


class TestAuthenticationError:
    """Tests for AuthenticationError."""
    
    def test_inherits_from_publishing_error(self):
        """Test that AuthenticationError inherits from PublishingError."""
        error = AuthenticationError("Auth failed")
        assert isinstance(error, PublishingError)
        assert isinstance(error, Exception)
    
    def test_init_with_message(self):
        """Test initialization with message."""
        error = AuthenticationError("Invalid credentials")
        assert error.message == "Invalid credentials"
        assert str(error) == "Invalid credentials"
    
    def test_init_with_details(self):
        """Test initialization with details."""
        error = AuthenticationError("Login failed", {"email": "user@example.com"})
        assert error.message == "Login failed"
        assert error.details["email"] == "user@example.com"
    
    def test_can_be_raised(self):
        """Test that AuthenticationError can be raised."""
        with pytest.raises(AuthenticationError):
            raise AuthenticationError("2FA required")
    
    def test_can_be_caught_as_publishing_error(self):
        """Test that AuthenticationError can be caught as PublishingError."""
        try:
            raise AuthenticationError("Session expired")
        except PublishingError as e:
            assert isinstance(e, AuthenticationError)


class TestBrowserError:
    """Tests for BrowserError."""
    
    def test_inherits_from_publishing_error(self):
        """Test that BrowserError inherits from PublishingError."""
        error = BrowserError("Browser crashed")
        assert isinstance(error, PublishingError)
        assert isinstance(error, Exception)
    
    def test_init_with_message(self):
        """Test initialization with message."""
        error = BrowserError("Selector not found")
        assert error.message == "Selector not found"
        assert str(error) == "Selector not found"
    
    def test_init_with_details(self):
        """Test initialization with details."""
        error = BrowserError("Timeout", {"selector": "#editor", "timeout": 30000})
        assert error.message == "Timeout"
        assert error.details["selector"] == "#editor"
        assert error.details["timeout"] == 30000
    
    def test_can_be_raised(self):
        """Test that BrowserError can be raised."""
        with pytest.raises(BrowserError):
            raise BrowserError("Page load failed")
    
    def test_can_be_caught_as_publishing_error(self):
        """Test that BrowserError can be caught as PublishingError."""
        try:
            raise BrowserError("Network error")
        except PublishingError as e:
            assert isinstance(e, BrowserError)


class TestContentError:
    """Tests for ContentError."""
    
    def test_inherits_from_publishing_error(self):
        """Test that ContentError inherits from PublishingError."""
        error = ContentError("Invalid markdown")
        assert isinstance(error, PublishingError)
        assert isinstance(error, Exception)
    
    def test_init_with_message(self):
        """Test initialization with message."""
        error = ContentError("Malformed frontmatter")
        assert error.message == "Malformed frontmatter"
        assert str(error) == "Malformed frontmatter"
    
    def test_init_with_details(self):
        """Test initialization with details."""
        error = ContentError("Parse error", {"line": 10, "column": 5})
        assert error.message == "Parse error"
        assert error.details["line"] == 10
        assert error.details["column"] == 5
    
    def test_can_be_raised(self):
        """Test that ContentError can be raised."""
        with pytest.raises(ContentError):
            raise ContentError("Content too long")
    
    def test_can_be_caught_as_publishing_error(self):
        """Test that ContentError can be caught as PublishingError."""
        try:
            raise ContentError("Invalid characters")
        except PublishingError as e:
            assert isinstance(e, ContentError)


class TestFileError:
    """Tests for FileError."""
    
    def test_inherits_from_publishing_error(self):
        """Test that FileError inherits from PublishingError."""
        error = FileError("File not found")
        assert isinstance(error, PublishingError)
        assert isinstance(error, Exception)
    
    def test_init_with_message(self):
        """Test initialization with message."""
        error = FileError("Permission denied")
        assert error.message == "Permission denied"
        assert str(error) == "Permission denied"
    
    def test_init_with_details(self):
        """Test initialization with details."""
        error = FileError("Read error", {"path": "/path/to/file.md", "errno": 13})
        assert error.message == "Read error"
        assert error.details["path"] == "/path/to/file.md"
        assert error.details["errno"] == 13
    
    def test_can_be_raised(self):
        """Test that FileError can be raised."""
        with pytest.raises(FileError):
            raise FileError("File is empty")
    
    def test_can_be_caught_as_publishing_error(self):
        """Test that FileError can be caught as PublishingError."""
        try:
            raise FileError("Invalid file format")
        except PublishingError as e:
            assert isinstance(e, FileError)


class TestExceptionHierarchy:
    """Tests for exception hierarchy and broad exception handling."""
    
    def test_all_exceptions_inherit_from_publishing_error(self):
        """Test that all custom exceptions inherit from PublishingError."""
        exceptions = [
            AuthenticationError("test"),
            BrowserError("test"),
            ContentError("test"),
            FileError("test"),
        ]
        
        for exc in exceptions:
            assert isinstance(exc, PublishingError)
    
    def test_can_catch_all_with_publishing_error(self):
        """Test that all custom exceptions can be caught with PublishingError."""
        exception_types = [
            AuthenticationError,
            BrowserError,
            ContentError,
            FileError,
        ]
        
        for exc_type in exception_types:
            try:
                raise exc_type("Test error")
            except PublishingError as e:
                assert isinstance(e, exc_type)
    
    def test_specific_exception_handling(self):
        """Test that specific exceptions can be caught individually."""
        # Test AuthenticationError
        with pytest.raises(AuthenticationError):
            raise AuthenticationError("Auth failed")
        
        # Test BrowserError
        with pytest.raises(BrowserError):
            raise BrowserError("Browser crashed")
        
        # Test ContentError
        with pytest.raises(ContentError):
            raise ContentError("Parse failed")
        
        # Test FileError
        with pytest.raises(FileError):
            raise FileError("File not found")
    
    def test_exception_type_differentiation(self):
        """Test that different exception types can be differentiated."""
        auth_error = AuthenticationError("Auth")
        browser_error = BrowserError("Browser")
        content_error = ContentError("Content")
        file_error = FileError("File")
        
        assert type(auth_error) != type(browser_error)
        assert type(browser_error) != type(content_error)
        assert type(content_error) != type(file_error)
        assert type(file_error) != type(auth_error)
