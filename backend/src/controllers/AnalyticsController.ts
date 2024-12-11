import { Request, Response } from 'express';
import StudentPerformance from '../models/StudentPerformance';
import Course from '../models/Course';
import Student from '../models/Student';
import { getGradeFromGPA } from '../utils/gradeCalculator';
import ExcelJS from 'exceljs';

export class AnalyticsController {
  // Get department-wise performance analytics
  static async getDepartmentAnalytics(req: Request, res: Response) {
    try {
      const { department, academicYear } = req.query;

      const performances = await StudentPerformance.find({
        academicYear: academicYear as string,
      })
        .populate('student')
        .populate('course');

      // Filter by department if specified
      const departmentPerformances = department
        ? performances.filter((p) => (p.student as any).department === department)
        : performances;

      const analytics = {
        overview: {
          totalStudents: new Set(departmentPerformances.map(p => p.student)).size,
          totalCourses: new Set(departmentPerformances.map(p => p.course)).size,
          averageCGPA: departmentPerformances.reduce((acc, p) => acc + p.cgpa, 0) / departmentPerformances.length,
        },
        semesterWise: {},
        courseWise: {},
        trends: {
          cgpaTrend: [],
          attendanceTrend: [],
        },
      };

      // Calculate semester-wise metrics
      departmentPerformances.forEach(performance => {
        const sem = performance.semester;
        if (!analytics.semesterWise[sem]) {
          analytics.semesterWise[sem] = {
            averageSGPA: 0,
            averageAttendance: 0,
            studentCount: 0,
          };
        }
        analytics.semesterWise[sem].averageSGPA += performance.sgpa;
        analytics.semesterWise[sem].averageAttendance += performance.attendance.percentage;
        analytics.semesterWise[sem].studentCount++;
      });

      // Normalize semester-wise averages
      Object.keys(analytics.semesterWise).forEach(sem => {
        const stats = analytics.semesterWise[sem];
        stats.averageSGPA /= stats.studentCount;
        stats.averageAttendance /= stats.studentCount;
      });

      res.json(analytics);
    } catch (error) {
      res.status(500).json({
        error: 'Error generating department analytics',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Get student performance trends
  static async getStudentTrends(req: Request, res: Response) {
    try {
      const { studentId } = req.params;

      const performances = await StudentPerformance.find({
        student: studentId,
      })
        .sort({ semester: 1 })
        .populate('course');

      const trends = {
        sgpa: performances.map(p => ({
          semester: p.semester,
          value: p.sgpa,
        })),
        attendance: performances.map(p => ({
          semester: p.semester,
          value: p.attendance.percentage,
        })),
        coursePerformance: performances.map(p => ({
          semester: p.semester,
          course: (p.course as any).name,
          assessmentScores: p.assessments.map(a => ({
            name: (a.assessment as any).name,
            score: (a.marksObtained / (a.assessment as any).totalMarks) * 100,
          })),
        })),
      };

      res.json(trends);
    } catch (error) {
      res.status(500).json({
        error: 'Error fetching student trends',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Generate and export performance report
  static async exportPerformanceReport(req: Request, res: Response) {
    try {
      const { department, semester, academicYear } = req.query;

      const performances = await StudentPerformance.find({
        ...(semester && { semester: parseInt(semester as string) }),
        academicYear: academicYear as string,
      })
        .populate('student')
        .populate('course')
        .populate('assessments.assessment');

      // Filter by department if specified
      const filteredPerformances = department
        ? performances.filter((p) => (p.student as any).department === department)
        : performances;

      // Create Excel workbook
      const workbook = new ExcelJS.Workbook();
      const worksheet = workbook.addWorksheet('Performance Report');

      // Add headers
      worksheet.columns = [
        { header: 'USN', key: 'usn', width: 15 },
        { header: 'Student Name', key: 'name', width: 30 },
        { header: 'Course', key: 'course', width: 20 },
        { header: 'Attendance %', key: 'attendance', width: 15 },
        { header: 'SGPA', key: 'sgpa', width: 10 },
        { header: 'CGPA', key: 'cgpa', width: 10 },
        { header: 'Grade', key: 'grade', width: 10 },
      ];

      // Add data
      filteredPerformances.forEach(performance => {
        worksheet.addRow({
          usn: (performance.student as any).usn,
          name: (performance.student as any).fullName,
          course: (performance.course as any).name,
          attendance: performance.attendance.percentage.toFixed(2),
          sgpa: performance.sgpa.toFixed(2),
          cgpa: performance.cgpa.toFixed(2),
          grade: getGradeFromGPA(performance.sgpa),
        });
      });

      // Style the worksheet
      worksheet.getRow(1).font = { bold: true };
      worksheet.getRow(1).fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FFE0E0E0' },
      };

      // Generate Excel file
      const buffer = await workbook.xlsx.writeBuffer();

      // Set response headers
      res.setHeader(
        'Content-Type',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      );
      res.setHeader(
        'Content-Disposition',
        `attachment; filename=performance_report_${academicYear}_${semester || 'all'}.xlsx`
      );

      res.send(buffer);
    } catch (error) {
      res.status(500).json({
        error: 'Error generating performance report',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Get course completion analytics
  static async getCourseCompletionAnalytics(req: Request, res: Response) {
    try {
      const { courseId } = req.params;

      const performances = await StudentPerformance.find({
        course: courseId,
        status: 'completed',
      }).populate('student');

      const analytics = {
        totalStudents: performances.length,
        gradeDistribution: {
          'A+': 0,
          'A': 0,
          'B+': 0,
          'B': 0,
          'C+': 0,
          'C': 0,
          'F': 0,
        },
        assessmentCompletion: {},
        attendanceDistribution: {
          excellent: 0, // >= 90%
          good: 0,     // >= 75%
          average: 0,  // >= 65%
          poor: 0,     // < 65%
        },
      };

      performances.forEach(performance => {
        // Grade distribution
        const grade = getGradeFromGPA(performance.sgpa);
        analytics.gradeDistribution[grade]++;

        // Attendance distribution
        const attendance = performance.attendance.percentage;
        if (attendance >= 90) analytics.attendanceDistribution.excellent++;
        else if (attendance >= 75) analytics.attendanceDistribution.good++;
        else if (attendance >= 65) analytics.attendanceDistribution.average++;
        else analytics.attendanceDistribution.poor++;

        // Assessment completion
        performance.assessments.forEach(assessment => {
          const assessmentName = (assessment.assessment as any).name;
          if (!analytics.assessmentCompletion[assessmentName]) {
            analytics.assessmentCompletion[assessmentName] = {
              submitted: 0,
              pending: 0,
            };
          }
          if (assessment.status === 'submitted' || assessment.status === 'evaluated') {
            analytics.assessmentCompletion[assessmentName].submitted++;
          } else {
            analytics.assessmentCompletion[assessmentName].pending++;
          }
        });
      });

      res.json(analytics);
    } catch (error) {
      res.status(500).json({
        error: 'Error fetching course completion analytics',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }
}
