var url = "54.84.224.246";
var ids;

$(function(){
  var query = getParameterByName('q');
  if (query.length > 0) {
    $('.query').val(query);
    startQuery();
  }
  // Swarm it up
  $('.swarm').click(function() {
    startQuery();
  });

  $('.query').keypress(function(event) {
      if (event.which == 13) {
        event.preventDefault();
        startQuery();
      }
  });

  $('body').on('click', '.linked', function() {
    var text = $(this).text();
    $('.query').val(text);
    startQuery();
  });
});

function startQuery() {
  $('.body-section').addClass('hidden').removeClass('animated fadeIn');
  startLoading();
  removeHeader();

  var query = $('.query').val();
  // Make the actual API call
  $.post('http://' + url + '/api/articles', {query: query}, function (data) {
    finishLoading();
    drawArticles(data.articles);
    drawPercentage(Math.round(data.sentiment*100));
  }, 'json');

  $.post('http://' + url + '/api/entities', {query: query}, function (data) {
    drawEntities(data);
  }, 'json');
}

function startLoading() {
  $('.loading').removeClass('hidden animated fadeOut').addClass('animated fadeIn');
}

function removeHeader() {
  var logo = $('.logo');
  if (logo.length > 0) {
    logo.animate({height: 0}, 1000, function() {
      logo.remove();
    });
  }
}

function finishLoading() {
  $('.loading').addClass('animated fadeOut').removeClass('fadeIn');
}

function drawPercentage(percentage) {
  $('.analysis').removeClass('hidden animated fadeOut').addClass('animated fadeIn');

  $('.progress-bar-success').css({width: percentage + '%'});
  $('.progress-bar-danger').css({width: (100-percentage) + '%'});

  var red = Math.round((100-percentage)*255/100);
  var green = Math.round(percentage*255/100);
  var sentiment = $('.sentiment-like').text(Math.round(percentage) + '%');
  var success_bar = $('.progress-bar-success');

  sentiment.css({'margin-left': success_bar.width() + 'px'})
           .removeClass('invisible');
                        
}

function drawArticles(articles) {
  $('.articles').removeClass('hidden').addClass('animated fadeIn');

  var holder = $('.articles-holder');
  holder.empty();
  $('.articles').removeClass('hidden');
  ids = [];
  for (var i = 0; i < articles.length; i++) {
    var article = articles[i];
    ids.push(article.id);
    var div =
      '<div class="row item">' + 
      '<div class="col-xs-1">';
    if (article.sentiment >= 0.6) {
      div += '<img src="img/like.png" class="img-responsive svg-img-big" alt="Dislike">'
    } else if (article.sentiment <= 0.4 ){
      div += '<img src="img/dislike.png" class="img-responsive svg-img-big" alt="Dislike">'
    }
    div += '</div>' +
           '<div class="col-xs-11 article' + article.id + '">' +
           '<a href="' + article.link + '"><h2 class="invisible">' + article.title + '</h2></a>' +
           '<p class="snippet lead invisible">' + article.snippet + '</p>' +
           '</div>' +
           '</div>'
    holder.append(div);
  }

  animateArticles();
}

function drawEntities(data) {
  var holder = $('.related .list-group');
  var entities = data.entities
  holder.empty();
  holder.removeClass('hidden');
  for (var i = 0; i < entities.length; i++) {
    var entity = entities[i];
    $.post('http://' + url + '/api/images', {query: entity}, function(data) {
      holder.append('<div class="thumbnail"><img class="img-responsive" src="' + data.responseData.results[0].url + '"><a href="#" class="list-group-item linked"><h3 class="text-center">' + data.echo + '</h3></a></div>');
    }, 'json');
  }

  if (typeof ids === "undefined") {
    ids = [];
  }
  for (var i = 0; i < ids.length; i++) {
    var article_header = $('.article' + ids[i] + ' h2');
    article_header.after('<div class="labels"></div>');
    var labels = article_header.siblings('.labels');
    for (var j = 0; j < data[ids[i]].length; j++) {
      var entity = data[ids[i]][j];
      labels.append('<a href="#" class="linked label label-default">' + entity + '</a>');
    }
  }

  animateEntities();
}

function animateArticles() {
  $('.articles-holder .invisible').removeClass("invisible");
}

function animateEntities() {
  $('.related').removeClass("invisible").addClass("animated fadeIn");
}


function getParameterByName(name) {
  name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
  var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
      results = regex.exec(location.search);
  return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
