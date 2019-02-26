import configparser
import cv2
import logging
import logging.config
import time


def load_configuration(config_file):
    conf = configparser.ConfigParser()
    conf.read(config_file)
    return conf


def init_logging(log_conf_file):
    logging.config.fileConfig(fname=log_conf_file)
    logging.info("Initialized logger ....")


def show_image(frame):
    cv2.imshow('debug', frame)
    time.sleep(0.5)
    cv2.destroyWindow('debug')
