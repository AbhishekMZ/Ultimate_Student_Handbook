# Ultimate Student Handbook

A comprehensive web application designed to help students manage their academic life efficiently while staying motivated through gamification.

## Features

### Core Features
- Note Management
- Task Tracking
- Schedule Organization
- Progress Monitoring

### Gamification System

#### Phase 1: Core Gamification
1. **Achievement System**
   - Academic achievements (Course Master, Perfect Attendance, etc.)
   - Progress tracking for each achievement
   - Real-time achievement updates
   - Achievement showcase

2. **Experience Points (XP)**
   - Activity-based XP rewards
   - Level progression system
   - Milestone tracking
   - Performance statistics

3. **Progress Tracking**
   - Daily login streaks
   - Study session monitoring
   - Task completion rates
   - Performance analytics

#### Phase 2: Advanced Features
1. **Challenge System**
   - Daily Challenges
   - Weekly Missions
   - Monthly Quests
   - Custom Challenge Creation

2. **Skill Levels**
   - Study Skills progression
   - Organization mastery
   - Time Management expertise
   - Focus tracking

3. **Progress Visualization**
   - Achievement galleries
   - Performance graphs
   - Activity heatmaps
   - Skill progression charts

4. **Advanced Rewards**
   - Custom themes
   - Profile badges
   - Feature unlocks
   - Special status indicators

## Technical Details

### Backend
- Flask web framework
- MongoDB database
- Async support for better performance
- RESTful API architecture

### Frontend
- Modern JavaScript
- Dynamic UI updates
- Real-time progress tracking
- Interactive achievements

### Gamification API Endpoints

#### Progress Endpoints
- GET `/api/progress` - Get user's current progress
- GET `/api/achievements` - Get user's achievements
- POST `/api/daily-login` - Record daily login
- POST `/api/record-activity` - Record user activity
- POST `/api/study-session` - Record study session

#### Challenge System Endpoints (Coming Soon)
- GET `/api/challenges` - Get available challenges
- GET `/api/challenges/active` - Get user's active challenges
- POST `/api/challenges/accept` - Accept a challenge
- POST `/api/challenges/complete` - Complete a challenge

#### Skill System Endpoints (Coming Soon)
- GET `/api/skills` - Get user's skill levels
- GET `/api/skills/progress` - Get skill progression
- POST `/api/skills/update` - Update skill progress

## XP Rewards System

### Activity Rewards
- Creating notes: 10 XP
- Completing tasks: 20 XP
- Meeting deadlines: 30 XP
- Daily login: 5 XP
- Study streak: 15 XP per day

### Achievement Rewards
- Course Master: 100 XP
- Perfect Attendance: 50 XP
- Novice Note Taker: 30 XP
- Expert Note Taker: 100 XP
- Time Manager: 75 XP

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up MongoDB
4. Configure environment variables
5. Run the application:
   ```bash
   python app.py
   ```

## Development Guidelines

### Adding New Achievements
1. Define achievement in `ACHIEVEMENTS` dictionary in `models/gamification.py`
2. Add achievement logic in `GamificationSystem.check_achievements()`
3. Update frontend to display new achievement

### Adding New Activities
1. Add XP reward in `XP_REWARDS` dictionary
2. Implement activity tracking in `UserProgress.record_activity()`
3. Add API endpoint if needed
4. Update frontend to support new activity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details
