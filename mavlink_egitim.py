from pymavlink import mavutil

conn = mavutil.mavlink_connection("udp:0.0.0.0:14550")
conn.wait_heartbeat()

while True:
    msg = conn.recv_match(type = "GLOBAL_POSITION_INT", blocking = True).to_dict()
    print(msg)