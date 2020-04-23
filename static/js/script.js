$("#drag-question-image").on("click", function(event) {
        console.log("called function");
        bounds=this.getBoundingClientRect();
        var left=bounds.left;
        var bottom=bounds.bottom;
        var x = event.pageX - left;
        var y = (event.pageY - bottom) * (-1);
        var cw=this.clientWidth
        var ch=this.clientHeight
        var iw=this.naturalWidth
        var ih=this.naturalHeight
        var px=x/cw*iw
        var py=y/ch*ih
        document.getElementById("click-x-coord").value = px.toFixed(2);
        document.getElementById("click-y-coord").value = py.toFixed(2);
        var drop_zone_img = this.parentElement.children[1];
        drop_zone_img.style.left = String((px/iw) * cw) + "px";
        drop_zone_img.style.bottom = String((py/iw) * cw) + "px";
        drop_zone_img.style.top = "unset";
});

$( "#start-quiz-button" ).on("click", function() {
    var this_question_header = document.getElementById("q_qs0");
    var drag_and_drop_answers = this_question_header.children;
    var this_question_img = document.getElementById("drop_zone_container0");
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
    var this_drop_zone_id = "drop_zone_container0";
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
        drop_zones[i].style.left = String((drop_zone_x_pos/img_natural_width) * img_width) + "px";
        drop_zones[i].style.bottom = String((drop_zone_y_pos/img_natural_height) * img_height) + "px";
        console.log("answer client Height: " + this_question_header.children[i].children[0].clientHeight);
        drop_zones[i].style.height = String(this_question_img.clientHeight * this_height_adjustment) + "px";
        drop_zones[i].style.width = String(this_question_img.clientWidth * this_width_adjustment) + "px";
    }
});

$( document ).ready(function() {
    if(document.getElementById("drag_n_drop_answer_img") !== null && document.getElementById("drag_n_drop_answer_img").style.display !== "none"){
        //then we know we should show the add answer modal
        document.getElementById("myModal").style.display = "block";
        //and we should also hide the answer image upload form and show the drag form
        document.getElementsByClassName("image-form")[0].style.display = "none";
        document.getElementsByClassName("drag-form")[0].style.display = "inline";
        document.getElementsByClassName("drag-answer-img-container")[0].style.display = "block";
        if(document.getElementById("drag-question-image") !== null){
            document.getElementById("drag_n_drop_answer_img").style.maxHeight = String(document.getElementsByClassName("drag-n-drop-img")[0].clientHeight) + "px";
        }else{
            document.getElementById("drag_n_drop_answer_img").style.maxHeight = String(document.getElementById("drag_n_drop_answer_img").naturalHeight) + "px";
            console.log(document.getElementById("drag_n_drop_answer_img").style.maxHeight);
            document.getElementsByClassName("drag-answer-img-container")[0].style.height = document.getElementById("drag_n_drop_answer_img").style.maxHeight;
        }
    }
    console.log("got this far");
    //reset select fields so that they cooperate
    var els = document.getElementsByClassName("reset_me");
    for (i = 0; i < els.length; i++) {
        els[i].value = els[i].getAttribute('value');
    }

});

function changedDropBoxSize(element){
    console.log(element.value);
    var percentage = Number(element.value) / 100.0;
    var answer_img = document.getElementById('drag_n_drop_answer_img');
    answer_img.style.height = String(answer_img.naturalHeight * percentage) + "px";
    answer_img.style.width = String(answer_img.naturalWidth * percentage) + "px";
    if(document.getElementById("drag-question-image") !== null){
        var question_img_height = Number(document.getElementById("drag-question-image").clientHeight);
        var question_img_width = Number(document.getElementById("drag-question-image").clientWidth);
        var answer_img_height = Number(document.getElementById('drag_n_drop_answer_img').clientHeight);
        var answer_img_width = Number(document.getElementById('drag_n_drop_answer_img').clientWidth);
        document.getElementById("adjusted-height-ratio").value = answer_img_height/question_img_height;
        document.getElementById("adjusted-width-ratio").value = answer_img_width/question_img_width;
    }else{
        document.getElementById("adjusted-height-ratio").value = percentage;
        document.getElementById("adjusted-width-ratio").value = percentage;
    }
}

function changeBorderColor(element){
    document.getElementById("drag_n_drop_answer_img").style.borderColor = String(element.value);
}