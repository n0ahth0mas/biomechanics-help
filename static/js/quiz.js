// select all elements
const start = document.getElementById("start");
const quiz = document.getElementById("quiz");
const question = document.getElementById("question");
const qImg = document.getElementById("qImg");
const choiceA = document.getElementById("A");
const choiceB = document.getElementById("B");
const choiceC = document.getElementById("C");
const choiceD = document.getElementById("D");
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
        choiceA : "Correct",
        choiceB : "Wrong",
        choiceC : "Wrong",
        choiceD : "Wrong",
        reasoning : {A: 'this is correct', B:'this is incorrect', C:'this is incorrect', D: 'this is incorrect'},
        correct : "A"
    },{
        question : "What does CSS stand for?",
        imgSrc : "/static/img/question.png",
        choiceA : "Wrong",
        choiceB : "Correct",
        choiceC : "Wrong",
        choiceD : "Wrong",
        reasoning : {A: 'this is incorrect', B:'this is correct', C:'this is incorrect', D: 'this is incorrect'},
        correct : "B"
    },{
        question : "What does JS stand for?",
        imgSrc : "/static/img/question.png",
        choiceA : "Wrong",
        choiceB : "Wrong",
        choiceC : "Correct",
        choiceD : "Wrong",
        reasoning : {A: 'this is incorrect', B:'this is incorrect', C:'this is correct', D: 'this is incorrect'},
        correct : "C"
    }
];

// create some variables

const lastQuestion = questions.length - 1;
let runningQuestion = 0;
let count = 0;
const questionTime = 20; // 15s
const gaugeWidth = 150; // 150px
const gaugeUnit = gaugeWidth / questionTime;
let TIMER;
let score = 0;


// render a question
function renderQuestion(){
    let q = questions[runningQuestion];

    question.innerHTML = "<p>"+ q.question +"</p>";
    qImg.innerHTML = "<a href= " + q.imgSrc + " data-fancybox > <img src=" + q.imgSrc + "/> </a>"
    choiceA.innerHTML = q.choiceA;
    choiceB.innerHTML = q.choiceB;
    choiceC.innerHTML = q.choiceC;
    choiceD.innerHTML = q.choiceD;
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
    console.log("starting")
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
    if( answer == questions[runningQuestion].correct){
        // answer is correct
        score++;
        // change progress color to green
        answerIsClicked(true, answer);
        answerIsCorrect();

    }else{
        // answer is wrong
        // change progress color to red
        answerIsClicked(false, answer);
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
function answerIsClicked(correct, answer){
    if(correct){
        modalHead.innerHTML = "<p>Correct!<p>";
    } else{
        modalHead.innerHTML = "<p>Incorrect<p>";
    }

    if(answer == "A") modalBody.innerHTML = "<p>" + questions[runningQuestion].reasoning.A + "</p>";
    else if(answer == "B") modalBody.innerHTML = "<p>" + questions[runningQuestion].reasoning.B + "</p>";
    else if(answer == "C") modalBody.innerHTML = "<p>" + questions[runningQuestion].reasoning.C + "</p>";
    else modalBody.innerHTML = "<p>" + questions[runningQuestion].reasoning.D + "</p>";
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

//restart the quiz by resetting all of the data
function restart(){
    score = 0;
    runningQuestion = 0;
    count = 0;
    startQuiz();
}




















