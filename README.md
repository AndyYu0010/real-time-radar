# Real-time-radar
Python program used to control the TI mmWave radar ***XWR1843 EVM*** and data catch board ***DCA1000 EVM***, streaming out the 
adc samples data from DCA1000. Real time processes the adc data and generate Range-Doppler and Range-Angle
images.

## Required Python packages
* numpy
* serial
* pyqtgraph
* pyqt5

## Program Functions
* send_cmd(): Send command to ***DCA1000***.
* update_figure(): Refresh RDI and RAI.
* plot(): Create QTgui ogject to plot RDI and RAI.
* UdpListener(): Streaming out adc samples from ***DCA1000***.
* DataProcessor(): Processing adc samples to generate RDI and RAI.
* SerialConfig(): Config XWR1843 EVM.

## How to Use
This program is for ***XWR1843***, if you use other radar EVM, you should modify the code.
Execute by the following steps:
   1. Use TI's tool "UniFlash" flash the radar EVM, make sure that the radar EVM is running with demo firmware.
   2. Check and modify the config COM Port of radar EVM.
   3. Check the host IP is 192.168.33.30.
   4. Execute IWR1843_real_time_plot_RDI_RAI_app.py

## Demo 
![](Demo.PNG)

## Contact
Jih-Tsun Yu E-mail:t108368020@ntut.org.tw


## Acknowledgement
Thanks for TI, TI's e2e forum, and other people work on mmWave Radar make this happen.
Also grateful for the help from Prof. Po-Hsuang Tseng and Chieh-Hsun Hsieh


