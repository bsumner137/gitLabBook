import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import os

filelist = glob.glob('/home/bjorn/Documents/CU/PHYS_4430/Data/run1/*.txt')

video_raw = np.zeros((len(filelist),480,640))

for i in np.arange(len(filelist)):
    video_raw[i] = np.loadtxt(filelist[i])

mean_frame = video_raw.mean(axis=0)

lin_adj = 
