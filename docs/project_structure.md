# Student Performance Tracking System - Project Structure

## Directory Structure

```
student_tracking_system/
├── backend/                    # Backend server implementation
│   ├── api/                   # API endpoints and routes
│   │   ├── __init__.py
│   │   └── student_performance.py
│   ├── core/                  # Core business logic
│   │   ├── __init__.py
│   │   ├── database_manager.py
│   │   └── user_management.py
│   ├── database/             # Database models and migrations
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── migrations/
│   ├── services/             # Business services
│   │   └── __init__.py
│   └── utils/                # Utility functions
│       └── __init__.py
├── frontend/                  # React frontend application
│   ├── public/
│   ├── src/
│   │   ├── components/       # Reusable React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── styles/          # CSS and styling
│   │   └── utils/           # Frontend utilities
│   └── package.json
├── src/                      # Additional source code
│   ├── analytics/           # Analytics and data processing
│   ├── api/                 # API configuration
│   ├── feedback/           # User feedback handling
│   ├── progress/           # Progress tracking
│   ├── study/             # Study materials management
│   └── utils/             # Utility functions
├── data/                    # Data files
│   ├── processed/          # Processed data files
│   │   └── csv/
│   └── raw/                # Raw data files
├── docs/                    # Documentation
│   ├── api/                # API documentation
│   ├── database/          # Database schema docs
│   └── setup/             # Setup instructions
├── resources/              # Static resources
│   ├── pdfs/              # PDF resources
│   └── study_materials/   # Study materials
├── scripts/                # Utility scripts
│   ├── database/          # Database scripts
│   ├── deployment/        # Deployment scripts
│   └── setup/             # Setup scripts
└── tests/                  # Test suite
    ├── backend/           # Backend tests
    └── frontend/          # Frontend tests

## Key Files

### Configuration
- `.env.example` - Environment variables template
- `requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies

### Backend
- `backend/api/student_performance.py` - Student performance API endpoints
- `backend/core/database_manager.py` - Database management utilities
- `backend/database/database.py` - Database connection and models

### Frontend
- `frontend/src/App.js` - Main React application
- `frontend/src/components/` - Reusable UI components
- `frontend/src/pages/` - Page-level components

### Scripts
- `scripts/setup/create_database.py` - Database initialization
- `scripts/setup/populate_data.py` - Sample data generation
- `scripts/deployment/` - Deployment automation

## Import Structure

### Backend Imports
Use relative imports for internal backend modules:
```python
from ..database.database import DB_PATH
from .database_manager import DatabaseManager
```

### Source Imports
Use backend imports for database and core functionality:
```python
from backend.database.database import DB_PATH
from backend.core.database_manager import DatabaseManager
```

Use relative imports for same-package modules:
```python
from ..progress.progress_tracker import ProgressTracker
```

## Development Guidelines

1. Keep modules focused and single-responsibility
2. Use relative imports within packages
3. Place new features in appropriate directories
4. Add tests for new functionality
5. Update documentation for significant changes
6. Follow existing code style and patterns
