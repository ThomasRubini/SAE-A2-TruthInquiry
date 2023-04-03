function addTrait() {
    const traitElement = document.createElement("div");
    traitElement.classList.add("trait");
    traitElement.setAttribute("data-id", "");

    const traitNameContainerElement = document.createElement("div");
    traitNameContainerElement.classList.add("trait_name_container");

    const traitNameTitleElement = document.createElement("h3");
    traitNameTitleElement.classList.add("trait_name");
    traitNameTitleElement.appendChild(document.createTextNode("Nom de la réaction\u00A0:"));

    traitNameContainerElement.appendChild(traitNameTitleElement);

    const traitNameInputElement = document.createElement("input");
    traitNameInputElement.classList.add("trait_name_input");
    traitNameInputElement.setAttribute("type", "text");
    traitNameInputElement.setAttribute("value", "");

    traitNameContainerElement.appendChild(traitNameInputElement);

    traitElement.appendChild(traitNameContainerElement);

    const traitDescriptionElement = document.createElement("div");
    traitDescriptionElement.classList.add("trait_description_container");

    const traitDescriptionTitleElement = document.createElement("h3");
    traitDescriptionTitleElement.classList.add("trait_description");
    traitDescriptionTitleElement.appendChild(document.createTextNode("Description de la réaction\u00A0:"));

    traitDescriptionElement.appendChild(traitDescriptionTitleElement);

    const traitDescriptionInputElement = document.createElement("input");
    traitDescriptionInputElement.classList.add("trait_description_input");
    traitDescriptionInputElement.setAttribute("type", "text");
    traitDescriptionInputElement.setAttribute("value", "");

    traitDescriptionElement.appendChild(traitDescriptionInputElement);

    traitElement.appendChild(traitDescriptionElement);

    const buttonElement = document.createElement("button");
    buttonElement.classList.add("delete_trait_btn", "action_button", "short_color_transition");
    buttonElement.setAttribute("title", "Cliquez ici pour supprimer cette réaction");

    const svgElement = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svgElement.classList.add("action_icon", "short_color_transition");
    svgElement.setAttribute("viewBox", "0 0 48 48");

    const pathElement = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pathElement.setAttribute("d",
        "M12.45 38.7 9.3 35.55 20.85 24 9.3 12.5l3.15-3.2L24 20.8 35.55 9.3l3.15 3.2L27.2 24l11.5 11.55-3.15 3.15L24 27.2Z");

    svgElement.appendChild(pathElement);

    buttonElement.appendChild(svgElement);
    buttonElement.appendChild(document.createTextNode("Supprimer la réaction"));
    buttonElement.addEventListener("click", () => deleteTrait(buttonElement));

    traitElement.appendChild(buttonElement);

    const traitsElement = document.getElementById("traits");
    if (traitsElement === null) {
        // No places element, this should never happen
        // Do nothing in this case
        return;
    }

    traitsElement.appendChild(traitElement);
}

function deleteTrait(traitDeletionButton) {
    if (!confirm("Voulez-vous vraiement supprimer cette réaction ?")) {
        return;
    }

    const traitNode = traitDeletionButton.parentNode;
    traitNode.parentNode.removeChild(traitNode);
}

function saveChanges() {
    const data = [];

    for (const traitElement of document.getElementsByClassName("trait")) {
        const trait = {};
        trait["id"] = traitElement.getAttribute("data-id");
        trait["name"] = traitElement.querySelector(".trait_name_input").value;
        trait["desc"] = traitElement.querySelector(".trait_description_input").value;
        data.push(trait);
    }

    makeAPIRequest("admin/setTraits", {"traits": data, "lang": "FR"}, {"content": "json"}).then(() => {
        alert("Opération effectuée avec succès");
    });
}

function setListenersToTraitDeletionButtons() {
    for (const deleteTraitButton of document.getElementsByClassName("delete_trait_btn")) {
        deleteTraitButton.addEventListener("click", () => deleteTrait(deleteTraitButton));
    };
}

function setListenersToTraitAdditionButton() {
    const addTraitButton = document.getElementById("add_trait");
    if (addTraitButton === null) {
        // There is no add_place button, this should never happen
        // Do nothing in this case
        return;
    }

    addTraitButton.addEventListener("click", addTrait);
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

setListenersToTraitDeletionButtons();
setListenersToTraitAdditionButton();
setListenersToSaveChangesButton();
