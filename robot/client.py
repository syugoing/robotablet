import thread, time, json, urllib, urllib2, sys, os, threading, base64

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        self.isVirtualRobot = False
        self.freez = False
        self.connectonToken = None
        self.ws = None
        self.eyeTimer = None
        self.sendEyeBlocking = False
        self.action_count = 0
        self.framemanager = ALProxy("ALFrameManager")
        self.memory = ALProxy("ALMemory")

        try:
            self.photoCapture = ALProxy( "ALPhotoCapture" )
            self.video = ALProxy("ALVideoDevice")
        except Exception as e:
            self.photoCapture = None
            self.video = None
        pass

    def onUnload(self):
        self.freez = False
        self.connectonToken = None
        self.framemanager = None
        self.memory = None
        self.ws = None

        self.video = None
        self.photoCapture = None

        self.stopEye()
        pass

    def onInput_onStart(self, url):
        self.init_read_library()
        self.init_websocket_connection()
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box

    def onInput_inputCompleteAction(self):
        self.freez = False
        self.log("ACTION_COMPLETE token is "+ str(self.connectonToken))

        self.ws_send_message({"action":"actioncomplete", "data":str(self.connectonToken)})
        pass

    def onInput_inputCompleteConnection(self):
        self.freez = False
        self.log("ACTION_COMPLETE token is "+ str(self.connectonToken))

        self.ws_send_message({"action":"actioncomplete", "data":str(self.connectonToken)})

        if self.isVirtualRobot == False:
            self.initRecoding()
            self.sendEye()
            pass
        pass

    def onInput_initCompletePicture(self):
        self.freez = False

        self.ws_send_message({"action":"actioncomplete", "data":str(self.connectonToken)})

        pictureFilename = str(self.memory.getData("MyApplication/PictureFilename"))

        tmpDir = os.path.join(self.framemanager.getBehaviorPath(self.behaviorId), "./html/tmp_picture")

        file_name = "/"+pictureFilename+".jpg"
        #file_name = "/example.jpg"
        imagePath = str(tmpDir)
        imagePath += file_name

        imageData = open(imagePath).read()

        if imageData != "":
            sendData  = '[!dataURL!]||||'
            sendData += 'take_picture_image||||'
            sendData += 'data:image/jpeg;base64,'+base64.b64encode(imageData)+'||||'
            sendData += str(self.connectonToken)

            self.ws.send(sendData)
            pass

        self.sendEyeBlocking = False
        pass

    ## --- START RECODING ----- ##
    def initRecoding(self):
        videName = 'rospy_gvm_test'
        cameraId = 0
        resolution = 2
        colorspace = 11
        framerate = 15

        self.video.unsubscribeAllInstances(videName)

        self.camObj = self.video.subscribeCamera(videName, cameraId, resolution, colorspace, framerate)
        pass

    ## ---- START ROBOT ACTIONS ---- ##
    def getTokenMethod(self, connection_token):
        self.freez = True
        self.connectonToken = str(connection_token)
        self.log("GET CONNECTION TOKEN ["+self.connectonToken+"]")

        self.output_get_connection_token(self.connectonToken)
        pass

    def connectionSuccessMethod(self):
        self.freez = True

        self.output_success_connection()
        pass

    def robotActionMethod(self, data):
        self.freez = True

        self.action_count = self.action_count + 1

        self.output_do_method([self.action_count, str(data[1])])
        pass

    def robotTalkMethod(self, talk_text):
        decoded = urllib.unquote(talk_text)

        self.log(str(decoded))
        self.log("robot will talk")
        self.output_talking(decoded)
        pass

    def robotTakePictureMethod(self):
        self.log("robot will Take Picture")
        self.sendEyeBlocking = True
        self.output_take_picture()
        pass

    def disconnectionMethod(self):
        self.freez = True
        self.sendEyeBlocking = True
        self.stopEye()
        self.output_disconnection()
        pass
    ## ---- END ROBOT ACTIONS ---- ##


    ## ---- START WEBSOCKET FUNCTIONS ---- ##
    def ws_send_message(self, inputJson):
        try:
            jsonData = json.dumps(inputJson)
            self.ws.send(jsonData)
        except ValueError:
            self.log('ws has error')
        pass

    def ws_on_message(self, ws, message):
        self.log('message is ....');
        self.log(message);

        receive = json.loads(message)

        target_action = str(receive["action"])
        target_data   = str(receive["data"])

        if target_action == "get_token" :
            if self.freez == False :
                self.getTokenMethod(target_data)
        elif target_action == "success_connection" :
            self.log("success connection")
            if self.freez == False :
                self.connectionSuccessMethod()
        elif target_action == "robot_action":
            if self.freez == False :
                self.robotActionMethod([target_action, target_data])
            pass
        elif target_action == "robot_talk":
            self.log('talk')
            if self.freez == False :
                self.robotTalkMethod(target_data)
            pass
        elif target_action == "take_picture":
            if self.freez == False :
                self.robotTakePictureMethod()
            pass
        elif target_action == "disconnection" :
            if self.freez == False :
                self.disconnectionMethod()
            pass
        pass

    def ws_on_error(self, ws, error):
        self.output_connection_error()
        pass

    def ws_on_close(self, ws):
        self.log('connection closed')
        pass

    def ws_on_open(self, ws):
        self.ws_send_message({"action":"robottoken", "data":"none"})
        pass
    ## ---- END WEBSOCKET FUNCTIONS ---- ##


    ## ---- START INITIALIZE ---- ##
    def init_websocket_connection(self):
        import websocket

        websocket.enableTrace(True)

        websocket.setdefaulttimeout(500)

        websocketUrl = "ws://rconnect.oyoyo-project.com:80/"

        self.ws = websocket.WebSocketApp(websocketUrl,
            on_message = self.ws_on_message,
            on_error = self.ws_on_error,
            on_close = self.ws_on_close)

        self.ws.on_open = self.ws_on_open

        self.ws.run_forever()

        pass


    def init_read_library(self):
        self.folderName = os.path.join(self.framemanager.getBehaviorPath(self.behaviorId), "./lib")

        if self.folderName not in sys.path:
            sys.path.append(self.folderName)
    ## ---- END INITIALIZE ---- ##


    ## ---- SEND PING ---- ##
    def sendPing(self):
        jsonData = json.dumps({"action":"ping", "data":"none"})
        self.ws.send(jsonData)
        self.log("____________send ping____________")
        t=threading.Timer(30,self.sendPing)
        t.start()
        pass
    ## ---- SEND PING ---- ##


    ## ---- ROBOT EYE LOOP ---- ##
    def sendEyeTmp(self):
        self.log('send_eye_______2')
        self.video.subscribeCamera('camName', 0, 1)
        pass

    def sendEye(self):
        if self.sendEyeBlocking == False:
            import Image

            self.log("____________send eye____________")
            #INIT DATA
            tmpDir = os.path.join(self.framemanager.getBehaviorPath(self.behaviorId), "./html/tmp_picture")

            picture = self.video.getImageRemote(self.camObj)
            imgSize = (int(picture[0]),int(picture[1]))
            pngImg = Image.fromstring('RGB', imgSize, picture[6])

            savePath = tmpDir+"/tmp_eye.jpg"

            pngImg.save(savePath)

            imageData = open(savePath).read()

            if imageData != "":
                sendData  = '[!dataURL!]||||'
                sendData += 'eye_image||||'
                sendData += 'data:image/jpeg;base64,'+base64.b64encode(imageData)+'||||'
                sendData += str(self.connectonToken)

                self.ws.send(sendData)
                pass
        else:
            pass

        self.eyeTimer=threading.Timer(0.1,self.sendEye)
        self.eyeTimer.start()
        pass

    def stopEye(self):
        if self.eyeTimer != None:
            self.eyeTimer.cancel()
        pass
    ## ---- ROBOT EYE LOOP ---- ##