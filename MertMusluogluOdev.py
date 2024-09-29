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


    def attiduteYazdır(self):
        if self.mesaj and hasattr(self.mesaj, 'alt'):
            attidute = self.mesaj.alt
            self.logger.info(f"ATTIDUTE: {attidute}")
        sleep(1)

    def heartbYazdır(self):
        heartbeat = mavlinkBaglantisi.recv_match(type="HEARTBEAT", blocking=True)
        sleep(1)

nesneler = aksiyonlar(logger, None)

attidute_thread = Thread(target=nesneler.attiduteYazdır)
heartbeat_thread = Thread(target=nesneler.heartbYazdır)

attidute_thread.start()
heartbeat_thread.start()

while aktifMi:
    mesaj = mavlinkBaglantisi.recv_match(blocking=True)
    logger.info(mesaj)

    aksiyonlar.mesaj = mesaj
    sleep(1)

attidute_thread.join()
heartbeat_thread.join()
