from flask import Blueprint, jsonify, request, current_app
from models.gamification import GamificationSystem
from utils.auth import login_required
from datetime import datetime

gamification = Blueprint('gamification', __name__)
gamification_system = None

@gamification.before_app_first_request
def initialize_gamification():
    global gamification_system
    gamification_system = GamificationSystem(current_app.config['MONGO_DB'])

@gamification.route('/api/progress', methods=['GET'])
@login_required
async def get_progress():
    user_id = request.user_id
    progress = await gamification_system.get_user_progress(user_id)
    await gamification_system.check_achievements(progress)
    return jsonify(progress.to_dict())

@gamification.route('/api/achievements', methods=['GET'])
@login_required
async def get_achievements():
    user_id = request.user_id
    progress = await gamification_system.get_user_progress(user_id)
    await gamification_system.check_achievements(progress)
    
    achievements_data = [a.to_dict() for a in progress.achievements]
    completed_count = sum(1 for a in achievements_data if a['completed'])
    
    return jsonify({
        'achievements': achievements_data,
        'total_xp': progress.xp,
        'level': progress.level,
        'stats': progress.stats,
        'completion': {
            'total': len(achievements_data),
            'completed': completed_count,
            'percentage': (completed_count / len(achievements_data)) * 100
        }
    })

@gamification.route('/api/daily-login', methods=['POST'])
@login_required
async def record_daily_login():
    user_id = request.user_id
    progress = await gamification_system.get_user_progress(user_id)
    progress.update_login_streak()
    await gamification_system.update_user_progress(progress)
    await gamification_system.check_achievements(progress)
    
    return jsonify({
        'success': True,
        'streak': progress.daily_streak,
        'xp_gained': progress.XP_REWARDS['daily_login']
    })

@gamification.route('/api/record-activity', methods=['POST'])
@login_required
async def record_activity():
    user_id = request.user_id
    activity_data = request.json
    activity_type = activity_data.get('type')
    additional_data = activity_data.get('additional_data', {})
    
    if not activity_type:
        return jsonify({'success': False, 'error': 'Activity type is required'}), 400
    
    progress = await gamification_system.get_user_progress(user_id)
    old_level = progress.level
    
    progress.record_activity(activity_type, additional_data)
    await gamification_system.update_user_progress(progress)
    await gamification_system.check_achievements(progress)
    
    response_data = {
        'success': True,
        'xp_gained': progress.XP_REWARDS.get(activity_type, 0),
        'new_total_xp': progress.xp,
        'new_level': progress.level,
        'leveled_up': progress.level > old_level,
        'stats': progress.stats
    }
    
    if progress.level > old_level:
        response_data['level_up'] = {
            'old_level': old_level,
            'new_level': progress.level,
            'xp_for_next': (progress.level + 1) ** 2 * 25
        }
    
    return jsonify(response_data)

@gamification.route('/api/study-session', methods=['POST'])
@login_required
async def record_study_session():
    user_id = request.user_id
    session_data = request.json
    duration = session_data.get('duration', 0)  # duration in minutes
    
    progress = await gamification_system.get_user_progress(user_id)
    progress.record_activity('study_session', {'duration': duration})
    await gamification_system.update_user_progress(progress)
    await gamification_system.check_achievements(progress)
    
    return jsonify({
        'success': True,
        'stats': progress.stats,
        'study_streak': (datetime.now() - progress.study_streak_start).days + 1 if progress.study_streak_start else 0
    })
