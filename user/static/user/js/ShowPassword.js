function togglePassword() {
    const passwordField = document.getElementById('id_password');
    const toggleButton = document.getElementById('toggle-password');
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleButton.style.color = '#888';
    } else {
        passwordField.type = 'password';
        toggleButton.style.color = '';
    }
}
