import shutil
import os

sourcedir = "/home/bjorn/Documents/CU/PHYS_4430/Data/run4"; digits = 3

files = os.listdir(sourcedir)
for item in files:
    name = item.split('run4_')
    zeros = digits - len(name[1])
    newname = name[0] + "run4_" + str(zeros*"0") + name[1] + ".txt"
    shutil.move(sourcedir + "/"+item, sourcedir+"/"+newname)
