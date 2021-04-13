/* dismiss alerts */

(() => {
    'use strict';
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach((alert) => {
        const button = alert.querySelector('.btn-close');
        button.addEventListener('click', (event) => {
            event.preventDefault();
            event.stopPropagation();
            alert.remove();
        });
    });
})();