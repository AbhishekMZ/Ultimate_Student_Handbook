# Ultimate Student Handbook

A comprehensive digital platform to monitor and enhance student academic performance through personalized learning strategies.

## Project Structure

```
student_tracking_system/
├── src/                      # Backend source code
│   ├── core/                 # Core functionality
│   │   ├── database_manager.py
│   │   └── user_management.py
│   ├── analytics/           # Analytics and performance tracking
│   │   ├── analyze_performance.py
│   │   ├── analyze_curriculum.py
│   │   └── topic_processor.py
│   ├── study/              # Study material management
│   │   ├── study_guide_generator.py
│   │   ├── study_materials_browser.py
│   │   └── study_schedule_generator.py
│   ├── progress/           # Progress tracking
│   │   ├── progress_tracker.py
│   │   └── learning_path_generator.py
│   ├── feedback/           # Student feedback and goals
│   │   ├── student_survey.py
│   │   └── generate_goals.py
│   └── utils/              # Utility functions
│       └── read_pdf.py
├── dbms frontend/          # React frontend application
│   ├── src/               # Frontend source code
│   │   ├── components/    # Reusable components
│   │   ├── pages/        # Page components
│   │   └── utils/        # Frontend utilities
│   ├── public/           # Static files
│   └── package.json      # Frontend dependencies
├── data/                   # Data files
│   ├── raw/               # Raw data files
│   │   ├── textbooks/
│   │   └── textbook_sections/
│   └── processed/         # Processed data files
│       ├── csv/
│       └── json/
├── scripts/               # Setup and maintenance scripts
│   ├── setup/
│   └── data_generation/
├── tests/                 # Test files
└── docs/                  # Documentation
```

## Features

- Student progress tracking
- Personalized study materials generation
- Course and topic management
- Performance analytics
- Study schedule generation
- Data-driven learning recommendations
- Interactive dashboard
- Real-time progress monitoring
- Visual analytics and insights

## Technical Stack

### Backend
- Python 3.11+
- Flask web framework
- SQLite database
- Key libraries:
  - flask
  - flask-cors
  - sqlite3
  - matplotlib
  - numpy
  - tabulate

### Frontend
- React 18
- Material-UI components
- Key libraries:
  - @mui/material
  - react-router-dom
  - axios
  - chart.js
  - react-chartjs-2

## Setup

1. Clone the repository
```bash
git clone https://github.com/AbhishekMZ/Ultimate_Student_Handbook.git
cd student_tracking_system
```

2. Install backend dependencies
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies
```bash
cd dbms frontend
npm install
```

4. Initialize the database
```bash
python setup_project.py
```

5. Start the backend server
```bash
python run_api.py
```

6. Start the frontend development server
```bash
cd dbms frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Module Overview

### Backend Modules

#### Core (`src/core/`)
- `database_manager.py`: Core database operations and validation
- `user_management.py`: User account management

#### Analytics (`src/analytics/`)
- `analyze_performance.py`: Student performance analysis
- `analyze_curriculum.py`: Curriculum analysis
- `topic_processor.py`: Topic processing and analysis

#### Study (`src/study/`)
- `study_guide_generator.py`: Automated study guide creation
- `study_materials_browser.py`: Study material management
- `study_schedule_generator.py`: Schedule generation

#### Progress (`src/progress/`)
- `progress_tracker.py`: Student progress monitoring
- `learning_path_generator.py`: Personalized learning paths

#### Feedback (`src/feedback/`)
- `student_survey.py`: Student feedback collection
- `generate_goals.py`: Goal generation and tracking

### Frontend Pages

#### Dashboard (`pages/Dashboard.js`)
- Overview of key metrics
- Performance summaries
- Quick access to main features

#### Students (`pages/Students.js`)
- Student management
- Student list and details
- Performance overview

#### Courses (`pages/Courses.js`)
- Course catalog
- Course details and materials
- Topic organization

#### Progress (`pages/Progress.js`)
- Student progress tracking
- Topic completion status
- Understanding level metrics

#### Analytics (`pages/Analytics.js`)
- Performance analytics
- Visual data representation
- Trend analysis

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
