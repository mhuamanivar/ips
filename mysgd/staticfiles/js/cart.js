$(document).ready(function() {
    // Escuchamos el evento de submit en los formularios de los items del carrito
    $('.cart-item-form').submit(function(event) {
        event.preventDefault(); // Evitamos la acción por defecto del formulario

        var form = $(this); // Capturamos el formulario actual
        var actionUrl = form.attr('action'); // Obtenemos la URL de acción del formulario
        var formData = form.serialize(); // Serializamos los datos del formulario

        // Realizamos una petición AJAX POST
        $.ajax({
            url: actionUrl, // URL de la acción del formulario
            method: 'POST', // Método POST
            data: formData, // Datos serializados del formulario
            success: function(response) {
                // Actualizamos la cantidad mostrada en la página
                var quantityInput = form.find('.quantity-input');
                quantityInput.val(parseInt(quantityInput.val()) + (form.find('button[type="submit"][name="action"]').val() === 'increase' ? 1 : -1));
            },
            error: function(error) {
                console.log(error); // Manejo de errores
            }
        });
    });
});
