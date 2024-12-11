import mongoose, { Document, Schema } from 'mongoose';

export interface IAchievement extends Document {
  student: Schema.Types.ObjectId;
  title: string;
  description: string;
  type: 'badge' | 'milestone' | 'streak' | 'level';
  category: 'academic' | 'consistency' | 'improvement' | 'special';
  points: number;
  level: number;
  progress: number;
  targetValue: number;
  currentValue: number;
  isUnlocked: boolean;
  unlockedAt?: Date;
  icon: string;
  rewards: Array<{
    type: 'points' | 'badge' | 'powerup';
    value: number | string;
  }>;
  criteria: {
    type: string;
    value: number;
    timeFrame?: string;
  };
  createdAt: Date;
  updatedAt: Date;
}

const AchievementSchema = new Schema<IAchievement>(
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
      enum: ['badge', 'milestone', 'streak', 'level'],
      required: true,
    },
    category: {
      type: String,
      enum: ['academic', 'consistency', 'improvement', 'special'],
      required: true,
    },
    points: {
      type: Number,
      required: true,
      min: 0,
    },
    level: {
      type: Number,
      default: 1,
      min: 1,
    },
    progress: {
      type: Number,
      default: 0,
      min: 0,
      max: 100,
    },
    targetValue: {
      type: Number,
      required: true,
      min: 0,
    },
    currentValue: {
      type: Number,
      default: 0,
      min: 0,
    },
    isUnlocked: {
      type: Boolean,
      default: false,
    },
    unlockedAt: {
      type: Date,
    },
    icon: {
      type: String,
      required: true,
    },
    rewards: [{
      type: {
        type: String,
        enum: ['points', 'badge', 'powerup'],
        required: true,
      },
      value: {
        type: Schema.Types.Mixed,
        required: true,
      },
    }],
    criteria: {
      type: {
        type: String,
        required: true,
      },
      value: {
        type: Number,
        required: true,
      },
      timeFrame: {
        type: String,
      },
    },
  },
  {
    timestamps: true,
    indexes: [
      { student: 1, type: 1 },
      { category: 1 },
      { isUnlocked: 1 },
    ],
  }
);

// Method to check if achievement is completed
AchievementSchema.methods.checkCompletion = function() {
  if (this.currentValue >= this.targetValue && !this.isUnlocked) {
    this.isUnlocked = true;
    this.unlockedAt = new Date();
    this.progress = 100;
    return true;
  }
  this.progress = (this.currentValue / this.targetValue) * 100;
  return false;
};

export default mongoose.model<IAchievement>('Achievement', AchievementSchema);
