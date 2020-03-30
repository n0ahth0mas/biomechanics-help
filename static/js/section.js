//HTML items
const scoreCounter = document.getElementById("scoreCounter");
const finalScore = document.getElementById("quiz-final-score");

//timer Setup
let TIMER;
const questionTime = 60; // 15s
let gaugeWidth = 200;
const counter = document.getElementById("timer_time");
var count = 1;

var currentQuestion=0;

/* QUIZ */
function submitMultipleChoiceAnswer(button, truthValue, reason, buttonID){
    if(truthValue === 'True'){
        scoreCounter.innerHTML = String(Number(String(document.getElementById("scoreCounter").innerHTML)) + 1);
        alert("correct!");
    }else{
        document.getElementById(buttonID).className = "disabled";
        alert(reason);
    }
    //nextQuestion(button.parentElement);
}

function submitShortAnswer(input, answer){

    if(String(answer).includes(String(input.previousElementSibling.value))){
        scoreCounter.innerHTML = String(Number(String(document.getElementById("scoreCounter").innerHTML)) + 1);
        alert("correct!");
    }else{
        alert("wrong!");
    }
    nextQuestion(input.parentElement);
}

function nextQuestion(currentQuestion){
    if(currentQuestion.nextElementSibling != null){
        currentQuestion.style.display = "none";
        currentQuestion.nextElementSibling.style.display = "block";
    }else{
        finalScore.parentElement.style.display = "block";
        finalScore.innerHTML = String((parseFloat(document.getElementById("scoreCounter").innerHTML) / parseFloat(document.getElementById("quizLength").innerHTML)) * 100) + "%";
    }
}

function startQuiz(){
    document.getElementById("questions").style.display = "flex"
    document.getElementById("header").style.display = "none"
    TIMER = setInterval(renderCounter, 1000)

    //basically my idea starts here, so you would theoretically be able to access the question data in a list and get the first question
    renderQuestion(0)
}

//and then this would make the html elements visible based on the question id, and every time a person went on to a new question it would be re-rendered
function renderQuestion(questionID){
}


function renderCounter(){
    if(count<questionTime){
        counter.innerHTML = questionTime - count;
        count++;
    } else{
        nextQuestion()
    }
}