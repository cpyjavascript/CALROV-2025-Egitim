from pymavlink import mavutil
import logging
import threading
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s%] %(messsage)s"
)

baglanti = mavutil.mavlink_connection("udp:127.0.0.1:14550")

class ayirici:
    def heartbeat_ayirici():
        heartbeat_mesaji = baglanti.recv_match(type="HEARTBEAT",blocking="True")
        while True:
            logging.INFO(f"HEARTBEAT - System Status: {heartbeat_mesaji.system_status}")
            time.sleep(1.5)
    def attitude_ayirici():
        attitude_mesaji = baglanti.recv_match(type="ATTITUDE",blocking="True")
        while True:
            logging.INFO(f"ATTITUDE - Roll: {attitude_mesaji.roll}, Pitch: {attitude_mesaji.pitch}, Yaw: {attitude_mesaji.yaw}")
            time.sleep(1.5)

heartbeat_thread = threading.Thread(target=ayirici.heartbeat_ayirici)
attitude_thread = threading.Thread(target=ayirici.attitude_ayirici)

heartbeat_thread.start()
attitude_thread.start()

heartbeat_thread.join()
attitude_thread.join()

