from pymavlink import mavutil
from threading import Thread
import logging

logger = logging.getLogger(__name__)

connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')
connection.wait_heartbeat()

""""
while True:
    logger.critical(connection.recv_match(type="ATTITUDE",blocking=True))
    logger.critical(connection.recv_match(type="HEARTBEAT",blocking=True))
"""

class mavlinkLogs:
    def attitudeLogs(self):
        logger.critical(connection.recv_match(type="ATTITUDE",blocking=True))
    def heartbeatLogs(self):
        logger.critical(connection.recv_match(type="HEARTBEAT",blocking=True))

t1=Thread(target=mavlinkLogs().attitudeLogs())
t2=Thread(target=mavlinkLogs().heartbeatLogs())

t1.start()
t2.start()

t1.join()
t2.join()
