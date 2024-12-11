import express from 'express';
import { StudentController } from '../controllers/StudentController';
import { authenticate } from '../middleware/auth';
import { validateRole } from '../middleware/roleValidation';

const router = express.Router();

// Public routes
router.get('/search', StudentController.search);

// Protected routes
router.use(authenticate);

// Student routes
router.get('/', StudentController.getAll);
router.get('/:id', StudentController.getById);

// Admin only routes
router.post('/', validateRole(['admin']), StudentController.create);
router.put('/:id', validateRole(['admin']), StudentController.update);
router.delete('/:id', validateRole(['admin']), StudentController.delete);
router.post('/bulk-import', validateRole(['admin']), StudentController.bulkImport);

export default router;
