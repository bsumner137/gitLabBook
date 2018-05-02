import nidaqmx
import numpy as np
import time

class usb6009:
    """
    Creates an object that allows the user to interact with the National Instruments
    USB-6009 DAQ.  Methods include specifying a pulse train and the coltage level of the output
    """
    
    def __init__(self):
        self.ms = 1e-3
        self.pulse_time  #specify time duration of a  1000 element pulse
        self.channels = {}
        self.task = nidaqmx.Task()
        self.data = np.array([])
        self.time = 0 #calibration factor.  Multiply by desired time (in seconds) to get number of pulses
        self.duration = 0
        self.CHANNEL = [ np.array([[0],[0]]), np.array([[0],[1]]), np.array([[1],[0]]), np.array([[1],[1]]) ]
        
    def add(self, channel_ID):
        """
        Specify the name of the device and the desired channel for output
        """
        self.task.ao_channels.add_ao_voltage_chan(channel_ID, "", 0.0, 5.0)
        
    def calibrate(self):
    	"""
    	generates continuous pulses of 1000 counts.  Asks user to input average time of pulse
    	width.  Converts this into the appropriate conversion factor for later use.  Use this
    	AFTER adding channels. 
    	"""
    	
    	c1 = 5*np.concatenate(np.ones(1000),np.zeros(1000))
    	cal_data = np.array([c1,c1])
    	
    	print("Wait approximately 30 seconds for calibration\n")
    	for i in np.arange(66):
    		self.task.write(cal_data, auto_start = True)
    	
    	freq = float(input("Enter frequency:\n"))
    	self.time = nit(round(1000*2*freq))

    def build(self, on_off_sequence, time_sequence):
        """
        on_off_sequence is an array stating which signal (after processing by demux) should be on.
        This array should be a 1D array of ints: i.e. [1,3,2,4,1,2]

        time_sequence is a numpy array with the amount of time (in ms) for each row of the on_off_sequence.
        It should be a 1D array with the same number of elements as one column of the on_off_sequence
        """
        if self.time ==0:
            print("Perform Calibration")
        else:
            counts = self.time*time_sequence*1e-3
            self.duration = np.sum(time_sequence)*1e-3
            d1 = np.array([])
            
            for i in np.arange(len(channel_sequence)):
                d1 = np.concatenate((d1,self.CHANNEL[channel_sequence[i]]* np.ones(counts[i])))

            self.data = 5*d1
	
    def BlowIt(self):
    	"""
    	Use this when ready to send signals built in 'build' to the USB-6009
    	"""
    	print("Writing signal, beginning output\n")
    	
    	self.task.write(self.data, auto_start = False)
    	
    	self.start()
    	time.sleep(self.duration+1)
    	self.stop()
    	
    	
    	
    	
##ao_card = usb6009()
##ao_card.add("Dev2/ao0")
##ao_card.add("Dev2/ao1")
##ao_card.calibrate()
##ao_card.build(np.array([[0,1,0,1],[1,0,0,1]]), np.array([1,.5,1,.5,1,.5,1,1]))
##ao_card.BlowIt()
