// profile.js
document.addEventListener("DOMContentLoaded", function() {
    const links = document.querySelectorAll('.nav-link');
  
    links.forEach(link => {
      link.addEventListener('click', function(event) {
        event.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
          targetElement.scrollIntoView({ behavior: 'smooth' });
          history.replaceState(null, null, `#${targetId}`); // Utilizar replaceState en lugar de pushState
        }
      });
    });
  
    // Manejar el botón de retroceso del navegador
    window.addEventListener('popstate', function(event) {
      const hash = window.location.hash;
      const targetElement = document.querySelector(hash);
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
  