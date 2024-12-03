# Student Tracking System

A comprehensive student performance management platform with advanced data tracking and analytics capabilities.

## 🚀 Features

- **Authentication System**
  - JWT-based authentication
  - Secure password hashing (PBKDF2-SHA256)
  - Multi-device support
  - Session management

- **Student Performance Analytics**
  - Real-time grade tracking
  - Course progress monitoring
  - Performance metrics visualization
  - Personalized recommendations

- **Notification System**
  - Real-time notifications
  - Multiple notification types
  - Read/unread status tracking
  - Custom notification creation

- **Device Synchronization**
  - Multi-device data sync
  - Offline support
  - Conflict resolution
  - Real-time updates

## 🛠️ Technology Stack

### Backend
- Python
- Flask (Web Framework)
- SQLite (Database)
- JWT (Authentication)
- PBKDF2-SHA256 (Password Hashing)

### Frontend
- React
- Material-UI
- Axios
- React Router
- Context API

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+
- Git

## 🔧 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/student_tracking_system.git
cd student_tracking_system
```

2. **Set up the backend**
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

3. **Set up the frontend**
```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

## 🚀 Running the Application

1. **Start the backend server**
```bash
# From the root directory
python src/api/routes.py
```

2. **Start the frontend development server**
```bash
# From the frontend directory
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 📁 Project Structure

```
student_tracking_system/
├── src/
│   ├── core/
│   │   ├── auth.py          # Authentication logic
│   │   ├── analytics.py     # Performance analytics
│   │   ├── notifications.py # Notification system
│   │   ├── sync.py         # Device synchronization
│   │   └── app.py          # Main application class
│   └── api/
│       └── routes.py        # API endpoints
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   ├── hooks/         # Custom hooks
│   │   ├── services/      # API services
│   │   └── utils/         # Utility functions
│   ├── public/
│   └── package.json
├── data/                   # SQLite database
├── docs/                   # Documentation
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md
```

## 🔒 Security Features

- JWT-based authentication
- Password hashing with PBKDF2-SHA256
- Input validation and sanitization
- CORS protection
- Rate limiting
- Error handling and logging

## 🔄 API Endpoints

### Authentication
- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - User login

### Dashboard
- GET `/api/dashboard/<student_id>` - Get dashboard data
- GET `/api/performance/<student_id>/analytics` - Get performance analytics

### Courses
- GET `/api/courses/<student_id>` - Get student courses
- GET `/api/courses/<course_code>/progress/<student_id>` - Get course progress
- POST `/api/courses/<course_code>/progress/<student_id>` - Update course progress

### Notifications
- GET `/api/notifications/<student_id>` - Get notifications
- POST `/api/notifications/<notification_id>/read` - Mark notification as read

### Device Sync
- POST `/api/sync/<student_id>/device/<device_id>` - Sync device data
- GET `/api/sync/<student_id>/device/<device_id>` - Get device sync status

## 🧪 Testing

```bash
# Run backend tests
python -m pytest tests/

# Run frontend tests
cd frontend
npm test
```

## 📈 Performance Monitoring

The system includes built-in performance monitoring:
- API response times
- Database query performance
- Frontend component rendering
- Network request tracking

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Your Name - your.email@example.com
Project Link: [https://github.com/yourusername/student_tracking_system](https://github.com/yourusername/student_tracking_system)
