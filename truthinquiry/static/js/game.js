const INTRO_IMAGE_PATH = "/static/images/entrée-manoir.png";
const INTERROGATION_IMAGE_PATH = "/static/images/salle-interrogation.png";
const RESULTS_IMAGE_PATH = "/static/images/salle-resultats.png";
const NPC_REACTION_PATH = "/api/v1/getNpcReaction?npcid=";
const NPC_IMAGE_PATH = "/api/v1/getNpcImage?npcid=";

let npcsIds = [];
let gameData = {};
let currentNpc = null;
let username = null;

/*
 * Set the current game background to the first element with the current_background CSS class.
 */
function setGameBackground(backgroundPath) {
    document.querySelector(".current_background").style.backgroundImage = 'url("' + backgroundPath + '")';
}

/**
 * Set listeners to introduction and interrogation navigation buttons.
 */
function setIntroductionAndInterrogationListeners() {
    document.getElementById("introduction_next_btn")
        .addEventListener("click", showInterrogationViewFromIntroduction);
    document.getElementById("interrogation_suspect_previous_btn")
        .addEventListener("click", goBackToInterrogation);
    document.getElementById("interrogation_next_btn")
        .addEventListener("click", showEmotionAndCulpritChoicesView);
}

/**
 * Set listeners to questions buttons.
 */
function setQuestionButtonsListeners() {
    document.getElementById("QA_0")
        .addEventListener("click", askTypeZeroQuestion);
    document.getElementById("QA_1")
        .addEventListener("click", askTypeOneQuestion);
}

/**
 * Unset listeners to questions buttons.
 */
function unsetQuestionButtonsListeners() {
    document.getElementById("QA_0")
        .removeEventListener("click", askTypeZeroQuestion);
    document.getElementById("QA_1")
        .removeEventListener("click", askTypeOneQuestion);
}

/**
 * Go back to interrogation view, by hiding the interrogation suspect view.
 */
function goBackToInterrogation() {
    hideFirstClassElement("interrogation_suspect");
    showFirstClassElement("interrogation");
}

/**
 * Show the interrogation view from the introduction one and hide the interrogation one.
 */
function showInterrogationViewFromIntroduction() {
    hideFirstClassElement("introduction");
    showFirstClassElement("interrogation");
    setGameBackground(INTERROGATION_IMAGE_PATH);
}

/**
 * Show the emotion and culprit choices view and hide the interrogation one.
 */
function showEmotionAndCulpritChoicesView() {
    hideFirstClassElement("interrogation");
    showFirstClassElement("emotion_and_culprit_choices");
}

/**
 * Parse the gamedata object to retreive the room in which the npc passed as parameter is
 * located and the second npc located in the same room. When the passed npc is alone in the
 * room, a npc is choosen at random as the returned partener
 */
function getNpcLocationAndPartner(npcid) {
    const data = {};
    const npcidInt = parseInt(npcid);

    for (const room in gameData["rooms"]) {
        if (gameData["rooms"][room]["npcs"].includes(npcidInt)) {
            data["room"] = gameData["rooms"][room]["name"];

            if (gameData["rooms"][room]["npcs"].length === 1) {
                do {
                    const random = Math.floor(Math.random() * npcsIds.length);
                    data["partner"] = npcsIds[random];
                } while (data["partner"] === npcidInt);
            } else {
                data["partner"] = gameData["rooms"][room]["npcs"]
                    [gameData["rooms"][room]["npcs"][1] === npcidInt ? 0 : 1];
            }
        }
    }

    return data;
}

/**
 * Parse the gamedata object to retreive the room in which the npc passed as parameter is
 * located and the second npc located in the same room. When the passed npc is alone in the
 * room, a npc is choosen at random as the returned partener
 */
function disableCulpritButtons(culprit_choices_element, selected_suspect) {
    let childrenCulpritChoicesElement = culprit_choices_element.children;

    for (let index = 0; index < childrenCulpritChoicesElement.length; index++) {
        let child = childrenCulpritChoicesElement[index];

        if (selected_suspect != child) {
            child.querySelector(".culprit_btn").classList.add("hidden");
        } else {
            child.querySelector(".culprit_unchecked_icon").classList.add("hidden");
            child.querySelector(".culprit_checked_icon").classList.remove("hidden");
            child.querySelector(".culprit_btn").classList.add("culprit_btn_checked");
        }
    }
}

/**
 * Return the npc designed as the "culprit" of the crime, the culprit
 * is determined by being the only npc alone in a room.
 */
function getCulprit() {
    let culprit = null;

    Object.values(gameData["rooms"]).forEach(room => {
        if (room['npcs'].length === 1) {
            culprit = room['npcs'][0];
            return;  
        } 
    });

    return culprit;
}

/**
 * handler for the function call "askQuestion" for a type_zero question
 * also known as "Where were you ?"
 */
async function askTypeZeroQuestion() {
    askQuestion(npcLocationAndPartner => gameData["npcs"][currentNpc]["QA_0"].replace(
        "{SALLE}", npcLocationAndPartner["room"]));
}

/**
 * handler for the function call "askQuestion" for a type_one question
 * also known as "With who were you with ?"
 */
async function askTypeOneQuestion() {
    askQuestion(npcLocationAndPartner => gameData["npcs"][currentNpc]["QA_1"].replace(
        "{NPC}", gameData["npcs"][npcLocationAndPartner["partner"]]["name"]));
}

/**
 * This function primary goal is to display the answer to the question the player
 * asked to a npc. 
 * It parses the gamedata object to retreive the answer of the npc
 * and fill the variables left in the string accordingly to the type of the question.
 * Then it fetches the reacion of the npc and diplays it all.
 */
async function askQuestion(buildAnswer) {
    unsetQuestionButtonsListeners();

    document.querySelector(".suspect_answer").textContent = buildAnswer(
        getNpcLocationAndPartner(currentNpc));

    showFirstClassElement("question_answer");

    document.getElementById("currentNpcPicure").src = NPC_REACTION_PATH + currentNpc;

    //TODO: change this code which produces strange behaviors
    // Sleep for 4 sec
    await new Promise(r => setTimeout(r, 4000));

    document.getElementById("currentNpcPicure").src = NPC_REACTION_PATH + currentNpc;
    hideFirstClassElement("question_answer");

    document.querySelector(".suspect_answer").textContent = "";

    setQuestionButtonsListeners();
}

/**
 * This function sends the player's answers to the server
 */
async function sendAnswers() {
    const selections = document.getElementsByClassName("suspect_emotion_chooser");

    const playerResponses = {};

    for (let index = 0; index < selections.length; index++) {
        select = selections[index];
        playerResponses[select.id] = select.value;
    }

    const data = {};
    data["responses"] = JSON.stringify(playerResponses);
    return await makeAPIRequest("submitAnswers", data);
}

/**
 * Show the screen in which the player fill the emotion of each npc
 * then decide on which npc is the culprit.
 */
function renderAnswerSelectionPanel() {
    npcsIds.forEach(element => {
        const suspect = document.createElement("div");
        suspect.classList.add("suspect");

        const suspectEmotionChooser = document.createElement("select");
        suspectEmotionChooser.classList.add("suspect_emotion_chooser")
        suspectEmotionChooser.setAttribute("id", element);

        gameData["traits"].forEach(trait => {
            const option = document.createElement("option");
            option.value = trait;
            option.text = trait;
            suspectEmotionChooser.appendChild(option);
        });

        suspect.appendChild(suspectEmotionChooser);

        const img = document.createElement('img');
        img.classList.add("suspect_picture");
        img.src = NPC_IMAGE_PATH + element;
        suspect.appendChild(img);

        const button = document.createElement("button");
        button.classList.add("culprit_btn", "action_button");
        button.innerHTML = '<svg class="culprit_checked_icon hidden culprit_icon" xmlns="http://www.w3.org/2000/svg" viewbox="0 0 48 48"><path d="M18.9 36.75 6.65 24.5l3.3-3.3 8.95 9L38 11.1l3.3 3.25Z"></path></svg><svg class="culprit_unchecked_icon culprit_icon" xmlns="http://www.w3.org/2000/svg" viewbox="0 0 48 48"><path d="M12.45 38.7 9.3 35.55 20.85 24 9.3 12.5l3.15-3.2L24 20.8 35.55 9.3l3.15 3.2L27.2 24l11.5 11.55-3.15 3.15L24 27.2Z"></svg><p class="culprit_btn_text">Couplable</p>';

        const culpritChoices = document.getElementById("culprits_choices");

        button.addEventListener("click", () => {
            disableCulpritButtons(culpritChoices, suspect);
            sendAnswers();
        });

        suspect.appendChild(button);
        culpritChoices.appendChild(suspect);
    });
}

/**
 * Show the screen in which the player asks auestions to the npcs
 */
function renderInterrogation() {
    document.getElementById("QA_0").textContent = gameData["questions"]["QA_0"];
    document.getElementById("QA_1").textContent = gameData["questions"]["QA_1"];

    const interrogationSuspects = document.getElementById("interrogation_suspects");

    npcsIds.forEach(element => {
        const suspect = document.createElement("div");
        suspect.classList.add("suspect");

        const img = document.createElement('img');
        img.classList.add("suspect_picture");
        img.src = NPC_IMAGE_PATH + element;
        suspect.appendChild(img);

        const button = document.createElement("button");
        button.classList.add("ask_button", "action_button");
        button.textContent = "Interroger";
        button.addEventListener("click", () => {
            // TODO remove this listener when we know the questions has already been asked;
            currentNpc = element;
            document.getElementById("currentNpcPicure").src = NPC_IMAGE_PATH + element;
            hideFirstClassElement("interrogation");
            showFirstClassElement("interrogation_suspect");
        });

        suspect.appendChild(button);
        interrogationSuspects.appendChild(suspect);
    });
}


/**
 * Initialize the websocket for this page, its primary use is to
 * show the final page once it receive the event that all player have finished
 * it parses the payload send by the server containing the other players
 * nicknames and scores.
 */
function initSock() {
    const socket = io({
        auth : {
            game_id: gameData["game_id"]
        }
    });

    socket.on("connect", () => {
        console.log("Connected to the server!");
    });

    //TODO Send and receive userprogress when they have sent their responses
    socket.on("gameprogress", username => {
        console.log(username);
    });
    
    socket.on("gamefinished", finalResults => {
        hideFirstClassElement("emotion_and_culprit_choices");
        document.querySelector(".reveal_score").textContent =
            Object.values(finalResults["player"][username])
                .filter(x => x == true).length + " / 5";

        const playerListElement = document.querySelector(".players_list");

        for (const player in finalResults["player"]) {
            if (player === username) {
                continue;
            }

            const playerNode = document.createElement("h3");
            playerNode.classList.add("player_name_and_score");

            const playerResultArray = Object.values(finalResults["player"][player]);
            playerNode.textContent = "" + player + " : "
                + playerResultArray.filter(x => x == true).length;

            playerListElement.appendChild(playerNode);
        }

        const culprit = getCulprit();
        const culpritName = gameData["npcs"][culprit]["name"];
        document.querySelector(".reveal_culprit_title").textContent += " " + culpritName;

        const culpritElement = document.getElementById("culprit");
        culpritElement.src = NPC_IMAGE_PATH + culprit;
        culpritElement.setAttribute("alt", "Image du ou de la coupable, " + culpritName);

        showFirstClassElement("results_game");
        setGameBackground(RESULTS_IMAGE_PATH);

        const suspectListElement = document.querySelector(".suspects_list");

        npcsIds.filter(x => x != culprit)
            .forEach(npcid => {
                const suspect = document.createElement("div");
                suspect.classList.add("summary_suspect");

                const img = document.createElement("img");
                img.src = NPC_IMAGE_PATH + npcid;
                suspect.appendChild(img);

                const emotionTitle = document.createElement("h2");
                emotionTitle.classList.add("explain_suspect_emotion_title");
                emotionTitle.textContent = "Ce suspect était "
                    + finalResults["npcs"][npcid]["reaction"] + ".";

                suspect.appendChild(emotionTitle);

                const emotionDesc = document.createElement("p");
                emotionDesc.classList.add("explain_suspect_emotion_description");
                emotionDesc.textContent = "Cette émotion se caractérise par "
                    + finalResults["npcs"][npcid]["description"];
                suspect.appendChild(emotionDesc);

                suspectListElement.appendChild(suspect);
            });
    });
}
/** 
 * This function retreive the initial gamedata of the game
 * containing all of the needed textual ressources to make
 * the game playable
*/

async function setGameData() {
    const response = await makeAPIRequest("getGameData");
    gameData = response["gamedata"];
    username = response["username"];
    npcsIds = Object.keys(gameData["npcs"]).sort(() => 0.5 - Math.random());
}

/**
 * Initialize the game, by setting the game data, initializing the socket, rendering the answer
 * selection panel, rendering the interrogation view, setting questions buttons listeners,
 * setting introduction and interrogation listeners, showing the introduction view and setting the
 * introduction image as the game background.
 */
async function initGame() {
    await setGameData();
    initSock();
    renderAnswerSelectionPanel();
    renderInterrogation();
    setQuestionButtonsListeners()
    setIntroductionAndInterrogationListeners();
    showFirstClassElement("introduction");
    setGameBackground(INTRO_IMAGE_PATH);
}

initGame();
