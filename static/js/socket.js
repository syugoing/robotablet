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

function sendAction(robotBehavior) {
  wsMessage = {
    'from': 'tablet',
    'to': 'robot',
    'robotBehavior': robotBehavior
  };

  socket.send(JSON.stringify(wsMessage));
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
      var tabletBehavior = json.tabletBehavior;

      $iframe.attr('class', 'onmessage');

      if (to == "tablet") {
        var action = tabletBehavior.action;
        console.log(action);

        if (action == "hide_iframe") {
          $iframe.removeAttr('src');

        } else if (action == "show_image") {
          var image = tabletBehavior.image;
          if (image) {
            $iframe.attr('src', '/iframe?action=' + action + '&image=' + image);

          } else {
            $iframe.attr('src', '/iframe?action=' + action);

          }

        } else if (action == "show_menu") {
          var menu = tabletBehavior.menu;
          if (menu) {
            $iframe.attr('src', '/iframe?action=' + action + '&menu=' + menu);

          } else {
            $iframe.attr('src', '/iframe?action=' + action);

          }

        } else {
          $iframe.attr('src', '/iframe?action=' + action);

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
