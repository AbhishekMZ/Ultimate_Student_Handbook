import mongoose, { Document, Schema } from 'mongoose';

export interface ICourse extends Document {
  courseCode: string;
  name: string;
  department: string;
  semester: number;
  credits: number;
  description: string;
  syllabus: string[];
  prerequisites: string[];
  isElective: boolean;
  maxStudents: number;
  faculty: Schema.Types.ObjectId[];
  status: 'active' | 'inactive';
  createdAt: Date;
  updatedAt: Date;
}

const CourseSchema = new Schema<ICourse>(
  {
    courseCode: {
      type: String,
      required: true,
      unique: true,
      uppercase: true,
      trim: true,
    },
    name: {
      type: String,
      required: true,
      trim: true,
    },
    department: {
      type: String,
      required: true,
      trim: true,
    },
    semester: {
      type: Number,
      required: true,
      min: 1,
      max: 8,
    },
    credits: {
      type: Number,
      required: true,
      min: 1,
    },
    description: {
      type: String,
      required: true,
      trim: true,
    },
    syllabus: [{
      type: String,
      required: true,
      trim: true,
    }],
    prerequisites: [{
      type: String,
      trim: true,
    }],
    isElective: {
      type: Boolean,
      default: false,
    },
    maxStudents: {
      type: Number,
      required: true,
      min: 1,
    },
    faculty: [{
      type: Schema.Types.ObjectId,
      ref: 'User',
    }],
    status: {
      type: String,
      enum: ['active', 'inactive'],
      default: 'active',
    },
  },
  {
    timestamps: true,
    indexes: [
      { courseCode: 1 },
      { department: 1 },
      { semester: 1 },
      { status: 1 },
      { isElective: 1 },
    ],
  }
);

export default mongoose.model<ICourse>('Course', CourseSchema);
