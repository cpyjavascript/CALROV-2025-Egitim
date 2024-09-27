from pymavlink import mavutil
import time
import logging
from threading import Thread

mavlink_connection = mavutil.mavlink_connection("udp:127.0.0.1:14550")
logger = logging.getLogger(__name__)
mavlink_connection.wait_heartbeat()



class MyClass():
    
    def __init__(self, logger, mavlink_message):
        self.logger = logger
        self.mavlink_message = mavlink_message
        
        
        
        
    def attitude_control(self):
        self.logger.critical(mavlink_message)
        
        

    def heartbeat_control(self):
        self.logger.critical(mavlink_message)




while True:
    
    mavlink_message = mavlink_connection.recv_match(blocking=True).to_dict()
    class_parts = MyClass(mavlink_message= mavlink_message, logger = logger)
    
    thread_heartbeat_check = Thread(target = class_parts.heartbeat_control)
    thread_attitude_check = Thread(target = class_parts.attitude_control)

    thread_attitude_check.start()
    thread_heartbeat_check.start()

    time.sleep(0.25)







