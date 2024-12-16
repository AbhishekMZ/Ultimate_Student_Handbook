# Ultimate Student Handbook

A comprehensive web application designed to assist students in managing their academic life through note-taking, task tracking, and gamification features.

## Features

- **Task Management**: Track assignments, deadlines, and study sessions
- **Note Taking**: Organize and manage study notes
- **Gamification System**: 
  - Experience points (XP) for activities
  - Achievement system
  - Daily, weekly, and monthly challenges
  - Skill progression tracking
- **Progress Tracking**: Monitor academic progress and study habits

## Project Structure

```
student_tracking_system/
├── app/
│   ├── core/           # Core application functionality
│   ├── gamification/   # Gamification system components
│   ├── models/         # Database models
│   ├── routes/         # API routes and endpoints
│   ├── utils/          # Utility functions and helpers
│   ├── config.py       # Application configuration
│   └── __init__.py     # App initialization
├── static/
│   ├── css/
│   │   ├── components/ # Component-specific styles
│   │   └── themes/     # Theme-related styles
│   ├── js/
│   │   ├── core/       # Core JavaScript functionality
│   │   ├── gamification/# Gamification-related scripts
│   │   └── utils/      # Utility scripts
│   └── images/         # Image assets
├── templates/
│   ├── auth/          # Authentication templates
│   └── dashboard/     # Dashboard and main UI templates
├── tests/             # Test suite
├── .env.example       # Example environment variables
├── requirements.txt   # Python dependencies
└── run.py            # Application entry point
```

## API Endpoints

### Authentication
- `POST /auth/register`: Register new user
- `POST /auth/login`: User login
- `POST /auth/logout`: User logout

### Gamification
- `GET /api/progress`: Get user progress
- `GET /api/achievements`: Get user achievements
- `POST /api/daily-login`: Record daily login
- `POST /api/record-activity`: Record user activity
- `GET /api/challenges`: Get available challenges
- `POST /api/challenges/accept`: Accept a challenge
- `PUT /api/challenges/progress`: Update challenge progress

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/student_tracking_system.git
   cd student_tracking_system
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file:
   ```
   SECRET_KEY=your-secret-key
   MONGODB_URI=your-mongodb-uri
   MONGODB_NAME=student_tracking
   ```

5. Run the application:
   ```bash
   python run.py
   ```

## Testing

Run the test suite:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
