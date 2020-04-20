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
    //put drop zones in the right position
    var this_drop_zone_id = "drop_zone_container" + String(0);
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
        drop_zones[i].style.left = String((drop_zone_x_pos/img_natural_width) * img_width) + "px";
        drop_zones[i].style.bottom = String((drop_zone_y_pos/img_natural_height) * img_height) + "px";
    }

});

$( document ).ready(function() {
    if(drag_n_drop_answer_img.style.display !== "none"){
        //then we know we should show the add answer modal
        document.getElementById("myModal").style.display = "block";
        //and we should also hide the answer image upload form and show the drag form
        document.getElementsByClassName("image-form")[0].style.display = "none";
        document.getElementsByClassName("drag-form")[0].style.display = "inline";
        document.getElementsByClassName("drag-answer-img-container")[0].style.display = "block";
        document.getElementById("drag_n_drop_answer_img").style.maxHeight = String(document.getElementsByClassName("drag-n-drop-img")[0].clientHeight) + "px";
    }
});

function changedDropBoxSize(element){
    console.log(element.value);
    var percentage = Number(element.value) / 100.0;
    var answer_img = document.getElementById('drag_n_drop_answer_img');
    answer_img.style.height = String(answer_img.naturalHeight * percentage) + "px";
    answer_img.style.width = "auto";
}

function changeBorderColor(element){
    document.getElementById("drag_n_drop_answer_img").style.borderColor = String(element.value);
}