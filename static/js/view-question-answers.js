/* show/hide answers button */

(() => {
    'use strict';
    let questionWrappers = document.querySelectorAll(".question-wrapper");
    if (!questionWrappers) { return None; }
    questionWrappers.forEach(question => {
        let incorrectIcons = question.querySelectorAll(".answer>i:not(.correct)");
        let correctIcon = question.querySelector(".answer>i.correct");
        let toggleButton = question.querySelector(".toggle-answer-button");
        // add event listener to toggleButton with contextual access to incorrectIcons and correctIcon
        toggleButton.addEventListener('click', function(e) {
            e.preventDefault();
            if (this.textContent === "Show answer") {
                this.textContent = "Hide answer"
            } else {
                this.textContent = "Show answer"
            }
            correctIcon.classList.toggle('fa-question-circle');
            correctIcon.classList.toggle('fa-check-circle');
            incorrectIcons.forEach(incorrectIcon => {
                incorrectIcon.classList.toggle('fa-question-circle');
                incorrectIcon.classList.toggle('fa-times-circle');
            });

        });
    });

})();