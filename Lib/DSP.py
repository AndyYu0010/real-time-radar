# version: 1.0

import numpy as np


def Range_Doppler(data, mode=0, padding_size=None):
    """
    :param data: array_like
                    Input array with the shape [chirps, samples, channels]

    :param mode: int, optional
                    Mode of the output Range Doppler Image format, default is 0
                    0: return RDI in raw mode
                    1: return RDI in abs mode with fft shift and flip
                    2: return both mode 0 and 1

    :param padding_size: sequence of ints, optional
                    Shape(length after the transformed), s[0] refers to axis 0, s[1] to axis 1

    :return:complex array
                    Output RDI depends on mode, return a range doppler cube
    """
    # Windowing data
    window_1 = np.reshape(np.hanning(data.shape[1]), (data.shape[1], -1))
    window_2 = np.reshape(np.hanning(data.shape[0]), (-1, data.shape[0]))
    window = window_1 * window_2
    channel = data.shape[2]
    for i in range(channel):
        data[:, :, i] = data[:, :, i] * window.T
    # Range doppler processing
    if mode == 0:
        rdi_raw = np.fft.fft2(data, s=padding_size, axes=[0, 1])
        return rdi_raw

    elif mode == 1:
        rdi_abs = np.fft.fft2(data, s=padding_size, axes=[0, 1])
        rdi_abs = np.transpose(np.fft.fftshift(np.abs(rdi_abs), axes=0), [1, 0, 2])
        rdi_abs = np.flip(rdi_abs, axis=0)
        return rdi_abs

    elif mode == 2:
        rdi_raw = np.fft.fft2(data, s=padding_size, axes=[0, 1])
        rdi_abs = np.transpose(np.fft.fftshift(np.abs(rdi_raw), axes=0), [1, 0, 2])
        rdi_abs = np.flip(rdi_abs, axis=0)
        return [rdi_raw, rdi_abs]

    else:
        print("Error mode")
        raise ValueError


def Range_Angle(data, mode=0, padding_size=None):
    """
    :param data: array_like
                    Input array with the shape [chirps, samples, channels]

    :param mode: int, optional
                    Mode of the output Range Doppler Image format, default is 0
                    0: return RAI in raw mode
                    1: return RAI in abs mode with fft shift and flip
                    2: return both mode 0 and 1

    :param padding_size: sequence of ints, optional
                    Shape(length after the transformed), s[0] refers to axis 0, s[1] to axis 1, etc

    :return: complex array
                    Output RAI depends on mode, return a range angle cube
    """
    # Range Angel processing
    # Windowing data
    window_1 = np.reshape(np.hanning(data.shape[1]), (data.shape[1], -1))
    window_2 = np.reshape(np.hanning(data.shape[0]), (-1, data.shape[0]))
    window = window_1 * window_2
    channel = data.shape[2]
    for i in range(channel):
        data[:, :, i] = data[:, :, i] * window.T

    data = np.fft.fft2(data, s=[padding_size[0], padding_size[1]], axes=[0, 1])

    if mode == 0:
        rai_raw = np.fft.fft(data, n=padding_size[2], axis=2)
        return rai_raw

    elif mode == 1:
        rai_abs = np.fft.fft(data, n=padding_size[2], axis=2)
        rai_abs = np.fft.fftshift(np.abs(rai_abs), axes=2)
        rai_abs = np.flip(rai_abs, axis=1)
        return rai_abs

    elif mode == 2:
        rai_raw = np.fft.fft(data, n=padding_size[2], axis=2)
        rai_abs = np.fft.fftshift(np.abs(rai_raw), axes=2)
        rai_abs = np.flip(rai_abs, axis=1)
        return [rai_raw, rai_abs]

    else:
        print("Error mode")
        raise ValueError
