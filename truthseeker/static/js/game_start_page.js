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

function startSoloGame() {
    if (!areInputsValid(false)) {
        return;
    }

    hideInvalidInputErrorMessage();

    //TODO: code to start solo game
}

function createMultiPlayerRoom() {
    if (!areInputsValid(false)) {
        return;
    }

    hideInvalidInputErrorMessage();

    startGame()
}

function joinMultiPlayerRoom() {
    if (!areInputsValid(true)) {
        return;
    }

    hideInvalidInputErrorMessage();

    //TODO: code to join multi player game
}

/**
 * Set the current theme for the game.
 *
 * <p>
 * The theme preference is read from the local storage.
 * </p>
 *
 * <p>
 * If accessing to the local storage is not allow, an error message which prevents playing the game
 * and requesting user to enable localStorage is shown, and the error is logged in the console.
 * </p>
 */
function setCurrentTheme() {
    const htmlElement = document.getElementsByTagName("html")[0];

    try {
        const currentTheme = localStorage.getItem("pref_theme");

        if (currentTheme == "light") {
            htmlElement.classList.remove("dark");
            htmlElement.classList.add("light");
        } else {
            // Use dark theme by default
            htmlElement.classList.remove("light");
            htmlElement.classList.add("dark");
        }

        const btn = document.getElementsByClassName("theme_switcher")[0];
        btn.addEventListener("pointerup", changeTheme);
    } catch (e) {
        console.error("Unable to set theme from localStorage", e);
        htmlElement.classList.add("dark");
        showUnsupportedBrowserMessage("Votre navigateur ne semble pas supporter le localStorage. Certains navigateurs nécessitant l'autorisation d'utiliser des cookies pour utiliser le localStorage, vérifiez que les cookies sont autorisés pour le site du jeu dans le vôtre.");
    }
}

/**
 * Change the theme from the current theme to its opposite.
 *
 * <p>
 * If the current theme is "dark", it will become "light" and vice versa.
 * </p>
 *
 * <p>
 * The new theme is saved in the localStorage, if the browser allows this action; otherwise, an
 * error message is shown in the console.
 * </p>
 */
function changeTheme() {
    const currentTheme = localStorage.getItem("pref_theme");

    const htmlElement = document.getElementsByTagName("html")[0];
    let newTheme;
    if (currentTheme == "light") {
        htmlElement.classList.remove("light");
        htmlElement.classList.add("dark");
        newTheme = "dark";
    } else {
        htmlElement.classList.remove("dark");
        htmlElement.classList.add("light");
        newTheme = "light";
    }

    try {
        localStorage.setItem("pref_theme", newTheme);
    } catch (e) {
        console.error("Unable to save theme change to localStorage", e);
    }
}

async function startGame(){
    username = document.getElementById("game_username").value;
    let data = {}
    data["username"] = username
    await makeAPIRequest("createGame",data);
}
async function joinGame(){
    username = document.getElementById("game_username").value();
    gameid = document.getElementById("game_room_code").value();
}
// Set event listeners

document.getElementById("play_button").addEventListener("click", showGameModeSelection);
document.getElementById("back_button").addEventListener("click", hideGameModeSelection);
document.getElementById("start_solo_game_button").addEventListener("click", startSoloGame);
document.getElementById("create_room_button").addEventListener("click", createMultiPlayerRoom);
document.getElementById("join_room_button").addEventListener("click", joinMultiPlayerRoom);

// Execution of functions

setCurrentTheme();
