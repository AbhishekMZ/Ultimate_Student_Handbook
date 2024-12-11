import Joi from 'joi';

export const validateStudent = (student: any) => {
  const schema = Joi.object({
    usn: Joi.string()
      .required()
      .pattern(/^[1-4][A-Z]{2}\d{2}[A-Z]{2}\d{3}$/)
      .message('Invalid USN format'),
    
    fullName: Joi.string()
      .required()
      .min(3)
      .max(100)
      .pattern(/^[a-zA-Z\s]*$/)
      .message('Full name should only contain letters and spaces'),
    
    email: Joi.string()
      .required()
      .email()
      .message('Invalid email format'),
    
    department: Joi.string()
      .required()
      .min(2)
      .max(50),
    
    semester: Joi.number()
      .required()
      .min(1)
      .max(8),
    
    section: Joi.string()
      .required()
      .length(1)
      .uppercase(),
    
    phoneNumber: Joi.string()
      .required()
      .pattern(/^\d{10}$/)
      .message('Phone number must be 10 digits'),
    
    dateOfBirth: Joi.date()
      .required()
      .max('now')
      .message('Date of birth cannot be in the future'),
    
    gender: Joi.string()
      .required()
      .valid('male', 'female', 'other'),
    
    address: Joi.object({
      street: Joi.string().required(),
      city: Joi.string().required(),
      state: Joi.string().required(),
      pincode: Joi.string()
        .required()
        .pattern(/^\d{6}$/)
        .message('Invalid pincode'),
    }).required(),
    
    guardianName: Joi.string()
      .required()
      .min(3)
      .max(100)
      .pattern(/^[a-zA-Z\s]*$/)
      .message('Guardian name should only contain letters and spaces'),
    
    guardianContact: Joi.string()
      .required()
      .pattern(/^\d{10}$/)
      .message('Guardian contact must be 10 digits'),
    
    admissionYear: Joi.number()
      .required()
      .min(2000)
      .max(new Date().getFullYear()),
    
    status: Joi.string()
      .valid('active', 'inactive', 'alumni')
      .default('active'),
  });

  return schema.validate(student, { abortEarly: false });
};
