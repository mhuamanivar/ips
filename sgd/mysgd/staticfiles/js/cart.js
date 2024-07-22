document.addEventListener('DOMContentLoaded', function() {
    function updateTotal() {
        let total = 0;
        document.querySelectorAll('.cart-item-form').forEach(form => {
            let price = parseFloat(form.closest('tr').querySelector('td:nth-child(3)').textContent.replace('S/. ', ''));
            let quantity = parseInt(form.querySelector('.quantity-input').value);
            total += price * quantity;
        });
        document.getElementById('total-price').textContent = 'S/. ' + total.toFixed(2);
    }

    // Llama a updateTotal al cargar la página
    updateTotal();
});
