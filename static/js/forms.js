/* form validation. credit: https://mdbootstrap.com/docs/standard/forms/validation/ */

(() => {
    'use strict';
    // Fetch form
    const form = document.querySelector('form');
    form.addEventListener('submit', (event) => {
        if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
        }
        form.classList.add('was-validated');
    }, false);
})();