async function makeAPIRequest(endpoint, body){
    return new Promise((resolve, reject)=>{
        const fetchOptions = {
            method: "POST",
            body: new URLSearchParams(body)
        }
        fetch("/api/v1/"+endpoint, fetchOptions).then(resp => {
            resp.json().then(jsonResp=>{
                if(jsonResp["error"] == 0){
                    resolve(jsonResp)
                }else{
                    reject(endpoint+": "+jsonResp["msg"])
                }
            });
        })
    })
}
async function makeAPIImageRequest(endpoint, body){
    return new Promise((resolve, reject)=>{
        const fetchOptions = {
            method: "POST",
            body: new URLSearchParams(body)
        }
        fetch("/api/v1/"+endpoint, fetchOptions).then(resp => {
            resolve(resp)
        })
    })
}
