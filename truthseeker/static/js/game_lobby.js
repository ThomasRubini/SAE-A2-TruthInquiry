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
    let roomCode = getRoomCode();
    let roomCodeElement = document.getElementsByClassName("room_code")[0];
    roomCodeElement.textContent = roomCode;
    roomCodeElement.setAttribute("href", "/lobby/" + roomCode);
    document.getElementsByClassName("room_code_text")[0].classList.remove("hidden");
}

/**
 * Display the players list element.
 */
function displayPlayerList() {
    document.getElementsByClassName("players_list")[0].classList.remove("hidden");
}

/**
 * Display the multi player mode choices, by removing the hidden CSS class on the first
 * multi_player_mode_choices element.
 */
function displayMultiPlayerModeChoices() {
    document.getElementsByClassName("multi_player_mode_choices")[0].classList.remove("hidden");
}

/**
 * Display the room view, by removing the hidden CSS class on the first room_view element.
 */
function displayRoomView() {
    document.getElementsByClassName("room_view")[0].classList.remove("hidden");
}

/**
 * Display the join room view, by removing the hidden CSS class on the first join_room_view
 * element.
 */
function displayJoinRoomView() {
    document.getElementsByClassName("join_room_view")[0].classList.remove("hidden");
}

/**
 * Hide the invalid rounds count message element, by adding the hidden CSS class.
 *
 * @param {Element} invalidRoundsCountMessageElement the invalid rounds counts message
 */
function hideInvalidRoundsCountErrorMessage(invalidRoundsCountMessageElement) {
    invalidRoundsCountMessageElement.classList.add("hidden");
}

// Start game functions

function startHistoryGame() {
    //TODO: start the history game
}

function startChallengeGame() {
    let roundsCount = getChallengeModeRoundsCount();
    if (roundsCount == -1) {
        return;
    }

    //TODO: start the challenge game
}

// Listeners functions

/**
 * Set listeners to game buttons.
 *
 * <p>
 * This function adds a click event listener on start buttons
 * </p>
 */
function setListenersToGameButtons() {
    document.getElementById("multi_player_history_start_button").addEventListener("click", startHistoryGame);
    document.getElementById("multi_player_challenge_start_button").addEventListener("click", startChallengeGame);
}

function unsetListenersToButtons() {
    document.getElementById("multi_player_history_start_button").removeEventListener("click", startHistoryGame);
    document.getElementById("multi_player_challenge_start_button").removeEventListener("click", startChallengeGame);
}

// Utility functions

function isRoomOwner() {
    //FIXME: check if player is room owner
    return true;
}

function hasJoinedRoom() {
    //FIXME: check if player has joined the room
    return true;
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
    let errorElement = document.getElementsByClassName("multi_player_challenge_mode_invalid_input")[0];
    if (!/^\d+$/.test(roundsCountText)) {
        displayInvalidRoundsCountErrorMessage(errorElement);
        return -1;
    }

    let roundsCountNumber = parseInt(roundsCountText);
    if (roundsCountNumber < 5 || roundsCountNumber > 15) {
        displayInvalidRoundsCountErrorMessage(errorElement);
        return -1;
    }

    hideInvalidRoundsCountErrorMessage(errorElement);
    return roundsCountNumber;
}

/**
 * Get the code of the room.
 *
 * @returns the code of the room
 */
function getRoomCode() {
    //FIXME
    return "ABCDEF";
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
function initLobby() {
    if (hasJoinedRoom()) {
        displayRoomView();
        if (isRoomOwner()) {
            displayRoomCode();
            displayMultiPlayerModeChoices();
            setListenersToGameButtons();
        }

        displayPlayerList();
    } else {
        displayJoinRoomView();
        //TODO
        /**
         * setListenerToJoinRoomButton();
         */
    }
}

initLobby();