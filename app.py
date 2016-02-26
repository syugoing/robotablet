import json
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

robot_waiters = set()  # list of robots
tablet_waiters = set()  # list of tablets


class RobotHttpHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, *args):
        """Invoked from robot in arbitrary timing."""

        self.finish({'status': 'ok'})  # dummy response

        mode = self.get_argument('mode', default=None)

        contents = {}
        contents['mode'] = mode

        if mode == 'show_html':
            html = self.get_argument('html', default=None)
            contents['html'] = html

        elif mode == 'show_image':
            image = self.get_argument('image', default=None)
            contents['image'] = image

        contents = json.dumps(contents)

        for tablet in tablet_waiters:
            tablet.write_message(contents)


class TabletIndexHandler(tornado.web.RequestHandler):

    def get(self):
        """Invoked from tablet to display index page."""
        self.render('tablet.html')


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
