import json
import logging
import os

import tornado.httpserver
import tornado.ioloop
import tornado.log
import tornado.options
import tornado.web
import tornado.websocket

modes = ['show_image', 'show_menu', 'hide_iframe',
         'stay_iframe']  # list of selectable modes

robot_waiters = set()  # list of robots
tablet_waiters = set()  # list of tablets
ws_messages = []


class RobotHttpHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    # GET /http?mode=:mode
    def get(self, *args):
        """Invoked from robot in arbitrary timing."""

        mode = self.get_argument('mode')
        image = self.get_argument('image', default=None)

        if mode not in modes:
            self.finish({'status': 'ng'})
            return

        ws_contents = {'mode': mode, 'image': image}
        ws_message = {'from': 'robot', 'to': 'tablet',
                      'ws_contents': ws_contents}

        to = ws_message['to']

        ws_messages.append(ws_message)

        if to == 'tablet':
            for tablet in tablet_waiters:
                tablet.write_message(ws_message)

        self.finish({'status': 'ok'})


class TabletIndexHandler(tornado.web.RequestHandler):
    # GET /

    def get(self):
        """Invoked from tablet to display index page."""
        self.render('tablet.html')


class TabletIframeHandler(tornado.web.RequestHandler):
    # GET /iframe?mode=:mode

    def get(self):
        """Invoked from parent page of tablet for iframe."""

        mode = self.get_argument('mode')

        if mode == 'show_image':
            image = self.get_argument('image', default='default.png')
            self.render(mode + '.html', image=image)

        elif mode not in ['hide_iframe', 'stay_iframe'] and mode in modes:
            self.render(mode + '.html')


class SocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        """Invoked when a new WebSocket is opened."""

        logging.info('onopen - tablets: {0}, robots: {1}'.format(
            len(tablet_waiters), len(robot_waiters)))

    def on_message(self, ws_message):
        """Handle incoming messages on the WebSocket."""

        self.send_message(ws_message)

        logging.info('onmessage - tablets: {0}, robots: {1}'.format(
            len(tablet_waiters), len(robot_waiters)))

    def send_message(self, ws_message):

        ws_message = json.loads(ws_message)
        to = ws_message['to']

        ws_messages.append(ws_message)

        if to == 'robot':
            for robot in robot_waiters:
                robot.write_message(ws_message)

        elif to == 'tablet':
            for tablet in tablet_waiters:
                tablet.write_message(ws_message)

    def on_close(self):
        """Invoked when the WebSocket is closed."""

        logging.info('onclose - tablets: {0}, robots: {1}'.format(
            len(tablet_waiters), len(robot_waiters)))


class TabletSocketHandler(SocketHandler):

    def open(self):
        """Invoked when a new WebSocket is opened."""

        if self not in tablet_waiters:
            tablet_waiters.add(self)

        super(TabletSocketHandler, self).open()

    def on_close(self):
        """Invoked when the WebSocket is closed."""

        if self in tablet_waiters:
            tablet_waiters.remove(self)

        super(TabletSocketHandler, self).on_close()


class RobotSocketHandler(SocketHandler):

    def open(self):
        """Invoked when a new WebSocket is opened."""

        if self not in robot_waiters:
            robot_waiters.add(self)

        super(RobotSocketHandler, self).open()

    def on_close(self):
        """Invoked when the WebSocket is closed."""

        if self in robot_waiters:
            robot_waiters.remove(self)

        super(RobotSocketHandler, self).on_close()


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            # from Robot
            (r'/http', RobotHttpHandler),
            (r'/rs', RobotSocketHandler),

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
