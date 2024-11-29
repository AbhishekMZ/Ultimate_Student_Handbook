# Student Success Tracking System

A comprehensive digital platform to monitor and enhance student academic performance through personalized learning strategies.

## Project Structure

```
student_tracking_system/
├── src/                      # Source code
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

## Technical Stack

- Python 3.11+
- SQLite database
- Key libraries:
  - sqlite3
  - matplotlib
  - numpy
  - tabulate

## Setup

1. Clone the repository
```bash
git clone https://github.com/AbhishekMZ/Ultimate_Student_Handbook.git
cd student_tracking_system
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Initialize the database
```bash
python scripts/setup/reset_database.py
```

## Module Overview

### Core (`src/core/`)
- `database_manager.py`: Core database operations and validation
- `user_management.py`: User account management

### Analytics (`src/analytics/`)
- `analyze_performance.py`: Student performance analysis
- `analyze_curriculum.py`: Curriculum analysis
- `topic_processor.py`: Topic processing and analysis

### Study (`src/study/`)
- `study_guide_generator.py`: Automated study guide creation
- `study_materials_browser.py`: Study material management
- `study_schedule_generator.py`: Schedule generation

### Progress (`src/progress/`)
- `progress_tracker.py`: Student progress monitoring
- `learning_path_generator.py`: Personalized learning paths

### Feedback (`src/feedback/`)
- `student_survey.py`: Student feedback collection
- `generate_goals.py`: Learning goal generation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details
