var fakeArticles = {
  sentiment: 0.73,
  articles: [
    {title: "Obama Eats Children",
     snippet: "Obama found eating small and mid-sized children"},
    {title: "Michelle Obama Cooks",
     snippet: "Tasty new treats coming out of the Obama household"},
    {title: "Sharknado Approaches",
     snippet: "A Sharknado was spotted off the coast of Uzebekastan"}
  ]
}

$(function(){
  $('.body').removeClass("hidden");
  $('.loading').css({opacity: 0});
  
  // Swarm it up
  $('.swarm').click(function() {
    var query = $('.query').val();
    // Make the actual API call
    //$.post('http://google.com/articles', {query: query}, function (data) {
      //TODO(bsprague) Remove this when we have legit data
      data = fakeArticles;
      $('.analysis').css({opacity: 0})
                    .removeClass("hidden")
                    .animate({opacity: 1}, 500, function() {
                      drawPercentage(Math.round(data.sentiment*100));
                    });
      drawArticles(data.articles);
      $('.articles').css({opacity: 0})
                    .removeClass("hidden")
                    .animate({opacity: 1}, 500, function() {
                      animateArticles();
                    });
    //}, 'json');
  });
});

function drawPercentage(percentage) {
  $('.progress-bar-danger').css({width: (100-percentage) + '%'});

  $('.progress-bar-danger').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(e) {
    $('.progress-bar-success').css({width: percentage + '%'});
  });

  $('.progress-bar-success').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(e) {
    var red = Math.round((100-percentage)*255/100);
    var green = Math.round(percentage*255/100);
    $('.sentiment').removeClass('invisible')
                   .addClass('animated bounceIn')
                   .text(percentage + '%')
                   .css({color: 'rgb(' + red + ', ' + green + ', 0)'});
  });
}

function drawArticles(articles) {
  var holder = $('.articles-holder');
  for (var i = 0; i < articles.length; i++) {
    var article = articles[i];
    holder.append('<h1 class="invisible">' + article.title + '</h1>');
    holder.append('<p class="snippet lead invisible">' + article.snippet + '</p>');
  }
}

function animateArticles() {
  $('.articles-holder > *').removeClass("invisible").addClass("animated fadeInDown");
}

function getParameterByName(name) {
  name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
  var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
      results = regex.exec(location.search);
  return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
