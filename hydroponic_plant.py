import pyfirmata


class HydroponicPlan(object):

    def __init__(self, port='/dev/ttyUSB0'):
        # TODO auto search for Arduino port
        self.board = pyfirmata.Arduino(port)

        self._substrate_humidity_set_point = 70
        self.operation_mode = 'auto'

        self.DIGITAL = {
            'substrate_humidity_pump': self.board.digital[6]
        }

        self.ANALOG = {
            'substrate_humidity_1': self.board.analog[0],
            'substrate_humidity_2': self.board.analog[1],
            'substrate_humidity_3': self.board.analog[2],
            'solution_ph': self.board.analog[3],
        }
        for _, analog_input in self.ANALOG.items():
            analog_input.enable_reporting()

    @property
    def status(self):
        return {
            'operation_mode': self.operation_mode,
            'substrate_humidity': self.substrate_humidity,
            'solution_ph': self.solution_ph,
            'substrate_humidity_pump': self.substrate_humidity_pump,
            'substrate_humidity_set_point': self.substrate_humidity_set_point
        }

    @property
    def substrate_humidity(self):
        it = pyfirmata.util.Iterator(self.board)
        it.start()
        while self.ANALOG['substrate_humidity_1'].read() is None:
            pass
        reading_1 = round(map_value(self.ANALOG['substrate_humidity_1'].read(), 0, 0.7, 0, 100), 2)

        while self.ANALOG['substrate_humidity_2'].read() is None:
            pass
        reading_2 = round(map_value(self.ANALOG['substrate_humidity_2'].read(), 0, 0.7, 0, 100), 2)

        while self.ANALOG['substrate_humidity_3'].read() is None:
            pass
        reading_3 = round(map_value(self.ANALOG['substrate_humidity_3'].read(), 0, 0.7, 0, 100), 2)

        return round((reading_1 + reading_2 + reading_3) / 3.0, 2)

    @property
    def solution_ph(self):
        it = pyfirmata.util.Iterator(self.board)
        it.start()
        while self.ANALOG['solution_ph'].read() is None:
            pass
        return self.ANALOG['solution_ph'].read()

    @property
    def substrate_humidity_set_point(self):
        return self._substrate_humidity_set_point

    @substrate_humidity_set_point.setter
    def substrate_humidity_set_point(self, set_point):
        self._substrate_humidity_set_point = set_point

    @property
    def substrate_humidity_pump(self):
        if self.operation_mode == 'auto':
            if self.substrate_humidity < self.substrate_humidity_set_point:
                self.DIGITAL['substrate_humidity_pump'].write(1)
            else:
                self.DIGITAL['substrate_humidity_pump'].write(0)
        return self.DIGITAL['substrate_humidity_pump'].value

    @substrate_humidity_pump.setter
    def substrate_humidity_pump(self, value):
        if self.operation_mode == 'manual':
            self.DIGITAL['substrate_humidity_pump'].write(value)


def map_value(value, input_min, input_max, output_min, output_max):
    return (value - input_min) * (output_max - output_min) / (input_max - input_min) + output_min
