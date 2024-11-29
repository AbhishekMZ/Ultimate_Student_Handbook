import csv
import random
from datetime import datetime, timedelta

# Course details with their codes and max marks
courses = {
    "CD252IA": {"name": "DBMS", "max_marks": 50},
    "AI255TBA": {"name": "AISE", "max_marks": 50},
    "AI254TA": {"name": "MLOps", "max_marks": 50},
    "AI253IA": {"name": "ANN", "max_marks": 50},
    "HS251TA": {"name": "PME", "max_marks": 50}
}

def get_test_dates():
    # Start date for the semester (assuming it started in August)
    start_date = datetime(2023, 8, 1)
    
    # Generate four dates with roughly one month gap
    dates = []
    for i in range(4):
        test_date = start_date + timedelta(days=30*i)
        dates.append(test_date.strftime("%Y-%m-%d"))
    return dates

def generate_marks(base_performance, is_final=False):
    """Generate marks based on student's base performance and test type"""
    if is_final:
        # Final test has slightly higher average due to better preparation
        min_percent = max(60, base_performance - 15)
        max_percent = min(100, base_performance + 15)
    else:
        # Regular tests have more variation
        min_percent = max(50, base_performance - 20)
        max_percent = min(100, base_performance + 10)
    
    percentage = random.uniform(min_percent, max_percent)
    max_marks = 100 if is_final else 50
    return round((percentage / 100) * max_marks)  # Converting to marks out of max_marks

def calculate_base_performance(tenth_marks, twelfth_marks):
    """Calculate base performance from previous academic records"""
    return (float(tenth_marks) + float(twelfth_marks)) / 2

def generate_exam_results():
    # Read student data
    students = []
    with open('students.csv', 'r') as file:
        reader = csv.DictReader(file)
        students = list(reader)
    
    # Get test dates
    test_dates = get_test_dates()
    
    # Prepare exam results
    exam_results = []
    header = ['StudentID', 'CourseCode', 'TestNumber', 'TestDate', 'SyllabusCovered', 'MaxMarks', 'MarksObtained']
    
    for student in students:
        base_performance = calculate_base_performance(student['TenthMarks'], student['TwelfthMarks'])
        
        # Generate results for each course
        for course_code, course_info in courses.items():
            # Adjust base performance based on student's strengths/weaknesses
            adjusted_performance = base_performance
            if course_info['name'] in student['Strengths']:
                adjusted_performance += 5
            if course_info['name'] in student['Weaknesses']:
                adjusted_performance -= 5
            
            # Generate four test results for each course
            for test_num in range(1, 5):
                is_final = (test_num == 4)
                syllabus_covered = "100%" if is_final else "33%"
                max_marks = 100 if is_final else 50
                marks = generate_marks(adjusted_performance, is_final)
                
                exam_results.append({
                    'StudentID': student['StudentID'],
                    'CourseCode': course_code,
                    'TestNumber': test_num,
                    'TestDate': test_dates[test_num - 1],
                    'SyllabusCovered': syllabus_covered,
                    'MaxMarks': max_marks,
                    'MarksObtained': marks
                })
    
    # Write to CSV file
    with open('exam_results.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(exam_results)

if __name__ == "__main__":
    generate_exam_results()
    print("Exam results generated successfully!")
