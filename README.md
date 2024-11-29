# Student Success Tracking System

A comprehensive digital platform to monitor and enhance student academic performance through personalized learning strategies.

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

## Project Structure

- `database_manager.py`: Core database operations and validation
- `progress_tracker.py`: Student progress monitoring
- `study_materials_browser.py`: Study material management
- `study_schedule_generator.py`: Intelligent schedule creation
- `analyze_performance.py`: Performance analytics
- `study_guide_generator.py`: Automated study guide creation
- `user_management.py`: User account management
- `student_survey.py`: Student feedback collection
- `generate_goals.py`: Learning goal generation

## Setup

1. Clone the repository
```bash
git clone [repository-url]
cd student_tracking_system
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Initialize the database
```bash
python reset_database.py
```

## Usage

1. Start by adding students and courses
2. Track progress through the progress tracker
3. Generate personalized study materials
4. Analyze performance metrics
5. Create and adjust study schedules

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details
