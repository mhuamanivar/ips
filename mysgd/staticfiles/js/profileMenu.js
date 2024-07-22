// profileMenu.js

document.addEventListener('DOMContentLoaded', function() {
    const profileButton = document.querySelector('.dropdown > a');
    const profileMenu = document.querySelector('.dropdown .dropdown-content');

    if (profileButton && profileMenu) {
        profileMenu.style.display = 'none';

        profileButton.addEventListener('click', (event) => {
            event.preventDefault();
            profileMenu.style.display = (profileMenu.style.display === 'block') ? 'none' : 'block';

            // Mostrar el nombre de usuario solo al abrir el menú desplegable
            if (profileMenu.style.display === 'block') {
                const username = "{{ user.username }}";
                const usernameElement = profileMenu.querySelector('.username');
                if (usernameElement) {
                    usernameElement.textContent = username;
                }
            }
        });

        window.addEventListener('click', (event) => {
            if (!profileButton.contains(event.target) && !profileMenu.contains(event.target)) {
                profileMenu.style.display = 'none';
            }
        });
    } else {
        console.log('No se encontraron elementos adecuados para el menú desplegable de perfil.');
    }
});
