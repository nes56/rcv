import constants
import cv2
import json
import logging
import os
import rcv_utils
import socket



# globals
API_structure = {
        "front": False,
        "found": False,
        "p1": {"d": 0, "a": 0},
        "p2": {"d": 0, "a": 0},
    }


class Nes56CvManager():
    def __init__(self, conf):
        logging.debug("entered Nes56CvManager.__init__(...)")
        self._conf = conf
        self._client_socket = None
        self._cap = None
        self._width = None
        self._height = None
        self._video_source_type = None
        self._video_source = None
        self._camera_name = None
        self._fps = None
        self._roborio_ip = conf.get('rcv_server', 'roborio_ip')
        self._roborio_port = int(conf.get('rcv_server', 'roborio_port'))
        self._socket_timeout = int(conf.get('rcv_server', 'socket_timeout'))
        self._show = bool(conf.get('rcv_server', 'show'))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logging.debug("Entered Nes56CvManager.__exit__(..)")
        if self._client_socket:
            self._client_socket.close()
        if self._cap:
            self._cap.realease()

    def init_video_source(self):
        logging.debug("Enetered Nes56CvManager.init_video_source()")
        self._video_source_type, self._video_source = conf.get('rcv_server', 'video_source').split(':')
        if self._video_source_type == 'camera':
            self._video_source = int(self._video_source)
            self._height = float(conf.get('rcv_server', 'height'))
            self._width = float(conf.get('rcv_server', 'width'))
            self._camera_name = conf.get('rcv_server', 'camera_name')
            self._fps = float(conf.get('rcv_server', 'fps'))
        elif self._video_source_type == 'video':
            self._camera_name = os.path.basename(self._video_source)
        else:
            raise ValueError("Unsupported video_source - '{}'".format(self._video_source_type))
        self._cap = cv2.VideoCapture(self._video_source)
        if self._video_source_type == 'camera':
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self._cap.set(cv2.CAP_PROP_FPS, fps)

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
            else:
                logging.debug("connected")
        except:
            logging.exception("Exception", exc_info=1)

    def send_data_to_roborio(self, data):
        logging.debug("entered Nes56CvManager.send_data_to_roborio")
        try:
            self._client_socket.sendall(data)
            logging.debug("sent succesfully {}".format(data))
        except socket.error as e:
            logging.error("error in sending " + str(e))
            self._client_socket.close()
            self._client_socket = None


    def get_next_frame(self):
        pass

    def analyze_frame(self):
        pass


if __name__ == '__main__':
    rcv_utils.init_logging(constants.CONFIGURATION)
    conf = rcv_utils.load_configuration(constants.CONFIGURATION)
    with Nes56CvManager(conf) as rcv_manager:
        rcv_manager.connect_to_roborio()
        rcv_manager.init_video_source
        #for i in range(10):
        #    rcv_manager.send_data_to_roborio(json.dumps(API_structure))




