# Student Handbook

A comprehensive web application for students to manage their academic life. This application helps students keep track of their notes, tasks, and schedule in one place.

## Features

- **User Authentication**
  - Secure login and registration system
  - Session management for protected routes

- **Notes Management**
  - Create and view personal notes
  - Organize notes with titles and timestamps
  - Rich text editing capabilities

- **Task Management**
  - Create and track tasks
  - Set due dates for tasks
  - Mark tasks as complete/incomplete
  - View tasks by status and due date

- **Dashboard**
  - Clean and intuitive user interface
  - Quick access to all features
  - Responsive design for all devices

## Technology Stack

- **Backend**
  - Flask (Python web framework)
  - MongoDB (Database)
  - Flask-CORS (Cross-Origin Resource Sharing)

- **Frontend**
  - HTML5
  - CSS3 (Modern styling with Flexbox and Grid)
  - JavaScript (ES6+)
  - Responsive Design

## Project Structure

```
student_tracking_system/
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── dashboard.js
├── templates/
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── app.py
└── requirements.txt
```

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd student_tracking_system
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start MongoDB service

4. Run the application:
```bash
python app.py
```

5. Access the application at `http://localhost:5000`

## Usage

1. Register a new account or login with existing credentials
2. Use the dashboard to:
   - Create and manage notes
   - Add and track tasks
   - View your calendar
   - Update your profile

## Development

- The application uses Flask's blueprint structure for scalability
- MongoDB is used for flexible document storage
- Frontend is built with vanilla JavaScript for simplicity and performance
- Responsive design ensures compatibility across devices

## Security Features

- Password hashing for user security
- Session-based authentication
- Protected API endpoints
- CORS protection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
