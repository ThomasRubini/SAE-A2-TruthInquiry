var npcs_ids = []
var gamedata = {}
var currentNpc = null


function show(className){
    document.getElementsByClassName(className)[0].classList.remove("hidden");
}

function hide(className){
    document.getElementsByClassName(className)[0].classList.add("hidden");
}

function setListenerToIntroductionNextBtn(){
    document.getElementById("introduction_next_btn").addEventListener("click", showInterogationViewFromIntroduction);
}

function setListenerToInterrogationSuspectPreviousBtn(){
    document.getElementById("interrogation_suspect_previous_btn").addEventListener("click",goBackToInterogation)
}

function setListenerToInterrogationNextBtn(){
    document.getElementById("interrogation_next_btn").addEventListener("click", showEmotionAndCulpritChoicesView)
}

function goBackToInterogation(){
    hide("interrogation_suspect");
    show("interrogation");
}


function showInterogationViewFromIntroduction(){
    hide("introduction");
    show("interrogation");
}

function showEmotionAndCulpritChoicesView(){
    hide("interrogation");
    show("emotion_and_culprit_choices");
}

function getNpcLocationAndPartner(npcid){
    data = {}
    npcid = parseInt(npcid)
    for(const room in gamedata["rooms"]){
        if(gamedata["rooms"][room]["npcs"].includes(npcid)){
            data["room"] = gamedata["rooms"][room]["name"];
            if(gamedata["rooms"][room]["npcs"].length === 1){
                do{
                    const random = Math.floor(Math.random() * npcs_ids.length);
                    data["partner"] = npcs_ids[random]
                }while(data["partner"] === npcid);
            }
            else{
                data["partner"] = gamedata["rooms"][room]["npcs"][gamedata["rooms"][room]["npcs"][1] === npcid ?0:1];
            }
        }
    }
    return data;
}

async function askTypeOneQuestion(){
    partnerId = getNpcLocationAndPartner(currentNpc)["partner"];
    anwser = gamedata["npcs"][currentNpc]["QA_1"];
    anwser = anwser.replace("{NPC}",gamedata["npcs"][partnerId]["name"]);
    document.getElementsByClassName("suspect_answer")[0].textContent = anwser;
    show("question_answer");
    document.getElementById("currentNpcPicure").src = "/api/v1//getNpcReaction?npcid="+currentNpc;
    //sleep for 5 sec
    await new Promise(r => setTimeout(r, 5000));
    document.getElementById("currentNpcPicure").src = "/api/v1/getNpcImage?npcid="+currentNpc;
    hide("question_answer");
    document.getElementsByClassName("suspect_answer")[0].textContent = "";
}


async function askTypeZeroQuestion(){
    room = getNpcLocationAndPartner(currentNpc)["room"];
    anwser = gamedata["npcs"][currentNpc]["QA_0"];
    anwser = anwser.replace("{SALLE}",room);
    document.getElementsByClassName("suspect_answer")[0].textContent = anwser;
    show("question_answer");
    document.getElementById("currentNpcPicure").src = "/api/v1//getNpcReaction?npcid="+currentNpc;
    //sleep for 5 sec
    await new Promise(r => setTimeout(r, 5000));
    document.getElementById("currentNpcPicure").src = "/api/v1/getNpcImage?npcid="+currentNpc;
    hide("question_answer");
    document.getElementsByClassName("suspect_answer")[0].textContent = "";
}

async function sendAnswers(){
    selects = document.getElementsByClassName("suspect_emotion_chooser");
    let playerResponses = {}
    for (let index = 0; index < selects.length; index++) {
        select = selects[index];
        playerResponses[select.id] = select.value
    }
    data = {};
    data["responses"] = JSON.stringify(playerResponses);
    return await makeAPIRequest("submitAnswers",data);
}

function renderAnswerSelectionPanel() {
    npcs_ids.forEach(element => {
        let suspect = document.createElement("div");
        suspect.classList.add("suspect");

        suspect_emotion_chooser = document.createElement("select");
        suspect_emotion_chooser.classList.add("suspect_emotion_chooser")
        suspect_emotion_chooser.setAttribute("id",element);
        gamedata["traits"].forEach(trait =>{
            let option = document.createElement("option");
            option.value = trait;
            option.text = trait;
            suspect_emotion_chooser.appendChild(option);
        });
        suspect.appendChild(suspect_emotion_chooser);
        let data = {};
        let img = document.createElement('img');
        img.classList.add("suspect_picture");
        img.src = "/api/v1/getNpcImage?npcid="+element; 
        suspect.appendChild(img);
        let button = document.getElementById("culpritButton");
        let button_clone = button.cloneNode(true);
        button_clone.removeAttribute("id");
        button_clone.classList.remove("hidden");
        suspect.appendChild(button_clone);
        document.getElementById("culprits_choices").appendChild(suspect);
    });
}

function renderInterogation(){
    document.getElementById("QA_0").textContent = gamedata["questions"]["QA_0"],
    document.getElementById("QA_1").textContent = gamedata["questions"]["QA_1"],
    npcs_ids.forEach(element => {
        let suspect = document.createElement("div");
        suspect.classList.add("suspect");

        let img = document.createElement('img');
        img.classList.add("suspect_picture");
        img.src = "/api/v1/getNpcImage?npcid="+element; 
        suspect.appendChild(img);
        let button = document.getElementById("interogationButton");
        let button_clone = button.cloneNode(true);
        button_clone.classList.remove("hidden");
        button_clone.addEventListener("click",()=>{
            currentNpc = element
            document.getElementById("currentNpcPicure").src = "/api/v1/getNpcImage?npcid="+element;
            hide("interrogation");
            show("interrogation_suspect");
        })
        suspect.appendChild(button_clone)
        document.getElementById("interrogation_suspects").appendChild(suspect);
    });
}

function initSock(){
    socket = io({
        auth:{
            game_id: gamedata["game_id"]
        }
    });

    socket.on("connect", () => {
        console.log("Connected !")
    })

    socket.on("gameprogress", (username) => {
        console.log(username);
    });
    
    socket.on("gamefinshed", (finalResults) => {
        console.log(finalResults);
    });
}

async function setGameData(){
    data = {};
    response = await makeAPIRequest("getGameData");
    gamedata = response["gamedata"];
    npcs_ids = Object.keys(gamedata["npcs"]);
}

async function initGame(){
    await setGameData();
    initSock();
    renderAnswerSelectionPanel();
    renderInterogation();
    setListenerToInterrogationSuspectPreviousBtn()
    setListenerToIntroductionNextBtn()
    setListenerToInterrogationNextBtn();
    show("introduction");
}
initGame();