/**
 * Make a request to the given endpoint of the API with the given body.
 *
 * @param {String} endpoint the endpoint on which make an API request
 * @param {Object} body     an object to send in the API request (this object can be omitted)
 * @returns a Promise, which resolves when the server can be reached and responds without an error
 * and rejects otherwise
 */
async function makeAPIRequest(endpoint, body, options={}) {
    let fetchOptions = {
        method: "POST",
        headers: {
            'Accept': 'application/json'
        }
    };

    if (options["content"] === 'json') {
        fetchOptions["headers"]["Content-Type"] = 'application/json'
        fetchOptions["body"] = JSON.stringify(body)
    } else if (options["content"] === 'form') {
        fetchOptions["body"] = body;
    } else {
        fetchOptions["body"] = new URLSearchParams(body);
    }

    return new Promise((resolve, reject) => {

        fetch("/api/v1/" + endpoint, fetchOptions).then(response => {
            const responseCode = response.status;
            if (responseCode >= 500) {
                reject("Error " + responseCode + " when fetching " + endpoint);
                alert("Une réponse invalide du serveur a été obtenue, veuillez réessayer ultérieurement.");
                return;
            }

            response.json().then(jsonResponse => {
                if (typeof(jsonResponse["error"]) === 'number' && jsonResponse["error"] !== 0) {
                    const message = jsonResponse["msg"];
                    alert("Erreur du serveur " + endpoint+ " : " + message);
                    reject(endpoint + ": " + message);
                } else {
                    resolve(jsonResponse);
                }
            });
        }).catch((e) => {
            console.error("Failed to fetch API", e);
            alert("Une erreur est survenue lors de la connexion au serveur, veuillez vérifier votre connexion et / ou réessayer ultérieurement.");
            reject(endpoint);
        });
    });
}
