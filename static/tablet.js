$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    console.log("ready");
    updater.start();
});

var updater = {
    socket: null,
    attempts: 1,

    start: function() {

        if (updater.socket == null) {
            var url = "ws://" + location.host + "/ws";
            updater.socket = new WebSocket(url);
            updater.$message = $("#message");
            updater.$dialog_id = $("#dialog_id");

            console.log(url);
            updater.socket.onopen = function() {
                console.log("onopen");
                updater.$message.attr("class", "label label-success");
                updater.$message.text("open");

                // reset the tries back to 1 since we have a new connection opened.
                updater.attempts = 1;
            };

            updater.socket.onmessage = function(event) {
                console.log("onmessage");
                updater.$message.attr("class", "label label-primary");
                updater.$dialog = $('iframe:first').contents().find('#dialog');

                var json = JSON.parse(event.data);
                console.log(json);

                if (json.url != null) {
                    updater.$message.text("recieved url");

                    $("#iframe").attr("src", "");

                    var iframe_src = json.url;
                    $("#iframe").attr("src", iframe_src);

                } else if (json.dialog != null) {
                    updater.$message.text("recieved dialog");

                    var iframe_src = "http://" + location.host + "/iframe";
                    $("#iframe").attr("src", iframe_src);

                    updater.$dialog_id.attr("class", "label label-primary");
                    updater.$dialog_id.text(json.dialog);


                } else if (json.question != null) {
                    updater.$message.text("recieved question");

                    updater.$dialog.append("<div class='row'></div>");
                    updater.$dialog.append(
                        $("<div class='row'>").append(
                            $("<div class='col s9 offset-s2'>").append(
                                $("<div class='arrow_box_left'>").append("<h2 class='logo'>" + json.question + "</h2>").fadeIn("slow")
                            )
                        )
                    );

                } else if (json.answer != null) {
                    updater.$message.text("recieved answer");

                    updater.$dialog.append("<div class='row'></div>");
                    updater.$dialog.append(
                        $("<div class='row'>").append(
                            $("<div class='col s9 offset-s1'>").append(
                                $("<div class='arrow_box_right'>").append("<h2 class='logo'>" + json.answer + "</h2>").fadeIn("slow")
                            )
                        )
                    );
                }
            };

            updater.socket.onclose = function(event){
                console.log("onclose. reason: %s", event.reason);
                updater.$message.attr("class", "label label-important");
                updater.$message.text("closed");

                var time = updater.generateInterval(updater.attempts);

                setTimeout(function(){
                    // We"ve tried to reconnect so increment the attempts by 1
                    updater.attempts++;
                    console.log("attempts: ", updater.attempts);

                    // Connection has closed so try to reconnect every 10 seconds.
                    updater.socket = null;
                    updater.start();

                }, time);
            };

            updater.socket.onerror = function(event){
                console.log("onerror");
                updater.$message.attr("class", "label label-warning");
                updater.$message.text("error occurred");
            }
        }
    },

    generateInterval: function(k){
        // generate the interval to a random number between 0 and the max
        return Math.min(30, (Math.pow(2, k) - 1)) * 1000 * Math.random();
    },

    ping: function(){
        updater.socket.send("PING");
    }
};