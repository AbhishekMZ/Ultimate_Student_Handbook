// Challenge System UI
class ChallengeUI {
    constructor() {
        this.availableChallenges = [];
        this.activeChallenges = [];
        this.completedChallenges = [];
        this.initializeUI();
    }

    async initializeUI() {
        // Create challenges panel
        const challengesPanel = document.createElement('div');
        challengesPanel.className = 'challenges-panel';
        challengesPanel.innerHTML = `
            <div class="challenges-header">
                <h3>Challenges</h3>
                <div class="challenges-tabs">
                    <button class="tab active" data-tab="available">Available</button>
                    <button class="tab" data-tab="active">Active</button>
                    <button class="tab" data-tab="completed">Completed</button>
                </div>
            </div>
            <div class="challenges-content">
                <div class="challenges-list" id="available-challenges"></div>
                <div class="challenges-list hidden" id="active-challenges"></div>
                <div class="challenges-list hidden" id="completed-challenges"></div>
            </div>
        `;
        document.querySelector('.dashboard-sidebar').appendChild(challengesPanel);

        // Add event listeners
        this.addEventListeners();

        // Load initial data
        await this.refreshChallenges();
    }

    addEventListeners() {
        // Tab switching
        const tabs = document.querySelectorAll('.challenges-tabs .tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                const tabName = tab.dataset.tab;
                document.querySelectorAll('.challenges-list').forEach(list => {
                    list.classList.add('hidden');
                });
                document.getElementById(`${tabName}-challenges`).classList.remove('hidden');
            });
        });
    }

    async refreshChallenges() {
        await Promise.all([
            this.loadAvailableChallenges(),
            this.loadActiveChallenges(),
            this.loadCompletedChallenges()
        ]);
    }

    async loadAvailableChallenges() {
        try {
            const response = await fetch('/api/challenges');
            const data = await response.json();
            this.availableChallenges = data.challenges;
            this.updateAvailableChallengesUI();
        } catch (error) {
            console.error('Error loading available challenges:', error);
        }
    }

    async loadActiveChallenges() {
        try {
            const response = await fetch('/api/challenges/active');
            const data = await response.json();
            this.activeChallenges = data.active_challenges;
            this.updateActiveChallengesUI();
        } catch (error) {
            console.error('Error loading active challenges:', error);
        }
    }

    async loadCompletedChallenges() {
        try {
            const response = await fetch('/api/challenges/completed');
            const data = await response.json();
            this.completedChallenges = data.completed_challenges;
            this.updateCompletedChallengesUI();
        } catch (error) {
            console.error('Error loading completed challenges:', error);
        }
    }

    updateAvailableChallengesUI() {
        const container = document.getElementById('available-challenges');
        container.innerHTML = this.availableChallenges.map(challenge => `
            <div class="challenge-card">
                <div class="challenge-icon">${challenge.icon}</div>
                <div class="challenge-info">
                    <h4>${challenge.title}</h4>
                    <p>${challenge.description}</p>
                    <div class="challenge-rewards">
                        <span class="xp-reward">+${challenge.xp_reward} XP</span>
                        ${Object.entries(challenge.skill_rewards || {}).map(([skill, points]) =>
                            `<span class="skill-reward">+${points} ${skill}</span>`
                        ).join('')}
                    </div>
                    <button class="accept-challenge" onclick="challenges.acceptChallenge('${challenge.title}')">
                        Accept Challenge
                    </button>
                </div>
            </div>
        `).join('');
    }

    updateActiveChallengesUI() {
        const container = document.getElementById('active-challenges');
        container.innerHTML = this.activeChallenges.map(challenge => `
            <div class="challenge-card active">
                <div class="challenge-icon">${challenge.challenge.icon}</div>
                <div class="challenge-info">
                    <h4>${challenge.challenge.title}</h4>
                    <p>${challenge.challenge.description}</p>
                    <div class="challenge-progress">
                        ${challenge.challenge.requirements.map(req => `
                            <div class="requirement">
                                <div class="progress-bar">
                                    <div class="progress" style="width: ${(challenge.progress[req.type] / req.target) * 100}%"></div>
                                </div>
                                <span class="progress-text">${challenge.progress[req.type]}/${req.target}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `).join('');
    }

    updateCompletedChallengesUI() {
        const container = document.getElementById('completed-challenges');
        container.innerHTML = this.completedChallenges.map(challenge => `
            <div class="challenge-card completed">
                <div class="challenge-icon">${challenge.challenge.icon}</div>
                <div class="challenge-info">
                    <h4>${challenge.challenge.title}</h4>
                    <p>${challenge.challenge.description}</p>
                    <div class="challenge-completion">
                        <span class="completion-date">
                            Completed on ${new Date(challenge.completed_at).toLocaleDateString()}
                        </span>
                        <div class="rewards-earned">
                            <span class="xp-earned">+${challenge.challenge.xp_reward} XP</span>
                            ${Object.entries(challenge.challenge.skill_rewards || {}).map(([skill, points]) =>
                                `<span class="skill-earned">+${points} ${skill}</span>`
                            ).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    async acceptChallenge(challengeTitle) {
        try {
            const response = await fetch('/api/challenges/accept', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ challenge_title: challengeTitle })
            });
            
            const result = await response.json();
            if (result.success) {
                await this.refreshChallenges();
                this.showNotification('Challenge accepted!', 'success');
            } else {
                this.showNotification(result.error, 'error');
            }
        } catch (error) {
            console.error('Error accepting challenge:', error);
            this.showNotification('Failed to accept challenge', 'error');
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// Initialize challenges when document is ready
document.addEventListener('DOMContentLoaded', () => {
    window.challenges = new ChallengeUI();
});
