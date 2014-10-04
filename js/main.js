var paper;

$(function(){
  $('.body').css({opacity: 0}).removeClass("hidden")
  setTimeout(function(){
    $('.body').animate({opacity: 1}, 500);
    $('.wobblebar').animate({opacity: 0});
  }, 1000);
  var percentage = parseInt(getParameterByName("percentage"));
  drawCanvas();
});

function drawCanvas() {
  if (typeof paper !== "undefined") {
    paper.remove();
  }
  var canvas = $('.canvas');
  var width = canvas.width()
  var height = canvas.height()
  paper = Raphael(canvas.get(0), width, height);
}

function getParameterByName(name) {
  name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
  var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
      results = regex.exec(location.search);
  return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
