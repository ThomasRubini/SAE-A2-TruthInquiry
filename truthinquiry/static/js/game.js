const INTRO_IMAGE_PATH = "/static/images/entrée-manoir.jpg";
const INTERROGATION_IMAGE_PATH = "/static/images/salle-interrogation.jpg";
const RESULTS_IMAGE_PATH = "/static/images/salle-resultats.jpg";
const NPC_REACTION_PATH = "/api/v1/getNpcReaction?npcid=";
const NPC_IMAGE_PATH = "/api/v1/getNpcImage?npcid=";
const NPC_FINAL_REACTION_PATH = "/api/v1/getReaction?uuid="

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

function setChatBoxButtonsListeners() {
    document.getElementById("close_chat_button")
        .addEventListener("click", closeChatBox);
    document.getElementById("open_chat_button")
        .addEventListener("click", openChatBox);
    document.getElementById("chat_button_send")
        .addEventListener("click", sendChatMessage);
}

/**
 * Show the chat box.
 */
function openChatBox() {
    document.getElementById("chatbox").style.display = "block";
}
  
/**
 * Hide the chat box.
 */
function closeChatBox() {
    document.getElementById("chatbox").style.display = "none";
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
 * Parse the gamedata object to retreive the room in which the npc passed as parameter is located
 * and the second npc located in the same room.
 *
 * <p>
 * When the passed npc is alone in the room, a npc is chosen at random as the returned partener.
 * </p>
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
 * Parse the gamedata object to retreive the room in which the npc passed as parameter is located
 * and the second npc located in the same room.
 *
 * <p>
 * When the passed npc is alone in the room, a npc is chosen at random as the returned partner.
 * </p>
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
 * Return the npc designed as the "culprit" of the crime, the culprit is determined by being the
 * only npc alone in a room.
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
 * Handler for the function call {@link askQuestion} for a type_zero question also known as
 * "Where were you ?".
 */
async function askTypeZeroQuestion() {
    askQuestion(npcLocationAndPartner => gameData["npcs"][currentNpc]["QA_0"].replace(
        "{SALLE}", npcLocationAndPartner["room"]));
}

/**
 * Handler for the function call {@link askQuestion} for a type_one question also known as
 * "With who were you with ?".
 */
async function askTypeOneQuestion() {
    askQuestion(npcLocationAndPartner => gameData["npcs"][currentNpc]["QA_1"].replace(
        "{NPC}", gameData["npcs"][npcLocationAndPartner["partner"]]["name"]));
}

/**
 * This function's primary goal is to display the answer to the question the player
 * asked to a npc.
 *
 * <p>
 * It parses the gamedata object to retreive the answer of the npc and fill the variables left in
 * the string accordingly to the type of the question; then it fetches the reacion of the npc and
 * diplays it all.
 * </p>
 */
async function askQuestion(buildAnswer) {
    unsetQuestionButtonsListeners();

    document.querySelector(".suspect_answer").textContent = buildAnswer(
        getNpcLocationAndPartner(currentNpc));

    showFirstClassElement("suspect_answer");

    document.getElementById("currentNpcPicure").src = NPC_REACTION_PATH + currentNpc;

    //TODO: change this code which produces strange behaviors
    // Sleep for 4 sec
    await new Promise(r => setTimeout(r, 4000));

    document.getElementById("currentNpcPicure").src = NPC_IMAGE_PATH + currentNpc;
    hideFirstClassElement("suspect_answer");

    document.querySelector(".suspect_answer").textContent = "";

    setQuestionButtonsListeners();
}

/**
 * Send the player's answers to the server.
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
    const culpritChoices = document.getElementById("culprits_choices");

    npcsIds.forEach(element => {
        const suspect = document.createElement("li");
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
        img.setAttribute("alt", "Image d'un suspect");
        img.src = NPC_IMAGE_PATH + element;
        suspect.appendChild(img);

        const button = document.createElement("button");
        button.classList.add("culprit_btn", "action_button");

        button.appendChild(createCulpritSvgElement("culprit_checked_icon",
            "M18.9 36.75 6.65 24.5l3.3-3.3 8.95 9L38 11.1l3.3 3.25Z", true));
        button.appendChild(createCulpritSvgElement("culprit_unchecked_icon",
            "M12.45 38.7 9.3 35.55 20.85 24 9.3 12.5l3.15-3.2L24 20.8 35.55 9.3l3.15 3.2L27.2 24l11.5 11.55-3.15 3.15L24 27.2Z",
            false));

        button.appendChild(document.createTextNode("Couplable"));

        button.addEventListener("click", (event) => {
            disableCulpritButtons(culpritChoices, suspect);
            if (gameData["solo"] === true) event.target.textContent = "envoie des réponses..."; 
            else event.target.textContent = "attente des autres joueurs...";
            sendAnswers();
        });

        suspect.appendChild(button);
        culpritChoices.appendChild(suspect);
    });
}

/**
 * Create a culprit SVG {@link Element}.
 *
 * @param {String} buttonCssClass     the specific CSS class to add to the culprit button
 * @param {String} pathAttributeValue the value of the path attribute of the SVG element generated
 * @returns a svg {@link Element} with a culprit button depending of the custom CSS class, path
 * attribute value and isHidden values
 */
function createCulpritSvgElement(buttonCssClass, pathAttributeValue, isHidden) {
    const svgElement = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svgElement.classList.add(buttonCssClass, "culprit_icon");
    if (isHidden) {
        svgElement.classList.add("hidden");
    }
    svgElement.setAttribute("viewBox", "0 0 48 48");

    const pathElement = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pathElement.setAttribute("d", pathAttributeValue);

    svgElement.appendChild(pathElement);
    return svgElement;
}

/**
 * Show the screen in which the player asks questions to the npcs.
 */
function renderInterrogation() {
    if (gameData["solo"] === true) document.getElementById("open_chat_button").classList.add("hidden");

    document.getElementById("QA_0").textContent = gameData["questions"]["QA_0"];
    document.getElementById("QA_1").textContent = gameData["questions"]["QA_1"];

    const interrogationSuspects = document.getElementById("interrogation_suspects");

    npcsIds.forEach(npc_id => {
        const suspect = document.createElement("li");
        suspect.classList.add("suspect");

        const name = document.createElement('p')
        name.textContent = gameData['npcs'][npc_id]["name"]
        name.classList.add("suspect_name");
        suspect.appendChild(name);

        const img = document.createElement('img');
        img.id = "suspect_picture_of_" + npc_id
        img.classList.add("suspect_picture");
        img.setAttribute("alt", "Image d'un suspect");
        img.src = NPC_IMAGE_PATH + npc_id;
        img.addEventListener("click", () => {
            // TODO remove this listener when we know the questions has already been asked;
            currentNpc = npc_id;
            document.getElementById("suspect_picture_of_" + npc_id).classList.add("gray");
            document.getElementById("currentNpcPicure").src = NPC_IMAGE_PATH + npc_id;
            hideFirstClassElement("interrogation");
            showFirstClassElement("interrogation_suspect");
        });
        suspect.appendChild(img);

        const button = document.createElement("button");
        button.classList.add("ask_button", "action_button");
        button.textContent = "Interroger";
        button.addEventListener("click", () => {
            // TODO remove this listener when we know the questions has already been asked;
            currentNpc = npc_id;
            document.getElementById("suspect_picture_of_" + npc_id).classList.add("gray");
            document.getElementById("currentNpcPicure").src = NPC_IMAGE_PATH + npc_id;
            hideFirstClassElement("interrogation");
            showFirstClassElement("interrogation_suspect");
        });
        suspect.appendChild(button);
        interrogationSuspects.appendChild(suspect);
    });
}

function sendChatMessage(){
    const message = document.getElementById("chat_message_box").value;
    const data = {};
    data["msg"] = message;
    makeAPIRequest("chatMessage",data);
    document.getElementById("chat_message_box").value = '';
}

function renderIntroduction(){
    document.getElementById("username").textContent += username;
}

/**
 * Initialize the websocket for this page, its primary use is to show the final page once it
 * receives the event that all players have finished.
 *
 * <p>
 * It parses the payload send by the server containing the other players
 * nicknames and scores.
 * </p>
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

    socket.on("chatMessage", message => {
        const message_received = document.createElement("li");
        message_received.classList.add("message");
        message_received.textContent = message;
        document.getElementById("message_list").appendChild(message_received);
    });
    
    socket.on("gamefinished", finalResults => {
        console.log(finalResults);
        hideFirstClassElement("emotion_and_culprit_choices");
        const revealScoreElement = document.createElement("h2");
        revealScoreElement.classList.add("reveal_score");
        revealScoreElement.textContent = Object.values(finalResults["player"][username])
            .filter(x => x == true).length + " / 5";

        document.querySelector(".player_score").appendChild(revealScoreElement);

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

        const culpritElement = document.createElement("img");
        culpritElement.classList.add("suspect_picture");
        culpritElement.setAttribute("alt", "Image du ou de la coupable, " + culpritName);
        culpritElement.src = NPC_IMAGE_PATH + culprit;
        culpritElement.setAttribute("draggable", "false");

        document.querySelector(".reveal_culprit")
            .appendChild(culpritElement);

        showFirstClassElement("results_game");
        setGameBackground(RESULTS_IMAGE_PATH);

        const suspectListElement = document.querySelector(".suspects_list");

        npcsIds.filter(x => x != culprit)
            .forEach(npcid => {
                const suspect = document.createElement("div");
                suspect.classList.add("summary_suspect");

                const img = document.createElement("img");
                img.classList.add("suspect_picture");
                img.setAttribute("alt", "Image d'un suspect");
                img.src = NPC_FINAL_REACTION_PATH + finalResults["npcs"][npcid]["uuid"];
                suspect.appendChild(img);
                
                const explain = document.createElement("div")
                explain.classList.add("explain")

                const emotionTitle = document.createElement("h2");
                emotionTitle.classList.add("explain_suspect_emotion_title");
                emotionTitle.textContent = "Ce suspect était "
                    + finalResults["npcs"][npcid]["reaction"] + ".";
                
                explain.appendChild(emotionTitle);
                
                const emotionDesc = document.createElement("p");
                emotionDesc.classList.add("explain_suspect_emotion_description");
                emotionDesc.textContent = "Cette émotion se caractérise par "
                    + finalResults["npcs"][npcid]["description"];
                explain.appendChild(emotionDesc);
                suspect.appendChild(explain)
                suspectListElement.appendChild(suspect);
            });
    });
}

/**
 * Retreive the initial gamedata of the game containing all of the needed textual ressources to
 * make the game playable.
 */
async function setGameData() {
    const response = await makeAPIRequest("getGameData");
    gameData = response["gamedata"];
    username = response["username"];
    npcsIds = Object.keys(gameData["npcs"]).sort(() => 0.5 - Math.random());
}

/**
 * Initialize the game by setting the game data, initializing the socket, rendering the answer
 * selection panel, rendering the interrogation view, setting questions buttons listeners,
 * setting introduction and interrogation listeners, showing the introduction view and setting the
 * introduction image as the game background.
 */
async function initGame() {
    await setGameData();
    initSock();
    renderIntroduction();
    renderAnswerSelectionPanel();
    renderInterrogation();
    setQuestionButtonsListeners()
    setIntroductionAndInterrogationListeners();
    setChatBoxButtonsListeners();
    showFirstClassElement("introduction");
    setGameBackground(INTRO_IMAGE_PATH);
}

initGame();
