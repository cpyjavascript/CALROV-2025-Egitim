from time import sleep
from pymavlink import mavutil
import logging
import threading
import  time
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s")

master = mavutil.mavlink_connection("udp:127.0.0.1:14550")
master.wait_heartbeat()
class Log:
    def heartbeat():
        while True:
            logging.info(master.recv_match(type='HEARTBEAT', blocking=True).to_dict())

    def attitude():
        while True:
            logging.info(master.recv_match(type='ATTITUDE', blocking=True).to_dict())
log = Log

threading.Thread(target=log.heartbeat).start()
threading.Thread(target=log.attitude).start()




