import time
from pymavlink import mavutil

target_system = 1
target_component = 1
baglanti = mavutil.mavlink_connection('udpout:127.0.0.1:14550', source_system=target_system)

start_time = time.time()


def hearbeat_atar_2000():
    baglanti.mav.heartbeat_send(
        type=mavutil.mavlink.MAV_TYPE_QUADROTOR,
        autopilot=mavutil.mavlink.MAV_AUTOPILOT_GENERIC,
        base_mode=0,
        custom_mode=0,
        system_status=mavutil.mavlink.MAV_STATE_ACTIVE
    )


def bu_da_attitude_atıyo(roll, pitch, yaw):
    time_boot_ms = int((time.time() - start_time) * 1000)  # Geçen süreyi milisaniyeye çevir

    baglanti.mav.attitude_send(
        time_boot_ms=time_boot_ms,
        roll=roll,
        pitch=pitch,
        yaw=yaw,
        rollspeed=0,
        pitchspeed=0,
        yawspeed=0
    )


if __name__ == '__main__':
    while True:
        hearbeat_atar_2000()
        bu_da_attitude_atıyo(roll=0.212313, pitch=0.8281381, yaw=0.0137163163)
        time.sleep(1.5)
