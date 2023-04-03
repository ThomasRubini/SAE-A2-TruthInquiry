/**
 * Show the game selection view.
 *
 * <p>
 * The "hidden" class is added on the footer, the game_start elements and the game_mode_selection
 * elements are show. The body margin is also set to 0 by adding the ingame class.
 * </p>
 */
function showGameModeSelection() {
    document.getElementsByTagName("body")[0].classList.add("ingame");
    document.getElementsByTagName("footer")[0].classList.add("hidden");
    document.getElementsByClassName("game_start")[0].classList.add("hidden");
    document.getElementsByClassName("game_mode_selection")[0].classList.remove("hidden");
}

/**
 * Show the game selection view.
 *
 * <p>
 * The "hidden" class is removed on the footer, the game_start elements and the game_mode_selection
 * elements are hidden. The body margin is also set to its normal value by removing the ingame
 * class.
 * </p>
 */
function hideGameModeSelection() {
    document.getElementsByTagName("body")[0].classList.remove("ingame");
    document.getElementsByTagName("footer")[0].classList.remove("hidden");
    document.getElementsByClassName("game_start")[0].classList.remove("hidden");
    document.getElementsByClassName("game_mode_selection")[0].classList.add("hidden");
}

/**
 * Hide an error message on the first game_start_failed CSS element.
 *
 * <p>
 * The element will be hidden by removing the hidden CSS class on the element.
 * </p>
 */
function hideInvalidInputErrorMessage() {
    document.getElementsByClassName("game_start_failed")[0].classList.add("hidden");
}

/**
 * Show an error message on the first game_start_failed CSS element.
 *
 * <p>
 * The current error message text will be replaced by the given message and the element will be
 * shown, by removing the hidden CSS class on the element.
 * </p>
 *
 * @param {boolean} errorMessage the error message to show
 */
function showInvalidInputErrorMessage(errorMessage) {
    let gameStartFailedElement = document.getElementsByClassName("game_start_failed")[0];
    gameStartFailedElement.textContent = errorMessage;
    gameStartFailedElement.classList.remove("hidden");
}

/**
 * Determine whether a nickname is invalid.
 *
 * <p>
 * A nickname is invalid when it only contains spaces characters or is empty.
 * </p>
 *
 * @returns whether a nickname is invalid
 */
function isNickNameInvalid() {
    return document.getElementById("game_username").value.trim() == "";
}

/**
 * Determine whether a room code is invalid.
 *
 * <p>
 * A room code is invalid when it only contains spaces characters or is empty.
 * </p>
 *
 * @returns whether a room code is invalid
 */
function isRoomCodeInvalid() {
    return document.getElementById("game_room_code").value.trim() == "";
}

/**
 * Determine whether nickname and/or room code inputs are valid.
 *
 * <p>
 * The nickname validity is always checked, while the room code validity is checked only when
 * checkRoomCode is true (because when creating a room or playing on a solo match, the room code is
 * not used so checking it would be useless and would require a valid room code).
 * </p>
 *
 * @param {boolean} checkRoomCode whether the room code input should be checked
 * @returns whether the checked inputs are valid
 */
function areInputsValid(checkRoomCode) {
    if (isNickNameInvalid()) {
        showInvalidInputErrorMessage("Le nom saisi n'est pas valide.");
        return false;
    }

    if (checkRoomCode && isRoomCodeInvalid())  {
        showInvalidInputErrorMessage("Le code de salon saisi n'est pas valide.");
        return false;
    }

    return true;
}


/**
 * Handler for the multiplayer room creation button 
 */
function createMultiPlayerRoom(event) {
    if (!areInputsValid(false)) {
        return;
    }

    hideInvalidInputErrorMessage();
    event.target.textContent = "Chargement\u00A0...";
    startGame();
}

/**
 * Handler for the join room button 
 */
function joinMultiPlayerRoom(event) {
    if (!areInputsValid(true)) {
        return;
    }

    hideInvalidInputErrorMessage();
    event.target.textContent = "Chargement\u00A0...";
    joinGame(event);
}

/**
 * Launch a single player game.
 *
 * <p>
 * It sends the api request to
 * create a game then it immediately starts the game by using the startGame API endpoint.
 * </p>
 */
async function startSoloGame(event) {
    if (!areInputsValid(false)) {
        return;
    }
    event.target.textContent = "Chargement\u00A0...";
    hideInvalidInputErrorMessage();
    username = document.getElementById("game_username").value;
    let data = {}
    data["username"] = username;
    data["solo"] = true;
    await makeAPIRequest("createGame",data);
    makeAPIRequest("startGame").then(() => {
        window.location.href = "/solo";
    }, () => {
        startHistoryGameButton.target.textContent = "Jouer";
    });
}

/**
 * This function creates a multiplayer game by sending the createGame api call
 * then, if no error occured, redirects to the lobby page.
 */
async function startGame() {
    username = document.getElementById("game_username").value;
    let data = {}
    data["username"] = username;
    response = makeAPIRequest("createGame", data);
    response.then((value) => {
        if (value["error"] != 0){
            alert(value["msg"]);
        } else {
            gameid = value["game_id"]
            window.location.href = "/lobby/" + gameid;
        }
    });
}

/**
 * This function read the username and the room code in order to
 * join an already existing game, to do so it calls the joinGame endpoint
 * with the aftermentioned username and room code as parameter. 
 */
async function joinGame(event) {
    username = document.getElementById("game_username").value;
    gameid = document.getElementById("game_room_code").value;
    const data = {};
    data["username"] = username;
    data["game_id"] = gameid;
    makeAPIRequest("joinGame", data).then(() => {
        window.location.href = "/lobby/" + gameid;
    }, () => {
        event.target.textContent = "Jouer";
    });
}
// Set event listeners

document.getElementById("play_button").addEventListener("click", showGameModeSelection);
document.getElementById("back_button").addEventListener("click", hideGameModeSelection);
document.getElementById("start_solo_game_button").addEventListener("click", startSoloGame);
document.getElementById("create_room_button").addEventListener("click", createMultiPlayerRoom);
document.getElementById("join_room_button").addEventListener("click", joinMultiPlayerRoom);

// Execution of functions

//setCurrentTheme();
