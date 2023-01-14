var npcs_ids = []
var gamedata = {}
var button = ""

function showInterogation(){
    document.getElementsByClassName("interrogation")[0].classList.remove("hidden");
}
function hideInterogation(){
    document.getElementsByClassName("interrogation")[0].classList.add("hidden");
}

function showEmotionAndCulpritChoices(){
    document.getElementsByClassName("emotion_and_culprit_choices")[0].classList.remove("hidden");
}
function hideEmotionAndCulpritChoices(){
    document.getElementsByClassName("emotion_and_culprit_choices")[0].classList.add("hidden");
}

function setListenerToInterrogationNextBtn(){
    document.getElementById("interrogation_next_btn").addEventListener("click", showInterogationView)
}

function showInterogationView(){
    hideInterogation();
    showEmotionAndCulpritChoices();
}

function renderAnswerSelectionPanel() {
    npcs_ids.forEach(element => {
        console.log(element);
        let suspect = document.createElement("div");
        suspect.classList.add("suspect");

        suspect_emotion_chooser = document.createElement("select");
        suspect_emotion_chooser.classList.add("suspect_emotion_chooser")
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
        button_clone.classList.remove("hidden");
        suspect.appendChild(button_clone);
        document.getElementById("culprits_choices").appendChild(suspect);
    });
}

function renderInterogation(){
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
        suspect.appendChild(button_clone)
        document.getElementById("interrogation_suspects").appendChild(suspect);
    });
}

function initSock(){
    socket = io({
        auth:{
            game_id: gameid
        }
    });

    socket.on("connect", () => {
        console.log("Connected !")
    })

    socket.on("gameprogress", (username) => {
        console.log(username);
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
    //initSock();
    renderAnswerSelectionPanel();
    renderInterogation();
    setListenerToInterrogationNextBtn();
    showInterogation();
}

initGame();