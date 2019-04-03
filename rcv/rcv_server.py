import constants
import logging
from nes56_cv_manager import Nes56CvManager
import rcv_utils
import signal

rcv = None


def exit_gracefully(signum, frame):
    logging.info("In exit_gracefully({}, {})".format(signum, frame)) 
    if rcv:
        rcv.stop()


signal.signal(signal.SIGTERM, exit_gracefully)
signal.signal(signal.SIGINT, exit_gracefully)


class RcvService:
    def __init__(self):
        rcv_utils.init_logging(constants.CONFIGURATION)
        self._conf = rcv_utils.load_configuration(constants.CONFIGURATION)
        self._rcv_manager = None


    def stop(self):
        self._rcv_manager.stop()

    def do_work(self):
        logging.debug("Entering RcvService.do_work()")
        with Nes56CvManager(self._conf) as self._rcv_manager:
            self._rcv_manager.connect_to_roborio()
            self._rcv_manager.init_video_source()
            self._rcv_manager.run_loop()
        logging.debug("Exiting RcvService.do_work()")



if __name__ == '__main__':
    rcv = RcvService()
    rcv.do_work()
