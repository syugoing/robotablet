import json
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

robot_waiters = set()  # list of robots
tablet_waiters = set()  # list of tablets
modes = ['show_image', 'show_menu', 'hide_iframe']  # list of selectable modes


class RobotHttpHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    # GET /http?mode=:mode
    def get(self, *args):
        """Invoked from robot in arbitrary timing."""

        self.finish({'status': 'ok'})  # dummy response

        mode = self.get_argument('mode')
        image = self.get_argument('image', default=None)

        contents = {"mode": mode, "image": image}
        contents = json.dumps(contents)

        if mode in modes:
            for tablet in tablet_waiters:
                tablet.write_message(contents)


class TabletIndexHandler(tornado.web.RequestHandler):
    # GET /
    def get(self):
        """Invoked from tablet to display index page."""
        self.render('tablet.html')


class TabletIframeHandler(tornado.web.RequestHandler):
    # GET /iframe?mode=:mode
    def get(self):
        """Invoked from parent page of tablet for iframe"""

        mode = self.get_argument('mode')
        image = self.get_argument('image', default=None)

        if mode == 'show_image':
            self.render(mode + '.html', image=image)

        elif mode != "hide_iframe" and mode in modes:
            self.render(mode + '.html')


class TabletSocketHandler(tornado.websocket.WebSocketHandler):
    commands = []

    def open(self):
        """Invoked when a new WebSocket is opened."""

        if self not in tablet_waiters:
            tablet_waiters.add(self)

    def on_message(self, message):
        """Handle incoming messages on the WebSocket."""

        message = json.loads(message)

        self.commands.append(message)
        for robot in robot_waiters:
            robot.write_message(message)

        for tablet in tablet_waiters:
            tablet.write_message(message)

    def on_close(self):
        """Invoked when the WebSocket is closed."""

        if self in tablet_waiters:
            tablet_waiters.remove(self)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            # from Robot
            (r'/http', RobotHttpHandler),

            # from Tablet
            (r'/', TabletIndexHandler),
            (r'/iframe', TabletIframeHandler),
            (r'/ts', TabletSocketHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(3000)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
