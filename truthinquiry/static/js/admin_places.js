function addPlace() {
    const placeElement = document.createElement("div");
    placeElement.classList.add("place");

    const inputElement = document.createElement("input");
    inputElement.classList.add("place_input");
    inputElement.setAttribute("type", "text");
    inputElement.setAttribute("id", "");

    placeElement.appendChild(inputElement);

    const buttonElement = document.createElement("button");
    buttonElement.classList.add("delete_place_btn", "action_button", "short_color_transition");
    buttonElement.setAttribute("title", "Cliquez ici pour supprimer ce lieu");

    const svgElement = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svgElement.classList.add("action_icon", "short_color_transition");
    svgElement.setAttribute("viewBox", "0 0 48 48");

    const pathElement = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pathElement.setAttribute("d",
        "M12.45 38.7 9.3 35.55 20.85 24 9.3 12.5l3.15-3.2L24 20.8 35.55 9.3l3.15 3.2L27.2 24l11.5 11.55-3.15 3.15L24 27.2Z");

    svgElement.appendChild(pathElement);

    buttonElement.appendChild(svgElement);
    buttonElement.appendChild(document.createTextNode("Supprimer le lieu"));
    buttonElement.addEventListener("click", () => deletePlace(buttonElement));

    placeElement.appendChild(buttonElement);

    const placesElement = document.getElementById("places");
    if (placesElement === null) {
        // No places element, this should never happen
        // Do nothing in this case
        return;
    }

    placesElement.appendChild(placeElement);
}

function deletePlace(placeRemoveButton) {
    if (!confirm("Voulez-vous vraiement supprimer ce lieu ?")) {
        return;
    }

    const placeElement = placeRemoveButton.parentNode;
    placeElement.parentNode.removeChild(placeElement);
}

function saveChanges() {
    const data = [];
    for (const section of document.getElementsByClassName("place")) {
        const place = {};
        place["id"] = section.id;
        place["name"] = section.querySelector("input").value;
        data.push(place);
    }

    makeAPIRequest("admin/setPlaces", {"places": data, "lang": "FR"}, {"content": "json"}).then(() => {
        alert("Opération effectuée avec succès");
    });
}

function setListenersToPlaceAdditionButton() {
    const addPlaceButton = document.getElementById("add_place");
    if (addPlaceButton === null) {
        // There is no add_place button, this should never happen
        // Do nothing in this case
        return;
    }

    addPlaceButton.addEventListener("click", addPlace);
}

function setListenersToPlaceDeletionButtons() {
    for (const deletePlaceButton of document.getElementsByClassName("delete_place_btn")) {
        deletePlaceButton.addEventListener("click", () => deletePlace(deletePlaceButton));
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

setListenersToPlaceDeletionButtons();
setListenersToPlaceAdditionButton();
setListenersToSaveChangesButton();
