# Student Success Platform Frontend

The React-based frontend for the Ultimate Student Handbook project, providing an intuitive interface for student performance tracking and analytics.

## Directory Structure

```
dbms frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   └── Navigation.js    # Main navigation component
│   ├── pages/              # Page components
│   │   ├── Dashboard.js     # Main dashboard
│   │   ├── Students.js      # Student management
│   │   ├── Courses.js       # Course catalog
│   │   ├── Progress.js      # Progress tracking
│   │   └── Analytics.js     # Performance analytics
│   ├── utils/              # Utility functions
│   ├── App.js              # Main application component
│   └── index.js            # Application entry point
├── public/                 # Static files
└── package.json            # Project dependencies
```

## Features

- Material-UI based modern interface
- Responsive design for all screen sizes
- Real-time data visualization
- Interactive charts and graphs
- Intuitive navigation
- Student performance tracking
- Course management interface
- Analytics dashboard

## Dependencies

- React 18.2.0
- Material-UI (@mui/material) 5.14.18
- React Router DOM 6.20.0
- Axios 1.6.2
- Chart.js 4.4.0
- React ChartJS 2 5.2.0

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm start
```

The application will be available at http://localhost:3000

## Available Scripts

- `npm start` - Start development server
- `npm build` - Build production version
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## API Integration

The frontend communicates with the Flask backend at http://localhost:5000 through the following endpoints:

### Students
- GET `/api/students` - Get all students
- GET `/api/students/:id` - Get student details
- POST `/api/students` - Create new student
- PUT `/api/students/:id` - Update student

### Courses
- GET `/api/textbooks` - Get all courses
- GET `/api/textbooks/:id` - Get course details
- GET `/api/textbooks/:id/topics` - Get course topics

### Progress
- GET `/api/progress/:studentId` - Get student progress
- POST `/api/progress` - Update progress
- GET `/api/progress/:studentId/topics` - Get topic progress

### Analytics
- GET `/api/analytics/:studentId` - Get student analytics
- GET `/api/analytics/:studentId/performance` - Get performance metrics
- GET `/api/analytics/:studentId/strengths` - Get strength analysis

## Component Overview

### Navigation
- Main navigation bar
- Responsive drawer for mobile
- Route management

### Dashboard
- Overview cards
- Performance charts
- Quick access links

### Students
- Student list view
- Student details
- Performance metrics

### Courses
- Course catalog
- Course details
- Topic organization

### Progress
- Progress tracking
- Completion status
- Understanding metrics

### Analytics
- Performance charts
- Trend analysis
- Strength/weakness identification

## Contributing

Please read the main project's CONTRIBUTING.md for guidelines.
