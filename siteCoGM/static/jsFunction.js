

///////////////////////////////////
//jquery style
/////////////////////////////////////////////////////////////


$(document).ready(function(){

    $("#header").click(function(){
        var theurl = "/CoGM/";
        $(location).attr('href',theurl);
    });
    
    
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

function redirectToBoul(theboulid){
    var theurl = "/boulangerie_" + theboulid + "/";
    window.location.href = theurl;
}

function boulangerie_favorite_added_id(theboulid){
    var theurl = "/boulangerie_favorite_added_id/" + theboulid + "/";
    window.location.href = theurl;
}      







///////////////////////////////////
// Google map
/////////////////////////////////////////////////////////////



function initializeMapBoulangerieID(jsonboul) {

    //alert(jsonbouls[0].fields.name);
    var lat = jsonboul.fields.latitude;
    var long = jsonboul.fields.longitude;

    var mapDiv = document.getElementById('mapBoulangerieID');

    var map = new google.maps.Map(mapDiv, {
        center: new google.maps.LatLng(lat, long),
        //center: new google.maps.LatLng(48.85780, 2.38028),
        zoom: 16,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(lat, long),
        map: map,
        title: 'Click to zoom'
    });
    google.maps.event.addListener(marker, 'click', function() {
        //redirectToBoul(jsonboul.pk);
        boulangerie_favorite_added_id(jsonboul.pk);
    });


}


function initializeCarteBoulangeries(js_lboul, arglat, arglng, argzoom) {

    var lat = arglat;
    var long = arglng;
    var zoom = argzoom;
    
    var mapDiv = document.getElementById('carteBoulangeries');

    var map = new google.maps.Map(mapDiv, {
        center: new google.maps.LatLng(lat, long),
        zoom: zoom,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });




    var infowindows = new Array();
    var markers = new Array();

    function myAddListener(i){google.maps.event.addListener(markers[i], 'click', function() {
        var thecenter=map.getCenter();
        var thelink = [
            "<a style='font-size:medium' href='/boulangerie_favorite_added_",
            js_lboul[i].pk,
            "/",
            thecenter.lat(),
            "_",
            thecenter.lng(),
            "_",
            map.getZoom(),
            "/",
            "'>Ajouter aux favoris</a>",
        ].join('\n');  

        var content = [
            "<p style='color:red;font-size:large'>" + js_lboul[i].fields.name + "</p>",
            "<p style='font-size:medium'>" + js_lboul[i].fields.numero + " " + js_lboul[i].fields.rue + " - " + js_lboul[i].fields.ville + " " + js_lboul[i].fields.code,
            "<br>",
            thelink,
        ].join('\n');  
        infowindows[i].setContent(content)

        infowindows[i].open(map, this);

    });}



    //var image = new google.maps.MarkerImage(
    //    "/static/baguette.jpg",
    //    new google.maps.Size(100,100)
    //);
   //var image = "/static/baguette.jpg";

    for(var i=0; i<js_lboul.length; i++){
        var lat = js_lboul[i].fields.latitude;
        var long = js_lboul[i].fields.longitude;
        markers[i] = new google.maps.Marker({
            position: new google.maps.LatLng(lat, long),
            map: map,
            //icon:image, 
            title: 'Infos'
        });
 

        infowindows[i] = new google.maps.InfoWindow({
            //content: content
        });

        myAddListener(i);

    }
    


}


function oldinitializeCarteBoulangeries(js_lboul) {

    
    var lat = js_lboul[0].fields.latitude;
    var long = js_lboul[0].fields.longitude;


    var mapDiv = document.getElementById('carteBoulangeries');

    var map = new google.maps.Map(mapDiv, {
        center: new google.maps.LatLng(lat, long),
        //center: new google.maps.LatLng(48.85780, 2.38028),
        zoom: 16,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var markers = new Array();
    function myAddListener(i){google.maps.event.addListener(markers[i], 'click', function() {
            //alert("foo");
            //redirectToBoul(js_lboul[i].pk);
            boulangerie_favorite_added_id(js_lboul[i].pk);
    });}

    for(var i=0; i<js_lboul.length; i++){
        var lat = js_lboul[i].fields.latitude;
        var long = js_lboul[i].fields.longitude;
        markers[i] = new google.maps.Marker({
            position: new google.maps.LatLng(lat, long),
            map: map,
            title: 'Click to zoom'
        });

        myAddListener(i);

    }
    


}











