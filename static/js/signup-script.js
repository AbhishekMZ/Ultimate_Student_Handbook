// signup-script.js
document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signup-form');

    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const fullName = document.getElementById('full-name').value.trim();
        const usn = document.getElementById('usn').value.trim();
        const year = document.getElementById('year').value;
        const email = document.getElementById('email').value.trim();
        const newPassword = document.getElementById('new-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        // Basic validations
        if (!fullName || !usn || !year || !email || !newPassword) {
            alert('Please fill in all fields.');
            return;
        }

        if (newPassword !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }

        alert(Account created successfully for ${fullName} (${usn}).);
        signupForm.reset();
    });
});
