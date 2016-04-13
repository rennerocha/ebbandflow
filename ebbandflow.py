from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession

from hydroponic_plant import HydroponicPlan


class AppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        hydroponic_plant = HydroponicPlan()
        status = hydroponic_plant.status
        yield self.publish('com.ebbandflow.onread', status)


        def onwrite(msg):
            # self.log.info("event for 'onwrite' received: {msg}", msg=msg)

            substrate_humidity_set_point = msg.get('substrate_humidity_set_point', None)
            if substrate_humidity_set_point:
                hydroponic_plant.substrate_humidity_set_point = int(substrate_humidity_set_point)

            substrate_humidity_pump = msg.get('substrate_humidity_pump', None)
            if substrate_humidity_pump is not None:
                hydroponic_plant.substrate_humidity_pump = int(substrate_humidity_pump)

            operation_mode = msg.get('operation_mode', None)
            if operation_mode and operation_mode in ['auto', 'manual']:
                hydroponic_plant.operation_mode = operation_mode

        yield self.subscribe(onwrite, 'com.ebbandflow.onwrite')
        self.log.info("subscribed to topic 'onwrite'")

        while True:
            status = hydroponic_plant.status
            self.log.info("hydroponic plant status: {0}".format(status))
            yield self.publish('com.ebbandflow.onread', status)
            yield sleep(60)
