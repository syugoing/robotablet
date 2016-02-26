$(document).ready(function() {
  if (!window.console) window.console = {};
  if (!window.console.log) window.console.log = function() {};

  console.log('ready');
  updater.start();
});

var updater = {

  socket: null,
  attempts: 1,

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

          // reset the tries back to 1 since we have a new connection opened.
          updater.attempts = 1;
        };
        // onopen

      // onmessage
      updater.socket.onmessage = function(event) {
        console.log('onmessage');

        updater.$message.attr('class', 'label label-primary');

        var json = JSON.parse(event.data);
        console.log(json);

        updater.$message.text('recieved');
      };

      // onclose
      updater.socket.onclose = function(event) {
        console.log('onclose. reason: %s', event.reason);

        updater.$message.attr('class', 'label label-important');
        updater.$message.text('closed');

        var time = updater.generateInterval(updater.attempts);

        setTimeout(function() {
          // We"ve tried to reconnect so increment the attempts by 1
          updater.attempts ++;
          console.log('attempts: ', updater.attempts);

          // Connection has closed so try to reconnect every 10 seconds.
          updater.socket = null;
          updater.start();

        }, time);
      };

      // onerror
      updater.socket.onerror = function(event) {
        console.log('onerror');

        updater.$message.attr('class', 'label label-warning');
        updater.$message.text('error occurred');
      };
    }
  },

  generateInterval: function(k) {
    // generate the interval to a random number between 0 and the max
    return Math.min(30, (Math.pow(2, k) - 1)) * 1000 * Math.random();
  }
};
