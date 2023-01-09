// Common functions
// These functions should be executed in all the game pages, except the privacy policy, licenses, and legal mentions ones.

/*
 * Prevent using Internet Explorer browser in the game, by detecting whether MSIE or Trident is
 * present in the user agent.
 *
 * <p>
 * If Internet Explorer is used, an error message which prevents playing the game and requesting
 * user to change their browser is shown.
 * </p>
 */
function detectIEBrowsers() {
    let browserName = window.navigator.userAgent;
    if (browserName.indexOf("MSIE") != -1 || browserName.indexOf("Trident") != -1) {
        showUnsupportedBrowserMessage("Il semblerait que vous utilisez Internet Explorer, un navigateur non supporté. Veuillez utiliser un autre navigateur récent tel que Firefox.");
    }
}

/**
 * Check the availability of the WebSocket API in the client.
 *
 * <p>
 * If it is not available, an error message which prevents playing the game and requesting user to
 * enable WebSocket API is shown.
 * </p>
 */
function checkWebSocketAvailability() {
    if (!window.WebSocket) {
        showUnsupportedBrowserMessage("Votre navigateur ne prend pas en charge les API WebSocket, nécessaires au fonctionnement du jeu. Veuillez les activer ou utiliser un navigateur compatible avec ces APIs, tel que Firefox.");
    }
}

/**
 * Show the unsupported browser dialog, which disables ability to play the game, using the given
 * unsupported browser message text.
 *
 * <p>
 * This method will provide the text supplied to the first element with the unsupported_browser_msg
 * CSS class found.
 * </p>
 *
 * @param {String} messageText the error message to show, as a string and not as an HTML block
 */
function showUnsupportedBrowserMessage(messageText) {
    showAlertDialog(document.getElementById("unsupported_browser_dialog"));
    let unsupportedBrowserMessageElement = document.getElementsByClassName("unsupported_browser_msg")[0];
    unsupportedBrowserMessageElement.textContent = messageText;
    unsupportedBrowserMessageElement.classList.add("unsupported_show");
}

/**
 * Show an alert dialog component which will show a background preventing interactions with the game.
 *
 * <p>
 * This function will add the alert_dialog_show CSS class to the element passed and show to the first
 * element found with the alert_dialog_background class.
 * </p>
 *
 * @param {Element} element an HTML element which should contain the alert_dialog CSS class
 */
function showAlertDialog(element) {
    element.classList.add("alert_dialog_show");
    document.getElementsByClassName("alert_dialog_background")[0].style.display = "block";
}

// Execution of main functions

detectIEBrowsers();
checkWebSocketAvailability();