function runRecommender() {

    var content = "<p> Looking for user matches...<br>" +
                  "This can take a couple minutes. <img src='static/img/spinning-wheel.gif'>" 

    $("#rec-content").html(content);
    showRecPane();

    console.log('getting recommendations for user '+user);

    $.getJSON('/user?name='+user+'&recommend=True', function(data) {
            console.log('got recommendations');

            showRecommendations(data.beer.slice(0,10));
            placeMarkers( data.loc.slice(0,5), 10,'green' );
        }
    );
};

// display the panes
function showRecPane() {
    document.getElementById('form-canvas').style.visibility='hidden';
    document.getElementById('recommend-canvas').style.visibility='visible';
}
function showRatPane() {
    document.getElementById('form-canvas').style.visibility='visible';
    document.getElementById('recommend-canvas').style.visibility='hidden';
}