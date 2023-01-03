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

document.getElementById("play_button").addEventListener("click", showGameModeSelection);
document.getElementById("back_button").addEventListener("click", hideGameModeSelection);
