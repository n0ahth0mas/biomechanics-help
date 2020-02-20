// select all elements
const start = document.getElementById("start");
const quiz = document.getElementById("quiz");
const question = document.getElementById("question");
const qImg = document.getElementById("qImg");
const counter = document.getElementById("counter");
const timeGauge = document.getElementById("timeGauge");
const progress = document.getElementById("progress");
const scoreDiv = document.getElementById("scoreContainer");
const modalHead = document.getElementById("modal-heading");
const modalBody = document.getElementById("modal-body");

// create our questions
let questions = [
    {
        question : "What does HTML stand for?",
        imgSrc : "/static/img/question.png",
        reasoning : "this is the reasoning behind the answer",
        correct : "test"
    },{
        question : "What does CSS stand for?",
        imgSrc : "/static/img/question.png",
        reasoning : "this is the reasoning behind the answer",
        correct : "test"
    },{
        question : "What does JS stand for?",
        imgSrc : "/static/img/question.png",
        reasoning : "this is the reasoning behind the answer",
        correct : "test"
    }
];

//get value sent from submit button
 function getInputValue(){
    // Selecting the input element and get its value
    var inputVal = document.getElementById("shortAns").value;

    checkAnswer(inputVal);

    document.getElementById("shortAns").value = "";
}

// create some variables

const lastQuestion = questions.length - 1;
let runningQuestion = 0;
let count = 0;
const questionTime = 60; // 15s
const gaugeWidth = 150; // 150px
const gaugeUnit = gaugeWidth / questionTime;
let TIMER;
let score = 0;

// render a question
function renderQuestion(){
    let q = questions[runningQuestion];

   question.innerHTML = "<p>"+ q.question +"</p>";
   qImg.innerHTML = "<a href= " + q.imgSrc + " data-fancybox > <img src=" + q.imgSrc + "/> </a>"
}

start.addEventListener("click",startQuiz);

// start quiz
function startQuiz(){
    scoreDiv.style.display = "none";
    start.style.display = "none";
    renderQuestion();
    quiz.style.display = "block";
    renderProgress();
    renderCounter();
    TIMER = setInterval(renderCounter,1000); // 1000ms = 1s
}

// render progress
function renderProgress(){
    progress.innerHTML = ""
    for(let qIndex = 0; qIndex <= lastQuestion; qIndex++){
        progress.innerHTML += "<div class='prog' id="+ qIndex +"></div>";
    }
}

// counter render

function renderCounter(){
    if(count <= questionTime){
        counter.innerHTML = count;
        timeGauge.style.width = count * gaugeUnit + "px";
        count++
    }else{
        count = 0;
        // change progress color to red
        answerIsWrong();
        if(runningQuestion < lastQuestion){
            runningQuestion++;
            renderQuestion();
        }else{
            // end the quiz and show the score
            clearInterval(TIMER);
            scoreRender();
        }
    }
}

// checkAnswer

function checkAnswer(answer){
    if(answer.includes(questions[runningQuestion].correct)){
        // answer is correct
        score++;
        // change progress color to green
        answerIsClicked(true);
        answerIsCorrect();
    }else{
        // answer is wrong
        // change progress color to red
        answerIsClicked(false);
        answerIsWrong();
    }
    count = 0;
    if(runningQuestion < lastQuestion){
        runningQuestion++;
        renderQuestion();
    }else{
        // end the quiz and show the score
        clearInterval(TIMER);
        scoreRender();
    }
}

// provides feedback on clicked answer
function answerIsClicked(correct){
    if(correct){
        modalHead.innerHTML = "<p>Correct!<p>";
    } else{
        modalHead.innerHTML = "<p>Incorrect<p>";
    }

    modalBody.innerHTML = "<p>" + questions[runningQuestion].reasoning + "</p>";
}

// answer is correct
function answerIsCorrect(){
    document.getElementById(runningQuestion).style.backgroundColor = "#0f0";
}

// answer is Wrong
function answerIsWrong(){
    document.getElementById(runningQuestion).style.backgroundColor = "#f00";
}

// score render
function scoreRender(){
    scoreDiv.style.display = "block";

    // calculate the amount of question percent answered by the user
    const scorePerCent = Math.round(100 * score/questions.length);

    // choose the image based on the scorePerCent
    let img = (scorePerCent >= 80) ? "/static/img/5.png" :
              (scorePerCent >= 60) ? "/static/img/4.png" :
              (scorePerCent >= 40) ? "/static/img/3.png" :
              (scorePerCent >= 20) ? "/static/img/2.png" :
              "/static/img/1.png";

    scoreDiv.innerHTML = "<img src="+ img +">";
    scoreDiv.innerHTML += "<p>"+ scorePerCent +"%</p>";
    scoreDiv.innerHTML += "<button type=\"button\" id=\"retryBtn\" onclick=\"restart()\">Retry</button>"
}

function restart(){
    score = 0;
    runningQuestion = 0;
    count = 0;
    startQuiz();
}























