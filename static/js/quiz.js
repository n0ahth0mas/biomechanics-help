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

let firstAttempt = true;

//change answer storing and accessing to make things in a list

let pastAnswers = [];
// create our questions

var questions2 = [];
var answerIdCounter = 0;



function makeQuestions(){
    for(var i =0; i<q_list.length; i++){
        var question = new Object();
        question.qID = q_list[i][0];
        question.text = q_list[i][1];
        question.type = q_list[i][5];
        question.imgSrc = "/static/img/question.png"
        question.answers = makeAnswers(q_list[i][0]);
        questions2.push(question);
    }
    console.log(questions2);
}

var aIDIndex = 0;
var aCorrectness = 3;
var aText = 4;
var aReasoning = 5;

function makeAnswers(qID){
    var answerList = [];
        for(var i = 0; i<a_list[answerIdCounter].length; i++){
            var answer = new Object();
            answer.aID = a_list[answerIdCounter][i][aIDIndex];
            answer.qID = qID;
            answer.correct = a_list[answerIdCounter][i][aCorrectness];
            answer.text = a_list[answerIdCounter][i][aText];
            answer.reasoning = a_list[answerIdCounter][i][aReasoning];
            answerList.push(answer);
        }
    answerIdCounter++;
    return answerList;
}

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
const questionTime = 60; // 15s
const gaugeWidth = 150; // 150px
const gaugeUnit = gaugeWidth / questionTime;
let TIMER;
let score = 0;

makeQuestions();

// render a question
function renderQuestion(){
    //makeQuestions();
    let q = questions2[runningQuestion];

    question.innerHTML = "<p>"+ q.text +"</p>";
    qImg.innerHTML = "<a href= " + q.imgSrc + " data-fancybox > <img src=" + q.imgSrc + "/> </a>"
    choiceA.innerHTML = q.answers[0].text;
    choiceB.innerHTML = q.answers[1].text;
    //choiceC.innerHTML = q.answers[2].text;
    //choiceD.innerHTML = q.answers[3].text;
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
        resetColor();
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
    let currentAnswer = true
    if( answer == questions[runningQuestion].correct){
        // answer is correct
        if (firstAttempt) score++;
        // change progress color to green
        answerIsClicked(currentAnswer, answer);
        answerIsCorrect();
        firstAttempt = true;

    }else{
        // answer is wrong
        // change progress color to red
        currentAnswer = false;
        firstAttempt = false;
        answerIsClicked(currentAnswer, answer);
        changeColor(pastAnswers);
        answerIsWrong();

    }
    count = 0;
    if (currentAnswer){
        if(runningQuestion < lastQuestion){
            runningQuestion++;
            renderQuestion();
        }else{
            // end the quiz and show the score
            clearInterval(TIMER);
            scoreRender();
        }
    } else {
        renderQuestion();
    }
}

// provides feedback on clicked answer
function answerIsClicked(correct, answer){
    if(correct){
        modalHead.innerHTML = "<p>Correct!<p>";
        pastAnswers = [];
    } else{
        modalHead.innerHTML = "<p>Incorrect<p>";
        pastAnswers += answer
    }

    if(answer == "A") modalBody.innerHTML = "<p>" + questions[runningQuestion].reasoning.A + "</p>";
    else if(answer == "B") modalBody.innerHTML = "<p>" + questions[runningQuestion].reasoning.B + "</p>";
    else if(answer == "C") modalBody.innerHTML = "<p>" + questions[runningQuestion].reasoning.C + "</p>";
    else modalBody.innerHTML = "<p>" + questions[runningQuestion].reasoning.D + "</p>";
}


function changeColor(pastAnswers){
    for(i=0; i<pastAnswers.length; i++){
        if (pastAnswers[i] == "A"){
            choiceA.style.backgroundColor ="#808080"
            choiceA.style.pointerEvents = "none";
        } else if (pastAnswers[i] == "B"){
            choiceB.style.backgroundColor ="#808080"
            choiceB.style.pointerEvents = "none";
        } else if (pastAnswers[i] == "C"){
            choiceC.style.backgroundColor ="#808080"
            choiceC.style.pointerEvents = "none";
        } else {
            choiceD.style.backgroundColor ="#808080"
            choiceD.style.pointerEvents = "none";
        }
    }
}

function resetColor(){
    pastAnswers = "";

    choiceA.style.backgroundColor ="#ffffff";
    choiceB.style.backgroundColor ="#ffffff";
    choiceC.style.backgroundColor ="#ffffff";
    choiceD.style.backgroundColor ="#ffffff";

    choiceA.style.pointerEvents = "auto";
    choiceB.style.pointerEvents = "auto";
    choiceC.style.pointerEvents = "auto";
    choiceD.style.pointerEvents = "auto";
}


// answer is correct
function answerIsCorrect(){
    if (firstAttempt) document.getElementById(runningQuestion).style.backgroundColor = "#0f0";
    else document.getElementById(runningQuestion).style.backgroundColor = "#FFA500";
    resetColor();
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
    scoreDiv.innerHTML += "<p> You got "+ scorePerCent +"% correct on the first try</p>";
    scoreDiv.innerHTML += "<button type=\"button\" id=\"retryBtn\" onclick=\"restart()\">Retry</button>"
}

//restart the quiz by resetting all of the data
function restart(){
    score = 0;
    runningQuestion = 0;
    count = 0;
    startQuiz();
}




















