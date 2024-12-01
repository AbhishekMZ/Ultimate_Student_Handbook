import sqlite3
import json
from datetime import datetime
import csv
from src import DB_PATH, DATA_DIR
from src.core.database_manager import DatabaseManager
import os

class SurveyManager:
    def __init__(self):
        self.db_path = DB_PATH
        self.db_manager = DatabaseManager()
        self.feedback_file = os.path.join(DATA_DIR, 'processed', 'csv', 'feedback.csv')
        self.questions = {
            'Technical': [
                ('Programming', 'Rate your programming skills (1-5)', 0.8),
                ('Database', 'Rate your database management skills (1-5)', 0.7),
                ('Problem_Solving', 'Rate your problem-solving abilities (1-5)', 0.9),
                ('System_Design', 'Rate your system design understanding (1-5)', 0.7),
                ('AI_ML', 'Rate your AI/ML understanding (1-5)', 0.8)
            ],
            'Soft Skills': [
                ('Communication', 'Rate your communication skills (1-5)', 0.8),
                ('Teamwork', 'Rate your ability to work in teams (1-5)', 0.9),
                ('Time_Management', 'Rate your time management skills (1-5)', 0.7),
                ('Leadership', 'Rate your leadership abilities (1-5)', 0.6),
                ('Presentation', 'Rate your presentation skills (1-5)', 0.7)
            ],
            'Learning': [
                ('Self_Study', 'Rate your self-study effectiveness (1-5)', 0.8),
                ('Practical', 'Rate your hands-on learning ability (1-5)', 0.9),
                ('Theory', 'Rate your theoretical understanding (1-5)', 0.7),
                ('Research', 'Rate your research abilities (1-5)', 0.7),
                ('Project_Work', 'Rate your project execution skills (1-5)', 0.8)
            ]
        }
        
    def validate_rating(self, rating):
        try:
            rating = int(rating)
            if 1 <= rating <= 5:
                return True
            print("Please enter a rating between 1 and 5")
            return False
        except ValueError:
            print("Please enter a valid number")
            return False

    def conduct_survey(self, student_id):
        print("\n=== Student Skill Assessment Survey ===")
        print("Rate each aspect from 1 (Needs Improvement) to 5 (Excellent)")
        
        responses = {}
        for category, questions in self.questions.items():
            print(f"\n{category} Assessment:")
            category_scores = {}
            for skill, question, weight in questions:
                while True:
                    try:
                        rating = input(f"{question}: ")
                        if self.validate_rating(rating):
                            score = int(rating) * weight
                            category_scores[skill] = {
                                'raw_score': int(rating),
                                'weighted_score': score,
                                'weight': weight
                            }
                            break
                    except KeyboardInterrupt:
                        print("\nSurvey cancelled by user")
                        return None
            responses[category] = category_scores
        
        return self.analyze_responses(responses)

    def analyze_responses(self, responses):
        if not responses:
            return None
            
        analysis = {
            'category_scores': {},
            'strengths': [],
            'weaknesses': [],
            'overall_score': 0,
            'detailed_analysis': {}
        }
        
        all_scores = []
        
        # Calculate scores for each category
        for category, skills in responses.items():
            category_raw_scores = [data['raw_score'] for data in skills.values()]
            category_weighted_scores = [data['weighted_score'] for data in skills.values()]
            
            avg_raw = mean(category_raw_scores)
            avg_weighted = mean(category_weighted_scores)
            
            analysis['category_scores'][category] = {
                'average_raw': round(avg_raw, 2),
                'average_weighted': round(avg_weighted, 2)
            }
            
            all_scores.extend(category_weighted_scores)
            
            # Analyze individual skills
            for skill, data in skills.items():
                analysis['detailed_analysis'][skill] = {
                    'raw_score': data['raw_score'],
                    'weighted_score': round(data['weighted_score'], 2),
                    'weight': data['weight']
                }
        
        # Calculate overall statistics
        overall_mean = mean(all_scores)
        try:
            overall_stdev = stdev(all_scores)
        except:
            overall_stdev = 0
            
        analysis['overall_score'] = round(overall_mean, 2)
        
        # Identify strengths and weaknesses
        threshold = overall_stdev * 0.5
        for skill, data in analysis['detailed_analysis'].items():
            score_diff = data['weighted_score'] - overall_mean
            if score_diff > threshold:
                analysis['strengths'].append({
                    'skill': skill,
                    'score': data['weighted_score'],
                    'difference': round(score_diff, 2)
                })
            elif score_diff < -threshold:
                analysis['weaknesses'].append({
                    'skill': skill,
                    'score': data['weighted_score'],
                    'difference': round(score_diff, 2)
                })
        
        # Sort strengths and weaknesses by difference
        analysis['strengths'].sort(key=lambda x: x['difference'], reverse=True)
        analysis['weaknesses'].sort(key=lambda x: x['difference'])
        
        return analysis

    def format_results(self, analysis):
        if not analysis:
            return None
            
        # Format strengths and weaknesses for CSV storage
        strengths = '; '.join([
            f"{s['skill']}({s['score']:+.2f})" for s in analysis['strengths']
        ])
        weaknesses = '; '.join([
            f"{w['skill']}({w['score']:+.2f})" for w in analysis['weaknesses']
        ])
        
        return {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'analysis': analysis
        }

    def ensure_csv_exists(self):
        if not os.path.exists('students.csv'):
            with open('students.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['StudentID', 'Name', 'Email', 'TenthMarks', 'TwelfthMarks', 
                               'Strengths', 'Weaknesses', 'Semester', 'Courses'])
                # Add sample data
                writer.writerow(['ST001', 'John Doe', 'john@example.com', '85', '88', '', '', '3', 'DBMS,AISE'])
                writer.writerow(['ST002', 'Jane Smith', 'jane@example.com', '92', '90', '', '', '3', 'MLOPS,ANN'])

    def update_student_csv(self, student_id, results):
        if not results:
            return False
            
        self.ensure_csv_exists()
        temp_file = 'students_temp.csv'
        found = False
        
        try:
            with open('students.csv', 'r', newline='') as file_in, \
                 open(temp_file, 'w', newline='') as file_out:
                
                reader = csv.DictReader(file_in)
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(file_out, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in reader:
                    if row['StudentID'] == student_id:
                        row['Strengths'] = results['strengths']
                        row['Weaknesses'] = results['weaknesses']
                        found = True
                    writer.writerow(row)
            
            if found:
                os.replace(temp_file, 'students.csv')
                print("\nStudent record updated successfully!")
            else:
                os.remove(temp_file)
                print("\nError: Student ID not found!")
                
            return found
            
        except Exception as e:
            print(f"\nError updating student record: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False

    def display_results(self, results):
        if not results or not results['analysis']:
            return
            
        analysis = results['analysis']
        
        print("\n=== Survey Results ===")
        
        print("\nCategory Scores:")
        for category, scores in analysis['category_scores'].items():
            print(f"{category}:")
            print(f"  Raw Average: {scores['average_raw']}")
            print(f"  Weighted Average: {scores['average_weighted']}")
        
        print(f"\nOverall Score: {analysis['overall_score']}")
        
        print("\nStrengths:")
        for strength in analysis['strengths']:
            print(f"  {strength['skill']}: {strength['score']} ({strength['difference']:+.2f})")
        
        print("\nAreas for Improvement:")
        for weakness in analysis['weaknesses']:
            print(f"  {weakness['skill']}: {weakness['score']} ({weakness['difference']:+.2f})")

def main():
    try:
        survey = SurveyManager()
        
        print("Welcome to Student Skill Assessment")
        print("Available Student IDs: ST001, ST002")
        student_id = input("Please enter your Student ID: ")
        
        # Conduct survey and get results
        raw_results = survey.conduct_survey(student_id)
        if raw_results:
            # Format and display results
            results = survey.format_results(raw_results)
            survey.display_results(results)
            
            # Update CSV file
            survey.update_student_csv(student_id, results)
        
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        print("\nThank you for completing the assessment!")

if __name__ == "__main__":
    main()
