import numpy as np


def remove_header(filename, packet_num):
    """
    for raw mmWave studio data use
    :param filename: string
                    Input file name

    :param packet_num: int
                    Number of Packet
                    1441: 1 tx
                    2881: 2 tx
                    4322: 3 tx

    """
    bin_data = np.fromfile(filename, dtype=np.int16)
    index = []
    for i in range(packet_num):
        j = i * 735
        index.append([j, j + 1, j + 2, j + 3, j + 4, j + 5, j + 6])
    output = np.delete(bin_data, index)
    return output
