import constants
import logging
from nes56_cv_manager import Nes56CvManager
import rcv_utils
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
        self._nes56_cv_manager.stop()

    def do_work(self):
        logging.debug("Eneterring RcvService.do_work()")
        with Nes56CvManager(self._conf) as rcv_manager:
            rcv_manager.connect_to_roborio()
            rcv_manager.init_video_source()
            rcv_manager.run_loop()
        logging.debug("Exiting RcvService.do_work()")



if __name__ == '__main__':
    rcv = RcvService()
    rcv.do_work()
