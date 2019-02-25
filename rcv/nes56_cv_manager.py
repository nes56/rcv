import constants
import json
import rcv_utils
import logging
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
        self._roborio_ip = conf.get('rcv_server', 'roborio_ip')
        self._roborio_port = int(conf.get('rcv_server', 'roborio_port'))
        self._socket_timeout = int(conf.get('rcv_server', 'socket_timeout'))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logging.debug("Entered Nes56CvManager.__exit__(..)")
        if self._client_socket:
            self._client_socket.close()

    def init_video_source(self):


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
        for i in range(10):
            rcv_manager.send_data_to_roborio(json.dumps(API_structure))




