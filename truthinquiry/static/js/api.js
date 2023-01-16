async function makeAPIRequest(endpoint, body) {
    return new Promise((resolve, reject) => {
        const fetchOptions = {
            method: "POST",
            body: new URLSearchParams(body)
        };

        fetch("/api/v1/" + endpoint, fetchOptions).then(response => {
            const responseCode = response.status;
            console.log(responseCode);
            if (responseCode >= 500) {
                reject("Error " + responseCode + " when fetching " + endpoint);
                alert("Une réponse invalide du serveur a été obtenue, veuillez réessayer ultérieurement.");
                return;
            }

            response.json().then(jsonResponse => {
                if (jsonResponse["error"] === 0) {
                    resolve(jsonResponse);
                } else {
                    const message = jsonResponse["msg"];
                    alert("Erreur du serveur : " + message);
                    reject(endpoint + ": " + message);
                }
            });
        }).catch((e) => {
            console.error("Failed to fetch API", e);
            alert("Une erreur est survenue lors de la connexion au serveur, veuillez vérifier votre connexion et / ou réessayer ultérieurement.");
            reject(endpoint);
        });
    });
}
