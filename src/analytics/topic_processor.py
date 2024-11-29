import csv
import sqlite3
import json
from study_guide_generator import StudyGuideGenerator
from learning_path_generator import LearningPathGenerator

class TopicProcessor:
    def __init__(self, db_path='student_tracking.db'):
        self.db_path = db_path
        self.study_guide_generator = StudyGuideGenerator(db_path)
        self.learning_path_generator = LearningPathGenerator(db_path)

    def get_topic_metadata(self, topic_id):
        # Dictionary mapping topic prefixes to their metadata
        topic_metadata = {
            'DBMS': {
                'course_name': 'Database Management Systems',
                'descriptions': {
                    'U1': {
                        'T1': 'Introduction to Database Concepts and Architecture',
                        'T2': 'Entity-Relationship Model and Database Design',
                        'T3': 'Relational Model and Algebra'
                    },
                    'U2': {
                        'T1': 'SQL Fundamentals and Query Processing',
                        'T2': 'Advanced SQL and Database Programming'
                    },
                    'U3': {
                        'T1': 'Database Design and Normalization',
                        'T2': 'Transaction Management and Concurrency Control'
                    },
                    'U4': {
                        'T1': 'Database Security and Authorization',
                        'T2': 'Database Recovery and Backup Systems'
                    },
                    'U5': {
                        'T1': 'Advanced Database Concepts and Applications'
                    }
                }
            },
            'AISE': {
                'course_name': 'AI-integrated Software Engineering',
                'descriptions': {
                    'U1': {
                        'T1': 'Introduction to AI in Software Engineering',
                        'T2': 'Machine Learning Fundamentals for SE'
                    },
                    'U2': {
                        'T1': 'AI-Powered Requirements Engineering',
                        'T2': 'Intelligent Software Design Patterns'
                    },
                    'U3': {
                        'T1': 'Automated Code Generation and Testing',
                        'T2': 'AI-Based Code Review and Quality Assurance'
                    },
                    'U4': {
                        'T1': 'Intelligent Project Management',
                        'T2': 'AI Ethics in Software Development'
                    },
                    'U5': {
                        'T1': 'Future Trends in AI-SE Integration'
                    }
                }
            },
            'MLOPS': {
                'course_name': 'Machine Learning Operations',
                'descriptions': {
                    'U1': {
                        'T1': 'Introduction to MLOps',
                        'T2': 'ML Project Lifecycle Management'
                    },
                    'U2': {
                        'T1': 'Data Pipeline Architecture',
                        'T2': 'Feature Engineering and Management'
                    },
                    'U3': {
                        'T1': 'Model Training and Versioning'
                    },
                    'U4': {
                        'T1': 'Model Deployment Strategies',
                        'T2': 'Model Monitoring and Maintenance'
                    },
                    'U5': {
                        'T1': 'MLOps Infrastructure and Scaling',
                        'T2': 'Advanced MLOps Practices'
                    }
                }
            },
            'ANN': {
                'course_name': 'Artificial Neural Networks',
                'descriptions': {
                    'U1': {
                        'T1': 'Neural Network Fundamentals',
                        'T2': 'Activation Functions and Network Architecture'
                    },
                    'U2': {
                        'T1': 'Backpropagation and Training Algorithms',
                        'T2': 'Optimization Techniques'
                    },
                    'U3': {
                        'T1': 'Convolutional Neural Networks',
                        'T2': 'Recurrent Neural Networks'
                    },
                    'U4': {
                        'T1': 'Deep Learning Frameworks',
                        'T2': 'Transfer Learning and Pre-trained Models'
                    },
                    'U5': {
                        'T1': 'Advanced Neural Architectures',
                        'T2': 'Neural Networks in Production'
                    }
                }
            },
            'PME': {
                'course_name': 'Principles of Management & Economics',
                'descriptions': {
                    'U1': {
                        'T1': 'Introduction to Management Principles',
                        'T2': 'Organizational Behavior and Leadership'
                    },
                    'U2': {
                        'T1': 'Microeconomic Principles',
                        'T2': 'Macroeconomic Concepts'
                    },
                    'U3': {
                        'T1': 'Strategic Management',
                        'T2': 'Market Analysis and Competition'
                    },
                    'U4': {
                        'T1': 'Financial Management Principles',
                        'T2': 'Economic Decision Making'
                    },
                    'U5': {
                        'T1': 'Global Business Environment',
                        'T2': 'Business Ethics and Sustainability'
                    }
                }
            }
        }

        # Parse topic_id (e.g., "DBMS_U1_T1")
        parts = topic_id.split('_')
        if len(parts) != 3:
            return None

        subject, unit, topic = parts
        if subject not in topic_metadata:
            return None

        unit_data = topic_metadata[subject]['descriptions'].get(unit, {})
        description = unit_data.get(topic, 'General topic in ' + topic_metadata[subject]['course_name'])

        return {
            'description': description,
            'course_name': topic_metadata[subject]['course_name']
        }

    def calculate_importance_level(self, unit_number, topic_number):
        # Higher importance for foundational topics (earlier units)
        # and primary topics (T1 vs T2)
        unit_num = int(unit_number[1])
        topic_num = int(topic_number[1])
        
        base_importance = 5 - (unit_num - 1) * 0.5  # Earlier units are more important
        topic_adjustment = -0.5 if topic_num > 1 else 0  # First topics slightly more important
        
        importance = round(max(1, min(5, base_importance + topic_adjustment)))
        return importance

    def estimate_study_hours(self, section_numbers, page_numbers):
        # Estimate study hours based on content volume
        if section_numbers == "All":
            num_sections = 5  # Default assumption for "All" sections
        else:
            start, end = section_numbers.split('-')
            start_section = float(start.split('.')[-1])
            end_section = float(end.split('.')[-1])
            num_sections = end_section - start_section + 1

        if isinstance(page_numbers, str):
            start_page, end_page = map(int, page_numbers.split('-'))
            num_pages = end_page - start_page + 1
        else:
            num_pages = 20  # Default assumption if page numbers not provided

        # Rough estimation: 30 minutes per section + 15 minutes per page
        estimated_hours = round((num_sections * 0.5 + num_pages * 0.25), 1)
        return max(2, min(8, estimated_hours))  # Cap between 2 and 8 hours

    def generate_learning_outcomes(self, description, topic_id):
        # Generate learning outcomes based on topic description and ID
        outcomes = []
        
        # Basic understanding outcome
        outcomes.append(f"Understand the core concepts of {description.lower()}")
        
        # Topic-specific outcomes based on course prefix
        course_prefix = topic_id.split('_')[0]
        
        if course_prefix == 'DBMS':
            if "Concepts" in description:
                outcomes.extend([
                    "Define and explain fundamental database terminology",
                    "Identify different types of database management systems",
                    "Understand the importance of data organization and management"
                ])
            elif "Design" in description:
                outcomes.extend([
                    "Apply design principles to real-world database scenarios",
                    "Create effective database schemas and models",
                    "Evaluate and optimize database designs"
                ])
            elif "SQL" in description:
                outcomes.extend([
                    "Write complex SQL queries for data manipulation",
                    "Implement database operations using SQL",
                    "Optimize SQL queries for better performance"
                ])
            elif "Security" in description:
                outcomes.extend([
                    "Implement database security measures",
                    "Manage user authentication and authorization",
                    "Protect against common database vulnerabilities"
                ])
        
        elif course_prefix == 'AISE':
            if "Introduction" in description:
                outcomes.extend([
                    "Understand the role of AI in software engineering",
                    "Identify opportunities for AI integration in SE",
                    "Evaluate AI-powered SE tools and frameworks"
                ])
            elif "Requirements" in description:
                outcomes.extend([
                    "Apply AI techniques to requirements gathering",
                    "Implement automated requirements analysis",
                    "Validate requirements using AI tools"
                ])
            elif "Testing" in description:
                outcomes.extend([
                    "Implement AI-powered testing strategies",
                    "Create automated test cases using ML",
                    "Evaluate test coverage and effectiveness"
                ])
        
        elif course_prefix == 'MLOPS':
            if "Introduction" in description:
                outcomes.extend([
                    "Understand MLOps principles and practices",
                    "Identify key components of ML systems",
                    "Design ML pipelines and workflows"
                ])
            elif "Pipeline" in description:
                outcomes.extend([
                    "Design and implement data pipelines",
                    "Manage data quality and versioning",
                    "Optimize pipeline performance"
                ])
            elif "Deployment" in description:
                outcomes.extend([
                    "Implement model deployment strategies",
                    "Monitor model performance in production",
                    "Handle model updates and versioning"
                ])
        
        elif course_prefix == 'ANN':
            if "Fundamentals" in description:
                outcomes.extend([
                    "Understand neural network architecture",
                    "Implement basic neural networks",
                    "Train and evaluate neural models"
                ])
            elif "CNN" in description or "Convolutional" in description:
                outcomes.extend([
                    "Design CNN architectures",
                    "Implement image processing networks",
                    "Optimize CNN performance"
                ])
            elif "RNN" in description or "Recurrent" in description:
                outcomes.extend([
                    "Understand RNN architecture and applications",
                    "Implement sequence processing models",
                    "Handle time-series data with RNNs"
                ])
        
        elif course_prefix == 'PME':
            if "Management" in description:
                outcomes.extend([
                    "Apply management principles to real scenarios",
                    "Develop effective leadership strategies",
                    "Implement organizational management techniques"
                ])
            elif "Economic" in description:
                outcomes.extend([
                    "Understand economic principles and theories",
                    "Analyze market trends and behaviors",
                    "Make informed economic decisions"
                ])
            elif "Strategy" in description:
                outcomes.extend([
                    "Develop business strategies",
                    "Analyze competitive environments",
                    "Implement strategic management plans"
                ])
        
        else:
            outcomes.extend([
                "Apply theoretical concepts to practical scenarios",
                "Analyze and solve domain-specific problems",
                "Evaluate and implement best practices"
            ])
        
        return outcomes

    def process_topics_csv(self, csv_file_path):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            with open(csv_file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # Get topic metadata
                    metadata = self.get_topic_metadata(row['TopicID'])
                    if not metadata:
                        print(f"Skipping invalid topic ID: {row['TopicID']}")
                        continue

                    # Parse unit and topic numbers from TopicID
                    parts = row['TopicID'].split('_')
                    unit_num = parts[1]
                    topic_num = parts[2]

                    # Calculate importance and study hours
                    importance_level = self.calculate_importance_level(unit_num, topic_num)
                    estimated_hours = self.estimate_study_hours(
                        row['SectionNumbers'],
                        row['PageNumbers']
                    )

                    # Generate learning outcomes
                    learning_outcomes = self.generate_learning_outcomes(
                        metadata['description'],
                        row['TopicID']
                    )

                    # Prepare topic data
                    topic_data = {
                        'name': metadata['description'],
                        'description': f"Part of {metadata['course_name']} curriculum. "
                                     f"Covers sections {row['SectionNumbers']} "
                                     f"(pages {row['PageNumbers']}).",
                        'importance_level': importance_level,
                        'estimated_hours': estimated_hours,
                        'prerequisites': [f"{parts[0]}_{unit_num}_T{int(topic_num[1])-1}"] if topic_num[1] != '1' else [],
                        'learning_outcomes': learning_outcomes
                    }

                    # Add topic to database
                    topic_id = self.study_guide_generator.add_topic(
                        row['TextbookID'],
                        int(row['ChapterNumber'].split('-')[0]),
                        topic_data
                    )

                    # Generate study materials
                    if topic_id:
                        print(f"Generating study materials for: {metadata['description']}")
                        self.study_guide_generator.generate_study_guide(topic_id, 'summary')
                        self.study_guide_generator.generate_study_guide(topic_id, 'notes')
                        self.study_guide_generator.generate_study_guide(topic_id, 'practice_questions')
                        self.study_guide_generator.generate_study_guide(topic_id, 'examples')

                        # Add dependencies if this isn't the first topic
                        if topic_num[1] != '1':
                            previous_topic_id = topic_id - 1
                            self.learning_path_generator.add_topic_dependency(
                                topic_id,
                                previous_topic_id,
                                'required'
                            )

            print("Topic processing completed successfully!")

        except Exception as e:
            print(f"Error processing topics: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

if __name__ == "__main__":
    processor = TopicProcessor()
    processor.process_topics_csv('topic_book_mapping.csv')
