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