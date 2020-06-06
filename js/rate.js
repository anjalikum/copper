$( document ).ready(function() {
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
});