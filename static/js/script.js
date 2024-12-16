// script.js
document.addEventListener('DOMContentLoaded', () => {
    const authForm = document.getElementById('auth-form');
    const signupForm = document.getElementById('signup-form');
    const signupLink = document.getElementById('signup-link');
    const loginLink = document.getElementById('login-link');
    const forgotPassword = document.getElementById('forgot-password');

    // Switch to Sign Up Form
    if (signupLink) {
        signupLink.addEventListener('click', () => {
            window.location.href = '/register';
        });
    }

    // Switch to Login Form
    if (loginLink) {
        loginLink.addEventListener('click', () => {
            window.location.href = '/login';
        });
    }

    // Handle Login
    if (authForm) {
        authForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(authForm);
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    window.location.href = data.redirect;
                } else {
                    alert(data.message || 'Login failed');
                }
            } catch (error) {
                console.error('Login error:', error);
                alert('An error occurred during login');
            }
        });
    }

    // Handle Registration
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const password = document.getElementById('new-password').value;
            const confirmPassword = document.getElementById('confirm-password').value;

            if (password !== confirmPassword) {
                alert('Passwords do not match!');
                return;
            }

            const formData = new FormData(signupForm);
            
            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert('Registration successful! Please login.');
                    window.location.href = '/login';
                } else {
                    alert(data.message || 'Registration failed');
                }
            } catch (error) {
                console.error('Registration error:', error);
                alert('An error occurred during registration');
            }
        });
    }

    // Handle Forgot Password
    if (forgotPassword) {
        forgotPassword.addEventListener('click', (e) => {
            e.preventDefault();
            alert('Password reset functionality will be implemented soon.');
        });
    }
});