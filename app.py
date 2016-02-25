import json
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options

define('port', default=3000, help='run on the given port', type=int)

tablet_waiters = set()  # list of tablets


class RobotHttpHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, *args):
        self.finish({'status': 'ok'})

        data = {'url': url, 'question': question,
                'answer': answer, 'dialog': dialog}
        data = json.dumps(data)
        for tablet in tablet_waiters:
            tablet.write_message(data)


class TabletIndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('tablet.html')


class TabletSocketHandler(tornado.websocket.WebSocketHandler):

    commands = []

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in tablet_waiters:
            tablet_waiters.add(self)

    def on_message(self, command):
        command = json.loads(command)

        self.commands.append(command)
        for tablet in self.tablet_waiters:
            if waiter == self:
                continue
            waiter.write_message(
                {'img_path': message['img_path'], 'message': message['message']})

    def on_close(self):
        if self in tablet_waiters:
            tablet_waiters.remove(self)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            # from Robot
            (r"/http", RobotHttpHandler),

            # from Tablet
            (r"/", TabletIndexHandler),
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
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
