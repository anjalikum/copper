$( document ).ready(function() {
  $("#profile").hide();

  $("#submit").click(function() {
    $("#profile").show();
    $("#form").hide();
  });
});

