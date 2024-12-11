import mongoose, { Document, Schema } from 'mongoose';

export interface IStudentPerformance extends Document {
  student: Schema.Types.ObjectId;
  course: Schema.Types.ObjectId;
  semester: number;
  academicYear: string;
  attendance: {
    totalClasses: number;
    attendedClasses: number;
    percentage: number;
  };
  assessments: Array<{
    assessment: Schema.Types.ObjectId;
    marksObtained: number;
    feedback: string;
    submissionDate: Date;
    status: 'pending' | 'submitted' | 'evaluated';
  }>;
  cgpa: number;
  sgpa: number;
  status: 'active' | 'completed' | 'failed';
  remarks: string;
  createdAt: Date;
  updatedAt: Date;
}

const StudentPerformanceSchema = new Schema<IStudentPerformance>(
  {
    student: {
      type: Schema.Types.ObjectId,
      ref: 'Student',
      required: true,
    },
    course: {
      type: Schema.Types.ObjectId,
      ref: 'Course',
      required: true,
    },
    semester: {
      type: Number,
      required: true,
      min: 1,
      max: 8,
    },
    academicYear: {
      type: String,
      required: true,
      trim: true,
    },
    attendance: {
      totalClasses: {
        type: Number,
        default: 0,
        min: 0,
      },
      attendedClasses: {
        type: Number,
        default: 0,
        min: 0,
      },
      percentage: {
        type: Number,
        default: 0,
        min: 0,
        max: 100,
      },
    },
    assessments: [{
      assessment: {
        type: Schema.Types.ObjectId,
        ref: 'Assessment',
        required: true,
      },
      marksObtained: {
        type: Number,
        required: true,
        min: 0,
      },
      feedback: {
        type: String,
        trim: true,
      },
      submissionDate: {
        type: Date,
      },
      status: {
        type: String,
        enum: ['pending', 'submitted', 'evaluated'],
        default: 'pending',
      },
    }],
    cgpa: {
      type: Number,
      min: 0,
      max: 10,
      default: 0,
    },
    sgpa: {
      type: Number,
      min: 0,
      max: 10,
      default: 0,
    },
    status: {
      type: String,
      enum: ['active', 'completed', 'failed'],
      default: 'active',
    },
    remarks: {
      type: String,
      trim: true,
    },
  },
  {
    timestamps: true,
    indexes: [
      { student: 1 },
      { course: 1 },
      { semester: 1 },
      { academicYear: 1 },
      { status: 1 },
      { 'attendance.percentage': 1 },
      { cgpa: 1 },
      { sgpa: 1 },
    ],
  }
);

// Add a compound index for student and course
StudentPerformanceSchema.index({ student: 1, course: 1 }, { unique: true });

// Add a method to calculate attendance percentage
StudentPerformanceSchema.methods.calculateAttendancePercentage = function() {
  const { totalClasses, attendedClasses } = this.attendance;
  if (totalClasses === 0) return 0;
  return (attendedClasses / totalClasses) * 100;
};

// Add a method to calculate SGPA
StudentPerformanceSchema.methods.calculateSGPA = function() {
  // Implementation will depend on your institution's grading system
  // This is a placeholder for the actual calculation
  return this.sgpa;
};

export default mongoose.model<IStudentPerformance>('StudentPerformance', StudentPerformanceSchema);
