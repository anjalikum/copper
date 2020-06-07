$( document ).ready(function() {
    $("#dlocat").hide()

    var star1, star2, star3, star4, star5;

    $('#stars_1').starrr({
        change: function(e, value){
          star1 = value;
        }
    });
    $('#stars_2').starrr({
        change: function(e, value){
          star2 = value;
        }
    });
    $('#stars_3').starrr({
        change: function(e, value){
          star3 = value;
        }
    });
    $('#stars_4').starrr({
        change: function(e, value){
          star4 = value;
        }
    });
    $('#stars_5').starrr({
        change: function(e, value){
          star5 = value;
        }
    });

    var lat, long, formatted;
    $('#cbutton').click(function(){
        var locat = $('#locat').val()
        console.log("https://api.radar.io/v1/geocode/forward?query="+locat);
        $.ajax({
            url: "https://api.radar.io/v1/geocode/forward?query="+locat,
            type: "GET",
            query: locat,
            headers: {
                Authorization: 'prj_live_pk_6c05c3c88319aa3472121a355127ceaaeb608812'
              },
            success: function (result) {
                lat = result.addresses[0].latitude;
                long = result.addresses[0].longitude;
                formatted = result.addresses[0].formattedAddress;

                $("#lat").html('').append(lat);
                $("#long").html('').append(long);
                $("#formatted").html('').append(formatted);
                initMap(lat,long);

                $("#dlocat").show();
            },
            error: function (error) {
                console.log(error);
            }
        });

    });    
});

function initMap(la, ln) {
  var uluru = {lat: la, lng: ln};
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 15, center: uluru});
  var marker = new google.maps.Marker({position: uluru, map: map});
}

