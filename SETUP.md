# Student Tracking System - Setup Guide

## Prerequisites

### Backend Requirements
```bash
Python 3.8+
pip (Python package manager)
SQLite3
```

### Frontend Requirements
```bash
Node.js 14+
npm 6+
```

## Step-by-Step Setup

### 1. Clone and Setup Environment

```bash
# Clone the repository (if using version control)
git clone <repository-url>
cd student_tracking_system

# Create and activate Python virtual environment
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/MacOS
```

### 2. Install Dependencies

```bash
# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 3. Configure Environment Variables

```bash
# Backend configuration
# Copy example env file and edit with your settings
copy .env.example .env

# Frontend configuration
cd frontend
copy .env.example .env
cd ..
```

### 4. Initialize Database

```bash
# Create initial database and run migrations
python scripts/manage_db.py upgrade
```

### 5. Start the Application

```bash
# Terminal 1 - Start Backend Server
.\venv\Scripts\activate  # On Windows
python src/api/routes.py

# Terminal 2 - Start Frontend Development Server
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Verification Steps

1. **Check Backend Health**
   ```bash
   curl http://localhost:5000/api/health
   # Should return: {"status": "healthy"}
   ```

2. **Check Frontend**
   - Open http://localhost:3000 in your browser
   - You should see the login page

3. **Create Test Account**
   ```bash
   curl -X POST http://localhost:5000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "password": "test123",
       "name": "Test User",
       "student_id": "ST001"
     }'
   ```

## Common Issues and Solutions

### Backend Issues

1. **Database Connection Error**
   ```
   Error: Unable to connect to database
   ```
   Solution:
   - Check if SQLite file exists in data/student_tracking.db
   - Run migrations: `python scripts/manage_db.py upgrade`

2. **Port Already in Use**
   ```
   Error: Address already in use
   ```
   Solution:
   - Check if another process is using port 5000
   - Kill the process or change the port in src/api/routes.py

### Frontend Issues

1. **Node Modules Missing**
   ```
   Error: Cannot find module 'react'
   ```
   Solution:
   ```bash
   cd frontend
   rm -rf node_modules
   npm install
   ```

2. **Environment Variables Not Loading**
   Solution:
   - Ensure .env file exists in frontend directory
   - Restart the development server

## Development Workflow

### 1. Database Changes
```bash
# Create new migration
python scripts/manage_db.py create "description_of_change"

# Apply migration
python scripts/manage_db.py upgrade

# Revert migration
python scripts/manage_db.py downgrade revision_id
```

### 2. API Development
- Add new routes in src/api/routes.py
- Implement business logic in src/core/
- Test using curl or Postman

### 3. Frontend Development
```bash
cd frontend

# Start development server
npm start

# Run tests
npm test

# Build for production
npm run build
```

## Deployment

### 1. Production Build
```bash
# Backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.api.routes:app

# Frontend
cd frontend
npm run build
```

### 2. Environment Configuration
Update .env files with production settings:
- Set DEBUG=False
- Configure proper database URL
- Set secure JWT secret
- Enable CORS for production domain

### 3. Security Checklist
- [ ] Enable HTTPS
- [ ] Set secure cookie flags
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable security headers

## Monitoring and Maintenance

### 1. Database Maintenance
```bash
# Backup database
sqlite3 data/student_tracking.db ".backup 'backup.db'"

# Check database integrity
sqlite3 data/student_tracking.db "PRAGMA integrity_check;"
```

### 2. Log Monitoring
- Backend logs: `logs/app.log`
- Frontend console logs
- Database query logs

### 3. Performance Monitoring
- API response times
- Database query performance
- Frontend load times
- Memory usage

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs in logs/app.log
3. Contact support team

## Contributing

1. Create feature branch
2. Make changes
3. Run tests
4. Submit pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
