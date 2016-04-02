/**
 * Created by xiaoyan on 01/04/2016.
 */
$(document).ready(function(){

    $("#about-btn").click
    ( function(event){
        alert("you clicked the button using JQuery");
    });
    $(".ouch").click( function(event) {
           alert("You clicked me! ouch!");
    });

    $("p").hover( function() {
            $(p).css('color', 'red');
    },
    function() {
            $(this).css('color', 'blue');
    });
    $("#about-btn").addClass('btn btn-primary')

    $("#about-btn").click( function(event) {
    msgstr = $("#msg").html()
        msgstr = msgstr + "o"
        $("#msg").html(msgstr)
 });
});