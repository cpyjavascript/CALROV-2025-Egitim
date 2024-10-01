from pymavlink import mavutil
from time import sleep
from threading import Thread
import logging

logger = logging.getLogger(__name__)

mavlinkBaglantisi = mavutil.mavlink_connection('udp:127.0.0.1:14550')
mavlinkBaglantisi.wait_heartbeat()

class functions:
    def attidute(self):
        logger.warning(mavlinkBaglantisi.recv_match(type="ATTITUDE",blocking=True))
    def heartb(self):
        logger.warning(mavlinkBaglantisi.recv_match(type="HEARTBEAT",blocking=True))

while True:
    attiduteThread=Thread(target=functions().attidute)
    heartbThread=Thread(target=functions().heartb)

    attiduteThread.start()
    heartbThread.start()

    attiduteThread.join()
    heartbThread.join()
