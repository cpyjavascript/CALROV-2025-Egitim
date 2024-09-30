import threading
import logging
import time
from pymavlink import mavutil

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MAVLinkListener:
    def __init__(self, connection_string):
        self.master = mavutil.mavlink_connection(connection_string)

    def listen_attitude(self):
        while True:
            msg = self.master.recv_match(type='ATTITUDE', blocking=True)
            if msg:
                self.process_attitude(msg)

    def listen_heartbeat(self):
        while True:
            msg = self.master.recv_match(type='HEARTBEAT', blocking=True)

            if msg:
                heartbeat_type = msg.type
                autopilot = msg.autopilot
                base_mode = msg.base_mode
                custom_mode = msg.custom_mode
                system_status = msg.system_status
                mavlink_version = msg.mavlink_version

                logging.info(f"Heartbeat Values: Type={heartbeat_type}, Autopilot={autopilot}, Base Mode={base_mode}, Custom Mode={custom_mode}, System Status={system_status}, MAVLink Version={mavlink_version}")

                time.sleep(2)

    def process_attitude(self, msg):
        pass

    def start_listening(self):
        attitude_thread = threading.Thread(target=self.listen_attitude)
        heartbeat_thread = threading.Thread(target=self.listen_heartbeat)

        attitude_thread.start()
        heartbeat_thread.start()

        attitude_thread.join()
        heartbeat_thread.join()

if __name__ == "__main__":
    connection_string = "udp:127.0.0.1:14550"
    listener = MAVLinkListener(connection_string)
    listener.start_listening()
