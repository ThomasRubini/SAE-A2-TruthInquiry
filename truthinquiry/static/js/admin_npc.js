
const reactionsDelta = {}

async function createOrUpdateNpc() {
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

    await makeAPIRequest("admin/setNpc", {"npc": data, "lang": "FR"}, {"content": "json"});

    await uploadReactionsDelta();

    alert("Opération effectuée avec succès");
}

async function uploadReactionsDelta() {
    let requests = [];


    for(const [traitId, reactionNode] of Object.entries(reactionsDelta)){
        const formData = new FormData();
        formData.append("npc_id", npc_id.value);
        formData.append("trait_id", traitId);
        
        if(reactionNode === null) formData.append("file", "null");
        else{
            const file = reactionNode.querySelector(".img_input").files[0]
            formData.append("file", file ? file : "");
        }

        requests.push(makeAPIRequest("admin/setReaction", formData, {"content": "form"}));
    }

    for(request of requests){
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

function changeReaction(inputNode){
    const parentNode = inputNode.parentNode;
    const imgNode = parentNode.querySelector('img');
    const traitId = parentNode.querySelector('.trait_id').value;
    
    const reader = new FileReader();
    reader.onload = (e)=>{
        imgNode.src = e.target.result
    }
    reader.readAsDataURL(inputNode.files[0]);

    reactionsDelta[traitId] = parentNode;
}

function deleteReaction(node){
    const reactionNode = node.parentNode;
    const traitId = reactionNode.querySelector(".trait_id").value;
    const reactionName = reactionNode.querySelector("p").innerText;

    reactionNode.parentNode.removeChild(reactionNode);
    
    const option = document.createElement("option");
    option.value = traitId
    option.innerText = reactionName

    reactions_to_add.appendChild(option);

    reactionsDelta[traitId] = null;
}

function addReaction(selectNode){
    const selectedOptionNode = selectNode.selectedOptions[0];
    
    const traitId = selectedOptionNode.value;
    const reactionName = selectedOptionNode.innerText;

    selectNode.removeChild(selectedOptionNode);

    const newReaction = reactions.querySelector("div").cloneNode(true);
    newReaction.querySelector("img").src = "";
    newReaction.querySelector(".img_input").value = null;
    newReaction.querySelector(".trait_id").value = traitId
    newReaction.querySelector("p").innerText = reactionName
    
    reactions.appendChild(newReaction);

    reactionsDelta[traitId] = newReaction;
}