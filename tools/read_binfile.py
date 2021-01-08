# version: 1.1

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


def read_bin_file(file_name, config, mode=0, header=True, packet_num=1443):
    """
    for bin data use
    :param file_name: string
                    Input file name

    :param config: sequence of ints
                    Radar config in the order
                    [0]: frames number
                    [1]: samples number
                    [2]: chirps number
                    [3]: transmit antenna number
                    [4]: receive antenna number

    :param mode: int, optional
                    Select radar EVM, default is 0
                    0: XWR1443
                    1: XWR1843

    :param header: Boolean, optional
                    Remove studio UDP header
                    True: remove
                    False: don't remove

    :param packet_num: int
                    Number of Packet
                    1441: 1 tx
                    2881: 2 tx
                    4322: 3 tx, default

    :return: complex array
                    Return data cube depends on mode
                    data cube [frame, chirp, sample, channel]
    """
    # Read file
    if header:
        data = remove_header(file_name, packet_num)
    else:
        data = np.fromfile(file_name, dtype=np.int16)

    frame = config[0]
    sample = config[1]
    chirp = config[2]
    tx_num = config[3]
    rx_num = config[4]

    if mode == 0:
        data = np.reshape(data, [-1, 8])
        data = data[:, 0:4:] + 1j * data[:, 4::]
        if rx_num == 4:
            cdata1 = np.reshape(data[:, 0], [frame, chirp, tx_num, sample])
            cdata1 = np.transpose(cdata1, [0, 1, 3, 2])  # frame, chirp, sample, channel
            cdata2 = np.reshape(data[:, 1], [frame, chirp, tx_num, sample])
            cdata2 = np.transpose(cdata2, [0, 1, 3, 2])  # frame, chirp, sample, channel
            cdata3 = np.reshape(data[:, 2], [frame, chirp, tx_num, sample])
            cdata3 = np.transpose(cdata3, [0, 1, 3, 2])  # frame, chirp, sample, channel
            cdata4 = np.reshape(data[:, 3], [frame, chirp, tx_num, sample])
            cdata4 = np.transpose(cdata4, [0, 1, 3, 2])  # frame, chirp, sample, channel

            if tx_num == 3:
                cdata = np.array([cdata1[:, :, :, 0], cdata2[:, :, :, 0], cdata3[:, :, :, 0], cdata4[:, :, :, 0],
                                  cdata1[:, :, :, 1], cdata2[:, :, :, 1], cdata3[:, :, :, 1], cdata4[:, :, :, 1],
                                  cdata1[:, :, :, 2], cdata2[:, :, :, 2], cdata3[:, :, :, 2], cdata4[:, :, :, 2]])
                cdata = np.transpose(cdata, [1, 2, 3, 0])
                # cdata = np.concatenate([cdata1, cdata2, cdata3, cdata4], axis=3)
                return cdata  # frame, chirp, sample, channel(tx1,tx2,tx3)

            elif tx_num == 1:
                cdata = np.array([cdata1[:, :, :, 0], cdata2[:, :, :, 0], cdata3[:, :, :, 0], cdata4[:, :, :, 0]])
                cdata = np.transpose(cdata, [1, 2, 3, 0])
                return cdata  # frame, chirp, sample, channel

    elif mode == 1:  # testing
        data = np.reshape(data, [-1, 4])
        data = data[:, 0:2:] + 1j * data[:, 2::]
        data = np.reshape(data, [frame, chirp, tx_num, rx_num, sample])
        if rx_num == 4:
            cdata1 = data[:, :, :, 0, :]
            cdata1 = np.transpose(cdata1, [0, 1, 3, 2])
            cdata2 = data[:, :, :, 1, :]
            cdata2 = np.transpose(cdata2, [0, 1, 3, 2])
            cdata3 = data[:, :, :, 2, :]
            cdata3 = np.transpose(cdata3, [0, 1, 3, 2])
            cdata4 = data[:, :, :, 3, :]
            cdata4 = np.transpose(cdata4, [0, 1, 3, 2])

            if tx_num == 3:
                cdata = np.concatenate((cdata1, cdata2, cdata3, cdata4), axis=3)
                return cdata  # frame, chirp, sample, channel

            elif tx_num == 1:
                cdata = np.array([cdata1[:, :, :, 0], cdata2[:, :, :, 0], cdata3[:, :, :, 0], cdata4[:, :, :, 0]])
                cdata = np.transpose(cdata, [1, 2, 3, 0])
                return cdata  # frame, chirp, sample, channel

    else:
        raise ValueError

