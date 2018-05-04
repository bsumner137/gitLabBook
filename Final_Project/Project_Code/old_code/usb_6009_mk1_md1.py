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
        self.data = np.array([])
        self.ctsPerSec = 0 #calibration factor.  Multiply by desired time (in seconds) to get number of pulses
        self.duration = 0
        self.CHANNEL = [ np.array([[0],[0]]), np.array([[0],[1]]), np.array([[1],[0]]), np.array([[1],[1]]) ]
        self.calibrated = False

    def add(self, channel_ID):
        """
        Specify the name of the device and the desired channel for output
        """

        self.task.ao_channels.add_ao_voltage_chan(channel_ID, "", 0.0, 5.0)
        self.channels += 1

    def calibrate(self, num_cycles):
        """
        generates continuous pulses of 1000 counts.  Asks user to input average frequency.
        Converts this into the appropriate conversion factor for later use.  Use this AFTER adding channels.
        """
        if not self.channels:
            print('No Channels.  Use add() to add channels')
            return
        
        c1 = 5*np.concatenate((np.ones(1000),np.zeros(1000)))
        cal_data = np.array([c1,c1])

        print("Calibrating, please wait\n")
        for i in np.arange(num_cycles):
            self.task.write(cal_data, auto_start = True)

        freq = float(input("Enter frequency to nearest Hz: "))
        self.ctsPerSec = freq*2000 #there are 2000 counts per cycle

        self.calibrated = True

    def build(self, channel_sequence, time_sequence):
        """
        on_off_sequence is an array stating which signal (after processing by demux) should be on.
        This array should be a 1D array of ints: i.e. [1,3,2,4,1,2]

        time_sequence is a numpy array with the amount of time (in ms, integers only) for each row of the on_off_sequence.
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

                
            self.data = 5*np.delete(d1,0,1)

    def BlowIt(self):
        """
        Use this when ready to send signals built in 'build' to the USB-6009
        """

        print("Writing signal, beginning output\n")

        self.task.write(self.data, auto_start = True)
##
##ao_card = usb6009()
##ao_card.add("Dev1/ao0")
##ao_card.add("Dev1/ao1")
##ao_card.calibrate(20)
