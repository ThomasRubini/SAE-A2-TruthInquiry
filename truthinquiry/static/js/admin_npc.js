
const reactionsDelta = {};

async function createOrUpdateNpc() {
    const data = {};
    data["id"] = document.querySelector("#npc_id").value;
    data["name"] = document.querySelector("#npc_name").value;
    
    const allAnswersJson = [];
    data["allAnswers"] = allAnswersJson;
    
    for (const answerTypeNode of document.querySelector(".answer_groups").children) {
        const answersJson = [];
        const answerTypeJson = {"answers": answersJson};
        allAnswersJson.push(answerTypeJson);

        answerTypeNode.querySelectorAll("input").forEach(answerNode => {
            answersJson.push({"text": answerNode.value});
        });
    }

    await makeAPIRequest("admin/setNpc", {"npc": data, "lang": "FR"}, {"content": "json"});
    await uploadReactionsDelta();

    alert("Opération effectuée avec succès");
}

async function uploadReactionsDelta() {
    const requests = [];
    const npcId = document.querySelector("#npc_id").value;

    for (const [traitId, reactionNode] of Object.entries(reactionsDelta)) {
        const formData = new FormData();
        formData.append("npc_id", npcId);
        formData.append("trait_id", traitId);
        
        if (reactionNode === null) {
            formData.append("file", "null");
        } else {
            const file = reactionNode.querySelector(".img_input").files[0];
            formData.append("file", file ? file : "");
        }

        requests.push(makeAPIRequest("admin/setReaction", formData, {"content": "form"}));
    }

    for (const request of requests) {
        await request;
    }
}

async function deleteNpc() {
    if (!confirm("Voulez-vous vraiment supprimer ce personnage ?")) {
        return;
    }

    const npcId = document.querySelector("#npc_id").value;
    await makeAPIRequest("admin/deleteNpc", {"npc_id": npcId, "lang": "FR"}, {"content": "json"});
    alert("Opération effectuée avec succès");
    document.location = "/admin";
}

function changeImageReaction(imageInputElement) {
    const parentNode = imageInputElement.parentNode;
    const imgNode = parentNode.querySelector('img');
    const traitId = parentNode.querySelector('.trait_id').value;
    
    const reader = new FileReader();
    reader.addEventListener("load", event => {
        imgNode.src = event.target.result
    });
    reader.readAsDataURL(imageInputElement.files[0]);

    reactionsDelta[traitId] = parentNode;
}

function deleteImageReaction(reactionDeletionButton) {
    if (!confirm("Voulez-vous vraiment supprimer l'image de cette réaction ?")) {
        return;
    }

    const reactionNode = reactionDeletionButton.parentNode;
    const traitId = reactionNode.querySelector(".trait_id").value;
    const reactionName = reactionNode.querySelector(".reaction_name").innerText;

    reactionNode.parentNode.removeChild(reactionNode);
    
    const option = document.createElement("option");
    option.value = traitId;
    option.innerText = reactionName;

    const addReactionsSelectorElement = document.getElementById("add_reactions_selector");
    if (addReactionsSelectorElement === null) {
        // No add_reactions_selector element, this should never happen
        // Do nothing in this case
        return;
    }

    addReactionsSelectorElement.appendChild(option);

    reactionsDelta[traitId] = null;
}

function addReaction(addReactionsSelectorElement) {
    const selectedOptionNode = addReactionsSelectorElement.selectedOptions[0];
    
    const traitId = selectedOptionNode.value;
    const reactionName = selectedOptionNode.innerText;

    addReactionsSelectorElement.removeChild(selectedOptionNode);

    const newReactionElement = document.createElement("section");
    newReactionElement.classList.add("reaction");

    const reactionNameElement = document.createElement("h3");
    reactionNameElement.classList.add("reaction_name");
    reactionNameElement.textContent = reactionName;

    newReactionElement.appendChild(reactionNameElement);

    const imageElement = document.createElement("img");
    imageElement.classList.add("reaction_image");
    imageElement.setAttribute("alt", "Image d'une réaction d'un personnage");
    imageElement.src = "/static/images/no_photography_white.svg";

    newReactionElement.appendChild(imageElement);

    const imageInputElement = document.createElement("input");
    imageInputElement.classList.add("img_input");
    imageInputElement.setAttribute("type", "file");
    imageInputElement.setAttribute("accept", "image/png, image/jpg, image/jpeg");
    imageInputElement.addEventListener("change", () => changeImageReaction(imageInputElement));

    newReactionElement.appendChild(imageInputElement);

    const traitIdInputElement = document.createElement("input");
    traitIdInputElement.classList.add("trait_id");
    traitIdInputElement.setAttribute("type", "hidden");
    traitIdInputElement.setAttribute("value", traitId);

    newReactionElement.appendChild(traitIdInputElement);

    const buttonElement = document.createElement("button");
    buttonElement.classList.add("delete_question_btn", "action_button", "short_color_transition");
    buttonElement.setAttribute("title", "Cliquez ici pour supprimer l'image de cette réaction");
    buttonElement.addEventListener("click", () => deleteImageReaction(buttonElement));

    const svgElement = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svgElement.classList.add("action_icon", "short_color_transition");
    svgElement.setAttribute("viewBox", "0 0 48 48");

    const pathElement = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pathElement.setAttribute("d",
        "M12.45 38.7 9.3 35.55 20.85 24 9.3 12.5l3.15-3.2L24 20.8 35.55 9.3l3.15 3.2L27.2 24l11.5 11.55-3.15 3.15L24 27.2Z");

    svgElement.appendChild(pathElement);

    buttonElement.appendChild(svgElement);
    buttonElement.appendChild(document.createTextNode("Supprimer l'image de la réaction"));

    newReactionElement.appendChild(buttonElement);

    const reactionsElement = document.getElementById("reactions");
    if (reactionsElement === null) {
        // No add_reactions_selector element, this should never happen
        // Do nothing in this case
        return;
    }

    reactionsElement.appendChild(newReactionElement);

    reactionsDelta[traitId] = newReactionElement;
}

function setListenersToImageInputs() {
    for (const imageInput of document.getElementsByClassName("img_input")) {
        imageInput.addEventListener("change", () => changeImageReaction(imageInput));
    }
}

function setListenersToImageReactionsRemovalButtons() {
    for (const imageReactionRemovalButton of document.getElementsByClassName("delete_image_reaction_btn")) {
        imageReactionRemovalButton.addEventListener("click", () => deleteImageReaction(imageReactionRemovalButton));
    }
}

function setListenersToAddReactionsSelector() {
    const addReactionsSelectorElement = document.getElementById("add_reactions_selector");
    if (addReactionsSelectorElement === null) {
        // No add_reactions_selector element, this should never happen
        // Do nothing in this case
        return;
    }

    addReactionsSelectorElement.addEventListener("change", () => addReaction(addReactionsSelectorElement));
}

setListenersToImageReactionsRemovalButtons();
setListenersToImageInputs();
setListenersToAddReactionsSelector();
