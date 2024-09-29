#Ömer Senih TOPRAK
from pymavlink import mavutil
import logging
import threading
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

Merkez=mavutil.mavlink_connection("udp:127.0.0.1:14550")


class Alici:
    
    def H_yazdir():
        H_mesaji=Merkez.recv_match(type="HEARTBEAT",blocking=True)
        while True:
            logging.info(H_mesaji)
            time.sleep(1)
    def A_yazdir():
        A_mesaji=Merkez.recv_match(type="ATTITUDE",blocking=True)
        while True:
            logging.info(A_mesaji)
            time.sleep(1)

H_Thread=threading.Thread(target=Alici.H_yazdir)
A_Thread=threading.Thread(target=Alici.A_yazdir)

H_Thread.start()
A_Thread.start()

H_Thread.join()
A_Thread.join()

