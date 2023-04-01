//functions for places.html

function addInputPlaces(){
    let newPlace = places.lastElementChild.cloneNode(true);
    newPlace.id = "";
    newPlace.querySelector("input").value = "";
    places.appendChild(newPlace);
}

function deleteInputPlaces(buttonNode){
    let placeNode = buttonNode.parentNode;
    placeNode.parentNode.removeChild(placeNode);
}

function saveFormPlaces(){
    let data = [];
    for(let section of places.querySelectorAll("section")){
        let place = {};
        place["id"] = section.id
        place["name"] = section.querySelector("input").value
        data.push(place);
    }
    makeAPIRequest("admin/setPlaces", {"places": data, "lang": "FR"}, {"content": "json"})
}


//functions for traits.html


function addInputTraits(){
    let newTrait = traits.lastElementChild.cloneNode(true);
    newTrait.id = "";
    newTrait.querySelector(".name_input").value = "";
    newTrait.querySelector(".desc_input").value = "";
    traits.appendChild(newTrait);
}

function deleteInputTraits(buttonNode){
    let traitNode = buttonNode.parentNode;
    traitNode.parentNode.removeChild(traitNode);
}

function saveFormTraits(){
    let data = [];
    for(let section of traits.querySelectorAll("section")){
        let trait = {};
        trait["id"] = section.id
        trait["name"] = section.querySelector(".name_input").value
        trait["desc"] = section.querySelector(".desc_input").value
        data.push(trait);
    }
    makeAPIRequest("admin/setTraits", {"traits": data, "lang": "FR"}, {"content": "json"})
}



//functions for questions.html




function addInputQuestions(button){
    let questionTypeContent = button.parentNode.querySelector(".questionTypeContent");
    let newQuestion = questionTypeContent.querySelector(".question").cloneNode(true);
    newQuestion.id = "";
    newQuestion.querySelector("input").value = "";
    questionTypeContent.appendChild(newQuestion);
}

function deleteInputQuestions(buttonNode){
    let placeNode = buttonNode.parentNode;
    placeNode.parentNode.removeChild(placeNode);
}

function saveFormQuestions(){
    let data = [];

    for(let questionTypeNode of allQuestions.querySelectorAll(".questionType")){
        let questionsJson = [];
        let questionTypeJson = {"questions": questionsJson};
        data.push(questionTypeJson);

        for(let questionNode of questionTypeNode.querySelectorAll("input")){
            questionsJson.push({"text": questionNode.value})
        }
    }

    makeAPIRequest("admin/setQuestions", {"questions": data, "lang": "FR"}, {"content": "json"})
}
