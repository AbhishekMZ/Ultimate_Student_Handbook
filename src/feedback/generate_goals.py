import sqlite3
import json
from datetime import datetime
import os
from backend.database.database import DB_PATH
from backend.core.database_manager import DatabaseManager

# Skill improvement strategies
IMPROVEMENT_STRATEGIES = {
    "Problem_Solving": {
        "monthly": [
            "Complete 2 coding challenges per week",
            "Participate in weekly problem-solving workshops",
            "Practice algorithm implementation exercises"
        ],
        "quarterly": [
            "Complete a complex project involving multiple algorithms",
            "Achieve 80% success rate in problem-solving assignments",
            "Mentor junior students in problem-solving techniques"
        ]
    },
    "Programming": {
        "monthly": [
            "Complete one mini-project in Python",
            "Practice daily coding exercises",
            "Implement 2 design patterns"
        ],
        "quarterly": [
            "Develop a full-stack application",
            "Contribute to an open-source project",
            "Create a portfolio of 3 significant programs"
        ]
    },
    "Database": {
        "monthly": [
            "Practice SQL queries daily",
            "Design and implement a small database",
            "Complete database normalization exercises"
        ],
        "quarterly": [
            "Develop a complex database project",
            "Master advanced SQL concepts",
            "Implement database optimization techniques"
        ]
    },
    "AI_ML": {
        "monthly": [
            "Implement basic ML algorithms",
            "Complete online ML course modules",
            "Practice with ML datasets"
        ],
        "quarterly": [
            "Develop an end-to-end ML project",
            "Master 3 advanced ML algorithms",
            "Participate in a Kaggle competition"
        ]
    },
    "System_Design": {
        "monthly": [
            "Create system architecture diagrams",
            "Study one design pattern per week",
            "Practice component design"
        ],
        "quarterly": [
            "Design a scalable system architecture",
            "Complete system design case studies",
            "Implement microservices architecture"
        ]
    },
    "Theory": {
        "monthly": [
            "Create concept summaries",
            "Participate in theory discussion groups",
            "Complete theoretical assignments"
        ],
        "quarterly": [
            "Write technical research papers",
            "Present theoretical concepts to class",
            "Create comprehensive study guides"
        ]
    },
    "Research": {
        "monthly": [
            "Read 2 research papers per week",
            "Write research summaries",
            "Practice literature review"
        ],
        "quarterly": [
            "Complete a research project",
            "Present research findings",
            "Publish a technical blog"
        ]
    },
    "Communication": {
        "monthly": [
            "Give 2 technical presentations",
            "Participate in group discussions",
            "Practice technical writing"
        ],
        "quarterly": [
            "Lead team presentations",
            "Write technical documentation",
            "Conduct workshop sessions"
        ]
    },
    "Teamwork": {
        "monthly": [
            "Participate in group projects",
            "Contribute to team discussions",
            "Practice pair programming"
        ],
        "quarterly": [
            "Lead a team project",
            "Organize team building activities",
            "Mentor new team members"
        ]
    },
    "Leadership": {
        "monthly": [
            "Lead weekly team meetings",
            "Organize study groups",
            "Take initiative in projects"
        ],
        "quarterly": [
            "Lead a major project",
            "Mentor junior students",
            "Organize technical events"
        ]
    },
    "Time_Management": {
        "monthly": [
            "Create weekly study schedules",
            "Use time tracking tools",
            "Set daily goals and priorities"
        ],
        "quarterly": [
            "Complete projects ahead of schedule",
            "Implement effective study techniques",
            "Balance multiple course projects"
        ]
    },
    "Self_Study": {
        "monthly": [
            "Complete online courses",
            "Create study materials",
            "Practice self-assessment"
        ],
        "quarterly": [
            "Master advanced topics independently",
            "Create learning resources",
            "Achieve certification goals"
        ]
    },
    "Project_Work": {
        "monthly": [
            "Complete project milestones",
            "Document project progress",
            "Learn new project tools"
        ],
        "quarterly": [
            "Deliver end-to-end projects",
            "Implement complex features",
            "Lead project presentations"
        ]
    },
    "Practical": {
        "monthly": [
            "Complete hands-on exercises",
            "Practice lab experiments",
            "Implement theoretical concepts"
        ],
        "quarterly": [
            "Build practical projects",
            "Master technical tools",
            "Create practical demonstrations"
        ]
    },
    "Presentation": {
        "monthly": [
            "Give weekly presentations",
            "Practice presentation skills",
            "Create effective slides"
        ],
        "quarterly": [
            "Present at technical seminars",
            "Create video tutorials",
            "Lead workshop sessions"
        ]
    }
}

class GoalGenerator:
    def __init__(self):
        self.db_path = DB_PATH
        self.db_manager = DatabaseManager()
        self.goals_file = os.path.join(DATA_DIR, 'processed', 'csv', 'goals.csv')
        self.improvement_plans_file = os.path.join(DATA_DIR, 'processed', 'json', 'improvement_plans.json')

    def parse_weaknesses(self, weaknesses_str):
        """Parse weaknesses string into a list of tuples (weakness, score)"""
        if not weaknesses_str:
            return []
        
        weaknesses = []
        parts = weaknesses_str.split(';')
        for part in parts:
            part = part.strip()
            if '(' in part and ')' in part:
                skill = part.split('(')[0].strip()
                score = float(part.split('(')[1].replace(')', '').replace('+', ''))
                weaknesses.append((skill, score))
        return weaknesses

    def generate_student_goals(self):
        """Generate monthly and quarterly goals for each student based on their weaknesses"""
        # Read student data
        students = []
        with open('students.csv', 'r') as file:
            reader = csv.DictReader(file)
            students = list(reader)
        
        # Prepare goals data
        goals_data = []
        
        for student in students:
            weaknesses = self.parse_weaknesses(student['Weaknesses'])
            
            # Sort weaknesses by score (ascending) to prioritize the most critical ones
            weaknesses.sort(key=lambda x: x[1])
            
            # Generate goals for top 3 weaknesses
            monthly_goals = []
            quarterly_goals = []
            
            for weakness, score in weaknesses[:3]:  # Focus on top 3 weaknesses
                if weakness in IMPROVEMENT_STRATEGIES:
                    # Add monthly goals
                    monthly_goals.extend([
                        f"{weakness}: {goal}"
                        for goal in IMPROVEMENT_STRATEGIES[weakness]['monthly']
                    ])
                    
                    # Add quarterly goals
                    quarterly_goals.extend([
                        f"{weakness}: {goal}"
                        for goal in IMPROVEMENT_STRATEGIES[weakness]['quarterly']
                    ])
            
            goals_data.append({
                'StudentID': student['StudentID'],
                'Name': student['Name'],
                'Weaknesses': student['Weaknesses'],
                'MonthlyGoals': monthly_goals,
                'QuarterlyGoals': quarterly_goals
            })
        
        # Write goals to CSV
        with open('student_goals.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['StudentID', 'Name', 'Weaknesses', 'MonthlyGoals', 'QuarterlyGoals'])
            writer.writeheader()
            
            for goal in goals_data:
                # Convert lists to string format
                goal['MonthlyGoals'] = '; '.join(goal['MonthlyGoals'])
                goal['QuarterlyGoals'] = '; '.join(goal['QuarterlyGoals'])
                writer.writerow(goal)
        
        # Also save as JSON for better readability
        with open('student_goals.json', 'w') as file:
            json.dump(goals_data, file, indent=2)

if __name__ == "__main__":
    goal_generator = GoalGenerator()
    goal_generator.generate_student_goals()
    print("Student goals generated successfully!")
