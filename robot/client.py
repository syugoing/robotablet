import os
import sys


def __init__(self):
    GeneratedClass.__init__(self)


def onLoad(self):
    self.ws = None
    self.freez = False
    self.connectonToken = None

    self.eyeTimer = None
    self.sendEyeBlocking = False
    self.action_count = 0
    self.isVirtualRobot = False

    self.framemanager = ALProxy('ALFrameManager')
    self.memory = ALProxy('ALMemory')

    try:
        self.photoCapture = ALProxy('ALPhotoCapture')
        self.video = ALProxy('ALVideoDevice')

    except Exception as e:
        self.photoCapture = None
        self.video = None


def onUnload(self):
    self.ws = None
    self.freez = False
    self.connectonToken = None

    self.framemanager = None
    self.memory = None
    self.photoCapture = None
    self.video = None

    self.stopEye()


def onInput_onStart(self, url):
    self.init_read_library()
    self.init_websocket_connection()


def onInput_onStop(self):
    self.onUnload()  # it is recommended to reuse the clean-up as the box is stopped
    self.onStopped()  # activate the output of the box


def init_read_library(self):
    self.folderName = os.path.join(
        self.framemanager.getBehaviorPath(self.behaviorId), './lib')

    if self.folderName not in sys.path:
        sys.path.append(self.folderName)


def init_websocket_connection(self):
    import websocket

    websocket.enableTrace(True)
    websocket.setdefaulttimeout(500)

    ws_url = 'ws://localhost:3000/'

    self.ws = websocket.WebSocketApp(ws_url,
                                     on_message=self.ws_on_message,
                                     on_error=self.ws_on_error,
                                     on_close=self.ws_on_close)

    self.ws.on_open = self.ws_on_open
    self.ws.run_forever()
