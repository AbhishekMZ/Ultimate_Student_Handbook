import sqlite3
import json
from datetime import datetime, timedelta
from backend.database.database import DB_PATH
from backend.core.database_manager import DatabaseManager

class PerformanceAnalyzer:
    def __init__(self):
        self.db_path = DB_PATH

    def analyze_student_performance(self, student_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Base query
        query = '''
        SELECT 
            s.student_id,
            s.name,
            s.weaknesses,
            AVG(er.marks_obtained * 100.0 / er.max_marks) as avg_performance,
            MIN(er.marks_obtained * 100.0 / er.max_marks) as min_performance,
            MAX(er.marks_obtained * 100.0 / er.max_marks) as max_performance
        FROM students s
        JOIN exam_results er ON s.student_id = er.student_id
        '''

        # Add student filter if specified
        if student_id:
            query += ' WHERE s.student_id = ?'
            cursor.execute(query, (student_id,))
        else:
            query += ' GROUP BY s.student_id'
            cursor.execute(query)
        
        student_metrics = cursor.fetchall()
        improvement_plans = []

        for student in student_metrics:
            student_id, name, weaknesses, avg_perf, min_perf, max_perf = student
            
            # Parse weaknesses
            weakness_list = []
            if weaknesses:
                parts = weaknesses.split(';')
                for part in parts:
                    if '(' in part:
                        skill = part.split('(')[0].strip()
                        score = float(part.split('(')[1].replace(')', '').replace('+', ''))
                        weakness_list.append((skill, score))
            
            # Sort weaknesses by score (ascending)
            weakness_list.sort(key=lambda x: x[1])
            
            # Generate monthly goals
            monthly_goals = []
            for weakness, score in weakness_list[:3]:  # Focus on top 3 weaknesses
                if score < 2.0:  # Critical weakness
                    monthly_goals.extend([
                        f"Increase {weakness} proficiency through daily practice exercises",
                        f"Complete weekly assessments in {weakness}",
                        f"Attend specialized workshops for {weakness}"
                    ])
                else:  # Moderate weakness
                    monthly_goals.extend([
                        f"Practice {weakness} exercises twice a week",
                        f"Complete bi-weekly assessments in {weakness}"
                    ])

            improvement_plans.append({
                'student_id': student_id,
                'name': name,
                'metrics': {
                    'average_performance': round(avg_perf, 2),
                    'minimum_performance': round(min_perf, 2),
                    'maximum_performance': round(max_perf, 2),
                    'improvement_potential': round(100 - avg_perf, 2)
                },
                'weaknesses': [{'skill': w[0], 'score': w[1]} for w in weakness_list],
                'monthly_goals': monthly_goals
            })

        conn.close()
        return improvement_plans

def analyze_student_performance():
    analyzer = PerformanceAnalyzer()
    improvement_plans = analyzer.analyze_student_performance()

    # Save improvement plans to JSON file
    with open('improvement_plans.json', 'w') as f:
        json.dump(improvement_plans, f, indent=2)
    
    # Create a summary table in the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS improvement_plans (
        student_id TEXT PRIMARY KEY,
        name TEXT,
        avg_performance REAL,
        critical_weaknesses TEXT,
        monthly_goals TEXT,
        quarterly_goals TEXT,
        last_updated DATE,
        FOREIGN KEY (student_id) REFERENCES students (student_id)
    )''')
    
    # Insert improvement plans into database
    for plan in improvement_plans:
        critical_weaknesses = '; '.join([f"{w['skill']}({w['score']:.1f})" for w in plan['weaknesses'][:3]])
        cursor.execute('''INSERT OR REPLACE INTO improvement_plans VALUES (?, ?, ?, ?, ?, ?, ?)''', (
            plan['student_id'],
            plan['name'],
            plan['metrics']['average_performance'],
            critical_weaknesses,
            '\n'.join(plan['monthly_goals']),
            '',  # Quarterly goals not generated in this version
            datetime.now().date()
        ))
    
    conn.commit()
    conn.close()
    
    print(f"Generated improvement plans for {len(improvement_plans)} students")
    print("Plans have been saved to 'improvement_plans.json' and the database")

if __name__ == "__main__":
    analyze_student_performance()
