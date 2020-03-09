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

var questions = [];
var answerIdCounter = 0;



function makeQuestions(){
console.log(q_list);
    for(var i =0; i<q_list.length; i++){
        var question = new Object();
        question.qID = q_list[i][0];
        question.text = q_list[i][1];
        question.type = q_list[i][5];
        question.imgSrc = "/static/img/question.png"
        question.answers = makeAnswers(q_list[i][0]);
        questions.push(question);
    }
    lastQuestion = questions.length-1
}

var aIDIndex = 0;
var aCorrectness = 2;
var aText = 3;
var aReasoning = 4;

function makeAnswers(qID){
    var answerList = [];
        for(var i = 0; i<a_list[answerIdCounter].length; i++){
            var answer = new Object();
            answer.aID = a_list[answerIdCounter][i][0];
            answer.qID = qID;
            answer.correct = a_list[answerIdCounter][i][2];
            answer.text = a_list[answerIdCounter][i][3];
            answer.reasoning = a_list[answerIdCounter][i][4];
            answerList.push(answer);
        }
    answerIdCounter++;
    return answerList;
}



// create some variables

var lastQuestion;
let runningQuestion = 0;
let count = 0;
const questionTime = 60; // 15s
const gaugeWidth = 150; // 150px
const gaugeUnit = gaugeWidth / questionTime;
let TIMER;
let score = 0;

var questionBubbles;

makeQuestions();

// render a question
function renderQuestion(){
    let q = questions[runningQuestion];

    question.innerHTML = "<p>"+ q.text +"</p>";
    qImg.innerHTML = "<a href= " + q.imgSrc + " data-fancybox > <img src=" + q.imgSrc + "/> </a>"

    if(firstAttempt) makeBubbles(q.answers);
}

function makeBubbles(answerList){
    questionBubbles = "";
    choices.innerHTML = "";
    for(var i=0; i<answerList.length; i++){
        var text = answerList[i].text;
        var choice = "<div class='choice' id= " +i + " onclick=checkAnswer(\""+i+"\")  data-toggle='modal' data-target='#answerModal'>"+ text+"</div>";
        console.log(choice);
        choices.innerHTML += choice;
    }
}

start.addEventListener("click",startQuiz);

// start quiz
function startQuiz(){
    scoreDiv.style.display = "none";
    start.style.display = "none";
    renderProgress();
    renderQuestion();
    quiz.style.display = "block";
    renderCounter();
    TIMER = setInterval(renderCounter,1000); // 1000ms = 1s
}

// render progress
function renderProgress(){
    console.log("running");
    progress.innerHTML = "";
    for(let qIndex = 0; qIndex <= lastQuestion; qIndex++){
    console.log(qIndex);
        progress.innerHTML += "<div class='prog' id="+ "button"+qIndex +"></div>";
        console.log("<div class='prog' id="+ "button "+qIndex +"></div>");
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

function checkAnswer(answerID){
    console.log(answerID);
    let currentAnswer = true
    var answerTruth;
    if(questions[runningQuestion].answers[answerID].correct.toLowerCase() == "true"){
        answerTruth = true;
        // answer is correct
        if (firstAttempt) score++;
        // change progress color to green
        answerIsClicked(currentAnswer, answerTruth, answerID);
        answerIsCorrect();
        firstAttempt = true;

    }else{
        answerTruth = false;
        // answer is wron
        // change progress color to red
        currentAnswer = false;
        firstAttempt = false;
        console.log("answerID is" + answerID);
        answerIsClicked(currentAnswer, answerTruth, answerID);
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
function answerIsClicked(correct, answer, i){
    if(correct){
        modalHead.innerHTML = "<p>Correct!<p>";
        pastAnswers = [];
    } else{
        modalHead.innerHTML = "<p>Incorrect<p>";
        console.log("i " + i);
        pastAnswers += i
    }
    modalBody.innerHTML = "<p>" + questions[runningQuestion].answers[i].reasoning + "</p>";
}


function changeColor(pastAnswers){
    for(i=0; i<pastAnswers.length; i++){
        var id =pastAnswers[i];
        document.getElementById(id).style.backgroundColor = "#808080"
        document.getElementById(id).style.pointerEvents = "#none"
        /*
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
        */
    }
}

function resetColor(){
    pastAnswers = [];

    for(i=0; i<questions[runningQuestion].answers.length; i++){
        document.getElementById(i).style.backgroundColor = "#ffffff"
        document.getElementById(i).style.pointerEvents = "auto";
    }
}


// answer is correct
function answerIsCorrect(){
    var color;
    if (firstAttempt) color = "#0f0";
    else color = "#FFA500";
    document.getElementById("button" + runningQuestion).style.backgroundColor = color;
    resetColor();
}

// answer is Wrong
function answerIsWrong(){
    document.getElementById("button" + runningQuestion).style.backgroundColor = "#f00";
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






/*
let questionsOLD = [
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
*/













