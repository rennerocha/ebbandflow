

from serial import *
from threading import Thread

last_received = ''

def receiving(ser):
    global last_received
    buffer = ''

    while True:
        # last_received = ser.readline()
        buffer += ser.read(ser.inWaiting())
        if '\n' in buffer:
            last_received, buffer = buffer.split('\n')[-2:]

            print last_received

if __name__ ==  '__main__':
    ser = Serial(
        port='/dev/ttyUSB0',
        baudrate=57600,
        timeout=0.1
    )

    ser.write('r')

    Thread(target=receiving, args=(ser,)).start()

