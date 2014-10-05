var tablink = tab.url;
var url = "54.84.224.246";
$.post('http://' + url + '/api/entities', {url: url}, function (entity_data) {
    var entities = entity_data.entities;
    for (var i = 0; i < entities.length; i++) {
      var entity = entities[i];
      $.post('http://' + url + '/api/sentiment', {entity: entity}, function (sentiment_data) {
        var sentiment = sentiment_data.sentiment;
        var red = Math.round(100 - sentiment*100);
        var green = Math.round(sentiment*100);
        $('body *').repalceText(entity, '<span style="color: rgb(' + red + ', ' + green + ', 0);"')
      }, 'json')
    }
}, 'json');
