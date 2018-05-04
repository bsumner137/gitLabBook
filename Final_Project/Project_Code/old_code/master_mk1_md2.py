from pymba import *
import time
import numpy as np
import matplotlib.pyplot as plt
import cc2


card = cc2.usb6009()

card.add("Dev1/ao0")
card.add("Dev1/ao1")

##condition = input("Do you wish to calibrate (y/n)? ")
##if condition =='y':
##    card.calibrate(100,100)
##else:
##    freq = float(input("Enter frequency at 100 counts: "))
##    card.ctsPerSec = 100*2*freq
##    card.calibrated = True

card.ctsPerSec = 200*6.313
card.calibrated = True

card.build('MOTon', np.array([1]), np.array([1000]))
card.build('atom_image',np.array([0,2,0]), np.array([50,50,50]))
card.build('dark_image',np.array([2,0]), np.array([50,50]))
card.build('light_image', np.array([2,0]),np.array([50,50]))
card.build('reset', np.array([2,1]), np.array([50,50]))

with Vimba() as vimba:
    system = vimba.getSystem()

    if system.GeVTLIsPresent:
        system.runFeatureCommand("GeVDiscoveryAllOnce")
        time.sleep(0.2)

    cameraIds = vimba.getCameraIds()

    camera = vimba.getCamera(cameraIds[0])
    camera.openCamera()

    camera.AcquisitionMode = 'SingleFrame'
    
    frame_fluor = camera.getFrame()
    frame_fluor.announceFrame()
    frame_atom = camera.getFrame()
    frame_atom.announceFrame()
    frame_dark = camera.getFrame()
    frame_dark.announceFrame()
    frame_light = camera.getFrame()
    frame_light.announceFrame()

    card.BlowIt('MOTon')
    
    camera.startCapture()
    frame_fluor.queueFrameCapture()
    camera.runFeatureCommand('AcquisitionStart')
    camera.runFeatureCommand('AcquisitionStop')
    frame_fluor.waitFrameCapture()
    camera.endCapture()

    card.BlowIt('atom_image')

    camera.startCapture()
    frame_atom.queueFrameCapture()
    camera.runFeatureCommand('AcquisitionStart')
    camera.runFeatureCommand('AcquisitionStop')
    frame_atom.waitFrameCapture()
    camera.endCapture()

    card.BlowIt('dark_image')

    camera.startCapture()
    frame_dark.queueFrameCapture()
    camera.runFeatureCommand('AcquisitionStart')
    camera.runFeatureCommand('AcquisitionStop')
    frame_dark.waitFrameCapture()
    camera.endCapture()
    
    card.BlowIt('light_image')

    camera.startCapture()
    frame_light.queueFrameCapture()
    camera.runFeatureCommand('AcquisitionStart')
    camera.runFeatureCommand('AcquisitionStop')
    frame_light.waitFrameCapture()
    camera.endCapture()

    card.BlowIt('reset')

    img_fluor = np.ndarray(buffer = frame_fluor.getBufferByteData(),
                           dtype = np.uint8,
                           shape = (frame_fluor.height,
                                    frame_fluor.width,
                                    1))

    img_atom = np.ndarray(buffer = frame_atom.getBufferByteData(),
                           dtype = np.uint8,
                           shape = (frame_atom.height,
                                    frame_atom.width,
                                    1))

    img_dark = np.ndarray(buffer = frame_dark.getBufferByteData(),
                           dtype = np.uint8,
                           shape = (frame_dark.height,
                                    frame_dark.width,
                                    1))

    img_light = np.ndarray(buffer = frame_light.getBufferByteData(),
                           dtype = np.uint8,
                           shape = (frame_light.height,
                                    frame_light.width,
                                    1))

    camera.revokeAllFrames()
    camera.closeCamera()

img_collection = [img_fluor, img_atom, img_dark, img_light]

with np.errstate(divide = 'ignore'):
    img_adj = np.where((img_atom - img_dark) != 0,(img_light - img_dark)/(img_atom-img_dark),1)
    img_adj = np.log(img_adj).squeeze()

img_zoom = img_adj[100:237,200:430]

fluor_image = img_fluor.squeeze()

fluor_zoom = fluor_image[100:237,200:430]


fig, axes = plt.subplots(nrows=2, ncols =2)

fluor = axes[0,0].imshow(fluor_image, cmap = 'prism')
fig.colorbar(fluor, ax = axes[0,0])

fluor_zoom = axes[1,0].imshow(fluor_zoom, cmap = 'prism')
fig.colorbar(fluor_zoom, ax = axes[1,0])

absorb = axes[0,1].imshow(img_adj, cmap = 'prism')
fig.colorbar(absorb, ax = axes[0,1])

absorb_zoom = axes[1,1].imshow(img_zoom, cmap = 'prism')
fig.colorbar(absorb_zoom, ax = axes[1,1])

fig.show()
#ax1.set_title('Fluorescing MOT')


##fluor = ax1.imshow(tempimage, cmap = 'prism')
##fig.colorbar(fluor, ax = ax1)

#ax2 = set_title('Background Subtracted\nAbsorption Image')
##absorb = ax2.imshow(img_adj,cmap = 'prism')
##fig.colorbar(absorb, ax = ax2)

for i in np.arange(len(img_collection)):
    imgplot = plt.imshow(img_collection[i].squeeze(), cmap = 'prism')
    plt.colorbar()
    plt.show()

##img_zoom = 
