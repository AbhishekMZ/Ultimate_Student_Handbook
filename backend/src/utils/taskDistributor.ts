import { IGoal } from '../models/Goal';
import { calculateWorkload } from './workloadCalculator';

interface TaskDistribution {
  goal: IGoal;
  newDueDate: Date;
}

export async function distributeCarryOverTasks(
  studentId: string,
  incompleteGoals: IGoal[]
): Promise<TaskDistribution[]> {
  const distribution: TaskDistribution[] = [];
  const MAX_DAILY_WORKLOAD = 480; // 8 hours in minutes

  // Sort goals by priority and remaining work
  const sortedGoals = incompleteGoals.sort((a, b) => {
    const priorityWeight = { high: 3, medium: 2, low: 1 };
    const aWeight = priorityWeight[a.priority] * (100 - a.progress);
    const bWeight = priorityWeight[b.priority] * (100 - b.progress);
    return bWeight - aWeight;
  });

  // Get next 7 days workload
  const nextWeek = new Date();
  nextWeek.setDate(nextWeek.getDate() + 7);
  const existingWorkload = await calculateWorkload(studentId, nextWeek);

  // Distribute tasks
  for (const goal of sortedGoals) {
    const remainingWork = goal.timeEstimate * (100 - goal.progress) / 100;
    let currentDate = new Date();
    let workAssigned = false;

    // Try to find a suitable day within the next 7 days
    for (let i = 0; i < 7 && !workAssigned; i++) {
      currentDate.setDate(currentDate.getDate() + 1);
      const dayWorkload = existingWorkload.daily[currentDate.toISOString().split('T')[0]] || 0;

      if (dayWorkload + remainingWork <= MAX_DAILY_WORKLOAD) {
        distribution.push({
          goal,
          newDueDate: new Date(currentDate),
        });
        existingWorkload.daily[currentDate.toISOString().split('T')[0]] = 
          dayWorkload + remainingWork;
        workAssigned = true;
      }
    }

    // If no suitable day found, distribute work across multiple days
    if (!workAssigned) {
      let remainingWorkload = remainingWork;
      currentDate = new Date();

      while (remainingWorkload > 0) {
        currentDate.setDate(currentDate.getDate() + 1);
        const dayWorkload = existingWorkload.daily[currentDate.toISOString().split('T')[0]] || 0;
        const availableTime = MAX_DAILY_WORKLOAD - dayWorkload;

        if (availableTime > 0) {
          const allocatedWork = Math.min(availableTime, remainingWorkload);
          remainingWorkload -= allocatedWork;
          existingWorkload.daily[currentDate.toISOString().split('T')[0]] = 
            dayWorkload + allocatedWork;

          if (remainingWorkload === 0) {
            distribution.push({
              goal,
              newDueDate: new Date(currentDate),
            });
          }
        }
      }
    }
  }

  return distribution;
}

export function calculateOptimalDistribution(
  goals: IGoal[],
  startDate: Date,
  endDate: Date
) {
  const distribution = new Map<string, IGoal[]>();
  const dateRange = getDateRange(startDate, endDate);

  // Initialize distribution map
  dateRange.forEach(date => {
    distribution.set(date.toISOString().split('T')[0], []);
  });

  // Sort goals by priority and deadline
  const sortedGoals = [...goals].sort((a, b) => {
    if (a.priority !== b.priority) {
      const priorityWeight = { high: 3, medium: 2, low: 1 };
      return priorityWeight[b.priority] - priorityWeight[a.priority];
    }
    return a.dueDate.getTime() - b.dueDate.getTime();
  });

  // Distribute goals
  sortedGoals.forEach(goal => {
    const goalDays = Math.ceil(goal.timeEstimate / 120); // Max 2 hours per day
    let assignedDays = 0;
    
    dateRange.forEach(date => {
      if (assignedDays < goalDays) {
        const dateKey = date.toISOString().split('T')[0];
        const dayGoals = distribution.get(dateKey) || [];
        
        const dayWorkload = dayGoals.reduce(
          (sum, g) => sum + (g.timeEstimate / g.maxCarryOvers), 0
        );

        if (dayWorkload < 480) { // 8 hours max per day
          distribution.set(dateKey, [...dayGoals, goal]);
          assignedDays++;
        }
      }
    });
  });

  return distribution;
}

// Helper function to generate date range
function getDateRange(start: Date, end: Date): Date[] {
  const dates: Date[] = [];
  let currentDate = new Date(start);

  while (currentDate <= end) {
    dates.push(new Date(currentDate));
    currentDate.setDate(currentDate.getDate() + 1);
  }

  return dates;
}
