/*
********************************
Variable Setup
********************************
*/

// elements of the HTML file

//popups
const modalHead = document.getElementById("modal-heading");
const modalBody = document.getElementById("modal-body");

//Quiz element/environment
const start = document.getElementById("start");
const quiz = document.getElementById("quiz");
const counter = document.getElementById("counter");
const timeGauge = document.getElementById("timeGauge");
const progress = document.getElementById("progress");
const scoreDiv = document.getElementById("scoreContainer");

//Individual question
const question = document.getElementById("question");
const qImg = document.getElementById("qImg");
var questionBubbles;

//Question and answer management
var tries = 0;
var pastAnswers = [];
var questions = [];
var answerIdCounter = 0;
var correctShort = "";

//functionality variables
var lastQuestion;
let runningQuestion = 0;
let count = 0;
const questionTime = 60; // 15s
const gaugeWidth = 150; // 150px
const gaugeUnit = gaugeWidth / questionTime;
let TIMER;
let score = 0;

/*
********************************
Question Creation
********************************
*/

//Question population
function makeQuestions(){
console.log(q_list);
    for(var i =0; i<q_list.length; i++){
        let question = new Object();
        question.qID = q_list[i][0];
        question.text = q_list[i][1];
        question.type = q_list[i][3];
        question.imgSrc = "/static/img/question.png"
        question.answers = makeAnswers(q_list[i][0]);
        questions.push(question);
    }
    lastQuestion = questions.length-1
}

//answer population
function makeAnswers(qID){
    let answerList = [];
        for(var i = 0; i<a_list[answerIdCounter].length; i++){
            let answer = new Object();
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

//make create question list
makeQuestions();

/*
********************************
Quiz Content Rendering
********************************
*/

//render a question, including variable amt of bubbles
function renderQuestion(){
    let q = questions[runningQuestion];

    question.innerHTML = "<p>"+ q.text +"</p>";
    qImg.innerHTML = "<a href= " + q.imgSrc + " data-fancybox > <img src=" + q.imgSrc + "/> </a>"

    if(firstAttempt && q.type.toLowerCase() == "quiz") makeBubbles(q.answers);
    else if(firstAttempt && q.type.toLowerCase() == "short") makeInput();
}

//create bubbles for the quiz type question
function makeBubbles(answerList){
    questionBubbles = "";
    choices.innerHTML = "";
    for(var i=0; i<answerList.length; i++){
        let text = answerList[i].text;
        let choice = "<div class='choice' id= " +i + " onclick=checkAnswer(\""+i+"\")  data-toggle='modal' data-target='#answerModal'>"+ text+"</div>";
        choices.innerHTML += choice;
    }
}

//create the input block for the short answer response
function makeInput(){
    choices.innerHTML = "";
    choices.innerHTML += "<input type='text' placeholder='Enter Answer Here' id='shortAns' name='shortAns'>"
    choices.innerHTML +=  "<button type='button' id='submitBtn' onclick='getInputValue()' data-toggle='modal' data-target='#answerModal'>Submit</button>"
}

//start quiz
start.addEventListener("click",startQuiz);
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
    }
}

// render counter
function renderCounter(){
    if(count <= questionTime){
        counter.innerHTML = count;
        timeGauge.style.width = count * gaugeUnit + "px";
        count++
    }else{
        count = 0;
        // change progress color to red
        progressColor(false);
        if(questions[runningQuestion].type.toLowerCase() == "quiz") resetColor();
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

/*
********************************
Answer Responses
********************************
*/

//get value sent from submit button, if short answer
 function getInputValue(){
    // Selecting the input element and get its value
    let inputVal = document.getElementById("shortAns").value;

    checkAnswer(inputVal);

    document.getElementById("shortAns").value = "";
}

//check answer
function checkAnswer(answerVal){
    let answerTruth = false;
    let changed = false;
    let tries = 0;
    if(questions[runningQuestion].type.toLowerCase() == "quiz"){
        answerTruth = (questions[runningQuestion].answers[answerVal].correct.toLowerCase() == "true");
    } else{
        if (tries >=3) choices.innerHTML +=  "<button type='button' id='skipBtn' onclick='nextQuestion()' data-toggle='modal' data-target='#answerModal'>Skip</button>"
        for(i=0; i<questions[runningQuestion].answers.length; i++){
            if(questions[runningQuestion].answers[i].correct.toLowerCase() == "true"){
                correctShort = questions[runningQuestion].answers[i].text;
                if(answerVal.toString().includes(correctShort)){
                    answerTruth = true;
                    answerVal = i;
                    changed = true;
                }
            }
        }
        if(!changed) answerVal = "none"
    }
    if(answerTruth){
        // answer is correct
        if (tries == 0) score++;
        answerIsClicked(answerTruth, answerVal);
    }else{
        // answer is wrong
        currentAnswer = false;
        tries++;
        answerIsClicked(answerTruth, answerVal);
        if(questions[runningQuestion].type.toLowerCase() == "quiz") changeColor(pastAnswers);
    }
    progressColor(answerTruth);
    count = 0;

    //if the answer is correct. . .
    if (answerTruth){
        tries = 0;
        //if the answer is correct and there are more questions/no more questions
        if(runningQuestion < lastQuestion){
        //move on to next question
            runningQuestion++;
            renderQuestion();
        }else{
            // end the quiz and show the score
            clearInterval(TIMER);
            scoreRender();
        }
    } else { //otherwise try again
        renderQuestion();
    }
}

// provides feedback on clicked answer
function answerIsClicked(answerTruth, i){
    if(answerTruth){
        modalHead.innerHTML = "<p>Correct!<p>";
        //reset the list of previous answers
        pastAnswers = [];
    } else{
        modalHead.innerHTML = "<p>Incorrect<p>";
        //add this bubble to the list of already answered questions
        pastAnswers += i
    }
    //provide feedback based on answer
    if(i === "none" && answerTruth) modalBody.innerHTML = "<p> Nice job! </p>";
    else if(i === "none") modalBody.innerHTML = "<p> That is incorrect, please try again </p>";
    else if(i === "skipped"){
        modalBody.innerHTML = "<p> The correct answer was " + correctShort + ". Try again next time!</p>";
        pastAnswers = [];
    }
    else modalBody.innerHTML = "<p>" + questions[runningQuestion].answers[i].reasoning + "</p>";
}

//grey out incorrect, already clicked answers
function changeColor(pastAnswers){
    for(i=0; i<pastAnswers.length; i++){
        let id =pastAnswers[i];
        document.getElementById(id).style.backgroundColor = "#808080"
        document.getElementById(id).style.pointerEvents = "#none"
    }
}

//changes the progress indicator based on whether or not the answer was correct
function progressColor(answerTruth){
    var color;
    //if the answer is correct
    if(answerTruth){
        if (tries ==0) color = "#0f0"; //chg color to green
        else color = "#FFA500"; //chg color to orange
        if(questions[runningQuestion].type.toLowerCase() == "quiz") resetColor();
    } else color = "#f00"; //chg color to red
    document.getElementById("button" + runningQuestion).style.backgroundColor = color;
}

//reset all
function resetColor(){
    pastAnswers = [];

    for(i=0; i<questions[runningQuestion].answers.length; i++){
        document.getElementById(i).style.backgroundColor = "#ffffff"
        document.getElementById(i).style.pointerEvents = "auto";
    }
}

/*
********************************
Results Screen
********************************
*/

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