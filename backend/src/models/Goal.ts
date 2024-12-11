import mongoose, { Document, Schema } from 'mongoose';

export interface IGoal extends Document {
  student: Schema.Types.ObjectId;
  title: string;
  description: string;
  type: 'daily' | 'weekly' | 'monthly';
  category: 'academic' | 'skill' | 'project' | 'reading' | 'practice';
  status: 'pending' | 'in_progress' | 'completed' | 'carried_over';
  priority: 'low' | 'medium' | 'high';
  difficulty: 'easy' | 'medium' | 'hard';
  points: number;
  startDate: Date;
  dueDate: Date;
  completedDate?: Date;
  carryOverCount: number;
  maxCarryOvers: number;
  subTasks: Array<{
    title: string;
    completed: boolean;
    points: number;
  }>;
  progress: number;
  streakCount: number;
  tags: string[];
  reminderTime?: Date;
  timeEstimate: number; // in minutes
  actualTimeSpent?: number; // in minutes
  feedback?: string;
  relatedCourse?: Schema.Types.ObjectId;
  createdAt: Date;
  updatedAt: Date;
}

const GoalSchema = new Schema<IGoal>(
  {
    student: {
      type: Schema.Types.ObjectId,
      ref: 'Student',
      required: true,
    },
    title: {
      type: String,
      required: true,
      trim: true,
    },
    description: {
      type: String,
      required: true,
      trim: true,
    },
    type: {
      type: String,
      enum: ['daily', 'weekly', 'monthly'],
      required: true,
    },
    category: {
      type: String,
      enum: ['academic', 'skill', 'project', 'reading', 'practice'],
      required: true,
    },
    status: {
      type: String,
      enum: ['pending', 'in_progress', 'completed', 'carried_over'],
      default: 'pending',
    },
    priority: {
      type: String,
      enum: ['low', 'medium', 'high'],
      default: 'medium',
    },
    difficulty: {
      type: String,
      enum: ['easy', 'medium', 'hard'],
      default: 'medium',
    },
    points: {
      type: Number,
      required: true,
      min: 0,
    },
    startDate: {
      type: Date,
      required: true,
    },
    dueDate: {
      type: Date,
      required: true,
    },
    completedDate: {
      type: Date,
    },
    carryOverCount: {
      type: Number,
      default: 0,
    },
    maxCarryOvers: {
      type: Number,
      default: 3,
    },
    subTasks: [{
      title: {
        type: String,
        required: true,
      },
      completed: {
        type: Boolean,
        default: false,
      },
      points: {
        type: Number,
        default: 0,
      },
    }],
    progress: {
      type: Number,
      default: 0,
      min: 0,
      max: 100,
    },
    streakCount: {
      type: Number,
      default: 0,
    },
    tags: [{
      type: String,
      trim: true,
    }],
    reminderTime: {
      type: Date,
    },
    timeEstimate: {
      type: Number,
      required: true,
      min: 0,
    },
    actualTimeSpent: {
      type: Number,
      min: 0,
    },
    feedback: {
      type: String,
      trim: true,
    },
    relatedCourse: {
      type: Schema.Types.ObjectId,
      ref: 'Course',
    },
  },
  {
    timestamps: true,
    indexes: [
      { student: 1, type: 1 },
      { status: 1 },
      { dueDate: 1 },
      { category: 1 },
    ],
  }
);

// Pre-save middleware to calculate points based on difficulty and priority
GoalSchema.pre('save', function(next) {
  const basePoints = {
    easy: 10,
    medium: 20,
    hard: 30,
  };

  const priorityMultiplier = {
    low: 1,
    medium: 1.5,
    high: 2,
  };

  this.points = basePoints[this.difficulty] * priorityMultiplier[this.priority];
  next();
});

export default mongoose.model<IGoal>('Goal', GoalSchema);
