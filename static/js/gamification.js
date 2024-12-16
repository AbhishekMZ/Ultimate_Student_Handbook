// Gamification System Frontend
class GamificationUI {
    constructor() {
        this.progress = null;
        this.achievements = null;
        this.initializeUI();
    }

    async initializeUI() {
        // Create progress bar in the dashboard
        const progressContainer = document.createElement('div');
        progressContainer.className = 'progress-container';
        progressContainer.innerHTML = `
            <div class="level-info">
                <span class="level">Level 1</span>
                <div class="xp-bar">
                    <div class="xp-progress"></div>
                </div>
                <span class="xp">0 XP</span>
            </div>
            <div class="achievements-showcase"></div>
            <div class="daily-streak">
                <span class="streak-count">0</span>
                <span class="streak-label">Day Streak</span>
            </div>
        `;
        document.querySelector('.dashboard-header').appendChild(progressContainer);

        // Initialize achievements panel
        this.createAchievementsPanel();
        
        // Load initial data
        await this.refreshProgress();
        await this.refreshAchievements();
        
        // Record daily login
        await this.recordDailyLogin();
    }

    createAchievementsPanel() {
        const panel = document.createElement('div');
        panel.className = 'achievements-panel';
        panel.innerHTML = `
            <div class="achievements-header">
                <h3>Achievements</h3>
                <div class="achievements-stats">
                    <span class="total-xp">0 XP</span>
                    <span class="achievement-count">0/0</span>
                </div>
            </div>
            <div class="achievements-list"></div>
        `;
        document.querySelector('.dashboard-sidebar').appendChild(panel);
    }

    async refreshProgress() {
        try {
            const response = await fetch('/api/progress');
            this.progress = await response.json();
            this.updateProgressUI();
        } catch (error) {
            console.error('Error fetching progress:', error);
        }
    }

    async refreshAchievements() {
        try {
            const response = await fetch('/api/achievements');
            this.achievements = await response.json();
            this.updateAchievementsUI();
        } catch (error) {
            console.error('Error fetching achievements:', error);
        }
    }

    updateProgressUI() {
        const levelInfo = document.querySelector('.level-info');
        const xpProgress = levelInfo.querySelector('.xp-progress');
        const levelSpan = levelInfo.querySelector('.level');
        const xpSpan = levelInfo.querySelector('.xp');
        const streakCount = document.querySelector('.streak-count');

        levelSpan.textContent = `Level ${this.progress.level}`;
        xpSpan.textContent = `${this.progress.xp} XP`;
        streakCount.textContent = this.progress.daily_streak;

        // Calculate progress to next level
        const xpForCurrentLevel = (this.progress.level - 1) * 100;
        const progressToNextLevel = ((this.progress.xp - xpForCurrentLevel) / 100) * 100;
        xpProgress.style.width = `${progressToNextLevel}%`;
    }

    updateAchievementsUI() {
        const achievementsList = document.querySelector('.achievements-list');
        const achievementStats = document.querySelector('.achievements-stats');
        
        achievementStats.querySelector('.total-xp').textContent = `${this.achievements.total_xp} XP`;
        achievementStats.querySelector('.achievement-count').textContent = 
            `${this.achievements.achievements.filter(a => a.completed).length}/${this.achievements.achievements.length}`;

        achievementsList.innerHTML = this.achievements.achievements
            .map(achievement => `
                <div class="achievement ${achievement.completed ? 'completed' : ''}">
                    <span class="achievement-icon">${achievement.icon}</span>
                    <div class="achievement-info">
                        <h4>${achievement.name}</h4>
                        <p>${achievement.description}</p>
                        <span class="achievement-points">+${achievement.points} XP</span>
                    </div>
                </div>
            `).join('');
    }

    async recordDailyLogin() {
        try {
            const response = await fetch('/api/daily-login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const result = await response.json();
            if (result.success) {
                await this.refreshProgress();
                await this.refreshAchievements();
            }
        } catch (error) {
            console.error('Error recording daily login:', error);
        }
    }

    async recordActivity(activityType) {
        try {
            const response = await fetch('/api/record-activity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ type: activityType })
            });
            const result = await response.json();
            if (result.success) {
                this.showXPGain(result.xp_gained);
                await this.refreshProgress();
                await this.refreshAchievements();
            }
        } catch (error) {
            console.error('Error recording activity:', error);
        }
    }

    showXPGain(xp) {
        const xpPopup = document.createElement('div');
        xpPopup.className = 'xp-popup';
        xpPopup.textContent = `+${xp} XP`;
        document.body.appendChild(xpPopup);
        
        setTimeout(() => {
            xpPopup.classList.add('fade-out');
            setTimeout(() => xpPopup.remove(), 500);
        }, 1500);
    }
}

// Initialize gamification when document is ready
document.addEventListener('DOMContentLoaded', () => {
    window.gamification = new GamificationUI();
});
