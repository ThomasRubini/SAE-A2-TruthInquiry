function createOrUpdateNpc() {
    const data = {};
    data["id"] = document.querySelector("#npc_id").value;
    data["name"] = document.querySelector("#npc_name").value;
    
    const allAnswersJson = [];
    data["allAnswers"] = allAnswersJson;
    
    for (let answerTypeNode of document.querySelector(".answer_groups").children) {
        const answersJson = [];
        const answerTypeJson = {"answers": answersJson};
        allAnswersJson.push(answerTypeJson);

        answerTypeNode.querySelectorAll("input").forEach(answerNode => {
            answersJson.push({"text": answerNode.value});
        });
    }

    makeAPIRequest("admin/setNpc", {"npc": data, "lang": "FR"}, {"content": "json"}).then(() => {
        alert("Opération effectuée avec succès");
    });
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

function changeReaction(inputNode){
    const parentNode = inputNode.parentNode;
    const imgNode = parentNode.querySelector('img');
    
    const reader = new FileReader();
    reader.onload = (e)=>{
        imgNode.src = e.target.result
    }
    reader.readAsDataURL(inputNode.files[0]);
}

function deleteReaction(node){
    const reactionNode = node.parentNode;
    const reactionId = reactionNode.querySelector(".reaction_id").value;
    const reactionName = reactionNode.querySelector("p").innerText;

    reactionNode.parentNode.removeChild(reactionNode);
    
    const option = document.createElement("option");
    option.value = reactionId
    option.innerText = reactionName

    reactions_to_add.appendChild(option);
}

function addReaction(selectNode){
    const selectedOptionNode = selectNode.selectedOptions[0];
    
    const reactionId = selectedOptionNode.value;
    const reactionName = selectedOptionNode.innerText;

    selectNode.removeChild(selectedOptionNode);

    const newReaction = reactions.querySelector("div").cloneNode(true);
    newReaction.querySelector("img").src = "";
    newReaction.querySelector(".img_input").value = null;
    newReaction.querySelector(".reaction_id").value = reactionId
    newReaction.querySelector("p").innerText = reactionName
    
    reactions.appendChild(newReaction);
}