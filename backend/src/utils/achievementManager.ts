import Achievement from '../models/Achievement';
import { notifyStudent } from './notifications';

interface AchievementCriteria {
  [key: string]: {
    type: string;
    targetValue: number;
    points: number;
    title: string;
    description: string;
    icon: string;
  };
}

const ACHIEVEMENT_CRITERIA: AchievementCriteria = {
  goal_created: {
    type: 'count',
    targetValue: 10,
    points: 50,
    title: 'Goal Setter',
    description: 'Created 10 goals',
    icon: '🎯',
  },
  goal_completed: {
    type: 'count',
    targetValue: 5,
    points: 100,
    title: 'Achiever',
    description: 'Completed 5 goals',
    icon: '🏆',
  },
  early_completion: {
    type: 'count',
    targetValue: 3,
    points: 150,
    title: 'Early Bird',
    description: 'Completed 3 goals before deadline',
    icon: '⭐',
  },
  perfect_week: {
    type: 'streak',
    targetValue: 7,
    points: 200,
    title: 'Perfect Week',
    description: 'Completed all daily goals for a week',
    icon: '🌟',
  },
  study_streak: {
    type: 'streak',
    targetValue: 30,
    points: 500,
    title: 'Study Master',
    description: 'Maintained study streak for 30 days',
    icon: '📚',
  },
  improvement: {
    type: 'progress',
    targetValue: 50,
    points: 300,
    title: 'Rising Star',
    description: 'Improved performance by 50%',
    icon: '📈',
  },
};

export async function updateAchievements(
  studentId: string,
  actionType: string,
  value: number
) {
  try {
    // Get or create achievement
    let achievement = await Achievement.findOne({
      student: studentId,
      'criteria.type': actionType,
      isUnlocked: false,
    });

    if (!achievement && ACHIEVEMENT_CRITERIA[actionType]) {
      achievement = new Achievement({
        student: studentId,
        title: ACHIEVEMENT_CRITERIA[actionType].title,
        description: ACHIEVEMENT_CRITERIA[actionType].description,
        type: 'badge',
        category: 'consistency',
        points: ACHIEVEMENT_CRITERIA[actionType].points,
        targetValue: ACHIEVEMENT_CRITERIA[actionType].targetValue,
        currentValue: 0,
        icon: ACHIEVEMENT_CRITERIA[actionType].icon,
        criteria: {
          type: actionType,
          value: ACHIEVEMENT_CRITERIA[actionType].targetValue,
        },
      });
    }

    if (achievement) {
      // Update progress
      achievement.currentValue += value;
      
      // Check if achievement is completed
      if (achievement.checkCompletion()) {
        // Notify student
        await notifyStudent(studentId, {
          type: 'achievement_unlocked',
          title: 'Achievement Unlocked!',
          message: `Congratulations! You've earned the "${achievement.title}" achievement!`,
          icon: achievement.icon,
        });

        // Grant rewards
        await grantAchievementRewards(studentId, achievement);
      }

      await achievement.save();
    }

    // Check for milestone achievements
    await checkMilestoneAchievements(studentId);
  } catch (error) {
    console.error('Error updating achievements:', error);
  }
}

async function checkMilestoneAchievements(studentId: string) {
  try {
    const unlockedAchievements = await Achievement.find({
      student: studentId,
      isUnlocked: true,
    });

    // Check for achievement combinations
    const achievementTypes = unlockedAchievements.map(a => a.criteria.type);
    
    // Example: Check for "All-rounder" achievement
    if (
      achievementTypes.includes('goal_completed') &&
      achievementTypes.includes('early_completion') &&
      achievementTypes.includes('perfect_week')
    ) {
      const allRounder = await Achievement.findOne({
        student: studentId,
        title: 'All-rounder',
      });

      if (!allRounder) {
        const newAchievement = new Achievement({
          student: studentId,
          title: 'All-rounder',
          description: 'Mastered multiple aspects of goal achievement',
          type: 'milestone',
          category: 'special',
          points: 1000,
          targetValue: 1,
          currentValue: 1,
          isUnlocked: true,
          unlockedAt: new Date(),
          icon: '👑',
          criteria: {
            type: 'combination',
            value: 3,
          },
        });

        await newAchievement.save();
        await notifyStudent(studentId, {
          type: 'special_achievement',
          title: 'Special Achievement Unlocked!',
          message: 'You\'ve become an All-rounder!',
          icon: '👑',
        });
      }
    }
  } catch (error) {
    console.error('Error checking milestone achievements:', error);
  }
}

async function grantAchievementRewards(studentId: string, achievement: any) {
  try {
    // Grant points
    // This would integrate with your points/rewards system
    
    // Special rewards based on achievement type
    switch (achievement.title) {
      case 'Perfect Week':
        // Maybe grant a "free pass" for one missed deadline
        break;
      case 'Study Master':
        // Maybe unlock special study resources or features
        break;
      case 'Rising Star':
        // Maybe provide additional points multiplier
        break;
    }

    // Update student's total points
    // This would integrate with your student profile system
  } catch (error) {
    console.error('Error granting achievement rewards:', error);
  }
}
