function addQuestion(questionAddButton) {
    const questionElement = document.createElement("div");
    questionElement.classList.add("question");

    const inputElement = document.createElement("input");
    inputElement.classList.add("question_input");
    inputElement.setAttribute("type", "text");

    questionElement.appendChild(inputElement);

    const buttonElement = document.createElement("button");
    buttonElement.classList.add("delete_question_btn", "action_button", "short_color_transition");
    buttonElement.setAttribute("title", "Cliquez ici pour supprimer cette question");

    const svgElement = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svgElement.classList.add("action_icon", "short_color_transition");
    svgElement.setAttribute("viewBox", "0 0 48 48");

    const pathElement = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pathElement.setAttribute("d",
        "M12.45 38.7 9.3 35.55 20.85 24 9.3 12.5l3.15-3.2L24 20.8 35.55 9.3l3.15 3.2L27.2 24l11.5 11.55-3.15 3.15L24 27.2Z");

    svgElement.appendChild(pathElement);

    buttonElement.appendChild(svgElement);
    buttonElement.appendChild(document.createTextNode("Supprimer la question"));
    buttonElement.addEventListener("click", () => deleteQuestion(buttonElement));

    questionElement.appendChild(buttonElement);

    const questionTypeListElements = questionAddButton.parentNode.getElementsByClassName("question_type_list");
    if (questionTypeListElements.length == 0) {
        // No question_type_list element, this should never happen
        // Do nothing in this case
        return;
    }

    // There should be at most one question_type_list element per question type
    questionTypeListElements[0].appendChild(questionElement);
}

function deleteQuestion(questionRemoveButton) {
    if (!confirm("Voulez-vous vraiement supprimer ce lieu ?")) {
        return;
    }

    const questionElement = questionRemoveButton.parentNode;
    questionElement.parentNode.removeChild(questionElement);
}

function saveChanges() {
    const data = [];

    for (const questionTypeNode of document.getElementsByClassName("question_type")) {
        const questionsJson = [];

        for (const questionNode of questionTypeNode.querySelectorAll(
            ".question_type_list .question .question_input")) {
            questionsJson.push({"text": questionNode.value});
        }

        const questionTypeJson = {"questions": questionsJson};
        data.push(questionTypeJson);
    }

    makeAPIRequest("admin/setQuestions", {"questions": data, "lang": "FR"}, {"content": "json"}).then(() => {
        alert("Opération effectuée avec succès");
    })
}

function setListenersToQuestionAdditionButtons() {
    for (const deleteQuestionButton of document.getElementsByClassName("add_question_btn")) {
        deleteQuestionButton.addEventListener("click", () => addQuestion(deleteQuestionButton));
    };  
}

function setListenersToQuestionDeletionButtons() {
    for (const deleteQuestionButton of document.getElementsByClassName("delete_question_btn")) {
        deleteQuestionButton.addEventListener("click", () => deleteQuestion(deleteQuestionButton));
    };
}

function setListenersToSaveChangesButton() {
    const saveChangesButton = document.getElementById("save_changes");
    if (saveChangesButton === null) {
        // There is no save_changes button, this should never happen
        // Do nothing in this case
        return;
    }
    saveChangesButton.addEventListener("click", saveChanges);
}

setListenersToQuestionAdditionButtons();
setListenersToQuestionDeletionButtons();
setListenersToSaveChangesButton();
