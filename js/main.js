var url = "54.84.224.246";
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
};

var fakeEntities = {
  entities: ["Muffins", "Al Sharpton", "Twitter", "DDR"]
};

$(function(){
  $('.body').removeClass("hidden");
  $('.loading').css({opacity: 0});
  
  // Swarm it up
  $('.swarm').click(function() {
    $('.articles').animate({opacity: 0}, 500, function() {
      $('.articles-holder').empty();
    });
    var query = $('.query').val();
    // Make the actual API call
    $('.loading').animate({opacity: 1}, 500);
    $.post('http://' + url + '/api/articles', {query: query}, function (data) {
      //data = fakeArticles;
      $('.analysis').css({opacity: 0})
                    .removeClass("hidden")
                    .animate({opacity: 1}, 500, function() {
                      drawPercentage(Math.round(data.sentiment*100));
                    });
      drawArticles(data.articles);
      $('.articles').css({opacity: 0})
                    .removeClass("hidden")
                    .animate({opacity: 1}, 500, function() {
                      $('.loading').animate({opacity: 0}, 500);
                      animateArticles();
                    });
   }, 'json');
    $.post('http://' + url + '/api/entities', {query: query}, function (data) {
        //data = fakeEntities;
        drawEntities(data.entities);
    }, 'json');
  });
});

function drawPercentage(percentage) {
  $('.progress-bar-success').css({width: percentage + '%'});

  $('.progress-bar-success').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(e) {
    $('.progress-bar-danger').css({width: (100-percentage) + '%'});
  });

  $('.progress-bar-danger').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(e) {
    var red = Math.round((100-percentage)*255/100);
    var green = Math.round(percentage*255/100);
    var sentiment = $('.sentiment-like').text(Math.round(percentage) + '%');
    var success_bar = $('.progress-bar-success');

    sentiment.css({'margin-left': success_bar.width() + 'px'})
             .removeClass('invisible')
             .addClass('animated bounceIn');
                        
  });
}

function drawArticles(articles) {
  var holder = $('.articles-holder');
  for (var i = 0; i < articles.length; i++) {
    var article = articles[i];
    var div =
      '<div class="row item">' + 
      '<div class="col-xs-1">';
    if (article.sentiment >= 0.5) {
      div += '<img src="img/like.png" class="img-responsive svg-img-big" alt="Dislike">'
    } else {
      div += '<img src="img/dislike.png" class="img-responsive svg-img-big" alt="Dislike">'
    }
    div += '</div>' +
           '<div class="col-xs-11">' +
           '<h2 class="invisible">' + article.title + '</h2>' +
           '<p class="snippet lead invisible">' + article.snippet + '</p>' +
           '</div>' +
           '</div>'
    holder.append(div);
  }
}

function drawEntities(entities) {
  var holder = $('.related .list-group');
  for (var i = 0; i < entities.length; i++) {
    var entity = entities[i];
    holder.append('<a href="#" class="list-group-item">' + entity + '</a>');
  }
}

function animateArticles() {
  $('.articles-holder .invisible').removeClass("invisible").addClass("animated fadeInDown");
}

function getParameterByName(name) {
  name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
  var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
      results = regex.exec(location.search);
  return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
