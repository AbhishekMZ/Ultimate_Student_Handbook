import mongoose, { Document, Schema } from 'mongoose';

export interface IStudent extends Document {
  usn: string;
  fullName: string;
  email: string;
  department: string;
  semester: number;
  section: string;
  phoneNumber: string;
  dateOfBirth: Date;
  gender: 'male' | 'female' | 'other';
  address: {
    street: string;
    city: string;
    state: string;
    pincode: string;
  };
  guardianName: string;
  guardianContact: string;
  admissionYear: number;
  status: 'active' | 'inactive' | 'alumni';
  createdAt: Date;
  updatedAt: Date;
}

const StudentSchema = new Schema<IStudent>(
  {
    usn: {
      type: String,
      required: true,
      unique: true,
      uppercase: true,
      trim: true,
    },
    fullName: {
      type: String,
      required: true,
      trim: true,
    },
    email: {
      type: String,
      required: true,
      unique: true,
      trim: true,
      lowercase: true,
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
    section: {
      type: String,
      required: true,
      uppercase: true,
      trim: true,
    },
    phoneNumber: {
      type: String,
      required: true,
      trim: true,
    },
    dateOfBirth: {
      type: Date,
      required: true,
    },
    gender: {
      type: String,
      enum: ['male', 'female', 'other'],
      required: true,
    },
    address: {
      street: {
        type: String,
        required: true,
        trim: true,
      },
      city: {
        type: String,
        required: true,
        trim: true,
      },
      state: {
        type: String,
        required: true,
        trim: true,
      },
      pincode: {
        type: String,
        required: true,
        trim: true,
      },
    },
    guardianName: {
      type: String,
      required: true,
      trim: true,
    },
    guardianContact: {
      type: String,
      required: true,
      trim: true,
    },
    admissionYear: {
      type: Number,
      required: true,
    },
    status: {
      type: String,
      enum: ['active', 'inactive', 'alumni'],
      default: 'active',
    },
  },
  {
    timestamps: true,
    indexes: [
      { usn: 1 },
      { email: 1 },
      { department: 1 },
      { semester: 1 },
      { status: 1 },
    ],
  }
);

export default mongoose.model<IStudent>('Student', StudentSchema);
