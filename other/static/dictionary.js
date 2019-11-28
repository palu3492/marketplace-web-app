
let popupElement, titleElement, defElement;
function documentLoaded(){
    popupElement = document.getElementById('outer-def');
    titleElement = document.getElementById('title');
    defElement = document.getElementById('definition');
    initWordBoxes();
    create();
}
let div;
function create(){
    div = document.createElement('div');
    div.id = 'black-bg';
    let body = document.getElementsByTagName('body')[0];
    body.appendChild(div);
}

function initWordBoxes(){
    let wordBoxes = document.getElementsByClassName('wordbox');
    let wordBox;
    for(let i=0; i<wordBoxes.length; i++) {
        wordBox = wordBoxes[i];
        wordBox.addEventListener('click', wordClicked);
    }
}

function wordClicked(e){
    let word = e.target.innerText;
    requestDefinition(word);
}

function requestDefinition(word){
    let url = '/definition?word='+word;
    let request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4) {
            if(this.status === 200) {
                definitionReceived(this.responseText, word);
            }else if(this.response == null && this.status === 0) {
                console.log("Error 1");
            }else{
                console.log("Error 2");
            }
        }
    };
    request.open("GET", url, true);
    request.send(null);
}

function definitionReceived(definition, word){
    titleElement.innerHTML = 'Definition of the word <b>' + word + '</b>';
    defElement.innerHTML = definition;
    openPopup();
}

function openPopup(){
    popupElement.style.display = 'block';
    div.style.display = 'block';
}

function closePopup(){
    popupElement.style.display = 'none';
    div.style.display = 'none';
}