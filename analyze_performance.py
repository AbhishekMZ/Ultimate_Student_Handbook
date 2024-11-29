import sqlite3
import json
from datetime import datetime, timedelta

def analyze_student_performance():
    conn = sqlite3.connect('student_tracking.db')
    cursor = conn.cursor()

    # Get performance metrics for each student
    cursor.execute('''
    SELECT 
        s.student_id,
        s.name,
        s.weaknesses,
        AVG(er.marks_obtained * 100.0 / er.max_marks) as avg_performance,
        MIN(er.marks_obtained * 100.0 / er.max_marks) as min_performance,
        MAX(er.marks_obtained * 100.0 / er.max_marks) as max_performance
    FROM students s
    JOIN exam_results er ON s.student_id = er.student_id
    GROUP BY s.student_id
    ''')
    
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
            elif score < 3.0:  # Moderate weakness
                monthly_goals.extend([
                    f"Practice {weakness} related tasks twice a week",
                    f"Complete bi-weekly assessments in {weakness}"
                ])
        
        # Generate quarterly goals
        quarterly_goals = []
        avg_weakness_score = sum(score for _, score in weakness_list) / len(weakness_list)
        
        if avg_perf < 60:
            quarterly_goals.append("Achieve at least 70% in all upcoming tests")
        elif avg_perf < 75:
            quarterly_goals.append("Achieve at least 80% in all upcoming tests")
        
        for weakness, score in weakness_list[:3]:
            quarterly_goals.append(f"Improve {weakness} score from {score:.1f} to at least {min(score + 1.5, 5.0):.1f}")
        
        improvement_plan = {
            "student_id": student_id,
            "name": name,
            "current_metrics": {
                "average_performance": round(avg_perf, 2),
                "minimum_performance": round(min_perf, 2),
                "maximum_performance": round(max_perf, 2),
                "weaknesses": weakness_list
            },
            "monthly_goals": monthly_goals,
            "quarterly_goals": quarterly_goals
        }
        
        improvement_plans.append(improvement_plan)
    
    # Save improvement plans to JSON file
    with open('improvement_plans.json', 'w') as f:
        json.dump(improvement_plans, f, indent=2)
    
    # Create a summary table in the database
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS improvement_plans (
        student_id TEXT PRIMARY KEY,
        name TEXT,
        avg_performance REAL,
        critical_weaknesses TEXT,
        monthly_goals TEXT,
        quarterly_goals TEXT,
        last_updated DATE,
        FOREIGN KEY (student_id) REFERENCES students (student_id)
    )
    ''')
    
    # Insert improvement plans into database
    for plan in improvement_plans:
        critical_weaknesses = '; '.join([f"{w[0]}({w[1]:.1f})" for w in plan['current_metrics']['weaknesses'][:3]])
        cursor.execute('''
        INSERT OR REPLACE INTO improvement_plans VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            plan['student_id'],
            plan['name'],
            plan['current_metrics']['average_performance'],
            critical_weaknesses,
            '\n'.join(plan['monthly_goals']),
            '\n'.join(plan['quarterly_goals']),
            datetime.now().date()
        ))
    
    conn.commit()
    conn.close()
    
    print(f"Generated improvement plans for {len(improvement_plans)} students")
    print("Plans have been saved to 'improvement_plans.json' and the database")

if __name__ == "__main__":
    analyze_student_performance()
