from pymavlink import mavutil


import logging 
import threading

logging.basicConfig(level=logging.INFO)



class MessageListener():

    def __init__(self):
        self.connection=mavutil.mavlink_connection('udpin:127.0.0.1:14550')  



    def get_heartbeat_message(self):
        while True:
            msg=self.connection.recv_match(blocking=True)

            if msg.get_type()== 'HEARTBEAT':
                logging.info(f"HeartBeat Message received from System {msg.get_srcSystem()}\n"
                             f"Type: {msg.type}\n"
                             f"Autopilot:{msg.autopilot}\n"
                             f"Base Mode: {msg.base_mode}\n"
                             f"Custom Mode: {msg.custom_mode}\n"
                             f"System Status: {msg.system_status}\n")



    def get_attitude_message(self):
               
        while True: 

            msg=self.connection.recv_match(blocking=True)
                        

            if msg.get_type()== 'ATTITUDE':
                logging.info(f"Attitude Message received from System {msg.get_srcSystem()}\n"
                         f"Time Boots ms: {msg.time_boot_ms}\n"
                         f"Roll:{msg.roll}\n"
                         f"Pitch: {msg.pitch}\n"
                         f"Yaw: {msg.yaw}\n"
                         f"Roll Speed: {msg.rollspeed}\n"
                         f"Yaw Speed: {msg.yawspeed}\n"
                         f"Pitch Speed: {msg.pitchspeed}\n")
                           

                



    def get_messages(self):
        thread_heartbeat= threading.Thread(target=self.get_heartbeat_message) 
        thread_attitude= threading.Thread(target=self.get_attitude_message) 



        thread_heartbeat.start()        
        thread_attitude.start()        



message_listener=MessageListener()          
message_listener.get_messages()     
