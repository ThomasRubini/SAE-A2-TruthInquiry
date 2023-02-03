const intro_image_path = "/static/images/entrée-manoir.png";
const interrogation_image_path = "/static/images/salle-interrogation.png";
const results_image_path = "/static/images/salle-resultats.png";

var npcs_ids = [];
var gamedata = {};
var currentNpc = null;
var username = null;

function show(className) {
    document.getElementsByClassName(className)[0].classList.remove("hidden");
}

function hide(className) {
    document.getElementsByClassName(className)[0].classList.add("hidden");
}

function setGameBackground(backgroundPath) {
    document.getElementsByClassName("current_background")[0].style.backgroundImage = 'url("' + backgroundPath +'")';
}

function setListenerToIntroductionNextBtn() {
    document.getElementById("introduction_next_btn").addEventListener("click", showInterogationViewFromIntroduction);
}

function setListenerToInterrogationSuspectPreviousBtn() {
    document.getElementById("interrogation_suspect_previous_btn").addEventListener("click", goBackToInterogation);
}

function setListenerToInterrogationNextBtn() {
    document.getElementById("interrogation_next_btn").addEventListener("click", showEmotionAndCulpritChoicesView);
}

function setQuestionButtonsListeners() {
    document.getElementById("QA_0").addEventListener("click", askTypeZeroQuestion);
    document.getElementById("QA_1").addEventListener("click", askTypeOneQuestion);
}

function removeQuestionButtonsListeners() {
    document.getElementById("QA_0").removeEventListener("click", askTypeZeroQuestion);
    document.getElementById("QA_1").removeEventListener("click", askTypeOneQuestion);
}

function goBackToInterogation() {
    hide("interrogation_suspect");
    show("interrogation");
}

function showInterogationViewFromIntroduction() {
    hide("introduction");
    show("interrogation");
    setGameBackground(interrogation_image_path);
}

function showEmotionAndCulpritChoicesView() {
    hide("interrogation");
    show("emotion_and_culprit_choices");
}

function getNpcLocationAndPartner(npcid) {
    data = {};
    npcid = parseInt(npcid);

    for (const room in gamedata["rooms"]) {
        if (gamedata["rooms"][room]["npcs"].includes(npcid)) {
            data["room"] = gamedata["rooms"][room]["name"];

            if (gamedata["rooms"][room]["npcs"].length === 1) {
                do {
                    const random = Math.floor(Math.random() * npcs_ids.length);
                    data["partner"] = npcs_ids[random];
                } while (data["partner"] === npcid);
            } else {
                data["partner"] = gamedata["rooms"][room]["npcs"][gamedata["rooms"][room]["npcs"][1] === npcid ? 0 : 1];
            }
        }
    }

    return data;
}

function disableCulpritButtons(culprit_choices_element, selected_suspect) {
    let childrenCulpritChoicesElement = culprit_choices_element.children;
    for (let index = 0; index < childrenCulpritChoicesElement.length; index++) {
        let child = childrenCulpritChoicesElement[index];
        if (selected_suspect != child) {
            child.getElementsByClassName("culprit_btn")[0].classList.add("hidden");
        } else {
            child.getElementsByClassName("culprit_unchecked_icon")[0].classList.add("hidden");
            child.getElementsByClassName("culprit_checked_icon")[0].classList.remove("hidden");
            child.getElementsByClassName("culprit_btn")[0].classList.add("culprit_btn_checked");
        }
    }
}

function getCulprit() {
    culprit = null;
    Object.values(gamedata["rooms"]).forEach(element => {
        if (element['npcs'].length === 1) {
            culprit = element['npcs'][0];
            return;  
        } 
    });

    return culprit;
}

async function askTypeOneQuestion() {
    removeQuestionButtonsListeners();
    partnerId = getNpcLocationAndPartner(currentNpc)["partner"];
    anwser = gamedata["npcs"][currentNpc]["QA_1"];
    anwser = anwser.replace("{NPC}",gamedata["npcs"][partnerId]["name"]);
    document.getElementsByClassName("suspect_answer")[0].textContent = anwser;
    show("question_answer");
    document.getElementById("currentNpcPicure").src = "/api/v1//getNpcReaction?npcid="+currentNpc;
    // Sleep for 5 sec
    await new Promise(r => setTimeout(r, 2000));
    document.getElementById("currentNpcPicure").src = "/api/v1/getNpcImage?npcid="+currentNpc;
    hide("question_answer");
    document.getElementsByClassName("suspect_answer")[0].textContent = "";
    setQuestionButtonsListeners();
}


async function askTypeZeroQuestion() {
    removeQuestionButtonsListeners();
    room = getNpcLocationAndPartner(currentNpc)["room"];
    anwser = gamedata["npcs"][currentNpc]["QA_0"];
    anwser = anwser.replace("{SALLE}",room);
    document.getElementsByClassName("suspect_answer")[0].textContent = anwser;
    show("question_answer");
    document.getElementById("currentNpcPicure").src = "/api/v1//getNpcReaction?npcid="+currentNpc;
    // Sleep for 5 sec
    await new Promise(r => setTimeout(r, 5000));
    document.getElementById("currentNpcPicure").src = "/api/v1/getNpcImage?npcid="+currentNpc;
    hide("question_answer");
    document.getElementsByClassName("suspect_answer")[0].textContent = "";
    setQuestionButtonsListeners();
}

async function sendAnswers() {
    selects = document.getElementsByClassName("suspect_emotion_chooser");
    let playerResponses = {};
    for (let index = 0; index < selects.length; index++) {
        select = selects[index];
        playerResponses[select.id] = select.value;
    }

    data = {};
    data["responses"] = JSON.stringify(playerResponses);
    return await makeAPIRequest("submitAnswers", data);
}

function renderAnswerSelectionPanel() {
    npcs_ids.forEach(element => {
        let suspect = document.createElement("div");
        suspect.classList.add("suspect");

        suspect_emotion_chooser = document.createElement("select");
        suspect_emotion_chooser.classList.add("suspect_emotion_chooser")
        suspect_emotion_chooser.setAttribute("id", element);
        gamedata["traits"].forEach(trait =>{
            let option = document.createElement("option");
            option.value = trait;
            option.text = trait;
            suspect_emotion_chooser.appendChild(option);
        });

        suspect.appendChild(suspect_emotion_chooser);

        let img = document.createElement('img');
        img.classList.add("suspect_picture");
        img.src = "/api/v1/getNpcImage?npcid=" + element;
        suspect.appendChild(img);

        let button = document.getElementById("culpritButton");
        let button_clone = button.cloneNode(true);
        let culprit_choices = document.getElementById("culprits_choices");

        button_clone.addEventListener("click", () => {
            disableCulpritButtons(culprit_choices, suspect);
            sendAnswers();
        });

        button_clone.removeAttribute("id");
        button_clone.classList.remove("hidden");
        suspect.appendChild(button_clone);
        culprit_choices.appendChild(suspect);
    });
}

function renderInterogation() {
    document.getElementById("QA_0").textContent = gamedata["questions"]["QA_0"],
    document.getElementById("QA_1").textContent = gamedata["questions"]["QA_1"],
    npcs_ids.forEach(element => {
        let suspect = document.createElement("div");
        suspect.classList.add("suspect");

        let img = document.createElement('img');
        img.classList.add("suspect_picture");
        img.src = "/api/v1/getNpcImage?npcid=" + element;
        suspect.appendChild(img);

        let button = document.getElementById("interogationButton");
        let button_clone = button.cloneNode(true);
        button_clone.classList.remove("hidden");
        button_clone.addEventListener("click", () => {
            // TODO remove this listener when we know the questions has already been asked;
            currentNpc = element
            document.getElementById("currentNpcPicure").src = "/api/v1/getNpcImage?npcid="+element;
            hide("interrogation");
            show("interrogation_suspect");
        });

        suspect.appendChild(button_clone);
        document.getElementById("interrogation_suspects").appendChild(suspect);
    });
}

function initSock(){
    socket = io({
        auth : {
            game_id: gamedata["game_id"]
        }
    });

    socket.on("connect", () => {
        console.log("Connected !")
    })

    //TODO Send and receive userprogress when they have sent their responses
    socket.on("gameprogress", (username) => {
        console.log(username);
    });
    
    socket.on("gamefinished", (finalResults) => {
        hide("emotion_and_culprit_choices");
        document.getElementsByClassName("reveal_score")[0].textContent = Object.values(finalResults["player"][username]).filter(x => x == true).length + "/5";
        for (const player in finalResults["player"]){
            if (player === username) {
                continue;
            }

            let playerNode = document.createElement("h3");
            playerNode.classList.add("player_name_and_score");

            let playerResultArray = Object.values(finalResults["player"][player]);
            playerNode.textContent = "" + player + " : " + playerResultArray.filter(x => x == true).length;

            document.getElementsByClassName("players_list")[0].appendChild(playerNode);
        }

        culprit = getCulprit();
        document.getElementsByClassName("reveal_culprit_title")[0].textContent += " " + gamedata["npcs"][culprit]["name"];
        document.getElementById("culprit").src = "/api/v1/getNpcImage?npcid="+culprit;

        show("results_game");
        setGameBackground(results_image_path);

        npcs_ids.filter(x => x != culprit).forEach(npcid =>{
            let suspect = document.createElement("div");
            suspect.classList.add("summary_suspect");
            let img = document.createElement("img")
            img.src = "/api/v1/getNpcImage?npcid=" + npcid;
            suspect.appendChild(img)

            let emotionTitle = document.createElement("h2");
            emotionTitle.classList.add("explain_suspect_emotion_title");
            emotionTitle.textContent = "Ce suspect était " + finalResults["npcs"][npcid]["reaction"];
            suspect.appendChild(emotionTitle);

            let emotionDesc = document.createElement("p");
            emotionDesc.classList.add("explain_suspect_emotion_description");
            emotionDesc.textContent = "Qui se caractérise par " + finalResults["npcs"][npcid]["description"];
            suspect.appendChild(emotionDesc)

            document.getElementsByClassName("suspects_list")[0].appendChild(suspect)
        })
    });
}

async function setGameData() {
    data = {};
    response = await makeAPIRequest("getGameData");
    gamedata = response["gamedata"];
    username = response["username"];
    npcs_ids = Object.keys(gamedata["npcs"]).sort((a, b) => 0.5 - Math.random())
}

async function initGame() {
    await setGameData();
    initSock();
    renderAnswerSelectionPanel();
    renderInterogation();
    setQuestionButtonsListeners()
    setListenerToInterrogationSuspectPreviousBtn()
    setListenerToIntroductionNextBtn()
    setListenerToInterrogationNextBtn();
    show("introduction");
    setGameBackground(intro_image_path);
}

initGame();