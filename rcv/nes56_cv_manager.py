import constants
import cv2
import logging
import os
import rcv_utils
import socket
import sys
import json


class Nes56CvManager():
    def __init__(self, conf):
        logging.debug("entered Nes56CvManager.__init__(...)")
        self._stop = False
        self._conf = conf
        self._client_socket = None
        self._cap = None
        self._width = None
        self._height = None
        self._video_source_type = None
        self._video_source = None
        self._camera_name = None
        self._fps = None
        self._connected = False
        self._roborio_ip = self._conf.get('rcv_server', 'roborio_ip')
        self._roborio_port = int(self._conf.get('rcv_server', 'roborio_port'))
        self._socket_timeout = int(self._conf.get('rcv_server', 'socket_timeout'))
        self._show = self._conf.getboolean ('rcv_server', 'show')
        self._is_front = self._conf.getboolean('rcv_server', 'is_front')
        # Handling the dynamic load of the frame handler
        self._frame_handler_module = self._conf.get('rcv_server', 'frame_handler')
        self._frame_handlers_dir = self._conf.get('rcv_server', 'frame_handlers_dir')
        handlers_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_handlers")
        sys.path.append(handlers_path)
        self._frame_handler_class = getattr(
            __import__(self._frame_handler_module), "FrameHandler")
        self._frame_handler = self._frame_handler_class(conf)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logging.debug("Entered Nes56CvManager.__exit__(..)")
        if self._client_socket:
            self._client_socket.close()
        if self._cap:
            self._cap.release()
        if self._show:
            cv2.destroyAllWindows()

    def init_video_source(self):
        logging.debug("Entered Nes56CvManager.init_video_source()")
        self._video_source_type, self._video_source = self._conf.get('rcv_server', 'video_source').split(':')
        print("video_source_type = {}".format(self._video_source_type))
        print("video_source = {}".format(self._video_source))
        if self._video_source_type == 'camera':
            self._video_source = int(self._video_source)
            self._height = float(self._conf.get('rcv_server', 'height'))
            self._width = float(self._conf.get('rcv_server', 'width'))
            self._camera_name = self._conf.get('rcv_server', 'camera_name')
            self._fps = float(self._conf.get('rcv_server', 'fps'))
        elif self._video_source_type == 'video':
            self._camera_name = os.path.basename(self._video_source)
        else:
            raise ValueError("Unsupported video_source - '{}'".format(self._video_source_type))
        self._cap = cv2.VideoCapture(self._video_source)
        if self._video_source_type == 'camera':
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)
            self._cap.set(cv2.CAP_PROP_FPS, self._fps)

    def is_capture_opened(self):
        return self._cap.isOpened()

    def connect_to_roborio(self):
        logging.debug("entered Nes56CvManager.connect_to_roborio")
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_socket.settimeout(self._socket_timeout)
        err = None
        try:
            err = self._client_socket.connect_ex((self._roborio_ip,
                                                  self._roborio_port))
            if err != 0:
                logging.error("couldn't connect "+ str(err))
                self._client_socket.close()
                self._client_socket = None
                self._connected = False
            else:
                logging.debug("connected")
                self._connected = True
        except:
            logging.exception("Exception", exc_info=1)
            self._connected = False

    def send_data_to_roborio(self, data):
        logging.debug("entered Nes56CvManager.send_data_to_roborio")
        try:
            self._client_socket.sendall(data)
            logging.debug("sent succesfully {}".format(data))
        except socket.error as e:
            logging.error("error in sending " + str(e))
            self._connected = False
            self._client_socket.close()
            self._client_socket = None

    def get_next_frame(self):
        ret, frame = self._cap.read()
        return (ret, frame)

    def analyze_frame(self, frame):
        return self._frame_handler.handle_frame(frame)

    def stop(self):
        self._stop = True

    def run_loop(self):
        while self.is_capture_opened() and not self._stop:
            ret, frame = self.get_next_frame()
            if not self._connected:
                self.connect_to_roborio()
            if ret == True and self._connected:
                data = self.analyze_frame(frame)
                data['front'] = self._is_front
                self.send_data_to_roborio(json.dumps(data).encode('utf-8'))
                logging.info(data)


if __name__ == '__main__':
    rcv_utils.init_logging(constants.CONFIGURATION)
    conf = rcv_utils.load_configuration(constants.CONFIGURATION)
    with Nes56CvManager(conf) as rcv_manager:
        rcv_manager.connect_to_roborio()
        rcv_manager.init_video_source()
        rcv_manager.run_loop()
