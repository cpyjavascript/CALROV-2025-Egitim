from threading import Thread
from pymavlink import mavutil
import logging
import time

logger = logging.getLogger(__name__)
conn = mavutil.mavlink_connection('udp:127.0.0.1:14550')

class MainClass():
    def __init__(self, logger, connection):
        self.logger = logger
        self.connection = connection

    def extractHeartbeat(self):
        #heartbeat_value = self.connection.get("mavpackettype")

        self.logger.warning(connection)
    
    def extractAttitude(self):
        #attitude_value = self.connection.get("mavpackettype")

        self.logger.warning(connection)

while True:
    connection = conn.recv_match(blocking = True).to_dict()

    classObject = MainClass(logger = logger, connection = connection)

    thread_heartbeat = Thread(target = classObject.extractHeartbeat)
    thread_attitude = Thread(target = classObject.extractAttitude)

    thread_heartbeat.start()
    thread_attitude.start()

    time.sleep(0.5)