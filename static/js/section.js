//HTML items
const scoreCounter = document.getElementById("scoreCounter");
const finalScore = document.getElementById("quiz-final-score");
const progressDiv = document.getElementById("prog_bub");
const totalIndex = progressDiv.childElementCount-1;
const enlargeBtn = document.getElementById("enlarge");

const modalHead = document.getElementById("modal-header");
const modalBody = document.getElementById("modal-body");

//timer Setup
let TIMER;
const questionTime = 60; // total seconds
let gaugeWidth = 200;
const counter = document.getElementById("timer_time");
var count = 1;

var questionIndex = 0;

var firstTry = 0;


var correctSubmitCount = 0;

//TO RESET AFTER QUESTIONS
var init=true;
var numCorrect = 0
var tries = 0;
var buttonIDs = [];
var selectedButtons = [];
var greyedOut = [];

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
    enlargeBtn.style.display = "none"
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
    renderDropBoxQuestion();
    //render point and click question if first
    var point_and_click_question_img = document.getElementById("point-click-question-img" + String(questionIndex));
    if(point_and_click_question_img !== null){
        //the first question is a point and click question
        point_and_click_question_img.className = "active_point_n_click big-section-img";
    }
}

function renderQuestion(){
    console.log(document.getElementById("q_qs"+questionIndex));
    document.getElementById("q_qs"+questionIndex).style.display = "flex";
    document.getElementById("q_header"+questionIndex).style.display = "flex";
    if(document.getElementById("q_img_container"+questionIndex) !== null){
        document.getElementById("q_img_container"+questionIndex).style.display = "flex";
    }
    if(document.getElementById("mcSubmit"+questionIndex)!= null){
        enlargeBtn.style.display = "flex"
    }
}

function popImageModal(){
    modalHead.innerHTML= "<h4>Answer Images for Question " + (questionIndex+1) +"</h4>"
    modalBody.innerHTML="Click images to enlarge them.<br><br>"
    var answers = document.getElementById("answers"+questionIndex).children
    for(var i =0; i<=answers.length-1; i++){
        console.log("img"+questionIndex+"."+i)
        if(typeof(document.getElementById("img"+questionIndex+"."+i)) != 'undefined' && document.getElementById("img"+questionIndex+"."+i) != null){
            img = document.getElementById("img"+questionIndex+"."+i).src
         modalBody.innerHTML+= "Answer " + (i+1) +": <a href= " + img + " data-fancybox><img src=" + img + " class='mcImg' /> </a>"
     }
    }
}

function removePrevious(){
    document.getElementById("q_qs"+questionIndex).style.display = "none";
    document.getElementById("q_header"+questionIndex).style.display = "none";
    if(document.getElementById("q_img_container"+questionIndex) !== null){
        document.getElementById("q_img_container"+questionIndex).style.display = "none";
    }
    questionIndex++;
    counter.innerHTML = 60;
    count = 1;
}

function progress(correct){
    var color;
    if(correct){
        if (tries == 0){
            color = "#0f0"; //chg color to green
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
// gets number of right answers
function initQs(buttonID){
console.log("running Init")
    for(var i=0; i<document.getElementById(buttonID).parentElement.children.length; i++){
        if(document.getElementById(buttonID).parentElement.children[i].value ==1) numCorrect++;
    }
    init = false;
}

//checks if button has been selected
function toggleSelected(buttonID, button, reason, correctness, text){
    if (init) initQs(buttonID)

    if(buttonIDs.includes(buttonID)){
        var index= buttonIDs.indexOf(buttonID);
        buttonIDs.splice(index, 1);
        selectedButtons.splice(index, 1);
        document.getElementById(buttonID).className = "mult_choice";
    } else{
        buttonIDs.push(buttonID);
        selectedButtons.push([buttonID, button, reason, correctness, text]);
        document.getElementById(buttonID).className = "selected";
    }
}

function checkMultChoice(){
    var truth = true;
    var correctChoice = 0
    var innerModalWrong = []
    var innerModalCorrect = []

    for(var i=0; i<selectedButtons.length; i++){
       truth = truth && (selectedButtons[i][3] == 1)
       if(selectedButtons[i][3] == 0){
            innerModalWrong.push("<h4>" + selectedButtons[i][4]+":</h4>");
            innerModalWrong.push("<p>"+ selectedButtons[i][2] + "<p>");
            document.getElementById(selectedButtons[i][0]).className = "disabled";
            greyedOut.push(selectedButtons[i][0])
       } else{
            innerModalCorrect.push("<h4>" + selectedButtons[i][4]+":</h4>");
            innerModalCorrect.push("<p>"+ selectedButtons[i][2] + "<p>");
            document.getElementById(selectedButtons[i][0]).className = "mult_choice"
            correctChoice++
       }
    }

    truth = truth && (selectedButtons.length>=1)
    progress(truth)
    if(truth && (numCorrect == correctChoice)){
        if (tries==0) firstTry++;
        modalHead.innerHTML = "<h3>Correct!</h3>"
        modalBody.innerHTML = "<p>Here's why your answers were correct</p>"
        for(var i=0; i<=innerModalCorrect.length-1; i++){
            console.log(innerModalCorrect[i])
            modalBody.innerHTML += innerModalCorrect[i]
        }
        console.log(greyedOut);
        for(var i=0; i<greyedOut.length; i++){
            document.getElementById(greyedOut[i]).className = "mult_choice"
        }
        nextQuestion();
    }else {
        if(correctChoice == 0){
            modalHead.innerHTML = "<h3>Incorrect<h3>"
            modalBody.innerHTML = "<p> Here's why the answers you selected are incorrect </p>"
        } else{
            modalHead.innerHTML = "<h3>Partially Correct!<h3>"
            modalBody.innerHTML = "<p>You got " + correctChoice + " out of " + numCorrect +". If it looks like you got all of the answers right, that means you selected a wrong answer somewhere! If you didn't find all of the correct answers, why don't you try again!</p>"
        }
        for(var i=0; i<=innerModalWrong.length-1; i++){
            console.log(innerModalWrong[i])
            modalBody.innerHTML += innerModalWrong[i]
        }
        tries++;
        buttonIDs = [];
        selectedButtons = [];
        innerModalWrong = [];
        innerModalCorrect = [];
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
  var answer_parent = document.getElementById(data).parentElement.parentElement;
  console.log(answer_parent);
  var drop_zone_index = String(element.id).replace("drop_element", "");
  drop_zone_index = Number(drop_zone_index);
  var answer_element_index = String(data).split(":").pop();
  answer_element_index = Number(answer_element_index);
  console.log(answer_element_index);
  var drop_zone_container = element.parentElement;
  var drop_zones = [].slice.call(drop_zone_container.children);
  drop_zones.pop();
  var this_reason = String(element.children[2].innerHTML);
  if(answer_element_index === drop_zone_index){
    //then we know that we have dragged the right answer onto the right drop zone
    correctSubmitCount++;
    //ask if we are done with this question
    //if the correntSubmitCount is equal to the total number of drop zones then we know that we have finished this question
    console.log("correctSubmitCount: " + correctSubmitCount);
    console.log("drop_zones.length: " + drop_zones.length);
    ev.target.appendChild(document.getElementById(data));
    if(correctSubmitCount === drop_zones.length){
        modalHead.innerHTML = "<h4>Correct! You finished the problem!</h4>";
        modalBody.innerHTML = this_reason;
        progress(true);
        //need to reset the question elements
        console.log(answer_parent.children.length);
        var answer_containers = answer_parent.getElementsByClassName("drag_answer_container_div");
        for(i=0; i < drop_zones.length;i++){
            (function (i) {
                var drag_element = drop_zones[i].children[drop_zones[i].children.length - 1];
                //need this drag elements index
                var this_answer_img_index = Number(String(drag_element.id).split(":").pop());
                console.log("this drag answer index: " + this_answer_img_index);
                //answer_parent.insertBefore(drag_element, answer_parent.children[0]);
                answer_containers[i].insertBefore(drag_element, answer_containers[i].children[0]);
            })(i);
        }
        correctSubmitCount = 0;
        if(tries === 0){
            firstTry++;
        }
        $('#myModal').modal('show');
        nextQuestion();
    }else{
        modalHead.innerHTML = "<h4>Correct!</h4>";
        modalBody.innerHTML = this_reason;
    }
  }else{
    //then we just dragged the wrong answer onto this drop zone
    //for now just make this wrong
    progress(false);
    modalHead.innerHTML = "<h4>Incorrect!</h4>";
    modalBody.innerHTML = "Let's try that again!";
    tries++;
  }
  $('#myModal').modal('show');
}

function submitShortAnswer(submitButton, answerList){
    var correct = false;
    var enteredVal = ""
    for(var i=0; i<=answerList.length-1; i++){
        console.log(answerList[i])
        var includes = ((submitButton.parentElement.children[0].value.toLowerCase()).includes(answerList[i][0].toLowerCase()))
        if (includes){
            enteredVal=i;
            correct = true
            break;
        }
    }
    progress(correct);
    if(correct){
        if(tries == 0) firstTry++;
        console.log(firstTry)
        console.log("correct");
        modalHead.innerHTML = "<h4>Correct!</h4>";
        modalBody.innerHTML = "Your answer is correct because: " + answerList[enteredVal][1];
        if(answerList.length > 1){
            modalBody.innerHTML += "<br><br>Other possible answers include:<br>";
            for(var i=0; i<=answerList.length-1; i++){
                if (i!= enteredVal) modalBody.innerHTML += (answerList[i][0] + "<br>");
            }
        }
        nextQuestion();
    }else if( tries>=2){
        console.log("last Try");
        modalHead.innerHTML = "<h4>Hmm, seems like you're stuck here.</h4>";
        modalBody.innerHTML = "Here are possible answers and reasons for why they are correct:<br>"
        for(var i=0; i<=answerList.length-1; i++){
            modalBody.innerHTML += answerList[i][0] +": " + answerList[i][1]+"<br>"
        }
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
    var this_question_header = document.getElementById("q_qs" + questionIndex);
    var drag_and_drop_answers = this_question_header.children;
    var this_question_img = document.getElementById("drop_zone_container" + questionIndex);
    if(this_question_img !== null){
        this_question_img = this_question_img.children[this_question_img.children.length-1];
        for(j = 0; j < drag_and_drop_answers.length; j++){
            var this_height_percentage = Number(drag_and_drop_answers[j].children[1].innerHTML);
            var this_width_percentage = Number(drag_and_drop_answers[j].children[2].innerHTML);
            var this_answer_img = drag_and_drop_answers[j].children[0];
            var this_answer_correctness = drag_and_drop_answers[j].children[3].innerHTML;
            //if this answer is true
            if(this_answer_correctness === '1'){
                console.log("thinks this one is correct");
                this_answer_img.style.height = String(this_question_img.clientHeight * this_height_percentage) + "px";
                console.log("set answer image height to: " + this_answer_img.style.height);
                this_answer_img.style.width = String(this_question_img.clientWidth * this_width_percentage) + "px";
            }else{
                console.log("thinks this one is wrong");
                //otherwise just apply the percentage and ignore the question image
                console.log("height percent: " + this_height_percentage);
                console.log("width percent: " + this_width_percentage);
                console.log(this_answer_img.naturalHeight);
                console.log(this_answer_img.naturalWidth);
                this_answer_img.style.height = String(this_answer_img.naturalHeight * this_height_percentage) + "px";
                this_answer_img.style.width = String(this_answer_img.naturalWidth * this_width_percentage) + "px";
                console.log(this_answer_img.style.height);
                console.log(this_answer_img.style.width);
            }
        }
        //put drop zones in the right position
        var this_drop_zone_id = "drop_zone_container" + String(questionIndex);
        var drop_zone_container = document.getElementById(this_drop_zone_id);
        var drop_zones = [].slice.call(drop_zone_container.children)
        drop_zones.pop();
        for(i = 0; i < drop_zones.length;i++){
            var drop_zone_x_pos = Number(drop_zones[i].children[0].innerHTML);
            var drop_zone_y_pos = Number(drop_zones[i].children[1].innerHTML);
            var this_question_image = drop_zones[i].parentElement.children[drop_zones[i].parentElement.children.length-1];
            var img_natural_width = this_question_image.naturalWidth;
            var img_natural_height = this_question_image.naturalHeight;
            this_question_image = this_question_image.parentElement;
            var img_width = this_question_image.clientWidth;
            var img_height = this_question_image.clientHeight;
            var this_height_adjustment = Number(drop_zones[i].children[3].innerHTML);
            var this_width_adjustment = Number(drop_zones[i].children[4].innerHTML);
            var this_drop_zone_color = drop_zones[i].children[5].innerHTML;
            drop_zones[i].style.borderColor = this_drop_zone_color;
            drop_zones[i].style.left = String((drop_zone_x_pos/img_natural_width) * img_width) + "px";
            drop_zones[i].style.bottom = String((drop_zone_y_pos/img_natural_height) * img_height) + "px";
            console.log("answer client Height: " + this_question_header.children[i].children[0].clientHeight);
            drop_zones[i].style.height = String(this_question_img.clientHeight * this_height_adjustment) + "px";
            drop_zones[i].style.width = String(this_question_img.clientWidth * this_width_adjustment) + "px";
        }
    }
}

function nextQuestion(){
    tries = 0;
    init= true;
    numCorrect = 0
    buttonIDs = [];
    selectedButtons = [];
    //modalBody.innerHTML = "";
    //modalHead.innerHTML= "";
    var current_point_and_click_question_img = document.getElementById("point-click-question-img" + String(questionIndex));
    if(current_point_and_click_question_img !== null){
        console.log(current_point_and_click_question_img);
        current_point_and_click_question_img.className = "point-n-click-img big-section-img";
    }
    if(questionIndex< totalIndex){
        //this represents the next point and click question
        var point_and_click_question_img = document.getElementById("point-click-question-img" + String(questionIndex + 1));
        if(point_and_click_question_img !== null){
            point_and_click_question_img.className = "active_point_n_click big-section-img";
        }
        enlargeBtn.style.display = "none"
        //we also want to hide the current point and click image
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

function clickedPointAndClickQ(event, question_image){
    bounds=question_image.getBoundingClientRect();
    var left=bounds.left;
    var bottom=bounds.bottom;
    var x = event.pageX - left;
    var y = (event.pageY - bottom) * (-1) + $(window).scrollTop();
    console.log("x: " + x);
    //console.log();
    console.log("y: " + y);
    //we need to check and make sure that our x and y fall in one of our answers
    //if this answer is wrong, let them know and say why
    //same for if they are right but instead we move on
    var info_by_answer = document.getElementById("answer-zone-deets" + questionIndex).children;
    for(i = 0; i < info_by_answer.length;i++){
        var this_answer_details = info_by_answer[i].children;
        var this_box_x_local_position = (Number(this_answer_details[0].innerHTML)/question_image.naturalWidth) * question_image.clientWidth;
        var this_box_y_local_position = (Number(this_answer_details[1].innerHTML)/question_image.naturalHeight) * question_image.clientHeight;
        var this_box_width_ratio = Number(this_answer_details[3].innerHTML);
        var this_box_height_ratio = Number(this_answer_details[4].innerHTML);
        var this_answer_correctness = this_answer_details[5].innerHTML;
        var this_answer_reason = this_answer_details[2].innerHTML;
        //in pixels
        console.log(question_image.clientWidth);
        var this_box_height = question_image.clientHeight * this_box_height_ratio;
        var this_box_width = question_image.clientWidth * this_box_width_ratio;
        console.log("this box local x position: " + this_box_x_local_position);
        console.log("this box local y postiion: " + this_box_y_local_position);
        console.log("this box width: " + this_box_width);
        console.log("this box height: " + this_box_height);
        //for the click to be inside our bounds it must be greater than our box's local x and y but less than its width and height plus those respective values
        if(this_box_x_local_position < x && this_box_y_local_position < y && (this_box_x_local_position + this_box_width) > x && (this_box_y_local_position + this_box_height) > y){
            //now we want to let the student know whether they got the answer correct and why
            if(this_answer_correctness === '1'){
                //they have clicked the right place
                if(tries === 0){
                    //they got it right on the first try
                    $('#myModal').find('#modal-header').html("<h4>Correct!</h4>");
                    $('#myModal').find('#modal-body').html(this_answer_reason);
                    $('#myModal').modal('show');
                    firstTry++;
                    progress(true);
                    nextQuestion();
                }else{
                    //they got it right but not on the first try
                    $('#myModal').find('#modal-header').html("<h4>Correct!</h4>");
                    $('#myModal').find('#modal-body').html(this_answer_reason);
                    $('#myModal').modal('show');
                    progress(true);
                    nextQuestion();
                }
            }else{
                //they have clicked the wrong place
                $('#myModal').find('#modal-header').html("<h4>Incorrect!</h4>");
                $('#myModal').find('#modal-body').html("Let's try that again!");
                $('#myModal').modal('show');
                tries++;
                progress(false);
            }
        }
    }
}