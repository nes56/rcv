import socket
import errno
from combine_modules import get_data, init
import logging

def send_data():
    logging.debug("sending data")
    global connection_available
    data = get_data()
    try:
        client_socket.sendall(data)
        logging.debug("sent succesfully")
    except socket.error as e:
        logging.error("error in sending " + str(e))
        client_socket.close()
        connection_available = False


def init_socket():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(1)


def establish_connection():
    logging.debug("trying to connect")
    init_socket()
    err = client_socket.connect_ex((ip, port))    
    if err == socket.error:
        pass
    if err != 0:
        logging.error("couldn't connect "+ str(err))
        client_socket.close()
        return False
    else:
        logging.debug("connected")
        return True


def connect_and_send():
    global connection_available
    if not connection_available:
        connection_available = establish_connection()
    if connection_available:
        send_data()


def main():
    global ip
    global port
    global connection_available
    ip = '127.0.0.1'
    port = 5801
    connection_available = False   
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/home/pi/rcv/logs/myapp.log',
                    filemode='w')
    init()
    logging.debug("intialized camera succesfully")
    while True:
        connect_and_send()


if __name__ == '__main__':
    main()