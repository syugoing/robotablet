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

function sendAction(msg) {
    socket.send(JSON.stringify(msg));
}

var wsStart = function() {

  if (socket === null) {

    socket = new WebSocket(url);

    var $message = $('#message');
    var $iframe = $('#iframe');

    console.log(url);

    // onopen
    // When tablet page opened.
    socket.onopen = function() {
      console.log('onopen');

      $message.attr('class', 'label label-success');
      $message.text('open');
      $iframe.attr('src', null);

    };

    // onmessage
    // When invoked from robot and page reload.
    socket.onmessage = function(event) {
      console.log('onmessage');

      var json = JSON.parse(event.data);
      console.log(json);
      var mode = json.mode;
      var image = json.image;
      console.log(mode);

      $message.attr('class', 'label label-primary');
      $message.text('recieved');

      if (mode == "hide_iframe") {
        $iframe.attr('src', null);

      } else if (mode == "stay_iframe") {
        // NOP

      } else if (mode == "show_image") {
        $iframe.attr('src', '/iframe?mode=' + mode + '&image=' + image);

      } else {
        $iframe.attr('src', '/iframe?mode=' + mode);

      }

      // reset the tries back to 0 since we have a new connection opened.
      retry_attempts = 0;

    };

    // onclose
    // When tablet page closed.
    socket.onclose = function(event) {
      console.log('onclose. reason: %s', event.reason);

      $message.attr('class', 'label label-important');
      $message.text('closed');

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

      $message.attr('class', 'label label-warning');
      $message.text('error occurred');
    };

  }
};
