var npcs_ids = []
var gamedata = {}
var button = ""
async function showAnswerSelectionPanel() {
    npcs_ids.forEach(async element => {
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
        let button = document.getElementById("mainButton");
        let button_clone = button.cloneNode(true);
        button_clone.classList.remove("hidden");
        suspect.appendChild(button_clone);
        document.getElementById("culprits_choices").appendChild(suspect);
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

function setGameData(){
    data = {};
    response = makeAPIRequest("getGameData");
    response.then((value) => {
        gamedata = value["gamedata"];
        npcs_ids = Object.keys(gamedata["npcs"]);
    })
}

setGameData()