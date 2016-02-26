$(document).ready(function() {
  if (!window.console) window.console = {};
  if (!window.console.log) window.console.log = function() {};

  console.log('ready');
  updater.start();
});

var updater = {

  socket: null,

  retry_attempts: 0,
  max_retry_attempts: 120,

  start: function() {

    if (updater.socket === null) {
      var url = 'ws://' + location.host + '/ts';

      updater.socket = new WebSocket(url);
      updater.$message = $('#message');

      console.log(url);

      // onopen
      updater.socket.onopen = function() {
          console.log('onopen');

          updater.$message.attr('class', 'label label-success');
          updater.$message.text('open');

      };

      // onmessage
      updater.socket.onmessage = function(event) {
        console.log('onmessage');

        updater.$message.attr('class', 'label label-primary');

        var json = JSON.parse(event.data);
        console.log(json);

        updater.$message.text('recieved');

        // reset the tries back to 0 since we have a new connection opened.
        updater.retry_attempts = 0;


      };

      // onclose
      updater.socket.onclose = function(event) {
        console.log('onclose. reason: %s', event.reason);

        updater.$message.attr('class', 'label label-important');
        updater.$message.text('closed');

        if (updater.retry_attempts < updater.max_retry_attempts) {
          // Connection has closed so try to reconnect.
          updater.retry_attempts++;

          updater.socket = null;
          updater.start();
          console.log("retry_attempts: ", updater.retry_attempts);

        } else {
          console.log("websocket closed by over max_retry_attempts: ", updater.retry_attempts);

        }

      };

      // onerror
      updater.socket.onerror = function(event) {
        console.log('onerror');

        updater.$message.attr('class', 'label label-warning');
        updater.$message.text('error occurred');
      };
    }
  }
};
