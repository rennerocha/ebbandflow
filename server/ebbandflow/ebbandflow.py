from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

import models
import time
import serial
import json

port = '/dev/ttyUSB0'
arduino = serial.Serial(port, 57600, timeout=5)
time.sleep(2)


class AppSession(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):

        def leitura():
            self.log.info("Leitura solicitada")
            ultimas_leituras = models.StatusPlanta.select().order_by(models.StatusPlanta.created_date.desc()).limit(10)
            return [leitura.to_dict() for leitura in ultimas_leituras]

        yield self.register(leitura, 'com.ebbandflow.leitura')

        def comando_serial(comando):
            arduino.write(bytes(comando))
            return 'OK'
        yield self.register(comando_serial, 'com.ebbandflow.comando_serial')

        intervalo_leitura = 5
        while True:
            arduino.write("r")  # Solicita leitura
            data = arduino.readlines()
            if(data):
                status = {}
                for line in data:
                    key, value = line.split('=')
                    status[key] = value.rstrip()
                models.StatusPlanta(**status).save()
                intervalo_leitura = int(status.get("intervalo_leitura", intervalo_leitura)) / 1000
                self.log.info("Leitura Arduino: {status}", data=json.dumps(status))
            yield sleep(intervalo_leitura)
