import time
import logging
import threading
from pymavlink import mavutil
baglanti=mavutil.mavlink_connection("udp:127.0.0.1:14550")
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MAVLinkinfo:
    def __init__(self, connection):
        self.mavlink = connection
        logging.debug
    
    def attitude_info(self):
        while True:
            message = self.mavlink.recv_match(type='ATTITUDE', blocking=True)
            if message:
                logging.debug("ATTITUDE: Roll=%f, Pitch=%f, Yaw=%f", 
                              message.roll, message.pitch, message.yaw)
            time.sleep(0.1)

    def heartbeat_info(self):
        while True:
            message = self.mavlink.recv_match(type='HEARTBEAT', blocking=True)
            if message:
                logging.debug("HEARTBEAT: Type=%d, Autopilot=%d, Base Mode=%d", 
                              message.type, message.autopilot, message.base_mode)
            time.sleep(0.1)

    def start(self):
        attitude_thread = threading.Thread(target=self.attitude_info)
        heartbeat_thread = threading.Thread(target=self.heartbeat_info)

        
        attitude_thread.start()
        heartbeat_thread.start()

        
        attitude_thread.join()
        heartbeat_thread.join()


if __name__ == "__main__":
    mavlink_listener = MAVLinkinfo(baglanti)
    mavlink_listener.start()
        