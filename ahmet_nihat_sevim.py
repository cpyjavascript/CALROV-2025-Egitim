from threading import Thread
from pymavlink import mavutil
import logging
import time

logger = logging.getLogger(__name__)
connection = mavutil.mavlink_connection("/dev/ttyACM0")

connection.wait_heartbeat()

class MainClass():
    def __init__(self, logger, connection):
        self.logger = logger
        self.connection = connection.recv_match(blocking = True).to_dict()

    def extractHeartbeat(self):
        heartbeat_value = self.connection["HEARTBEAT"]

        self.logger.warning(heartbeat_value)
    
    def extractAttitude(self):
        attitude_value = self.connection["ATTITUDE"]

        self.logger.warning(attitude_value)
    
classObject = MainClass(logger = logger, connection = connection)

while True:
    thread_heartbeat = Thread(target = classObject.extractHeartbeat)
    thread_attitude = Thread(target = classObject.extractAttitude)

    thread_heartbeat.start()
    thread_attitude.start()

    time.sleep(0.5)