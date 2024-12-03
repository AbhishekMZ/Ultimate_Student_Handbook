from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sqlite3
from dataclasses import dataclass
import json

@dataclass
class PerformanceMetrics:
    average_score: float
    completion_rate: float
    strength_areas: List[str]
    weak_areas: List[str]
    improvement_rate: float
    recommendations: List[str]

@dataclass
class CourseProgress:
    course_code: str
    syllabus_covered: float
    current_grade: float
    tests_completed: int
    next_milestone: str
    recommendations: List[str]

class PerformanceAnalytics:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_student_performance(self, student_id: str) -> Optional[PerformanceMetrics]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get exam results
            cursor.execute("""
                SELECT CourseCode, MarksObtained, MaxMarks
                FROM exam_results
                WHERE StudentID = ?
                ORDER BY TestDate DESC
            """, (student_id,))
            
            exam_results = cursor.fetchall()
            
            if not exam_results:
                return None

            # Calculate metrics
            total_score = 0
            total_possible = 0
            scores_by_course: Dict[str, List[float]] = {}

            for course, marks, max_marks in exam_results:
                score = (marks / max_marks) * 100
                total_score += score
                total_possible += 100
                
                if course not in scores_by_course:
                    scores_by_course[course] = []
                scores_by_course[course].append(score)

            # Get student strengths and weaknesses
            cursor.execute("""
                SELECT Strengths, Weaknesses
                FROM students
                WHERE StudentID = ?
            """, (student_id,))
            
            strengths_raw, weaknesses_raw = cursor.fetchone()
            
            # Parse JSON strings
            strengths = json.loads(strengths_raw) if strengths_raw else []
            weaknesses = json.loads(weaknesses_raw) if weaknesses_raw else []

            # Calculate improvement rate
            improvement_rates = []
            for course_scores in scores_by_course.values():
                if len(course_scores) > 1:
                    improvement = course_scores[-1] - course_scores[0]
                    improvement_rates.append(improvement)

            avg_improvement = sum(improvement_rates) / len(improvement_rates) if improvement_rates else 0

            # Generate recommendations
            recommendations = self._generate_recommendations(weaknesses, scores_by_course)

            return PerformanceMetrics(
                average_score=total_score / len(exam_results),
                completion_rate=total_score / total_possible * 100,
                strength_areas=strengths,
                weak_areas=weaknesses,
                improvement_rate=avg_improvement,
                recommendations=recommendations
            )

        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return None
        finally:
            conn.close()

    def get_course_progress(self, student_id: str, course_code: str) -> Optional[CourseProgress]:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get course progress
            cursor.execute("""
                SELECT TestNumber, MarksObtained, MaxMarks, SyllabusCovered
                FROM exam_results
                WHERE StudentID = ? AND CourseCode = ?
                ORDER BY TestDate DESC
            """, (student_id, course_code))
            
            results = cursor.fetchall()
            
            if not results:
                return None

            # Calculate current grade
            total_score = 0
            total_possible = 0
            for _, marks, max_marks, _ in results:
                total_score += marks
                total_possible += max_marks

            current_grade = (total_score / total_possible) * 100

            # Get latest syllabus coverage
            latest_coverage = float(results[0][3].strip('%')) / 100 if results[0][3] else 0

            # Determine next milestone
            next_milestone = self._determine_next_milestone(latest_coverage, current_grade)

            # Generate course-specific recommendations
            recommendations = self._generate_course_recommendations(
                course_code, current_grade, latest_coverage
            )

            return CourseProgress(
                course_code=course_code,
                syllabus_covered=latest_coverage,
                current_grade=current_grade,
                tests_completed=len(results),
                next_milestone=next_milestone,
                recommendations=recommendations
            )

        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")
            return None
        finally:
            conn.close()

    def _generate_recommendations(
        self, 
        weak_areas: List[str], 
        scores_by_course: Dict[str, List[float]]
    ) -> List[str]:
        recommendations = []

        # Analyze weak areas
        for area in weak_areas:
            if "Problem_Solving" in area:
                recommendations.append("Focus on solving more practice problems")
            elif "Time_Management" in area:
                recommendations.append("Create a structured study schedule")
            elif "Theory" in area:
                recommendations.append("Review fundamental concepts regularly")

        # Analyze course performance
        for course, scores in scores_by_course.items():
            avg_score = sum(scores) / len(scores)
            if avg_score < 60:
                recommendations.append(f"Seek additional help in {course}")
            elif avg_score < 75:
                recommendations.append(f"More practice needed in {course}")

        return recommendations

    def _generate_course_recommendations(
        self, 
        course_code: str, 
        current_grade: float,
        syllabus_covered: float
    ) -> List[str]:
        recommendations = []

        if current_grade < 60:
            recommendations.append("Review previous concepts thoroughly")
            recommendations.append("Consider seeking tutorial support")
        elif current_grade < 75:
            recommendations.append("Focus on weak topics through practice")
            recommendations.append("Participate in study groups")

        if syllabus_covered < 0.3:
            recommendations.append("Stay on track with course schedule")
        elif syllabus_covered < 0.7:
            recommendations.append("Prepare for advanced topics ahead")
        else:
            recommendations.append("Focus on revision and practice tests")

        return recommendations

    def _determine_next_milestone(self, coverage: float, grade: float) -> str:
        if coverage < 0.3:
            return "Complete foundation topics"
        elif coverage < 0.7:
            return "Master intermediate concepts"
        elif coverage < 1.0:
            return "Prepare for final assessment"
        else:
            if grade < 60:
                return "Improve overall grade"
            elif grade < 75:
                return "Aim for distinction"
            else:
                return "Maintain excellent performance"
