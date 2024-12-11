import mongoose, { Document, Schema } from 'mongoose';

export interface IAssessment extends Document {
  course: Schema.Types.ObjectId;
  name: string;
  type: 'internal' | 'assignment' | 'project' | 'exam';
  totalMarks: number;
  weightage: number;
  dueDate: Date;
  instructions: string;
  status: 'upcoming' | 'ongoing' | 'completed';
  createdBy: Schema.Types.ObjectId;
  createdAt: Date;
  updatedAt: Date;
}

const AssessmentSchema = new Schema<IAssessment>(
  {
    course: {
      type: Schema.Types.ObjectId,
      ref: 'Course',
      required: true,
    },
    name: {
      type: String,
      required: true,
      trim: true,
    },
    type: {
      type: String,
      enum: ['internal', 'assignment', 'project', 'exam'],
      required: true,
    },
    totalMarks: {
      type: Number,
      required: true,
      min: 0,
    },
    weightage: {
      type: Number,
      required: true,
      min: 0,
      max: 100,
    },
    dueDate: {
      type: Date,
      required: true,
    },
    instructions: {
      type: String,
      required: true,
      trim: true,
    },
    status: {
      type: String,
      enum: ['upcoming', 'ongoing', 'completed'],
      default: 'upcoming',
    },
    createdBy: {
      type: Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
  },
  {
    timestamps: true,
    indexes: [
      { course: 1 },
      { type: 1 },
      { dueDate: 1 },
      { status: 1 },
      { createdBy: 1 },
    ],
  }
);

export default mongoose.model<IAssessment>('Assessment', AssessmentSchema);
