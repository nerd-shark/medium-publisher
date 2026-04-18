# Integration Tests

This directory contains integration tests for the Medium Article Publisher. These tests interact with real browsers and external services (Medium.com).

## Prerequisites

1. **Medium Test Account**: You need a real Medium account for testing
2. **Environment Variables**: Set the following:
   ```bash
   export MEDIUM_TEST_EMAIL="your-test-email@example.com"
   export MEDIUM_TEST_PASSWORD="your-test-password"
   ```
3. **Playwright**: Ensure Playwright browsers are installed:
   ```bash
   python -m playwright install chromium
   ```

## Running Integration Tests

### Run All Integration Tests
```bash
pytest --integration tests/integration/
```

### Run Specific Test File
```bash
pytest --integration tests/integration/test_playwright_controller_integration.py
```

### Run Manual OAuth Tests
```bash
pytest --integration -m manual tests/integration/test_auth_handler_integration.py
```

### Skip Slow Tests
```bash
pytest --integration tests/integration/ -m "not slow"
```

### Run with Verbose Output
```bash
pytest --integration tests/integration/ -v
```

## Test Categories

### Fast Tests (1-5 minutes)
- `test_playwright_controller_integration.py` - Browser automation
- `test_auth_handler_integration.py` - Authentication (non-OAuth)
- `test_session_restoration_integration.py` - Session management

### Slow Tests (30-60 minutes)
- `test_content_typer_integration.py` - Rate limiting and typos
- `test_publishing_workflow_integration.py` - End-to-end publishing
- `test_version_workflow_integration.py` - Version updates
- `test_medium_editor_integration.py` - Editor interactions

### Manual Tests (5 minutes + user interaction)
- `test_auth_handler_integration.py::test_oauth_flow_manual_completion`
- `test_auth_handler_integration.py::test_oauth_session_restoration`

## Test Markers

- `@pytest.mark.integration` - All integration tests (skipped by default)
- `@pytest.mark.slow` - Tests that take 30+ minutes
- `@pytest.mark.manual` - Tests requiring manual user interaction

## Important Notes

### Rate Limiting
Tests that involve typing are VERY SLOW due to the 35 characters/minute rate limit. This is intentional and matches production behavior.

Example: A 1000-character article takes approximately 30 minutes to type.

### Manual OAuth Tests
OAuth tests require manual user interaction:
1. Test opens browser to Medium login page
2. User clicks "Sign in with Google"
3. User completes Google OAuth flow
4. Test detects successful login

### Draft Articles
Integration tests create real draft articles on Medium. These are NOT published publicly, but they will appear in your drafts.

### Test Failures
Tests may fail if:
- Medium's UI structure changes
- Network connection is unstable
- Session cookies expire
- Test account credentials are invalid

### Browser Visibility
By default, tests run with visible browser (headless=false) for debugging. To run headless, modify `test_config` in `conftest.py`.

## Test Structure

### conftest.py
- pytest configuration
- Custom markers (@pytest.mark.integration, @pytest.mark.slow, @pytest.mark.manual)
- Fixtures for credentials, config, test articles

### Test Files
- `test_playwright_controller_integration.py` - Browser automation
- `test_auth_handler_integration.py` - Authentication (email/password and OAuth)
- `test_medium_editor_integration.py` - Medium editor interactions
- `test_content_typer_integration.py` - Content typing with rate limiting
- `test_publishing_workflow_integration.py` - End-to-end publishing
- `test_version_workflow_integration.py` - Version updates
- `test_session_restoration_integration.py` - Session persistence

## Troubleshooting

### "Test credentials not provided"
Set MEDIUM_TEST_EMAIL and MEDIUM_TEST_PASSWORD environment variables.

### "Playwright browser not found"
Run: `python -m playwright install chromium`

### "Selector not found"
Medium's UI may have changed. Update selectors in `config/selectors.yaml`.

### "Rate limiting test too slow"
This is expected. Rate-limited tests take 30-60 minutes.

### "OAuth test timeout"
Complete the OAuth flow within 5 minutes, or the test will timeout.

## CI/CD Integration

For CI/CD pipelines, consider:
- Running only fast tests in PR validation
- Running slow tests nightly or weekly
- Skipping manual OAuth tests in automated pipelines
- Using headless mode for CI environments

Example CI command:
```bash
pytest --integration tests/integration/ -m "not slow and not manual" --headless
```

## Security

- Never commit test credentials to version control
- Use environment variables or secure secret management
- Test accounts should have minimal permissions
- Session cookies are stored in temporary directories during tests
- Clean up test drafts periodically

## Support

For issues with integration tests:
1. Check test output for detailed error messages
2. Verify test account credentials are valid
3. Ensure Medium.com is accessible
4. Check Playwright browser installation
5. Review test logs for debugging information
