# collect data from TI DCA1000 EVM

import serial
import time


# Radar EVM setting
class SerialConfig():
    def __init__(self, name, CLIPort, BaudRate):
        self.name = name
        self.CLIPort = serial.Serial(CLIPort, baudrate=BaudRate)

    def SendConfig(self, ConfigFileName):
        for line in open(ConfigFileName):
            self.CLIPort.write((line.rstrip('\r\n') + '\n').encode())
            print(line)
            time.sleep(0.01)

    def StartRadar(self):
        self.CLIPort.write('sensorStart\n'.encode())
        print('sensorStart\n')

    def StopRadar(self):
        self.CLIPort.write('sensorStop\n'.encode())
        print('sensorStop\n')

    def DisconnectRadar(self):
        self.CLIPort.write('sensorStop\n'.encode())
        self.CLIPort.close()