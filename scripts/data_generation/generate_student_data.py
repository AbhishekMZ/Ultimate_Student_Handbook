import csv
import random
from student_survey import StudentSurvey

# Extended list of common Indian names
first_names = [
    "Aarav", "Aditi", "Akash", "Ananya", "Arjun", "Diya", "Ishaan", "Kavya",
    "Krishna", "Lakshmi", "Manav", "Neha", "Pranav", "Priya", "Rahul", "Riya",
    "Rohan", "Sahil", "Sanjana", "Shreya", "Tanvi", "Varun", "Vedika", "Vihaan",
    "Zara", "Advait", "Anvi", "Dhruv", "Ishita", "Kabir", "Aditya", "Anjali",
    "Arnav", "Avani", "Chirag", "Deepa", "Esha", "Gaurav", "Harini", "Ishan",
    "Jatin", "Keerthi", "Kunal", "Madhav", "Nandini", "Nikhil", "Ojas", "Pooja",
    "Rajat", "Samarth", "Tanya", "Uday", "Varsha", "Yash", "Aanya", "Aarush",
    "Bhavya", "Darsh", "Gauri", "Harsh", "Ira", "Jay", "Karan", "Lavanya",
    "Mira", "Neel", "Palak", "Reyansh", "Saanvi", "Tara", "Uma", "Viraj"
]

last_names = [
    "Sharma", "Patel", "Kumar", "Singh", "Reddy", "Nair", "Pillai", "Iyer",
    "Joshi", "Malhotra", "Gupta", "Shah", "Mehta", "Verma", "Desai", "Rao",
    "Kapoor", "Menon", "Saxena", "Bhat", "Yadav", "Hegde", "Shetty", "Kamath",
    "Agarwal", "Bansal", "Choudhury", "Dubey", "Gandhi", "Khanna", "Mishra",
    "Naidu", "Oberoi", "Pandey", "Qureshi", "Rajan", "Sengupta", "Tiwari",
    "Unnikrishnan", "Venkatesh", "Walia", "Xavier", "Zacharia", "Ahuja",
    "Bhattacharya", "Chakraborty", "Das", "Easwaran", "Fernandes", "Goswami"
]

# Available courses with their codes
courses = {
    "DBMS": "CD252IA",    # Database Management Systems
    "AISE": "AI255TBA",   # AI-integrated Software Engineering
    "MLOps": "AI254TA",   # Machine Learning Operations
    "ANN": "AI253IA",     # Artificial Neural Networks
    "PME": "HS251TA"      # Principles of Management & Economics
}

def generate_student_id(num):
    return f"1RV22AI{num:03d}"

def generate_email(first_name, last_name):
    return f"{first_name.lower()}.{last_name.lower()}.ai22@rvce.edu.in"

def generate_marks():
    # Generate marks with a slight bias towards higher scores
    return min(99, max(75, int(random.gauss(88, 7))))

def run_sample_survey():
    survey = StudentSurvey()
    responses = {}
    
    for category, questions in survey.questions.items():
        category_scores = {}
        for skill, _, weight in questions:
            # Generate more varied scores with slight positive bias
            raw_score = min(5, max(1, int(random.gauss(3.7, 1.0))))
            score = raw_score * weight
            category_scores[skill] = {
                'raw_score': raw_score,
                'weighted_score': score,
                'weight': weight
            }
        responses[category] = category_scores
    
    analysis = survey.analyze_responses(responses)
    results = survey.format_results(analysis)
    return results['strengths'], results['weaknesses']

def select_courses():
    # Return all courses in a consistent order
    return ','.join(courses.keys())

def generate_student_data(num_students=200):
    students = []
    used_combinations = set()
    
    for i in range(1, num_students + 1):
        # Try to generate unique name combinations
        attempts = 0
        while attempts < 100:  # Prevent infinite loop
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            if (first_name, last_name) not in used_combinations:
                used_combinations.add((first_name, last_name))
                break
            attempts += 1
        
        if attempts >= 100:
            # If we can't find a unique combination, modify the first name slightly
            first_name = f"{first_name}{random.randint(1,9)}"
        
        student_id = generate_student_id(i)
        email = generate_email(first_name, last_name)
        tenth_marks = generate_marks()
        twelfth_marks = generate_marks()
        
        # Run sample survey for strengths and weaknesses
        strengths, weaknesses = run_sample_survey()
        
        # Select courses
        student_courses = select_courses()
        
        students.append([
            student_id,
            f"{first_name} {last_name}",
            email,
            str(tenth_marks),
            str(twelfth_marks),
            strengths,
            weaknesses,
            "5",
            student_courses
        ])
    
    return students

def write_to_csv(students):
    with open('students.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['StudentID', 'Name', 'Email', 'TenthMarks', 'TwelfthMarks', 
                        'Strengths', 'Weaknesses', 'Semester', 'Courses'])
        writer.writerows(students)

if __name__ == "__main__":
    print("Generating student data...")
    students = generate_student_data(200)  # Generate 200 students
    write_to_csv(students)
    print("Student data generated successfully!")
    print(f"Created {len(students)} student records in students.csv")
