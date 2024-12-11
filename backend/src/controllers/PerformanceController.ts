import { Request, Response } from 'express';
import StudentPerformance from '../models/StudentPerformance';
import Assessment from '../models/Assessment';
import Course from '../models/Course';
import { calculateGPA } from '../utils/gradeCalculator';

export class PerformanceController {
  // Record or update attendance
  static async updateAttendance(req: Request, res: Response) {
    try {
      const { studentId, courseId, date, status } = req.body;

      const performance = await StudentPerformance.findOne({
        student: studentId,
        course: courseId,
      });

      if (!performance) {
        return res.status(404).json({ error: 'Student performance record not found' });
      }

      // Update attendance
      performance.attendance.totalClasses += 1;
      if (status === 'present') {
        performance.attendance.attendedClasses += 1;
      }
      performance.attendance.percentage = 
        (performance.attendance.attendedClasses / performance.attendance.totalClasses) * 100;

      await performance.save();

      res.json({
        message: 'Attendance updated successfully',
        attendance: performance.attendance,
      });
    } catch (error) {
      res.status(500).json({
        error: 'Error updating attendance',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Record assessment marks
  static async recordAssessmentMarks(req: Request, res: Response) {
    try {
      const { studentId, assessmentId, marksObtained, feedback } = req.body;

      const assessment = await Assessment.findById(assessmentId);
      if (!assessment) {
        return res.status(404).json({ error: 'Assessment not found' });
      }

      const performance = await StudentPerformance.findOne({
        student: studentId,
        course: assessment.course,
      });

      if (!performance) {
        return res.status(404).json({ error: 'Student performance record not found' });
      }

      // Find or create assessment record
      const assessmentIndex = performance.assessments.findIndex(
        (a) => a.assessment.toString() === assessmentId
      );

      if (assessmentIndex === -1) {
        performance.assessments.push({
          assessment: assessmentId,
          marksObtained,
          feedback,
          submissionDate: new Date(),
          status: 'evaluated',
        });
      } else {
        performance.assessments[assessmentIndex] = {
          ...performance.assessments[assessmentIndex],
          marksObtained,
          feedback,
          status: 'evaluated',
        };
      }

      // Recalculate SGPA and CGPA
      const allPerformances = await StudentPerformance.find({
        student: studentId,
      }).populate('course');

      const { sgpa, cgpa } = calculateGPA(allPerformances);
      performance.sgpa = sgpa;
      performance.cgpa = cgpa;

      await performance.save();

      res.json({
        message: 'Assessment marks recorded successfully',
        performance: {
          assessments: performance.assessments,
          sgpa: performance.sgpa,
          cgpa: performance.cgpa,
        },
      });
    } catch (error) {
      res.status(500).json({
        error: 'Error recording assessment marks',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Get student performance summary
  static async getPerformanceSummary(req: Request, res: Response) {
    try {
      const { studentId } = req.params;
      const { semester } = req.query;

      const query: any = { student: studentId };
      if (semester) {
        query.semester = parseInt(semester as string);
      }

      const performances = await StudentPerformance.find(query)
        .populate('course')
        .populate('assessments.assessment');

      const summary = {
        overall: {
          cgpa: performances[0]?.cgpa || 0,
          totalCourses: performances.length,
          completedCourses: performances.filter(p => p.status === 'completed').length,
        },
        courses: performances.map(p => ({
          courseName: (p.course as any).name,
          courseCode: (p.course as any).courseCode,
          attendance: p.attendance,
          assessments: p.assessments.map(a => ({
            name: (a.assessment as any).name,
            marksObtained: a.marksObtained,
            totalMarks: (a.assessment as any).totalMarks,
            percentage: (a.marksObtained / (a.assessment as any).totalMarks) * 100,
            status: a.status,
          })),
          sgpa: p.sgpa,
        })),
      };

      res.json(summary);
    } catch (error) {
      res.status(500).json({
        error: 'Error fetching performance summary',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Get class performance analytics
  static async getClassPerformanceAnalytics(req: Request, res: Response) {
    try {
      const { courseId, semester } = req.params;

      const performances = await StudentPerformance.find({
        course: courseId,
        semester: parseInt(semester),
      }).populate('student');

      const analytics = {
        totalStudents: performances.length,
        attendanceStats: {
          average: performances.reduce((acc, p) => acc + p.attendance.percentage, 0) / performances.length,
          below75: performances.filter(p => p.attendance.percentage < 75).length,
        },
        assessmentStats: {},
        gradeDistribution: {
          A: performances.filter(p => p.sgpa >= 8.5).length,
          B: performances.filter(p => p.sgpa >= 7 && p.sgpa < 8.5).length,
          C: performances.filter(p => p.sgpa >= 5.5 && p.sgpa < 7).length,
          D: performances.filter(p => p.sgpa >= 4 && p.sgpa < 5.5).length,
          F: performances.filter(p => p.sgpa < 4).length,
        },
      };

      res.json(analytics);
    } catch (error) {
      res.status(500).json({
        error: 'Error fetching class performance analytics',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Generate student progress report
  static async generateProgressReport(req: Request, res: Response) {
    try {
      const { studentId, semester } = req.params;

      const performance = await StudentPerformance.find({
        student: studentId,
        semester: parseInt(semester),
      })
        .populate('student')
        .populate('course')
        .populate('assessments.assessment');

      if (!performance.length) {
        return res.status(404).json({ error: 'No performance records found' });
      }

      const report = {
        studentInfo: {
          name: (performance[0].student as any).fullName,
          usn: (performance[0].student as any).usn,
          semester: semester,
        },
        academicPerformance: performance.map(p => ({
          course: (p.course as any).name,
          attendance: p.attendance,
          assessments: p.assessments.map(a => ({
            name: (a.assessment as any).name,
            marksObtained: a.marksObtained,
            totalMarks: (a.assessment as any).totalMarks,
            percentage: (a.marksObtained / (a.assessment as any).totalMarks) * 100,
          })),
          sgpa: p.sgpa,
        })),
        summary: {
          cgpa: performance[0].cgpa,
          attendanceAverage: performance.reduce((acc, p) => acc + p.attendance.percentage, 0) / performance.length,
          totalCourses: performance.length,
        },
        recommendations: generateRecommendations(performance),
      };

      res.json(report);
    } catch (error) {
      res.status(500).json({
        error: 'Error generating progress report',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }
}

// Helper function to generate recommendations based on performance
function generateRecommendations(performances: any[]): string[] {
  const recommendations: string[] = [];

  performances.forEach(p => {
    // Attendance recommendations
    if (p.attendance.percentage < 75) {
      recommendations.push(`Improve attendance in ${(p.course as any).name} (currently ${p.attendance.percentage.toFixed(2)}%)`);
    }

    // Academic performance recommendations
    const lowPerformanceAssessments = p.assessments.filter(
      (a: any) => (a.marksObtained / (a.assessment as any).totalMarks) * 100 < 60
    );

    if (lowPerformanceAssessments.length > 0) {
      recommendations.push(
        `Focus on improving performance in ${(p.course as any).name} assessments`
      );
    }
  });

  // Overall recommendations
  const averageSGPA = performances.reduce((acc, p) => acc + p.sgpa, 0) / performances.length;
  if (averageSGPA < 7) {
    recommendations.push('Consider seeking academic counseling for overall performance improvement');
  }

  return recommendations;
}
