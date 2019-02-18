import configparser
import logging
import logging.config
import time


CONFIGURATION='/opt/rcv/service/rcv_server.conf'


class RcvService:
    def __init__(self):
        self._stop = False
        self._roborio_ip = None
        self._roborio_port = None
        self.load_configuration()
        self.init_logging()
        logging.info("self.__roborio_ip = {}".format(self._roborio_ip))
        logging.info("self.__roborio_port = {}".format(self._roborio_port))

    def load_configuration(self):
        conf = configparser.ConfigParser()
        conf.read(CONFIGURATION)
        self._roborio_ip = conf.get('rcv_server', 'roborio_ip')
        self._roborio_port = conf.get('rcv_server', 'roborio_port')

    def init_logging(self):
        logging.config.fileConfig(fname=CONFIGURATION)
        logging.info("Started....")

    def init_threads(self):
        pass

    def stop(self):
        self._stop = True

    def do_work(self):
        counter = 1
        while not self._stop:
            logging.debug("{}) ##### In loop ...".format(counter))
            time.sleep(2)
            counter += 1
            if counter == 10:
                self._stop = True


if __name__ == '__main__':
    rcv = RcvService()
    rcv.do_work()
    logging.info("Exiting ....")
