# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- View signed-up participants on each activity card
- Sign up for activities
- Unregister participants using the trash icon beside their email; participant counts and availability refresh automatically

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## Testing

From the repository root, install the dependencies and run the backend suite
with pytest:

```bash
python -m pip install -r requirements.txt
python -m pytest tests/
```

Tests live in the root `tests/` directory and use FastAPI's `TestClient`, so no
running server is required. New pytest tests use Arrange-Act-Assert (AAA):
prepare inputs and expected results, perform the request, then assert the
response and resulting state, with blank lines separating the three blocks.
Shared fixtures restore in-memory activity data after each new test. Existing
unittest-style tests retain their own setup and teardown and also run with pytest.

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/signup?email=student@mergington.edu` | Unregister a participant; returns 404 if the activity or registration does not exist |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
