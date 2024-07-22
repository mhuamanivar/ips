// placeholders.js

document.addEventListener('DOMContentLoaded', function() {
    // Agregar placeholders a los campos de contraseña si están presentes en la página
    const emailInput = document.getElementById('id_email');
    if (emailInput) {
        emailInput.placeholder = 'email@domain.com';
    }

    const password1Input = document.getElementById('id_password1');
    if (password1Input) {
        password1Input.placeholder = 'Contraseña';
    }

    const password2Input = document.getElementById('id_password2');
    if (password2Input) {
        password2Input.placeholder = 'Contraseña';
    }

    // Otros placeholders para diferentes formularios si es necesario
});
