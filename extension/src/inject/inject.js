var url = "54.84.224.246";
console.log('loaded');
$.post('http://' + url + '/api/entity', {url: document.URL}, function (entity_data) {
    var entities = entity_data.entities;
    console.log(entities);
    for (var i = 0; i < entities.length; i++) {
      var entity = entities[i];
      console.log(entity);
      $.post('http://' + url + '/api/sentiment', {query: entity}, function (sentiment_data) {
        console.log(sentiment_data);
        var sentiment = sentiment_data.sentiment;
        var entity = sentiment_data.query;
        console.log(entity);
        var red = Math.round(Math.round(100 - sentiment*100) * 255 / 100);
        var green = Math.round(Math.round(sentiment*100) * 255 / 100);
        $('body *').replaceText(new RegExp('('+entity+')', 'gi'), '<a style="color:inherit" href="http://hivemindisaweso.me/?q=' + entity + '"><div style="display:inline; padding: 3px; background-color: rgb(' + red + ', ' + green + ', 0); border-radius:4px; border:3px;">$1</div></a>');
      }, 'json')
    }
}, 'json');