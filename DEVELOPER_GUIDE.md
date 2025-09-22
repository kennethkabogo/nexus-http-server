# Developer Guide

## Project Structure

The project is organized into the following directories:

- `gemini_server/`: Main server code
  - `api/`: API route handlers
  - `middleware/`: Middleware functions
  - `security/`: Security-related functions and utilities
  - `utils/`: General utility functions
- `templates/`: HTML templates
- `frontend/`: React frontend code
- `tests/`: Unit tests
- `docs/`: Documentation files

## Setting Up the Development Environment

1. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Server

To run the server in development mode:
```
python main.py
```

The server will start on http://localhost:8000

## Running Tests

To run the tests:
```
python -m pytest tests/
```

## Adding New API Routes

1. Create a new handler function in `gemini_server/api/`
2. Import the handler in `gemini_server/server.py`
3. Add the route using the `@route` decorator

## Adding New Middleware

1. Create a new middleware function in `gemini_server/middleware/`
2. Import the middleware in `gemini_server/main.py`
3. Add it to the `all_middlewares` list

## Code Style

- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Write docstrings for all functions and classes
- Keep functions small and focused on a single responsibility