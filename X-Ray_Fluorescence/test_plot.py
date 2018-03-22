import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('SumCrossXRF/Calibration/7Mar_Cu1.txt', skip_header = 31, skip_footer = 71)
channel = np.arange(len(data))        
fig, ax = plt.subplots(figsize = (10,10))
ax.plot(channel, data)
ax.set_xlabel('Channel Number')
ax.set_ylabel('Counts (a.u.)')
ax.axhline(y=0, color = 'k')
ax.axvline(x=0, color = 'k')
fig.tight_layout()
fig.show()
