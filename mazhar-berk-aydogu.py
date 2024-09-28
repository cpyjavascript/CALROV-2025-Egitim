from pymavlink import mavutil
import logging
from threading import Thread, Lock
import time

lock = Lock()
conn = mavutil.mavlink_connection("udp:127.0.0.1:14550")
conn.wait_heartbeat()

class log:
    def Attidue_Log(_lock):
        _lock.acquire()
        msg = conn.recv_match(type = "ATTITUDE", blocking = True).to_dict()
        logging.error("ATTITUDE:\n" + str(msg))
        time.sleep(0.25)
        _lock.release()

    def Heartbeat_Log(_lock):
        _lock.acquire()
        msg = conn.recv_match(type = "HEARTBEAT", blocking = True).to_dict()
        logging.error("HEARTBEAT:\n" + str(msg))
        time.sleep(0.25)
        _lock.release()

while True:
    t1=Thread(target=log.Attidue_Log,args=(lock,))
    t2=Thread(target=log.Heartbeat_Log,args=(lock,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()