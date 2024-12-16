// signup-script.js
document.addEventListener('DOMContentLoaded', () => {
    // Constants for rate limiting
    const RATE_LIMIT = {
        MAX_ATTEMPTS: 5,
        COOLDOWN_PERIOD: 5 * 60 * 1000, // 5 minutes in milliseconds
        attempts: 0,
        lastAttemptTime: 0
    };

    // Constants for password requirements
    const PASSWORD_REQUIREMENTS = {
        minLength: 8,
        minUppercase: 1,
        minLowercase: 1,
        minNumbers: 1,
        minSpecial: 1,
        specialChars: '!@#$%^&*(),.?":{}|<>[]'
    };

    // Form elements
    const signupForm = document.getElementById('signup-form');
    const feedbackContainer = document.createElement('div');
    feedbackContainer.className = 'feedback-container';
    signupForm.appendChild(feedbackContainer);

    // Create password strength meter
    const createStrengthMeter = () => {
        const meter = document.createElement('div');
        meter.className = 'password-strength-meter';
        const indicator = document.createElement('div');
        indicator.className = 'strength-indicator';
        const text = document.createElement('span');
        text.className = 'strength-text';
        meter.appendChild(indicator);
        meter.appendChild(text);
        return { meter, indicator, text };
    };

    const strengthMeter = createStrengthMeter();
    document.getElementById('new-password').parentNode.appendChild(strengthMeter.meter);

    // Validation functions
    const validators = {
        fullName: (value) => {
            const regex = /^[a-zA-Z\s]{2,50}$/;
            return {
                isValid: regex.test(value),
                message: regex.test(value) ? 'Valid name' : 'Name should be 2-50 characters, letters only'
            };
        },
        email: (value) => {
            const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
            return {
                isValid: regex.test(value),
                message: regex.test(value) ? 'Valid email' : 'Please enter a valid email address'
            };
        },
        usn: (value) => {
            const regex = /^[1-4][A-Z]{2}\d{2}[A-Z]{2}\d{3}$/;
            return {
                isValid: regex.test(value),
                message: regex.test(value) ? 'Valid USN' : 'Invalid USN format (e.g., 1RV22CS123)'
            };
        },
        password: (value) => {
            const checks = {
                length: value.length >= PASSWORD_REQUIREMENTS.minLength,
                uppercase: (value.match(/[A-Z]/g) || []).length >= PASSWORD_REQUIREMENTS.minUppercase,
                lowercase: (value.match(/[a-z]/g) || []).length >= PASSWORD_REQUIREMENTS.minLowercase,
                numbers: (value.match(/[0-9]/g) || []).length >= PASSWORD_REQUIREMENTS.minNumbers,
                special: (value.match(new RegExp(`[${PASSWORD_REQUIREMENTS.specialChars}]`, 'g')) || []).length >= PASSWORD_REQUIREMENTS.minSpecial
            };

            const strength = Object.values(checks).filter(Boolean).length;
            const isValid = strength === Object.keys(checks).length;

            return {
                isValid,
                strength,
                message: isValid ? 'Strong password' : 'Password must contain uppercase, lowercase, number, and special character'
            };
        }
    };

    // Show validation feedback
    const showFeedback = (message, type = 'error') => {
        const feedback = document.createElement('div');
        feedback.className = `feedback ${type}`;
        feedback.textContent = message;
        feedbackContainer.innerHTML = '';
        feedbackContainer.appendChild(feedback);
        setTimeout(() => feedback.remove(), 5000);
    };

    // Update password strength meter
    const updatePasswordStrength = (validation) => {
        const strengthPercentage = (validation.strength / 5) * 100;
        strengthMeter.indicator.style.width = `${strengthPercentage}%`;
        strengthMeter.indicator.className = `strength-indicator strength-${validation.strength}`;
        strengthMeter.text.textContent = validation.message;
    };

    // Real-time validation
    const inputs = {
        fullName: document.getElementById('full-name'),
        email: document.getElementById('email'),
        usn: document.getElementById('usn'),
        password: document.getElementById('new-password'),
        confirmPassword: document.getElementById('confirm-password')
    };

    Object.entries(inputs).forEach(([field, input]) => {
        if (!input) return;
        
        input.addEventListener('input', (e) => {
            if (validators[field]) {
                const validation = validators[field](e.target.value);
                input.classList.toggle('valid', validation.isValid);
                input.classList.toggle('invalid', !validation.isValid);
                
                if (field === 'password') {
                    updatePasswordStrength(validation);
                }
            }
        });
    });

    // Rate limiting check
    const checkRateLimit = () => {
        const now = Date.now();
        if (RATE_LIMIT.attempts >= RATE_LIMIT.MAX_ATTEMPTS) {
            const timeElapsed = now - RATE_LIMIT.lastAttemptTime;
            if (timeElapsed < RATE_LIMIT.COOLDOWN_PERIOD) {
                const waitTime = Math.ceil((RATE_LIMIT.COOLDOWN_PERIOD - timeElapsed) / 1000);
                showFeedback(`Too many attempts. Please wait ${waitTime} seconds.`);
                return false;
            }
            RATE_LIMIT.attempts = 0;
        }
        return true;
    };

    // Form submission
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!checkRateLimit()) return;

        // Validate all fields
        let isValid = true;
        const formData = {};

        Object.entries(inputs).forEach(([field, input]) => {
            if (!input) return;
            
            const value = input.value.trim();
            formData[field] = value;

            if (validators[field]) {
                const validation = validators[field](value);
                if (!validation.isValid) {
                    isValid = false;
                    showFeedback(validation.message);
                }
            }
        });

        if (!isValid) {
            RATE_LIMIT.attempts++;
            RATE_LIMIT.lastAttemptTime = Date.now();
            return;
        }

        // Password confirmation
        if (formData.password !== formData.confirmPassword) {
            showFeedback('Passwords do not match');
            return;
        }

        try {
            // Get CSRF token
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
            if (!csrfToken) {
                throw new Error('CSRF token not found');
            }

            // Submit form
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrfToken
                },
                body: JSON.stringify(formData),
                credentials: 'same-origin'
            });

            const data = await response.json();

            if (data.success) {
                showFeedback('Registration successful! Redirecting...', 'success');
                setTimeout(() => window.location.href = '/login', 2000);
            } else {
                throw new Error(data.message || 'Registration failed');
            }
        } catch (error) {
            console.error('Registration error:', error);
            showFeedback(error.message || 'An error occurred during registration');
            RATE_LIMIT.attempts++;
            RATE_LIMIT.lastAttemptTime = Date.now();
        }
    });
});
