from real_time_process import UdpListener, DataProcessor
from radar_config import SerialConfig
from queue import Queue
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import threading
import time
import sys
import socket


def send_cmd(code):
    # command code list
    CODE_1 = (0x01).to_bytes(2, byteorder='little', signed=False)
    CODE_2 = (0x02).to_bytes(2, byteorder='little', signed=False)
    CODE_3 = (0x03).to_bytes(2, byteorder='little', signed=False)
    CODE_4 = (0x04).to_bytes(2, byteorder='little', signed=False)
    CODE_5 = (0x05).to_bytes(2, byteorder='little', signed=False)
    CODE_6 = (0x06).to_bytes(2, byteorder='little', signed=False)
    CODE_7 = (0x07).to_bytes(2, byteorder='little', signed=False)
    CODE_8 = (0x08).to_bytes(2, byteorder='little', signed=False)
    CODE_9 = (0x09).to_bytes(2, byteorder='little', signed=False)
    CODE_A = (0x0A).to_bytes(2, byteorder='little', signed=False)
    CODE_B = (0x0B).to_bytes(2, byteorder='little', signed=False)
    CODE_C = (0x0C).to_bytes(2, byteorder='little', signed=False)
    CODE_D = (0x0D).to_bytes(2, byteorder='little', signed=False)
    CODE_E = (0x0E).to_bytes(2, byteorder='little', signed=False)

    # packet header & footer
    header = (0xA55A).to_bytes(2, byteorder='little', signed=False)
    footer = (0xEEAA).to_bytes(2, byteorder='little', signed=False)

    # data size
    dataSize_0 = (0x00).to_bytes(2, byteorder='little', signed=False)
    dataSize_6 = (0x06).to_bytes(2, byteorder='little', signed=False)

    # data
    data_FPGA_config = (0x01020102031e).to_bytes(6, byteorder='big', signed=False)
    data_packet_config = (0xc005350c0000).to_bytes(6, byteorder='big', signed=False)

    # connect to DCA1000
    connect_to_FPGA = header + CODE_9 + dataSize_0 + footer
    read_FPGA_version = header + CODE_E + dataSize_0 + footer
    config_FPGA = header + CODE_3 + dataSize_6 + data_FPGA_config + footer
    config_packet = header + CODE_B + dataSize_6 + data_packet_config + footer
    start_record = header + CODE_5 + dataSize_0 + footer
    stop_record = header + CODE_6 + dataSize_0 + footer

    if code == '9':
        re = connect_to_FPGA
    elif code == 'E':
        re = read_FPGA_version
    elif code == '3':
        re = config_FPGA
    elif code == 'B':
        re = config_packet
    elif code == '5':
        re = start_record
    elif code == '6':
        re = stop_record
    else:
        re = 'NULL'
    print('send command:', re.hex())
    return re


def update_figure():
    global img_rdi, img_rai, updateTime, view_text, count
    count += 1
    img_rdi.setImage(RDIData.get()[:, :, 0].T, axis=1)
    img_rai.setImage(RAIData.get()[0, :, :].T, axis=1)
    view_text.setText("Frame No.: " + str(count))
    QtCore.QTimer.singleShot(1, update_figure)
    now = ptime.time()
    updateTime = now


def plot(cfg, port):
    global img_rdi, img_rai, updateTime, view_text, count
    count = 0
    app = QtGui.QApplication([])
    win = pg.GraphicsLayoutWidget()
    win.show()
    # view_text = win.addViewBox()
    view_text = win.addLabel("hello")
    view_rdi = win.addViewBox()
    view_rai = win.addViewBox()
    # lock the aspect ratio so pixels are always square
    view_rdi.setAspectLocked(True)
    view_rai.setAspectLocked(True)
    img_rdi = pg.ImageItem(border='w')
    img_rai = pg.ImageItem(border='w')
    # Colormap
    position = np.arange(64)
    position = position / 64
    position[0] = 0
    position = np.flip(position)
    colors = [[62, 38, 168, 255], [63, 42, 180, 255], [65, 46, 191, 255], [67, 50, 202, 255], [69, 55, 213, 255],
              [70, 60, 222, 255], [71, 65, 229, 255], [70, 71, 233, 255], [70, 77, 236, 255], [69, 82, 240, 255],
              [68, 88, 243, 255],
              [68, 94, 247, 255], [67, 99, 250, 255], [66, 105, 254, 255], [62, 111, 254, 255], [56, 117, 254, 255],
              [50, 123, 252, 255],
              [47, 129, 250, 255], [46, 135, 246, 255], [45, 140, 243, 255], [43, 146, 238, 255], [39, 150, 235, 255],
              [37, 155, 232, 255],
              [35, 160, 229, 255], [31, 164, 225, 255], [28, 129, 222, 255], [24, 173, 219, 255], [17, 177, 214, 255],
              [7, 181, 208, 255],
              [1, 184, 202, 255], [2, 186, 195, 255], [11, 189, 188, 255], [24, 191, 182, 255], [36, 193, 174, 255],
              [44, 195, 167, 255],
              [49, 198, 159, 255], [55, 200, 151, 255], [63, 202, 142, 255], [74, 203, 132, 255], [88, 202, 121, 255],
              [102, 202, 111, 255],
              [116, 201, 100, 255], [130, 200, 89, 255], [144, 200, 78, 255], [157, 199, 68, 255], [171, 199, 57, 255],
              [185, 196, 49, 255],
              [197, 194, 42, 255], [209, 191, 39, 255], [220, 189, 41, 255], [230, 187, 45, 255], [239, 186, 53, 255],
              [248, 186, 61, 255],
              [254, 189, 60, 255], [252, 196, 57, 255], [251, 202, 53, 255], [249, 208, 50, 255], [248, 214, 46, 255],
              [246, 220, 43, 255],
              [245, 227, 39, 255], [246, 233, 35, 255], [246, 239, 31, 255], [247, 245, 27, 255], [249, 251, 20, 255]]
    colors = np.flip(colors, axis=0)
    color_map = pg.ColorMap(position, colors)
    lookup_table = color_map.getLookupTable(0.0, 1.0, 256)
    img_rdi.setLookupTable(lookup_table)
    img_rai.setLookupTable(lookup_table)
    view_rdi.addItem(img_rdi)
    view_rai.addItem(img_rai)
    # Set initial view bounds
    view_rdi.setRange(QtCore.QRectF(0, 0, 128, 128))
    view_rai.setRange(QtCore.QRectF(0, 0, 128, 128))
    updateTime = ptime.time()
    tt = SerialConfig(name='ConnectRadar', CLIPort=port, BaudRate=115200)
    tt.StopRadar()
    tt.SendConfig(cfg)

    update_figure()
    QtGui.QApplication.instance().exec_()
    tt.StopRadar()


# Queue for access data
BinData = Queue()
RDIData = Queue()
RAIData = Queue()
# Radar config
adc_sample = 64
chirp = 32
tx_num = 1
rx_num = 4
radar_config = [adc_sample, chirp, tx_num, rx_num]
frame_length = adc_sample * chirp * tx_num * rx_num * 2
# Host setting
address = ('192.168.33.30', 4098)
buff_size = 2097152

# config DCA1000 to receive bin data
config_address = ('192.168.33.30', 4096)
FPGA_address_cfg = ('192.168.33.180', 4096)
cmd_order = ['9', 'E', '3', 'B', '5', '6']
sockConfig = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockConfig.bind(config_address)

for k in range(5):
    # Send the command
    sockConfig.sendto(send_cmd(cmd_order[k]), FPGA_address_cfg)
    time.sleep(0.1)
    # Request data back on the config port
    msg, server = sockConfig.recvfrom(2048)
    print('receive command:', msg.hex())

collector = UdpListener('Listener', BinData, frame_length, address, buff_size)
processor = DataProcessor('Processor', radar_config, BinData, RDIData, RAIData)
config = '../config/IWR1843_cfg.cfg'
collector.start()
processor.start()
plotIMAGE = threading.Thread(target=plot(config, port='COM4'))
plotIMAGE.start()

sockConfig.sendto(send_cmd('6'), FPGA_address_cfg)
sockConfig.close()
collector.join(timeout=1)
processor.join(timeout=1)


print("Program close")
sys.exit()
