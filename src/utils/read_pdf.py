import PyPDF2
import sys
import io
import re

# Set console output encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def get_pdf_info(file_path, start_page=None, end_page=None):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            if start_page is None:
                start_page = 0
            if end_page is None:
                end_page = total_pages
            
            start_page = max(0, start_page - 1)
            end_page = min(total_pages, end_page)
            
            info = {
                "Number of Pages": total_pages,
                "Analyzed Pages": f"{start_page + 1} to {end_page}",
                "Text Content": []
            }
            
            for page_num in range(start_page, end_page):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                text = text.encode('utf-8', errors='replace').decode('utf-8')
                text = ' '.join(text.split())
                info["Text Content"].append({
                    "Page": page_num + 1,
                    "Content": text
                })
            
            return info
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def analyze_curriculum(text_content, subjects):
    analysis = {}
    current_subject = None
    current_unit = None
    unit_pattern = re.compile(r'UNIT[- ]*[IVX]+[: ]*(.+)', re.IGNORECASE)
    
    for page in text_content:
        content = page["Content"]
        lines = content.split('.')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for subject headers
            for subject in subjects:
                if subject.lower() in line.lower():
                    current_subject = subject
                    if current_subject not in analysis:
                        analysis[current_subject] = {"units": {}}
            
            # Check for unit headers
            unit_match = unit_pattern.search(line)
            if unit_match and current_subject:
                current_unit = line
                if current_unit not in analysis[current_subject]["units"]:
                    analysis[current_subject]["units"][current_unit] = []
            
            # Add content to current unit if it's not a unit header
            if current_subject and current_unit and not unit_pattern.search(line):
                if line not in analysis[current_subject]["units"][current_unit]:
                    analysis[current_subject]["units"][current_unit].append(line)
    
    return analysis

def print_curriculum_analysis(analysis):
    for subject, data in analysis.items():
        print(f"\n{'=' * 80}")
        print(f"=== {subject} ===")
        print(f"{'=' * 80}")
        
        if not data["units"]:
            print("No units found for this subject")
            continue
            
        for unit, topics in data["units"].items():
            print(f"\n{unit}")
            print("-" * 40)
            for topic in topics:
                if topic.strip() and topic != unit:
                    print(f"- {topic.strip()}")

def main():
    pdf_path = "1. AI 2022 Scheme III Year B.E. Programs.pdf"
    subjects_to_analyze = [
        "Database Management System",
        "Artificial Intelligence integrated Software Engineering",
        "Machine Learning Operations",
        "Artificial Neural Networks & Deep Learning",
        "Principles of Management & Economics"
    ]
    
    # Analyze only pages 11-22
    info = get_pdf_info(pdf_path, 11, 22)
    if isinstance(info, str):
        print(info)
        sys.exit(1)
    
    analysis = analyze_curriculum(info["Text Content"], subjects_to_analyze)
    print_curriculum_analysis(analysis)
    
    # Compare with our current mappings
    print("\n\nMissing Topics Analysis:")
    print("=" * 80)
    
    # Read our current topic mappings
    import csv
    current_topics = {}
    try:
        with open('chapter_topics.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                subject_code = row['TopicID'].split('_')[0]
                if subject_code not in current_topics:
                    current_topics[subject_code] = []
                current_topics[subject_code].append({
                    'name': row['TopicName'],
                    'summary': row['TopicSummary']
                })
    except Exception as e:
        print(f"Error reading chapter_topics.csv: {e}")
        return
    
    # Compare and find missing topics
    subject_codes = {
        "Database Management System": "DBMS",
        "Artificial Intelligence integrated Software Engineering": "AISE",
        "Machine Learning Operations": "MLOPS",
        "Artificial Neural Networks & Deep Learning": "ANN",
        "Principles of Management & Economics": "PME"
    }
    
    for subject, data in analysis.items():
        code = subject_codes.get(subject)
        if not code:
            continue
            
        print(f"\n{subject}:")
        print("-" * 40)
        
        curriculum_topics = []
        for unit, topics in data["units"].items():
            curriculum_topics.extend([t.strip() for t in topics if t.strip()])
        
        mapped_topics = current_topics.get(code, [])
        missing_topics = []
        
        for curr_topic in curriculum_topics:
            found = False
            for mapped_topic in mapped_topics:
                topic_name = mapped_topic['name'].lower()
                topic_summary = mapped_topic['summary'].lower()
                curr_topic_lower = curr_topic.lower()
                
                if (topic_name in curr_topic_lower or 
                    curr_topic_lower in topic_name or 
                    any(term in topic_summary for term in curr_topic_lower.split())):
                    found = True
                    break
            
            if not found:
                missing_topics.append(curr_topic)
        
        if missing_topics:
            print("Topics in curriculum but not mapped to textbook sections:")
            for topic in missing_topics:
                print(f"- {topic}")
        else:
            print("All topics are mapped to textbook sections")

if __name__ == "__main__":
    main()
