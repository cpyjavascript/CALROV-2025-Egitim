import threading
import logging
from pymavlink import mavutil
the_connection = mavutil.mavlink_connection("udp:127.0.1:14550")
the_connection.wait_heartbeat()
class bilgi:
    def attitute_i(self):
        attitude_bigisi=the_connection.recv_match(type="ATTITUTE",blocking =True)
        while True:
         logging.info(attitude_bigisi)
    
    def heartbeat_i(self):
        heart_beat_bilgisi=the_connection.recv_match(type="HEARTBEAT",blocking =True)
        while True:
         logging(heart_beat_bilgisi)


    t1=threading.Thread(target=attitute_i)  
    t2=threading.Thread(target=heartbeat_i)  
    
    while True:
        t1.start()
        t2.start()

        t1.join()
        t2.join()

