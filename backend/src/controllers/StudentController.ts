import { Request, Response } from 'express';
import Student, { IStudent } from '../models/Student';
import { validateStudent } from '../validators/studentValidator';

export class StudentController {
  // Create a new student
  static async create(req: Request, res: Response) {
    try {
      const { error } = validateStudent(req.body);
      if (error) {
        return res.status(400).json({ error: error.details[0].message });
      }

      const existingStudent = await Student.findOne({
        $or: [{ usn: req.body.usn }, { email: req.body.email }],
      });

      if (existingStudent) {
        return res.status(400).json({
          error: 'Student with this USN or email already exists',
        });
      }

      const student = new Student(req.body);
      await student.save();

      res.status(201).json(student);
    } catch (error) {
      res.status(500).json({
        error: 'Error creating student',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Get all students with pagination and filters
  static async getAll(req: Request, res: Response) {
    try {
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 10;
      const skip = (page - 1) * limit;

      const filter: any = {};
      if (req.query.department) filter.department = req.query.department;
      if (req.query.semester) filter.semester = parseInt(req.query.semester as string);
      if (req.query.section) filter.section = req.query.section;
      if (req.query.status) filter.status = req.query.status;

      const students = await Student.find(filter)
        .skip(skip)
        .limit(limit)
        .sort({ createdAt: -1 });

      const total = await Student.countDocuments(filter);

      res.json({
        students,
        pagination: {
          currentPage: page,
          totalPages: Math.ceil(total / limit),
          totalStudents: total,
          hasMore: skip + students.length < total,
        },
      });
    } catch (error) {
      res.status(500).json({
        error: 'Error fetching students',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Get a single student by ID
  static async getById(req: Request, res: Response) {
    try {
      const student = await Student.findById(req.params.id);
      if (!student) {
        return res.status(404).json({ error: 'Student not found' });
      }
      res.json(student);
    } catch (error) {
      res.status(500).json({
        error: 'Error fetching student',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Update a student
  static async update(req: Request, res: Response) {
    try {
      const { error } = validateStudent(req.body);
      if (error) {
        return res.status(400).json({ error: error.details[0].message });
      }

      const student = await Student.findById(req.params.id);
      if (!student) {
        return res.status(404).json({ error: 'Student not found' });
      }

      // Check if email/USN is being changed and if it conflicts with existing records
      if (req.body.email !== student.email || req.body.usn !== student.usn) {
        const existingStudent = await Student.findOne({
          _id: { $ne: req.params.id },
          $or: [{ usn: req.body.usn }, { email: req.body.email }],
        });

        if (existingStudent) {
          return res.status(400).json({
            error: 'Student with this USN or email already exists',
          });
        }
      }

      const updatedStudent = await Student.findByIdAndUpdate(
        req.params.id,
        req.body,
        { new: true, runValidators: true }
      );

      res.json(updatedStudent);
    } catch (error) {
      res.status(500).json({
        error: 'Error updating student',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Delete a student
  static async delete(req: Request, res: Response) {
    try {
      const student = await Student.findByIdAndDelete(req.params.id);
      if (!student) {
        return res.status(404).json({ error: 'Student not found' });
      }
      res.json({ message: 'Student deleted successfully' });
    } catch (error) {
      res.status(500).json({
        error: 'Error deleting student',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Search students
  static async search(req: Request, res: Response) {
    try {
      const searchTerm = req.query.q as string;
      if (!searchTerm) {
        return res.status(400).json({ error: 'Search term is required' });
      }

      const students = await Student.find({
        $or: [
          { fullName: { $regex: searchTerm, $options: 'i' } },
          { usn: { $regex: searchTerm, $options: 'i' } },
          { email: { $regex: searchTerm, $options: 'i' } },
        ],
      }).limit(10);

      res.json(students);
    } catch (error) {
      res.status(500).json({
        error: 'Error searching students',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Bulk import students
  static async bulkImport(req: Request, res: Response) {
    try {
      const students = req.body.students as IStudent[];
      if (!Array.isArray(students) || students.length === 0) {
        return res.status(400).json({ error: 'Invalid students data' });
      }

      const results = await Promise.all(
        students.map(async (studentData) => {
          try {
            const { error } = validateStudent(studentData);
            if (error) {
              return {
                success: false,
                usn: studentData.usn,
                error: error.details[0].message,
              };
            }

            const existingStudent = await Student.findOne({
              $or: [{ usn: studentData.usn }, { email: studentData.email }],
            });

            if (existingStudent) {
              return {
                success: false,
                usn: studentData.usn,
                error: 'Student with this USN or email already exists',
              };
            }

            const student = new Student(studentData);
            await student.save();
            return { success: true, usn: studentData.usn };
          } catch (error) {
            return {
              success: false,
              usn: studentData.usn,
              error: error instanceof Error ? error.message : 'Unknown error',
            };
          }
        })
      );

      res.json({
        message: 'Bulk import completed',
        results,
        summary: {
          total: results.length,
          successful: results.filter((r) => r.success).length,
          failed: results.filter((r) => !r.success).length,
        },
      });
    } catch (error) {
      res.status(500).json({
        error: 'Error in bulk import',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }
}
