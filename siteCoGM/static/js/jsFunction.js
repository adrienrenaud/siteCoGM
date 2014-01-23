

///////////////////////////////////
//jquery style
/////////////////////////////////////////////////////////////


$(document).ready(function(){

    $("#header").click(function(){
        var theurl = "/CoGM/";
        $(location).attr('href',theurl);
    });
    
    //     $("#tocopy").click(function(){
    //     var theurl = "/CoGM/";
    //     $(location).attr('href',theurl);
    // });
    
    $('#tocopy').zclip({
        path: "http://www.steamdev.com/zclip/js/ZeroClipboard.swf",
        copy:$('#tobecopy').text()
    });



    /////////////////////////////////////////////////////////////
    /// change properties of html elements depending on context
    /////////////////////////////////////////////////////////////
    var addRemoveButtonValueAction = getAddRemoveButtonValueAction();
    $("[id=addRemoveForm]").attr("action", addRemoveButtonValueAction[0]);
    $("[id=addRemoveButton]").attr("value", addRemoveButtonValueAction[1]);
    function getAddRemoveButtonValueAction(){
        var thecurrenturl = $(location).attr('pathname');
        if (thecurrenturl=="/"){
            return ["/boulangerie_favorite_added/", "Add to fav"];
        }
        else if (thecurrenturl=="/boulangerie_favorite/"){
            return ["/boulangerie_favorite_removed/","Rem from fav"];
        }
        else {
            return ["/boulangerie_favorite_added/", "Add to fav"];
        }
    }
    /////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////

});

$("#logobis").attr("src","/static/baguette.jpg");





///////////////////////////////////
//JavaScript style 
/////////////////////////////////////////////////////////////

function setSessionUser(theUserId){
    var theurl = "/set_session_cogm_" + theUserId + "/";
    window.location.href = theurl;
}


















