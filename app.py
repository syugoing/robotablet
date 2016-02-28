import json
import logging
import os

import tornado.httpserver
import tornado.ioloop
import tornado.log
import tornado.options
import tornado.web
import tornado.websocket

actions = ['show_image', 'show_menu', 'hide_iframe',
           'stay_iframe']  # list of selectable actions

robot_waiters = set()  # list of robots
tablet_waiters = set()  # list of tablets
ws_messages = []


class RobotHttpHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    # GET /http?action=:action
    def get(self, *args):
        """Invoked from robot in arbitrary timing."""

        action = self.get_argument('action')
        image = self.get_argument('image', default=None)

        if action not in actions:
            self.finish({'status': 'ng'})
            return

        tablet_behavior = {'action': action, 'image': image}
        ws_message = {'from': 'robot', 'to': 'tablet',
                      'tabletBehavior': tablet_behavior}

        to = ws_message['to']

        ws_messages.append(ws_message)

        if to == 'tablet':
            for tablet in tablet_waiters:
                tablet.write_message(ws_message)

        logging.info('sendmessage to {0} - tablets: {1}, robots: {2}'.format(
            to, len(tablet_waiters), len(robot_waiters)))

        self.finish({'status': 'ok'})


class TabletIndexHandler(tornado.web.RequestHandler):
    # GET /

    def get(self):
        """Invoked from tablet to display index page."""
        self.render('tablet.html')


class TabletIframeHandler(tornado.web.RequestHandler):
    # GET /iframe?action=:action

    def get(self):
        """Invoked from parent page of tablet for iframe."""

        action = self.get_argument('action')

        if action == 'show_image':
            image = self.get_argument('image', default='default.png')
            self.render(action + '.html', image=image)

        elif action not in ['hide_iframe', 'stay_iframe'] and action in actions:
            self.render(action + '.html')


class SocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        """Invoked when a new WebSocket is opened."""

        logging.info('onopen - tablets: {0}, robots: {1}'.format(
            len(tablet_waiters), len(robot_waiters)))

    def on_message(self, ws_message):
        """Handle incoming messages on the WebSocket."""

        self._send_message(ws_message)

    def _send_message(self, ws_message):

        ws_message = json.loads(ws_message)
        to = ws_message['to']

        ws_messages.append(ws_message)

        if to == 'robot':
            for robot in robot_waiters:
                robot.write_message(ws_message)

        elif to == 'tablet':
            for tablet in tablet_waiters:
                tablet.write_message(ws_message)

        logging.info('onmessage to {0} - tablets: {1}, robots: {2}'.format(
            to, len(tablet_waiters), len(robot_waiters)))


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
