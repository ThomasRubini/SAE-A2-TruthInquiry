//functions for places.html

function addNewInputPlaces(){
    let newPlace = places.lastElementChild.cloneNode(true);
    newPlace.id = "";
    newPlace.querySelector("input").value = "";
    places.appendChild(newPlace);
}

function deletePlace(buttonNode){
    let placeNode = buttonNode.parentNode;
    placeNode.parentNode.removeChild(placeNode);
}

function saveForm(){
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


function addNewInputTraits(){
    let newTrait = traits.lastElementChild.cloneNode(true);
    newTrait.id = "";
    newTrait.querySelector(".name_input").value = "";
    newTrait.querySelector(".desc_input").value = "";
    traits.appendChild(newTrait);
}

function deleteTrait(buttonNode){
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