function submitMultipleChoiceAnswer(button, truthValue, reason){
    if(truthValue === 'True'){
        document.getElementById("scoreCounter").innerHTML = String(Number(String(document.getElementById("scoreCounter").innerHTML)) + 1);
        alert("correct!");
    }else{
        alert(reason);
    }
    nextQuestion(button.parentElement);
}

function submitShortAnswer(input, answer){

    if(String(answer).includes(String(input.previousElementSibling.value))){
        document.getElementById("scoreCounter").innerHTML = String(Number(String(document.getElementById("scoreCounter").innerHTML)) + 1);
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
        document.getElementById("quiz-final-score").parentElement.style.display = "block";
        document.getElementById("quiz-final-score").innerHTML = String((parseFloat(document.getElementById("scoreCounter").innerHTML) / parseFloat(document.getElementById("quizLength").innerHTML)) * 100) + "%";
    }
}