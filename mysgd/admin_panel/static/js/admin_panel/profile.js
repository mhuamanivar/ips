document.addEventListener('DOMContentLoaded', function () {
    const editButton = document.getElementById('edit-btn');
    const saveButton = document.getElementById('save-btn');
    const fields = document.querySelectorAll('.profile-form .form-group input, .profile-form .form-group textarea');

    // Inicialmente, todos los campos son no editables
    fields.forEach(field => {
        field.disabled = true;
    });

    // Función para activar el modo edición
    editButton.addEventListener('click', function () {
        fields.forEach(field => {
            field.disabled = false;
        });
        saveButton.style.display = 'inline-block'; // Muestra el botón de guardar
        editButton.style.display = 'none'; // Oculta el botón de editar
    });
});
