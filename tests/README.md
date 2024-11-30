# API Testing Guide

This directory contains automated tests for the Student Success Tracking System API. The tests verify the functionality, reliability, and error handling of our API endpoints.

## Test Structure

- `conftest.py`: Test configuration and fixtures
  - Sets up test client
  - Creates temporary test database
  - Provides test data

- `test_api.py`: API endpoint tests
  - Students API tests
  - Courses API tests
  - Progress tracking tests
  - Analytics tests
  - Error handling tests

## Running Tests

1. Install test dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run all tests:
   ```bash
   pytest tests/
   ```

3. Run specific test file:
   ```bash
   pytest tests/test_api.py
   ```

4. Run with verbose output:
   ```bash
   pytest -v tests/
   ```

5. Run with coverage report:
   ```bash
   pytest --cov=src tests/
   ```

## Test Categories

1. **Endpoint Tests**
   - Verify correct HTTP status codes
   - Check response data structure
   - Validate data content

2. **Data Validation**
   - Test required fields
   - Verify data types
   - Check constraints

3. **Error Handling**
   - Test invalid inputs
   - Check error responses
   - Verify error messages

4. **Integration Tests**
   - Test database interactions
   - Verify data persistence
   - Check relationships

## Adding New Tests

When adding new API endpoints, create corresponding test cases that:
1. Test successful operations
2. Verify error conditions
3. Check edge cases
4. Validate data integrity

Example test structure:
```python
def test_new_endpoint(client):
    # Test successful operation
    response = client.get('/api/new_endpoint')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'expected_field' in data

    # Test error condition
    response = client.get('/api/new_endpoint/invalid')
    assert response.status_code == 404
```

## Best Practices

1. Each test should be independent
2. Use descriptive test names
3. Test both valid and invalid scenarios
4. Clean up test data after each test
5. Use appropriate assertions
6. Document complex test cases
