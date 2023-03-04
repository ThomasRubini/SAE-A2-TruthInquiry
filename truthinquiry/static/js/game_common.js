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
    const browserName = window.navigator.userAgent;
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
 * Create a temporary cookie to detect whether cookies are allowed for the game website domain.
 *
 * <p>
 * This cookie, cookietest, with 1 as a value, is automatically deleted after being created.
 * </p>
 *
 * @returns whether cookies are allowed for the website domain
 */
function createTemporaryCookieThenDeleteIt() {
    try {
        // Create a temporary cookie
        document.cookie = "cookietest=1; SameSite=Strict; Path=/";
        const cookieTestResult = document.cookie.indexOf("cookietest=") !== -1;
        // Delete the temporary cookie
        document.cookie = "cookietest=1; SameSite=Strict; Expires=Thu, 01-Jan-1970 00:00:01 GMT; Path=/";
        return cookieTestResult;
    } catch (e) {
        return false;
    }
}

/**
 * Check the availability of cookies in the client.
 *
 * <p>
 * If it is not available, an error message which prevents playing the game and requesting user to
 * enable website cookies is shown.
 * </p>
 */
function checkCookiesAvailability() {
    if (!createTemporaryCookieThenDeleteIt()) {
        showUnsupportedBrowserMessage("Votre navigateur ne prend pas en charge les cookies, nécessaires au fonctionnement du jeu. Veuillez les activer dans les paramètres de votre navigateur.");
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
    const unsupportedBrowserMessageElement = document.querySelector(".unsupported_browser_msg");
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
    document.querySelector(".alert_dialog_background").style.display = "block";
}

/**
 * Show the first element with the given CSS class, by removing the hidden CSS class on it.
 *
 * @param {String} className the CSS class on which showing the first element found
 */
function showFirstClassElement(className) {
    document.querySelector("." + className).classList.remove("hidden");
}

/**
 * Hide the first element with the given CSS class, by adding the hidden CSS class on it.
 *
 * @param {String} className the CSS class on which hiding the first element found
 */
function hideFirstClassElement(className) {
    document.querySelector("." + className).classList.add("hidden");
}

// Execution of main functions

detectIEBrowsers();
checkWebSocketAvailability();
checkCookiesAvailability();
