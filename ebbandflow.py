from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
import serial

import random
import json


class AppSession(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):

        def onwrite(msg):
            self.log.info("event for 'onwrite' received: {msg}", msg=msg)

        yield self.subscribe(onwrite, 'com.ebbandflow.onwrite')
        self.log.info("subscribed to topic 'onwrite'")

        read_result = ''
        # ser = serial.Serial('/dev/ttyUSB0', 9600)
        while True:
            yield self.publish('com.ebbandflow.onread', json.dumps(read_result))
            self.log.info('published to "onread" with result {read_result}',
                read_result=read_result)
            # read_result = ser.readline()

            read_result = {
                'substrate_humidity': random.randint(50,70),
                'ph_up_pump': 'ON',
                'ph_down_pump': 'OFF',
                'substrate_humidity_pump': 'OFF',
                'env_temp': random.randint(20, 25),
                'env_humidity': random.randint(50, 70),
                'solution_temp': random.randint(15, 25),
                'solution_ph': random.randint(60, 80) / 10.0,
                'substrate_humidity': random.randint(50, 70),
            }

            yield sleep(5)