import nidaqmx
import numpy as np
import time

class usb6009:
    """
    Creates an object that allows the user to interact with the National Instruments USB-6009 DAQ.
    Methods include specifying a pulse train and the coltage level of the output
    """

    def __init__(self):
        self.ms = 1e-3
        self.channels = 0
        self.task = nidaqmx.Task()
        self.data = {}
        self.ctsPerSec = 0 #calibration factor.  Multiply by desired time (in seconds) to get number of pulses
        self.duration = 0
        self.CHANNEL = [ np.array([[0],[0]]), np.array([[1],[0]]), np.array([[0],[1]]), np.array([[1],[1]]) ]
        self.calibrated = False

    def add(self, channel_ID):
        """
        Specify the name of the device and the desired channel for output
        """

        self.task.ao_channels.add_ao_voltage_chan(channel_ID, "", 0.0, 5.0)
        self.channels += 1

    def calibrate(self, num_cycles, num_counts):
        """
        generates continuous pulses of 1000 counts.  Asks user to input average time of pulse width.
        Converts this into the appropriate conversion factor for later use.  Use this AFTER adding channels.
        """
        
        if not self.channels:
            print('No Channels.  Use add() to add channels')
            return

        CH2_calib = np.concatenate((np.tile(self.CHANNEL[2],num_counts), np.tile(self.CHANNEL[0], num_counts)),axis=1)
        CH2_calib = 5*np.tile(CH2_calib, num_cycles)

        print("Wait for calibration\n")
        self.task.write(CH2_calib, auto_start = True)

        freq = float(input("Enter frequency:\n"))
        self.ctsPerSec = num_counts*freq*2 #there are 2*num_counts counts per cycle

        self.calibrated = True

    def build(self, seq_id, channel_sequence, time_sequence):
        """
        on_off_sequence is an array stating whether the signal is to be on or off.  It should be a 2D array,
        with the first element the output of channel one, and the second ... i.e. np.array([[1,0,1,1,0],[0,0,1,0,1]])

        time_sequence is a numpy array with the amount of time (in ms) for each row of the on_off_sequence.
        It should be a 1D array with the same number of elements as one column of the on_off_sequence
        """

        if not self.calibrated:
            print("Perform Calibration")
            return

        else:
            counts = np.round(self.ctsPerSec*time_sequence*1e-3)
            counts = counts.astype(int)
            self.duration = np.sum(time_sequence)*1e-3

            d1 = np.array([[0],[0]])

            for i in np.arange(len(channel_sequence)):
                d1 = np.hstack((d1,np.tile(self.CHANNEL[channel_sequence[i]], counts[i])))

            self.data[seq_id] = 5*np.delete(d1,0,1)

    def BlowIt(self, sequence):
        """
        Use this when ready to send signals built in 'build' to the USB-6009
        """

        print("Writing signal, beginning output\n")

        self.task.write(self.data[sequence], auto_start = True)
