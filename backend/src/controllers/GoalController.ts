import { Request, Response } from 'express';
import Goal, { IGoal } from '../models/Goal';
import Achievement from '../models/Achievement';
import { calculateWorkload } from '../utils/workloadCalculator';
import { distributeCarryOverTasks } from '../utils/taskDistributor';
import { updateAchievements } from '../utils/achievementManager';

export class GoalController {
  // Create a new goal
  static async create(req: Request, res: Response) {
    try {
      const { studentId } = req.params;
      const goalData = { ...req.body, student: studentId };

      // Check existing workload
      const existingWorkload = await calculateWorkload(studentId, goalData.dueDate);
      if (existingWorkload.isOverloaded) {
        return res.status(400).json({
          error: 'Daily workload limit exceeded',
          suggestedDate: existingWorkload.nextAvailableSlot,
        });
      }

      const goal = new Goal(goalData);
      await goal.save();

      // Check and update achievements
      await updateAchievements(studentId, 'goal_created', 1);

      res.status(201).json(goal);
    } catch (error) {
      res.status(500).json({
        error: 'Error creating goal',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Update goal progress
  static async updateProgress(req: Request, res: Response) {
    try {
      const { goalId } = req.params;
      const { progress, actualTimeSpent, completedSubTasks } = req.body;

      const goal = await Goal.findById(goalId);
      if (!goal) {
        return res.status(404).json({ error: 'Goal not found' });
      }

      // Update progress and related fields
      goal.progress = progress;
      if (actualTimeSpent) goal.actualTimeSpent = actualTimeSpent;
      
      // Update subtasks if provided
      if (completedSubTasks) {
        completedSubTasks.forEach((subtaskId: string) => {
          const subtask = goal.subTasks.id(subtaskId);
          if (subtask) {
            subtask.completed = true;
          }
        });
      }

      // Check if goal is completed
      if (progress === 100) {
        goal.status = 'completed';
        goal.completedDate = new Date();
        
        // Update streak and achievements
        goal.streakCount += 1;
        await updateAchievements(goal.student.toString(), 'goal_completed', 1);
        
        // Additional rewards for completing before deadline
        if (new Date() < goal.dueDate) {
          await updateAchievements(goal.student.toString(), 'early_completion', 1);
        }
      }

      await goal.save();

      res.json(goal);
    } catch (error) {
      res.status(500).json({
        error: 'Error updating goal progress',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Handle carry-over of incomplete goals
  static async handleCarryOver(req: Request, res: Response) {
    try {
      const { studentId } = req.params;
      const today = new Date();

      // Find incomplete goals that need to be carried over
      const incompleteGoals = await Goal.find({
        student: studentId,
        status: { $in: ['pending', 'in_progress'] },
        dueDate: { $lt: today },
        carryOverCount: { $lt: 3 }, // Max 3 carry-overs
      });

      if (incompleteGoals.length === 0) {
        return res.json({ message: 'No goals to carry over' });
      }

      // Distribute tasks over next few days
      const distributionPlan = await distributeCarryOverTasks(
        studentId,
        incompleteGoals
      );

      // Update goals with new due dates
      const updatedGoals = await Promise.all(
        distributionPlan.map(async ({ goal, newDueDate }) => {
          goal.dueDate = newDueDate;
          goal.carryOverCount += 1;
          goal.status = 'carried_over';
          return goal.save();
        })
      );

      res.json({
        message: 'Goals carried over successfully',
        updatedGoals,
      });
    } catch (error) {
      res.status(500).json({
        error: 'Error handling carry-over',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Get student's goal dashboard
  static async getDashboard(req: Request, res: Response) {
    try {
      const { studentId } = req.params;
      const { timeframe } = req.query;

      // Get goals based on timeframe
      const goals = await Goal.find({
        student: studentId,
        type: timeframe || 'daily',
      }).sort({ dueDate: 1 });

      // Get achievements
      const achievements = await Achievement.find({
        student: studentId,
        isUnlocked: true,
      });

      // Calculate statistics
      const stats = {
        totalGoals: goals.length,
        completedGoals: goals.filter(g => g.status === 'completed').length,
        currentStreak: Math.max(...goals.map(g => g.streakCount)),
        totalPoints: achievements.reduce((sum, a) => sum + a.points, 0),
        completionRate: (goals.filter(g => g.status === 'completed').length / goals.length) * 100,
      };

      // Get upcoming deadlines
      const upcomingDeadlines = goals
        .filter(g => g.status !== 'completed' && g.dueDate > new Date())
        .slice(0, 5);

      // Get recent achievements
      const recentAchievements = achievements
        .sort((a, b) => b.unlockedAt.getTime() - a.unlockedAt.getTime())
        .slice(0, 5);

      res.json({
        stats,
        upcomingDeadlines,
        recentAchievements,
        goals: goals.map(goal => ({
          ...goal.toObject(),
          isOverdue: goal.status !== 'completed' && goal.dueDate < new Date(),
          timeRemaining: goal.dueDate.getTime() - new Date().getTime(),
        })),
      });
    } catch (error) {
      res.status(500).json({
        error: 'Error fetching dashboard',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  // Get goal suggestions based on student's performance and interests
  static async getGoalSuggestions(req: Request, res: Response) {
    try {
      const { studentId } = req.params;

      // Get student's completed goals and preferences
      const completedGoals = await Goal.find({
        student: studentId,
        status: 'completed',
      });

      // Analyze patterns and generate suggestions
      const suggestions = {
        daily: generateDailySuggestions(completedGoals),
        weekly: generateWeeklySuggestions(completedGoals),
        monthly: generateMonthlySuggestions(completedGoals),
      };

      res.json(suggestions);
    } catch (error) {
      res.status(500).json({
        error: 'Error generating suggestions',
        details: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }
}

// Helper functions for generating suggestions
function generateDailySuggestions(completedGoals: IGoal[]) {
  // Analyze patterns in completed goals
  const categories = completedGoals.reduce((acc, goal) => {
    acc[goal.category] = (acc[goal.category] || 0) + 1;
    return acc;
  }, {});

  // Generate suggestions based on most successful categories
  return Object.entries(categories)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 3)
    .map(([category]) => ({
      category,
      suggestedTimeEstimate: calculateAverageTimeEstimate(completedGoals, category),
      difficulty: suggestDifficulty(completedGoals, category),
    }));
}

function generateWeeklySuggestions(completedGoals: IGoal[]) {
  // Similar to daily but with focus on larger goals
  return completedGoals
    .filter(goal => goal.type === 'weekly')
    .reduce((acc, goal) => {
      if (!acc[goal.category]) {
        acc[goal.category] = {
          count: 0,
          totalTime: 0,
          successRate: 0,
        };
      }
      acc[goal.category].count++;
      acc[goal.category].totalTime += goal.actualTimeSpent || 0;
      acc[goal.category].successRate += goal.completedDate ? 1 : 0;
      return acc;
    }, {});
}

function generateMonthlySuggestions(completedGoals: IGoal[]) {
  // Focus on long-term improvement and skill development
  const monthlyPatterns = completedGoals
    .filter(goal => goal.type === 'monthly')
    .map(goal => ({
      category: goal.category,
      timeSpent: goal.actualTimeSpent,
      success: goal.status === 'completed',
      difficulty: goal.difficulty,
    }));

  return analyzeMonthlyPatterns(monthlyPatterns);
}

// Helper function to calculate average time estimate
function calculateAverageTimeEstimate(goals: IGoal[], category: string) {
  const categoryGoals = goals.filter(g => g.category === category);
  return categoryGoals.reduce((sum, goal) => sum + (goal.actualTimeSpent || goal.timeEstimate), 0) / categoryGoals.length;
}

// Helper function to suggest difficulty
function suggestDifficulty(goals: IGoal[], category: string) {
  const categoryGoals = goals.filter(g => g.category === category);
  const successRates = {
    easy: 0,
    medium: 0,
    hard: 0,
  };

  categoryGoals.forEach(goal => {
    if (goal.status === 'completed') {
      successRates[goal.difficulty]++;
    }
  });

  // Return the difficulty level with the highest success rate
  return Object.entries(successRates)
    .sort(([, a], [, b]) => b - a)[0][0];
}

// Helper function to analyze monthly patterns
function analyzeMonthlyPatterns(patterns: any[]) {
  return patterns.reduce((acc, pattern) => {
    if (!acc[pattern.category]) {
      acc[pattern.category] = {
        successRate: 0,
        averageTimeSpent: 0,
        recommendedDifficulty: 'medium',
        count: 0,
      };
    }

    acc[pattern.category].count++;
    acc[pattern.category].successRate += pattern.success ? 1 : 0;
    acc[pattern.category].averageTimeSpent += pattern.timeSpent || 0;

    return acc;
  }, {});
}
