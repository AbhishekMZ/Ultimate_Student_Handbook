from flask import Blueprint, jsonify, request, current_app
from models.challenges import ChallengeSystem
from utils.auth import login_required
from datetime import datetime

challenges = Blueprint('challenges', __name__)
challenge_system = None

@challenges.before_app_first_request
def initialize_challenges():
    global challenge_system
    challenge_system = ChallengeSystem(current_app.config['MONGO_DB'])

@challenges.route('/api/challenges', methods=['GET'])
@login_required
async def get_challenges():
    """Get all available challenges for the user"""
    user_id = request.user_id
    available_challenges = await challenge_system.get_available_challenges(user_id)
    return jsonify({
        'challenges': [challenge.to_dict() for challenge in available_challenges]
    })

@challenges.route('/api/challenges/active', methods=['GET'])
@login_required
async def get_active_challenges():
    """Get user's active challenges"""
    user_id = request.user_id
    active_challenges = await challenge_system.user_challenges_collection.find({
        'user_id': user_id,
        'completed_at': None
    }).to_list(length=None)
    return jsonify({
        'active_challenges': active_challenges
    })

@challenges.route('/api/challenges/completed', methods=['GET'])
@login_required
async def get_completed_challenges():
    """Get user's completed challenges"""
    user_id = request.user_id
    completed_challenges = await challenge_system.user_challenges_collection.find({
        'user_id': user_id,
        'completed_at': {'$ne': None}
    }).to_list(length=None)
    return jsonify({
        'completed_challenges': completed_challenges
    })

@challenges.route('/api/challenges/accept', methods=['POST'])
@login_required
async def accept_challenge():
    """Accept a challenge"""
    user_id = request.user_id
    challenge_title = request.json.get('challenge_title')
    
    if not challenge_title:
        return jsonify({
            'success': False,
            'error': 'Challenge title is required'
        }), 400
    
    user_challenge = await challenge_system.accept_challenge(user_id, challenge_title)
    if not user_challenge:
        return jsonify({
            'success': False,
            'error': 'Challenge not found or already expired'
        }), 404
    
    return jsonify({
        'success': True,
        'challenge': user_challenge.to_dict()
    })

@challenges.route('/api/challenges/progress', methods=['POST'])
@login_required
async def update_challenge_progress():
    """Update challenge progress based on activity"""
    user_id = request.user_id
    activity_data = request.json
    
    activity_type = activity_data.get('type')
    amount = activity_data.get('amount', 1)
    
    if not activity_type:
        return jsonify({
            'success': False,
            'error': 'Activity type is required'
        }), 400
    
    await challenge_system.update_challenge_progress(user_id, activity_type, amount)
    
    # Get updated active challenges
    active_challenges = await challenge_system.user_challenges_collection.find({
        'user_id': user_id,
        'completed_at': None
    }).to_list(length=None)
    
    return jsonify({
        'success': True,
        'active_challenges': active_challenges
    })

@challenges.route('/api/challenges/generate', methods=['POST'])
@login_required
async def generate_challenges():
    """Generate new challenges (admin only)"""
    # TODO: Add admin check
    await challenge_system.generate_challenges()
    return jsonify({
        'success': True,
        'message': 'New challenges generated successfully'
    })
