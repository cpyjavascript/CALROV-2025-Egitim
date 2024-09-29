from pymavlink import mavutil
from threading import Thread
from time import sleep
import logging

aktifMi = True
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Mert, hata alırsan "udp" adresine bak muhtemelen yanlış girmişsindir.
mavlinkBaglantisi = mavutil.mavlink_connection('udp:127.0.0.1:14550')
if mavlinkBaglantisi:
    logger.info("Bağlantı başarılı!")
else:
    logger.error("Bağlantı başarısız!")

mavlinkBaglantisi.wait_heartbeat()

class aksiyonlar:
    def __init__(self, logger, mesaj):
        self.logger = logger
        self.mesaj = mesaj


    def irtifaYazdır(self):
        if self.mesaj and hasattr(self.mesaj, 'alt'):
            irtifa = self.mesaj.alt
            self.logger.info(f"İrtifa: {irtifa} metre")
        sleep(1)

    def heartbYazdır(self):
        heartbeat = mavlinkBaglantisi.recv_match(type="HEARTBEAT", blocking=True)
        if heartbeat:
            self.logger.info(heartbeat)
        sleep(1)

nesneler = aksiyonlar(logger, None)

irtifa_thread = Thread(target=nesneler.irtifaYazdır)
heartbeat_thread = Thread(target=nesneler.heartbYazdır)

irtifa_thread.start()
heartbeat_thread.start()

while aktifMi:
    mesaj = mavlinkBaglantisi.recv_match(blocking=True)
    print(f"Gelen mesaj: {mesaj}")

    aksiyonlar.mesaj = mesaj
    sleep(1)

irtifa_thread.join()
heartbeat_thread.join()
