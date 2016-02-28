$(document).ready(function() {
  if (!window.console) window.console = {};
  if (!window.console.log) window.console.log = function() {};

  console.log("ready");
  wsStart();
});

var socket = null;
var retry_attempts = 0;
var max_retry_attempts = 120;

var url = 'ws://' + location.host + '/ts';

function sendAction(ws_contents) {
  ws_message = {
    'from': 'tablet',
    'to': 'robot',
    'ws_contents': ws_contents
  };

  socket.send(JSON.stringify(ws_message));
}

var wsStart = function() {

  if (socket === null) {

    socket = new WebSocket(url);
    var $iframe = $('#iframe');
    console.log(url);

    // onopen
    // When tablet page opened.
    socket.onopen = function() {
      console.log('onopen');

      $iframe.attr('class', 'onopen');
      $iframe.removeAttr('src');

    };

    // onmessage
    // When invoked from robot and page reload.
    socket.onmessage = function(event) {
      console.log('onmessage');

      var json = JSON.parse(event.data);

      var from = json.from;
      var to = json.to;
      var ws_contents = json.ws_contents;
      var mode = ws_contents.mode;
      console.log(mode);

      $iframe.attr('class', 'onmessage');

      if (to == "tablet") {
        if (mode == "hide_iframe") {
          $iframe.removeAttr('src');

        } else if (mode == "stay_iframe") {
          // NOP

        } else if (mode == "show_image") {
          var image = ws_contents.image;
          if (image === null) {
            $iframe.attr('src', '/iframe?mode=' + mode);

          } else {
            $iframe.attr('src', '/iframe?mode=' + mode + '&image=' + image);

          }

        } else {
          $iframe.attr('src', '/iframe?mode=' + mode);

        }
      }

      // reset the tries back to 0 since we have a new connection opened.
      retry_attempts = 0;

    };

    // onclose
    // When tablet page closed.
    socket.onclose = function(event) {
      console.log('onclose. reason: %s', event.reason);

      $iframe.attr('class', 'onclose');

      if (retry_attempts < max_retry_attempts) {
        // Connection has closed so try to reconnect.
        retry_attempts++;
        socket = null;

        // retry
        wsStart();
        console.log("retry_attempts: ", retry_attempts);

      } else {
        console.log("websocket closed by over max_retry_attempts: ", retry_attempts);

      }

    };

    // onerror
    // When error occurred.
    socket.onerror = function(event) {
      console.log('onerror');

      $iframe.attr('class', 'onerror');

    };

  }
};
