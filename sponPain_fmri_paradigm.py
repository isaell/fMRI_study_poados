#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Spontaneous Pain paradigm during fMRI
# # Isabel Ellerbrock, December 2019


from psychopy import core, visual, event, logging, gui

import numpy as np
import pandas as pd
import os
import sys

# build gui information
expName = 'sponPain'
mygui = gui.Dlg(title=expName)
mygui.addField("Subject ID:")
mygui.addField("Session (pre/post):")
mygui.show()  # this will present the actual gui to insert stim num and sess num

# create output data specifications
subj_id = mygui.data[0]
sess = mygui.data[1]
outFile = "C:/Users/pain_kosek/Documents/POADOS/sponPain_fmri_pain/data/" + \
    expName + "_" + subj_id + "_" + sess + ".csv"

if os.path.exists(outFile):
    sys.exit("Data path " + outFile + " already exists!")

# create a window to display stuff in
win = visual.Window(color=[0, 0, 0],
                    monitor='testMonitor',
                    mouseVisible=False,
                    screen=1,          # 1 = display computer scanning, 0 = control/MRI computer
                    # size=[1440, 810],  # either specify size for screen 1 or set fullscr = True
                    fullscr=True
                    )

# message to display before scanner pulse is received
# text='waiting for scanner...'
msg = visual.TextStim(win, color='LightGray', text='väntar på magnetkamera...')

# instruction text
instr = visual.TextStim(win,
                        font='Helvetica Bold',
                        pos=(0, 0),
                        height=0.1,
                        # text='Please rate your spontaneous pain from your knee/back continuously using only the '
                        #     'track ball on the mouse.\n\nPlease wait for the paradigm to begin.',
                        text='Skatta hur ont det gör hela tiden (klicka inte). \n\nVänta tills början.',
                        color='LightGray',
                        wrapWidth=None)

# fixation cross to be presented before rating starts
cross = visual.TextStim(win, font='Helvetica Bold', pos=(
    0, 0), height=0.25, text='+', color='LightGray')

# marker that will move with the mouse # #  size=(0.1, 0.15) # change marker size?
fixSpot = visual.GratingStim(win, tex="none", mask="circle", size=(
    0.08, 0.12), color='red', autoLog=False)

# rating scale
vas = visual.RatingScale(win,
                         name='rating',
                         marker='circle',       # define this here even though it will not be called!
                         precision=1,           # will give only whole numbers
                         size=1,                # affects the overall rating scale display
                         stretch=1.75,          # affects horizontal direction of the scale
                         pos=[0.0, -0.2],       # position of scale on screen
                         tickMarks=[0, 100],
                         tickHeight=1,
                         low=0,                 # minimum
                         high=100,              # maximum
                         # applied to all text elements (anchors, scale)  1.3
                         textSize=1.4,
                         # labels=['No pain at all', 'Extremely in pain'],
                         # labels=['0', '100']
                         labels=['Ingen smärta', 'Värsta tänkbara smärta'],
                         textFont='Helvetica Bold',
                         textColor='LightGray',
                         scale='Hur smärtsamt är det just nu?',  # title of scale
                         showAccept=False)

# custom mouse
vm = visual.CustomMouse(win,
                        leftLimit=-0.55, rightLimit=0.55,   # starts and ends at scale ends
                        topLimit=-0.2, bottomLimit=-0.2,  # you can only move mouse on line along scale
                        newPos=[-50, 0],  # starting position, currently 0
                        showLimitBox=False, clickOnUp=True)

# add cursor mouse to get rid of freezing problem
mouse = event.Mouse(win=win, visible=False)  # see below

# set some others stuff
# default, only Errors and Warnings are shown on the console
logging.console.setLevel(logging.WARNING)

# tmp files
timeData = []
ratingData = []
recordedMousePos = np.zeros((50000, 2))
k = 0  # running variable for loop # needs to start with 0
pulseReceived = False

# START PARADIGM HERE

# display instructions for 5 s
instr.draw()
win.flip()
core.wait(5)

while pulseReceived is False:
    msg.draw()
    win.flip()

# waiting for scanner
    if event.waitKeys(keyList=['s'], timeStamped=True):
        pulseReceived = True
        print('\nScanner pulse received\n')

    if event.getKeys(['escape']):
        core.quit()

# set up clocks
globalClock = core.Clock()

crossTimer = core.CountdownTimer(3)
while crossTimer.getTime() > 0:
    cross.draw()
    win.flip()

    if event.getKeys(['escape']):
        core.quit()

mouse.setPos(newPos=(-0.1, 0))
vm.pointer = fixSpot  # assign the fix spot to the vm pointer

ratingTimer = core.CountdownTimer(600)  # 600 s = 10 min
while ratingTimer.getTime() > 0:  # until timer is at 0

    vas.reset()

    # grabs current mouse position (rating)
    currentMousePos = vas._getMarkerFromPos(vm.getPos()[0])
    # grabs time since globalClock was created
    currentTime = globalClock.getTime()

    # if the mouse has been moved since last recorded position
    if currentMousePos != recordedMousePos[k-1, 0]:

        recordedMousePos[k, 0] = currentMousePos   # log new rating
        # log time when mouse was moved to new mouse position
        recordedMousePos[k, 1] = currentTime

        # round Rating to integer/whole number, round Time to 3 decimals in terminal window
        print('Time: {}, Rating: {}'.format(
            round(currentTime, 3), round(currentMousePos)))

        currentTime = currentTime  # does not round right now
        currentMousePos = round(currentMousePos)

        timeData.append(currentTime)
        ratingData.append(currentMousePos)

        # data storage
        data2store = pd.DataFrame({"Time": timeData, "Rating": ratingData})
        # or comma-separated ","
        data2store.to_csv(outFile, sep="\t", index=False)

        k = k + 1

    elif event.getKeys(['escape']):
        core.quit()

    # Do the drawing
    vas.draw()
    vm.draw()
    win.flip()


print('\nThe End')
win.close()
core.quit()
