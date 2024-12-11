interface Performance {
  assessments: Array<{
    marksObtained: number;
    assessment: {
      totalMarks: number;
      weightage: number;
    };
  }>;
  course: {
    credits: number;
  };
}

export function calculateGPA(performances: Performance[]) {
  // Calculate SGPA (Semester Grade Point Average)
  const calculateSGPA = (performance: Performance) => {
    let totalWeightedMarks = 0;
    let totalWeightage = 0;

    performance.assessments.forEach(assessment => {
      const percentage = (assessment.marksObtained / assessment.assessment.totalMarks) * 100;
      const weightedMarks = percentage * (assessment.assessment.weightage / 100);
      totalWeightedMarks += weightedMarks;
      totalWeightage += assessment.assessment.weightage;
    });

    // Convert percentage to 10-point scale
    return totalWeightage > 0 ? (totalWeightedMarks / totalWeightage) * 10 / 100 : 0;
  };

  // Calculate individual SGPAs
  const sgpas = performances.map(performance => ({
    sgpa: calculateSGPA(performance),
    credits: performance.course.credits,
  }));

  // Calculate overall SGPA for the current semester
  const currentSemesterSGPA = sgpas.reduce((acc, curr) => acc + curr.sgpa, 0) / sgpas.length;

  // Calculate CGPA (Cumulative Grade Point Average)
  const totalCredits = sgpas.reduce((acc, curr) => acc + curr.credits, 0);
  const weightedSGPA = sgpas.reduce((acc, curr) => acc + (curr.sgpa * curr.credits), 0);
  const cgpa = totalCredits > 0 ? weightedSGPA / totalCredits : 0;

  return {
    sgpa: currentSemesterSGPA,
    cgpa: cgpa,
  };
}

export function getGradeFromGPA(gpa: number): string {
  if (gpa >= 9.0) return 'A+';
  if (gpa >= 8.0) return 'A';
  if (gpa >= 7.0) return 'B+';
  if (gpa >= 6.0) return 'B';
  if (gpa >= 5.0) return 'C+';
  if (gpa >= 4.0) return 'C';
  return 'F';
}

export function calculateAttendanceGrade(percentage: number): string {
  if (percentage >= 90) return 'Excellent';
  if (percentage >= 75) return 'Good';
  if (percentage >= 65) return 'Average';
  return 'Poor';
}

export function generatePerformanceMetrics(performance: Performance) {
  const assessmentScores = performance.assessments.map(assessment => ({
    score: (assessment.marksObtained / assessment.assessment.totalMarks) * 100,
    weightage: assessment.assessment.weightage,
  }));

  const metrics = {
    highest: Math.max(...assessmentScores.map(score => score.score)),
    lowest: Math.min(...assessmentScores.map(score => score.score)),
    average: assessmentScores.reduce((acc, score) => acc + score.score, 0) / assessmentScores.length,
    weightedAverage: assessmentScores.reduce((acc, score) => 
      acc + (score.score * score.weightage), 0) / 
      assessmentScores.reduce((acc, score) => acc + score.weightage, 0),
  };

  return {
    ...metrics,
    performance: metrics.weightedAverage >= 75 ? 'Good' :
                 metrics.weightedAverage >= 60 ? 'Average' : 'Needs Improvement',
  };
}
