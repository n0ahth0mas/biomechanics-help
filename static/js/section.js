//HTML items
const scoreCounter = document.getElementById("scoreCounter");
const finalScore = document.getElementById("quiz-final-score");
const progressDiv = document.getElementById("prog_bub");
const totalIndex = progressDiv.childElementCount-1;

//timer Setup
let TIMER;
const questionTime = 60; // total seconds
let gaugeWidth = 200;
const counter = document.getElementById("timer_time");
var count = 1;

var questionIndex = 0;
var tries = 0;
var firstTry = 0;

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
        nextQuestion()
    }
}

/* QUIZ */
function submitMultipleChoiceAnswer(truthValue, reason, buttonID){
    var correct = (truthValue.toLowerCase() === 'true');
    progress(correct);
    if(correct){
        alert("correct!");
        renderQuestion()
        nextQuestion();
    }else{
        document.getElementById(buttonID).className = "disabled";
        tries++;
        alert(reason);
    }
}

function submitShortAnswer(answer){
    console.log(answer);
    /**
    if((document.getElementById(shortInput).value).includes(answer[3])){
        //scoreCounter.innerHTML = String(Number(String(document.getElementById("scoreCounter").innerHTML)) + 1);
        alert(reason);
        nextQuestion();
    }else{
        alert("Oops! Let's try that one again.");
    }
    **/
}

function nextQuestion(){
    if(questionIndex< totalIndex){
        console.log("next question");
        removePrevious();
        renderQuestion();
    }else{
        document.getElementById("questions").style.display = "none"
        document.getElementById("header").style.display = "flex"
        document.getElementById("header").innerHTML = "<h3>You got "+firstTry+" right on the first try, scoring "+ (questionIndex +1)/firstTry*100 +"%</h3>"
        document.getElementById("header").innerHTML +="<button class='mult_choice' onclick='restart()'>Try Again</button>"
    }
}