import configparser
import constants
import logging
import logging.config
import rcv_utils
import time
import signal

rcv = None


def exit_gracefully(signum, frame):
    global rcv
    logging.info("In exit_gracefully({}, {})".format(signum, frame)) 
    if rcv:
        rcv.stop()


signal.signal(signal.SIGTERM, exit_gracefully)


class RcvService:
    def __init__(self):
        self._stop = False
        rcv_utils.init_logging(constants.CONFIGURATION)
        self._conf = rcv_utils.load_configuration(constants.CONFIGURATION)


    def stop(self):
        self._stop = True

    def do_work(self):
        counter = 1
        while not self._stop:
            logging.debug("{}) ##### In loop ...".format(counter))
            time.sleep(2)
            counter += 1
            if counter == 100:
                self._stop = True
        logging.info("Exiting ....")


if __name__ == '__main__':
    rcv = RcvService()
    rcv.do_work()
