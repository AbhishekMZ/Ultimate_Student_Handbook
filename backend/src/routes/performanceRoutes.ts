import express from 'express';
import { PerformanceController } from '../controllers/PerformanceController';
import { authenticate } from '../middleware/auth';
import { validateRole } from '../middleware/roleValidation';

const router = express.Router();

// All routes require authentication
router.use(authenticate);

// Student accessible routes
router.get('/summary/:studentId', PerformanceController.getPerformanceSummary);

// Faculty and admin routes
router.use(validateRole(['faculty', 'admin']));
router.post('/attendance', PerformanceController.updateAttendance);
router.post('/assessment', PerformanceController.recordAssessmentMarks);
router.get('/analytics/class/:courseId/:semester', PerformanceController.getClassPerformanceAnalytics);
router.get('/report/:studentId/:semester', PerformanceController.generateProgressReport);

export default router;
