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
});

$( "#start-quiz-button" ).on("click", function() {
    //put drop zones in the right position
    var drop_zones = document.getElementsByClassName("drop-zone");
    for(i = 0; i < drop_zones.length;i++){
        var drop_zone_x_pos = Number(document.getElementById("drop_element_x_pos" + String(i)).innerHTML);
        var drop_zone_y_pos = Number(document.getElementById("drop_element_y_pos" + String(i)).innerHTML);
        var this_question_image = drop_zones[i].parentElement.children[drop_zones[i].parentElement.children.length-1];
        var img_natural_width = this_question_image.naturalWidth;
        var img_natural_height = this_question_image.naturalHeight;
        //this_question_image.style.display = "flex";
        console.log(this_question_image.parentElement);
        this_question_image = this_question_image.parentElement;
        var img_width = this_question_image.clientWidth;
        var img_height = this_question_image.clientHeight;
        drop_zones[i].style.left = String((drop_zone_x_pos/img_natural_width) * img_width) + "px";
        drop_zones[i].style.bottom = String((drop_zone_y_pos/img_natural_height) * img_height) + "px";
    }

});