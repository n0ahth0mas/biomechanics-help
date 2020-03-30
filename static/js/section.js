//HTML items
const scoreCounter = document.getElementById("scoreCounter");
const finalScore = document.getElementById("quiz-final-score");

//timer Setup
let TIMER;
const questionTime = 60; // 15s
const timeGauge = document.getElementById("timer_gauge");
let gaugeWidth = 200;
const gaugeUnit = gaugeWidth / questionTime;
const counter = document.getElementById("timer_time");
var count = 1;

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
}

function renderCounter(){
    if(count<questionTime){
        counter.innerHTML = count;
        timeGauge.style.width = count * gaugeUnit + "px";
        count++;
    }
}