// Display functions

/**
 * Display the invalid rounds count message element, by removing the hidden CSS class.
 *
 * @param {Element} invalidRoundsCountMessageElement the invalid rounds counts message
 */
function displayInvalidRoundsCountErrorMessage(invalidRoundsCountMessageElement) {
    invalidRoundsCountMessageElement.classList.remove("hidden");
}

/**
 * Get the room code and display the room code element.
 */
function displayRoomCode() {
    const roomCodeElement = document.querySelector(".room_code");
    const roomCode = getRoomCode();

    roomCodeElement.textContent = roomCode;
    roomCodeElement.setAttribute("href", "/lobby/" + roomCode);

    showFirstClassElement("room_code_text");
}

/**
 * Display the players list element.
 */
function displayPlayerList() {
    const response = makeAPIRequest("getGameMembers");

    response.then(value => {
        const playerList = document.querySelector(".player_names");
        value["members"].forEach(username => {
            playerList.appendChild(document.createTextNode(username + "\n"));
        });
    });

    showFirstClassElement("players_list");
}

/**
 * Display the multi player mode choices, by removing the hidden CSS class on the first
 * multi_player_mode_choices element.
 */
function displayMultiPlayerModeChoices() {
    showFirstClassElement("multi_player_mode_choices");
}

/**
 * Display the room view, by removing the hidden CSS class on the first room_view element.
 */
function displayRoomView() {
    showFirstClassElement("room_view");
}

/**
 * Display the room view, by removing the hidden CSS class on the first
 * multi_player_mode_waiting_for_host element.
 */
function displayWaitingForHostMessage() {
    showFirstClassElement("multi_player_mode_waiting_for_host");
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
function displayInvalidNickNameErrorMessage(errorMessage) {
    let gameStartFailedElement = document.querySelector(".game_start_failed");
    gameStartFailedElement.textContent = errorMessage;
    gameStartFailedElement.classList.remove("hidden");
}

// Start game functions

/**
 * Start a game in the history mode.
 */
function startHistoryGame() {
    makeAPIRequest("startGame");
}

/**
 * Start a game in the challenge mode.
 */
function startChallengeGame() {
    const roundsCount = getChallengeModeRoundsCount();
    if (roundsCount == -1) {
        return;
    }

    alert("Ce mode de jeu n'est malheureusement pas disponible.");
}

// Join room functions

function joinRoom() {
    if (isNickNameInvalid()) {
        displayInvalidNickNameErrorMessage("Le nom saisi n'est pas valide.");
        return;
    }

    hideFirstClassElement("game_start_failed");
    displayWaitingForHostMessage();

    const data = {};
    data["username"] = document.getElementById("game_username").value;
    data["game_id"] = getRoomCode();

    const response = makeAPIRequest("joinGame", data);

    response.then(() => {
        displayRoomView();
        displayPlayerList();
        initSock();
        hideFirstClassElement("join_room_view");
    })
}

// Room code functions

/**
 * Copy the room code to the clipboard.
 *
 * <p>
 * In order to not make an additional API call to get the room code, we use the value from the
 * room code HTML element and generate a HTTP link from this value, copied to the clipboard using
 * {@link copyTextToClipboard}.
 * </p>
 */
function copyCode() {
    const roomCode = getRoomCode();

    copyTextToClipboard(window.location.protocol + "//" + window.location.hostname + ":"
        + window.location.port + "/lobby/"  + roomCode);
}

// Listeners functions

/**
 * Set listeners to game buttons.
 *
 * <p>
 * This function adds a click event listener on start game buttons.
 * </p>
 */
function setListenersToGameButtons() {
    document.getElementById("multi_player_history_start_button")
        .addEventListener("click", startHistoryGame);
    document.getElementById("multi_player_challenge_start_button")
        .addEventListener("click", startChallengeGame);
}

/**
 * Set listeners to the join room button.
 *
 * <p>
 * This function adds a click event listener on the join room button.
 * </p>
 */
function setListenerToJoinRoomButton() {
    document.getElementById("join_game_button").addEventListener("click", joinRoom);
}

/**
 * Set listeners to the copy room code button.
 *
 * <p>
 * This function adds a click event listener on the copy room code button.
 * </p>
 */
function setListenerToCopyCodeButton() {
    document.getElementById("invite_friends_button").addEventListener("click", copyCode);
}

/**
 * Unset listeners to game buttons.
 *
 * <p>
 * This function removes the click event listener set with {@link setListenersToGameButtons} on
 * start game buttons.
 * </p>
 */
function unsetListenersToButtons() {
    document.getElementById("multi_player_history_start_button")
        .removeEventListener("click", startHistoryGame);
    document.getElementById("multi_player_challenge_start_button")
        .removeEventListener("click", startChallengeGame);
}

/**
 * Unset listeners to the join room button.
 *
 * <p>
 * This function removes the click event listener set with {@link setListenerToJoinRoomButton} on
 * the join room button.
 * </p>
 */
function unsetListenerToJoinRoomButton() {
    document.getElementById("join_game_button").removeEventListener("click", joinRoom);
}

/**
 * Unset listeners to the copy room code button.
 *
 * <p>
 * This function removes the click event listener set with {@link setListenerToCopyCodeButton} on
 * the copy room code button.
 * </p>
 */
function unsetListenerToCopyCodeButton() {
    document.getElementById("invite_friends_button").removeEventListener("click", copyCode);
}

// Utility functions

async function isRoomOwner() {
    const response = await makeAPIRequest("isOwner");
    return response["owner"];
}

async function hasJoinedRoom() {
    const response = await makeAPIRequest("hasJoined");
    return response["joined"];
}

/**
 * Copy the given text in the clipboard, if the browser allows it.
 *
 * <p>
 * A JavaScript alert is created witn an appropriate message, regardless of whether the copy succeeded.
 * </p>
 *
 * <p>
 * This function uses the Clipboard API. In the case it is not supported by the browser used, a JavaScript alert is shown.
 * </p>
 *
 * @param {string} textToCopy the text to copy to the clipboard
 */
function copyTextToClipboard(textToCopy) {
    if (!navigator.clipboard) {
        alert("Votre navigateur ne supporte pas l'API Clipboard. Veuillez copier le texte en ouvrant le menu contextuel de votre navigateur sur le lien et sélectionner l'option pour copier le lien.");
        return;
    }

    navigator.clipboard.writeText(textToCopy)
        .then(() => {
            alert("Lien copié avec succès dans le presse-papiers.");
        }, () => {
            alert("Impossible de copier le lien. Vérifiez si vous avez donné la permission d'accès au presse-papiers pour le site de Thruth Inquiry dans les paramètres de votre navigateur.");
        });
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
 * Get the rounds count for the challenge mode from the user input.
 *
 * <p>
 * As browsers allow to enter any character on a number imput, we need to validate the user value.
 * A regular expression which checks that every character is a number digit is used.
 * </p>
 *
 * <p>
 * If the user input isn't matched by the regular expression, an error message is shown to the user.
 * </p>
 *
 * @returns the rounds count or -1 if it is invalid
 */
function getChallengeModeRoundsCount() {
    let roundsCountText = document.getElementById("rounds_count").value;
    let errorElement = document.querySelector(".multi_player_challenge_mode_invalid_input");

    if (!/^\d+$/.test(roundsCountText)) {
        displayInvalidRoundsCountErrorMessage(errorElement);
        return -1;
    }

    let roundsCountNumber = parseInt(roundsCountText);
    if (roundsCountNumber < 5 || roundsCountNumber > 15) {
        displayInvalidRoundsCountErrorMessage(errorElement);
        return -1;
    }

    errorElement.classList.add("hidden");
    return roundsCountNumber;
}

/**
 * Get the code of the room.
 *
 * @returns the code of the room
 */
function getRoomCode() {
    return document.getElementById("game_id").value;
}

function initSock() {
    const socket = io({
        auth: {
            game_id: getRoomCode()
        }
    });

    socket.on("connect", () => {
        console.log("Connected to the server!");
    })

    socket.on("gamestart", () => {
        window.location.href = "/multi";
    })

    socket.on("playersjoin", username => {
        document.querySelector(".player_names")
            .appendChild(document.createTextNode(username + "\n"));
    });
}

// Lobby initialization

/**
 * Initialize the lobby page.
 *
 * <p>
 * If the player has joined the room, the room view will be shown. In the case the player is the
 * owner of the room, the room code and the multi player mode choice will be shown and the
 * listeners to the game buttons will be done.
 * </p>
 *
 * <p>
 * If the player has not joined the room, the join room view will be shown and a listener to the
 * join room button will be set.
 * </p>
 */
async function initLobby() {
    if (await hasJoinedRoom()) {
        initSock();
        displayRoomView();

        if (await isRoomOwner()) {
            displayRoomCode();
            displayMultiPlayerModeChoices();
            setListenersToGameButtons();
            setListenerToCopyCodeButton();
        } else {
            displayWaitingForHostMessage();
        }

        displayPlayerList();
    } else {
        showFirstClassElement("join_room_view");
        setListenerToJoinRoomButton();
    }
}

initLobby();
