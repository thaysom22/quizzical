


/* Form validation user feedback. credit: https://mdbootstrap.com/docs/standard/forms/validation/ */

(() => {
    'use strict';
    // Fetch form
    const form = document.querySelector('form');
    form.addEventListener('submit', (event) => {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }   
        // else if (form.id === "create-quiz-form") {
        //     onCreateQuizFormSubmit(event, form);
        // }
        form.classList.add('was-validated');
    }, false);
})();

/* submit create quiz form data to server as json */

// function onCreateQuizFormSubmit(event, createQuizForm) {
//     event.preventDefault();
//     event.stopPropagation();

//     createQuizDataObject = {
//         title: createQuizForm.querySelector('#create-quiz-title').value,
//         quiz_category_id: createQuizForm.querySelector('#create-quiz-category').value,
//         quiz_age_range_id: createQuizForm.querySelector('#create-quiz-age-range').value,
//     }

//     createQuizDataJSON = JSON.stringify(createQuizDataObject);


//     console.log("JSON sent to server:", createQuizDataJSON); // TEST
// }
