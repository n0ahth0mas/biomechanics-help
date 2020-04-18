//HTML items
const scoreCounter = document.getElementById("scoreCounter");
const finalScore = document.getElementById("quiz-final-score");
const progressDiv = document.getElementById("prog_bub");
const totalIndex = progressDiv.childElementCount-1;

const modalHead = document.getElementById("modal-header");
const modalBody = document.getElementById("modal-body");

//timer Setup
let TIMER;
const questionTime = 60; // total seconds
let gaugeWidth = 200;
const counter = document.getElementById("timer_time");
var count = 1;

var questionIndex = 0;
var tries = 0;
var firstTry = 0;

var buttonIDs = [];
var correctSubmitCount = 0;
//RENDERING

function startQuiz(){

    document.getElementById("questions").style.display = "flex"
    document.getElementById("header").style.display = "none"
    TIMER = setInterval(renderCounter, 1000);
    renderQuestion();
}

function restart(){
    removePrevious();
    document.getElementById("questions").style.display = "flex"
    document.getElementById("header").style.display = "none"
    for(i=0; i<questionIndex; i++){
        document.getElementById("progress" + i).style.background = "#FFFFFF";
    }
    for(i=0; i<buttonIDs.length; i++){
        document.getElementById(buttonIDs[i]).className = "mult_choice";
    }
    firstTry=0;
    tries=0;
    questionIndex=0;
    renderQuestion();
}

function renderQuestion(){
    console.log(document.getElementById("q_qs"+questionIndex));
    document.getElementById("q_qs"+questionIndex).style.display = "flex";
    document.getElementById("q_header"+questionIndex).style.display = "flex";
    document.getElementById("q_img_container"+questionIndex).style.display = "flex";

}

function removePrevious(){
    document.getElementById("q_qs"+questionIndex).style.display = "none";
    document.getElementById("q_header"+questionIndex).style.display = "none";
    document.getElementById("q_img_container"+questionIndex).style.display = "none";
    questionIndex++;
    counter.innerHTML = 60;
    count = 1;
}

function progress(correct){
    var color;
    if(correct){
        if (tries == 0){
            color = "#0f0"; //chg color to green
            console.log(firstTry)
            firstTry++
        }
        else color = "#FFA500"; //change to orange
    } else color = "#f00"; //chg color to red
    console.log("progress" +questionIndex);
    console.log(document.getElementById("progress" + questionIndex));
    document.getElementById("progress" + questionIndex).style.background = color;
}

function renderCounter(){
    if(count<questionTime){
        counter.innerHTML = questionTime - count;
        count++;
    } else{
        nextQuestion();
    }
}

/* QUIZ */
function submitMultipleChoiceAnswer(truthValue, reason, buttonID, button){
    if(truthValue == '1'){
        correct = true;
    }else{
        correct = false;
    }
    progress(correct);
    if(correct){
        modalHead.innerHTML = "<h4>Correct!</h4>";
        modalBody.innerHTML = reason;
        nextQuestion();
    }else{
        document.getElementById(buttonID).className = "disabled";
        buttonIDs.push(buttonID);
        tries++;
        modalHead.innerHTML = "<h4>Incorrect!</h4>";
        modalBody.innerHTML = reason;
    }
}

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev, element) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  var answer_parent = document.getElementById(data).parentElement;
  var drop_zone_index = String(element.id).replace("drop_element", "");
  drop_zone_index = Number(drop_zone_index);
  var answer_element_index = String(data).replace("drag_element", "");
  answer_element_index = Number(answer_element_index);
  var drop_zone_container = element.parentElement;
  var drop_zone_count = (element.parentElement.children.length - 1)/3;
  if(answer_element_index === drop_zone_index){
    //then we know that we have dragged the right answer onto the right drop zone
    correctSubmitCount++;
    //ask if we are done with this question
    //if the correntSubmitCount is equal to the total number of drop zones then we know that we have finished this question
    if(correctSubmitCount === drop_zone_count){
        alert("Correct, you finished the question!");
        progress(true);
        //need to reset the question elements
        for(i=0; i < drop_zone_count;i++){
            (function (i) {
                console.log(i);
                var drag_element_id = String("drag_element" + (i+1));
                console.log(drag_element_id);
                var drag_element = document.getElementById(drag_element_id);
                answer_parent.appendChild(drag_element);
            })(i);
        }
        nextQuestion();
    }else{
        alert("Correct!");
    }
    ev.target.appendChild(document.getElementById(data));
  }else{
    //then we just dragged the wrong answer onto this drop zone
    //for now just make this wrong
    progress(false);
    alert("Wrong! You bad!");
    tries++;
  }
}

function submitShortAnswer(answer, submitButton, reason){
    var correct = (submitButton.parentElement.children[0].value).includes(answer)
    progress(correct);
    if(correct){
        if(tries == 1) firstTry++;
        console.log("correct");
        modalHead.innerHTML = "<h4>Correct!</h4>";
        modalBody.innerHTML = reason;
        nextQuestion();
    }else if( tries>=2){
        console.log("last Try");
        modalHead.innerHTML = "<h4>Hmm, seems like you're stuck here.</h4>";
        modalBody.innerHTML = "The answer is " + answer+". Here's why: " + reason;
        nextQuestion();
    } else{
        console.log("incorrect");
        modalHead.innerHTML = "<h4>Incorrect</h4>";
        modalBody.innerHTML = "Oops! Let's try this one again";
        tries++;
    }
    submitButton.parentElement.children[0].value=""
}

function renderDropBoxQuestion() {
    //put drop zones in the right position
    var drop_zones = document.getElementsByClassName("drop-zone");
    for(i = 0; i < drop_zones.length;i++){
        var drop_zone_x_pos = Number(document.getElementById("drop_element_x_pos" + String(i)).innerHTML);
        var drop_zone_y_pos = Number(document.getElementById("drop_element_y_pos" + String(i)).innerHTML);
        var this_question_image = drop_zones[i].parentElement.children[drop_zones[i].parentElement.children.length-1];
        var img_natural_width = this_question_image.naturalWidth;
        var img_natural_height = this_question_image.naturalHeight;
        //this_question_image.style.display = "flex";
        console.log(this_question_image.parentElement);
        this_question_image = this_question_image.parentElement;
        var img_width = this_question_image.clientWidth;
        var img_height = this_question_image.clientHeight;
        drop_zones[i].style.left = String((drop_zone_x_pos/img_natural_width) * img_width) + "px";
        drop_zones[i].style.bottom = String((drop_zone_y_pos/img_natural_height) * img_height) + "px";
    }
}

function nextQuestion(){
    if(questionIndex< totalIndex){
        console.log("next question");
        removePrevious();
        renderQuestion();
        renderDropBoxQuestion();
    }else{
        document.getElementById("questions").style.display = "none";
        document.getElementById("header").style.display = "flex";
        document.getElementById("header").innerHTML = "<h3>You got "+firstTry+" right on the first try, scoring "+ firstTry/(questionIndex+1)*100 +"%</h3>";
        document.getElementById("header").innerHTML +="<button class='mult_choice' onclick='restart()'>Try Again</button>";
        document.getElementById("next").style.display = "flex";
    }
}

/* SLIDESHOW */
var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}


function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("page_vid");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
      slides[i].pause();
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}

