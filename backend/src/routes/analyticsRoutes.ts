import express from 'express';
import { AnalyticsController } from '../controllers/AnalyticsController';
import { authenticate } from '../middleware/auth';
import { validateRole } from '../middleware/roleValidation';

const router = express.Router();

// All routes require authentication
router.use(authenticate);

// Faculty and admin routes
router.use(validateRole(['faculty', 'admin']));

// Department analytics
router.get('/department', AnalyticsController.getDepartmentAnalytics);

// Student performance trends
router.get('/trends/:studentId', AnalyticsController.getStudentTrends);

// Export performance report
router.get('/export', AnalyticsController.exportPerformanceReport);

// Course completion analytics
router.get('/course/:courseId', AnalyticsController.getCourseCompletionAnalytics);

export default router;
