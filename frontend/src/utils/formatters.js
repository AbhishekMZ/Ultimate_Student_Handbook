export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

export const formatGrade = (grade) => {
  const numericGrade = parseFloat(grade);
  if (isNaN(numericGrade)) return 'N/A';
  return `${numericGrade.toFixed(1)}%`;
};

export const formatPercentage = (value) => {
  const numericValue = parseFloat(value);
  if (isNaN(numericValue)) return '0%';
  return `${Math.round(numericValue)}%`;
};

export const getGradeColor = (grade) => {
  const numericGrade = parseFloat(grade);
  if (isNaN(numericGrade)) return 'default';
  if (numericGrade >= 75) return 'success';
  if (numericGrade >= 60) return 'warning';
  return 'error';
};

export const formatTimeAgo = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
  const diffMinutes = Math.floor(diffTime / (1000 * 60));

  if (diffDays > 7) {
    return formatDate(dateString);
  } else if (diffDays > 0) {
    return `${diffDays}d ago`;
  } else if (diffHours > 0) {
    return `${diffHours}h ago`;
  } else if (diffMinutes > 0) {
    return `${diffMinutes}m ago`;
  }
  return 'Just now';
};

export const validateStudentId = (studentId) => {
  const pattern = /^1RV[0-9]{2}[A-Z]{2}[0-9]{3}$/;
  return pattern.test(studentId);
};

export const validateEmail = (email) => {
  const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return pattern.test(email);
};

export const getProgressColor = (progress) => {
  const value = parseFloat(progress);
  if (isNaN(value)) return 'default';
  if (value >= 80) return 'success';
  if (value >= 50) return 'warning';
  return 'error';
};

export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
};

export const getSemesterText = (semester) => {
  const suffixes = ['st', 'nd', 'rd', 'th'];
  const num = parseInt(semester);
  if (isNaN(num) || num < 1 || num > 8) return 'Invalid Semester';
  const suffix = num <= 3 ? suffixes[num - 1] : suffixes[3];
  return `${num}${suffix} Semester`;
};
