# Temporal Summation paradigm
# # Isabel Ellerbrock, October 2019

from psychopy import core, visual, event, sound, gui

import numpy as np
import pandas as pd
import os
import sys

# gui information
expName = "TS"
mygui = gui.Dlg(title=expName)
mygui.addField("Subject ID:")
mygui.addField("hand/knee/back:")
mygui.addField("Session (pre/post):")
mygui.show()  # this will present the actual gui to insert stim num and sess num

# create output data specifications
subj_id = mygui.data[0]
bodypart = mygui.data[1]
sess = mygui.data[2]

pth = "C:/Users/PainLab/Documents/POADOS/TemporalSummation/data/"
outFile = pth + expName + "_" + subj_id + "_" + bodypart + "1_" + sess + ".csv"

if os.path.exists(outFile):
    sys.exit("Data path " + outFile + " already exists!")

# create a window to display stuff in
win = visual.Window(
    color=[0, 0, 0],
    monitor="testMonitor",
    mouseVisible=False,
    # screen=2,  # 1 = display computer while scanning, 0 = control/MRI computer
    size=[1680, 1050],  # either specify size or set fullscr = True
    fullscr=True,
)

# instructions for rating scale
instr = visual.TextStim(
    win,
    font="Helvetica Bold",
    pos=(0, 0),
    height=0.12,
    text="Du kommer att få känna stick och skatta hur ont det gör.",
    color="LightGray",
    wrapWidth=None,
)

# instructions before first stimulus
alertFirst = visual.TextStim(
    win,
    font="Helvetica Bold",
    pos=(0, 0),
    height=0.12,
    text="Snart kommer du att känna ett stick.",
    color="LightGray",
    wrapWidth=None,
)

# instructions before series of stimuli
alertSeries = visual.TextStim(
    win,
    font="Helvetica Bold",
    pos=(0, 0),
    height=0.12,
    text="Snart kommer du att känna flera stick."
    "Skatta hur ont det gör hela tiden (klicka inte).",
    color="LightGray",
    wrapWidth=None,
)

# fixation cross to be presented before rating starts
cross = visual.TextStim(
    win, font="Helvetica Bold", pos=(0, 0), height=0.25, text="+", color="LightGray"
)

# grey screen
grey = visual.TextStim(
    win, font="Helvetica Bold", pos=(0, 0), height=0.25, text="", color="LightGray"
)

# screen between series
intermezzo = visual.TextStim(
    win,
    font="Helvetica Bold",
    pos=(0, 0),
    height=0.15,
    text="continue?",
    color="LightGray",
)

# rating scale
vasFirst = visual.RatingScale(
    win,
    name="rating",
    marker="none",  # define this here even though it will not be called!
    precision=1,  # will give only whole numbers
    size=1,  # affects the overall rating scale display
    stretch=2,  # affects horizontal direction of the scale
    pos=[0.0, -0.2],  # position of scale on screen
    tickMarks=[0, 100],
    tickHeight=1,
    low=0,  # minimum
    high=100,  # maximum
    textSize=1.1,  # applied to all text elements (anchors, scale)
    labels=["Ingen smärta", "Värsta tänkbara smärta"],  # labels=['0', '100'],
    textFont="Helvetica Bold",
    textColor="LightGray",
    scale="Skatta hur ont det gjorde (klicka inte).",
    showAccept=False,
)

# rating scale
vasSeries = visual.RatingScale(
    win,
    name="rating",
    marker="circle",  # define this here even though it will not be called!
    precision=1,  # will give only whole numbers
    size=1,  # affects the overall rating scale display
    stretch=2,  # affects horizontal direction of the scale
    pos=[0.0, -0.2],  # position of scale on screen
    tickMarks=[0, 100],
    tickHeight=1,
    low=0,  # minimum
    high=100,  # maximum
    textSize=1.1,  # applied to all text elements (anchors, scale)
    labels=["Ingen smärta", "Värsta tänkbara smärta"],  # labels=['0', '100'],
    textFont="Helvetica Bold",
    textColor="LightGray",
    scale="Skatta hur ont det gör (även efter sticken).",  # title/instructions of scale
    showAccept=False,
)

# sound for first stimulus
sound_first = sound.Sound(
    "C:/Users/PainLab/Documents/POADOS/TemporalSummation/sounds/first.wav",
    volume=1,
    sampleRate=44100,
)

# sound for series of stimuli
sound_TS = sound.Sound(
    "C:/Users/PainLab/Documents/POADOS/TemporalSummation/sounds/ts.wav",
    volume=1,
    sampleRate=44100,
)

# marker that will move with the mouse # #  size=(0.1, 0.15) # marker size
fixSpot = visual.GratingStim(
    win, tex="none", mask="circle", size=(0.06, 0.1), color="red", autoLog=False
)

# custom mouse
# the reason I introduce two vm is that the start position is not kept if only one vm is used
vm = visual.CustomMouse(
    win,
    leftLimit=-0.6,
    rightLimit=0.6,  # starts and ends at scale ends
    topLimit=-0.2,
    bottomLimit=-0.2,  # you can only move mouse on line along scale
    newPos=[-50, 0],  # starting position
    showLimitBox=False,
    clickOnUp=True,
)  # clickOnUp does not matter, concerns mouse clicks

vmTS = visual.CustomMouse(
    win,
    leftLimit=-0.6,
    rightLimit=0.6,  # starts and ends at scale ends
    topLimit=-0.2,
    bottomLimit=-0.2,  # you can only move mouse on line along scale
    newPos=[-50, 0],  # starting position
    showLimitBox=False,
    clickOnUp=True,
)  # clickOnUp does not matter, concerns mouse clicks

# mouse to couple to
mouse = event.Mouse(win=win, visible=False)

# set up clocks
clock = core.Clock()
TSclock = core.Clock()
SpareClock = core.Clock()

# other settings
recordedMousePos = np.zeros((5000, 2))
dur5s = 5.0  # duration that most instructions will be presented
dur10s = 10.0

# tmp files
timeData = []
ratingData = []
stimData = []

# # START SERIES 1
clock.reset()
while clock.getTime() < dur5s:
    instr.draw()  # display instructions for rating scale (0-100)
    win.flip()

    if event.getKeys(["escape"]):
        core.quit()

clock.reset()
while clock.getTime() < dur5s:
    alertFirst.draw()  # display alert first stim
    win.flip()

    if event.getKeys(["escape"]):
        core.quit()

# display cross and audio to present first stimulus
cross.draw()
win.flip()
sound_first.play()
core.wait(5)  # starts the moment the first sound starts

# first stim rating and cross afterwards = 10s
mouse.setPos(newPos=(0, 0))
vm.pointer = fixSpot  # assign the fix spot to the vm pointer

ratingTimer = core.CountdownTimer(dur10s)
while ratingTimer.getTime() > 0:  # until timer is at 0
    vasFirst.reset()

    currentMousePos = vasFirst._getMarkerFromPos(
        vm.getPos()[0]
    )  # grabs current mouse position (rating)

    # Do the drawing
    vasFirst.draw()
    vm.draw()
    win.flip()

    if ratingTimer.getTime() < 0.001:  # if time runs out, just grab their rating
        currentMousePos = round(currentMousePos)  # log rating
        print("First stim rating: ", currentMousePos)

        # assemble data
        ratingData.append(currentMousePos)
        timeData.append("0")
        stimData.append("first")

        # data storage
        data2store = pd.DataFrame(
            {"Cond": stimData, "Time": timeData, "Rating": ratingData}
        )

if event.getKeys(["escape"]):
    core.quit()

# display alert for TS series
clock.reset()
while clock.getTime() < dur5s:
    alertSeries.draw()
    win.flip()

    if event.getKeys(["escape"]):
        core.quit()

# display cross and audio to present TS repetitive stimuli (n=15)
cross.draw()
win.flip()

# set mouse and pointer
mouse.setPos(newPos=(0, 0))
vmTS.pointer = fixSpot

TSclock.reset()
for frame in range(
    1500
):  # 60 Hz are 60 frames/s, 1500 frames = 25s (previously: 1800 frames = 30s)
    vasSeries.reset()

    currentMousePos = vasSeries._getMarkerFromPos(
        vmTS.getPos()[0]
    )  # grabs current mouse position (rating)
    currentTime = TSclock.getTime()  # grabs time since globalClock was created

    currentTime = round(currentTime, 3)
    currentMousePos = round(currentMousePos)

    # round Rating to integer/whole number, round Time to 3 decimals in terminal window
    print("Time: {}, Rating: {}".format(round(currentTime, 3), round(currentMousePos)))

    timeData.append(currentTime)
    ratingData.append(currentMousePos)
    stimData.append("ts")

    if frame == 180:  # after 3s (=180 frames) start play sound
        sound_TS.play()
        # print("sound")

    if (
        frame == 300
    ):  # after 5s (=300 frames), 300+120 f, log start stimuli. The sound has 1 extra sec in beginning

        timeData.append(currentTime)
        ratingData.append(currentMousePos)
        stimData.append("startStim")
        # print("start")

    if (
        frame == 1140
    ):  # ca. after 5s + 15s (passed time + num of stim/time to apply them), log end of stimulation

        timeData.append(currentTime)
        ratingData.append(currentMousePos)
        stimData.append("stopStim")
        # print("end")

    elif event.getKeys(["escape"]):
        core.quit()

    # Do the drawing
    vasSeries.draw()
    vmTS.draw()
    win.flip()

# data storage
data2store = pd.DataFrame({"Cond": stimData, "Time": timeData, "Rating": ratingData})
data2store.to_csv(outFile, sep="\t", index=False)  # or comma-separated ","

# pause before continue is possible
grey.draw()
win.flip()
core.wait(2)

###
# transition phase from series 1 to 2
entered = False
while entered is False:
    intermezzo.draw()  # display intermezzo
    win.flip()

    if event.getKeys(
        keyList=["return", "c"]
    ):  # continue paradigm with keyboard buttons "enter/return" or "c"
        entered = True

    elif event.getKeys(["escape"]):
        core.quit()
###
# name of file for second series
outFile = pth + expName + "_" + subj_id + "_" + bodypart + "2_" + sess + ".csv"

# other settings
recordedMousePos = np.zeros((5000, 2))

# clear tmp files
timeData = []
ratingData = []
stimData = []

# START SERIES 2
core.wait(2)

clock.reset()
while clock.getTime() < dur5s:
    instr.draw()  # display instructions for rating scale (0-100)
    win.flip()

    if event.getKeys(["escape"]):
        core.quit()

clock.reset()
while clock.getTime() < dur5s:
    alertFirst.draw()  # display alert first stim
    win.flip()

    if event.getKeys(["escape"]):
        core.quit()

# display cross and audio to present first stimulus
cross.draw()
win.flip()
sound_first.play()
core.wait(5)  # starts the moment the first sound starts

# first stim rating and cross afterwards = 10s
mouse.setPos(newPos=(0, 0))
vm = visual.CustomMouse(
    win,
    leftLimit=-0.6,
    rightLimit=0.6,  # starts and ends at scale ends
    topLimit=-0.2,
    bottomLimit=-0.2,  # you can only move mouse on line along scale
    newPos=[-50, 0],  # starting position
    showLimitBox=False,
    clickOnUp=True,
)  # clickOnUp does not matter, concerns mouse clicks

vm.pointer = fixSpot  # assign the fix spot to the vm pointer

ratingTimer = core.CountdownTimer(dur10s)
while ratingTimer.getTime() > 0:  # until timer is at 0
    vasFirst.reset()  # reset scale as it is used several times

    currentMousePos = vasFirst._getMarkerFromPos(
        vm.getPos()[0]
    )  # grabs current mouse position (rating)

    # Do the drawing
    vasFirst.draw()
    vm.draw()
    win.flip()

    if ratingTimer.getTime() < 0.001:  # if time runs out, just grab their rating
        currentMousePos = round(currentMousePos)  # log rating
        print("First stim rating: ", currentMousePos)

        # assemble data
        ratingData.append(currentMousePos)
        timeData.append("0")
        stimData.append("first")

        # data storage
        data2store = pd.DataFrame(
            {"Cond": stimData, "Time": timeData, "Rating": ratingData}
        )

if event.getKeys(["escape"]):
    core.quit()

# display alert for TS series
clock.reset()
while clock.getTime() < dur5s:
    alertSeries.draw()
    win.flip()

    if event.getKeys(["escape"]):
        core.quit()

# display cross and audio to present TS repetitive stimuli (n=15)
cross.draw()
win.flip()

# set mouse and assign circle as pointer
mouse.setPos(newPos=(0, 0))
vmTS = visual.CustomMouse(
    win,
    leftLimit=-0.6,
    rightLimit=0.6,  # starts and ends at scale ends
    topLimit=-0.2,
    bottomLimit=-0.2,  # you can only move mouse on line along scale
    newPos=[-50, 0],  # starting position
    showLimitBox=False,
    clickOnUp=True,
)  # clickOnUp does not matter, concerns mouse clicks
vmTS.pointer = fixSpot

TSclock.reset()
for frame in range(
    1500
):  # 60 Hz are 60 frames/s, 1500 frames = 25s (previously: 1800 frames = 30s)
    vasSeries.reset()

    currentMousePos = vasSeries._getMarkerFromPos(
        vmTS.getPos()[0]
    )  # grabs current mouse position (rating)
    currentTime = TSclock.getTime()  # grabs time since globalClock was created

    currentTime = round(currentTime, 3)
    currentMousePos = round(currentMousePos)

    # round Rating to integer/whole number, round Time to 3 decimals in terminal window
    print("Time: {}, Rating: {}".format(round(currentTime, 3), round(currentMousePos)))

    timeData.append(currentTime)
    ratingData.append(currentMousePos)
    stimData.append("ts")

    if frame == 180:  # after 3s (=180 frames) start play sound
        sound_TS.play()
        # print("sound")

    if (
        frame == 300
    ):  # after 5s (=300 frames), 300+120 f, log start stimuli. The sound has 1 extra sec in beginning

        timeData.append(currentTime)
        ratingData.append(currentMousePos)
        stimData.append("startStim")
        # print("start")

    if (
        frame == 1140
    ):  # ca. after 5s + 15s (passed time + num of stim/time to apply them), log end of stimulation

        timeData.append(currentTime)
        ratingData.append(currentMousePos)
        stimData.append("stopStim")
        # print("end")

    elif event.getKeys(["escape"]):
        core.quit()

    # Do the drawing
    vasSeries.draw()
    vmTS.draw()
    win.flip()

# data storage
data2store = pd.DataFrame({"Cond": stimData, "Time": timeData, "Rating": ratingData})
data2store.to_csv(outFile, sep="\t", index=False)  # or comma-separated ","

# pause before continue is possible
grey.draw()
win.flip()
core.wait(2)

###
# transition phase from series 2 to 3
entered = False

while entered is False:
    intermezzo.draw()  # display intermezzo
    win.flip()

    if event.getKeys(keyList=["return", "c"]):
        entered = True

    elif event.getKeys(["escape"]):
        core.quit()
###
# name of file for third series
outFile = pth + expName + "_" + subj_id + "_" + bodypart + "3_" + sess + ".csv"

# other settings
recordedMousePos = np.zeros((5000, 2))

# tmp files
timeData = []
ratingData = []
stimData = []

# START PARADIGM 3
core.wait(2)

clock.reset()
while clock.getTime() < dur5s:
    instr.draw()  # display instructions for rating scale (0-100)
    win.flip()

    if event.getKeys(["escape"]):
        core.quit()

clock.reset()
while clock.getTime() < dur5s:
    alertFirst.draw()  # display alert first stim
    win.flip()

    if event.getKeys(["escape"]):
        core.quit()

# display cross and audio to present first stimulus
cross.draw()
win.flip()
sound_first.play()
core.wait(5)  # starts the moment the first sound starts

# first stim rating and cross afterwards = 10s
mouse.setPos(newPos=(0, 0))
vm = visual.CustomMouse(
    win,
    leftLimit=-0.6,
    rightLimit=0.6,  # starts and ends at scale ends
    topLimit=-0.2,
    bottomLimit=-0.2,  # you can only move mouse on line along scale
    newPos=[-50, 0],  # starting position
    showLimitBox=False,
    clickOnUp=True,
)  # clickOnUp does not matter, concerns mouse clicks

vm.pointer = fixSpot  # assign the fix spot to the vm pointer

ratingTimer = core.CountdownTimer(dur10s)
while ratingTimer.getTime() > 0:  # until timer is at 0
    vasFirst.reset()

    currentMousePos = vasFirst._getMarkerFromPos(
        vm.getPos()[0]
    )  # grabs current mouse position (rating)

    # Do the drawing
    vasFirst.draw()
    vm.draw()
    win.flip()

    if ratingTimer.getTime() < 0.001:  # if time runs out, just grab their rating
        currentMousePos = round(currentMousePos)  # log rating
        print("First stim rating: ", currentMousePos)

        # assemble data
        ratingData.append(currentMousePos)
        timeData.append("0")
        stimData.append("first")

        # data storage
        data2store = pd.DataFrame(
            {"Cond": stimData, "Time": timeData, "Rating": ratingData}
        )

if event.getKeys(["escape"]):
    core.quit()

# display alert for TS series
clock.reset()
while clock.getTime() < dur5s:
    alertSeries.draw()
    win.flip()

    if event.getKeys(["escape"]):
        core.quit()

# display cross and audio to present TS repetitive stimuli (n=15)
cross.draw()
win.flip()

mouse.setPos(newPos=(0, 0))
vmTS = visual.CustomMouse(
    win,
    leftLimit=-0.6,
    rightLimit=0.6,  # starts and ends at scale ends
    topLimit=-0.2,
    bottomLimit=-0.2,  # you can only move mouse on line along scale
    newPos=[-50, 0],  # starting position
    showLimitBox=False,
    clickOnUp=True,
)  # clickOnUp does not matter, concerns mouse clicks
vmTS.pointer = fixSpot

TSclock.reset()
for frame in range(
    1500
):  # 60 Hz are 60 frames/s, 1500 frames = 25s (previously: 1800 frames = 30s)
    vasSeries.reset()

    currentMousePos = vasSeries._getMarkerFromPos(
        vmTS.getPos()[0]
    )  # grabs current mouse position (rating)
    currentTime = TSclock.getTime()  # grabs time since globalClock was created

    currentTime = round(currentTime, 3)
    currentMousePos = round(currentMousePos)

    # round Rating to integer/whole number, round Time to 3 decimals in terminal window
    print("Time: {}, Rating: {}".format(round(currentTime, 3), round(currentMousePos)))

    timeData.append(currentTime)
    ratingData.append(currentMousePos)
    stimData.append("ts")

    if frame == 180:  # after 3s (=180 frames) start play sound
        sound_TS.play()
        # print("sound")

    if (
        frame == 300
    ):  # after 5s (=300 frames), 300+120 f, log start stimuli. The sound has 1 extra sec in beginning

        timeData.append(currentTime)
        ratingData.append(currentMousePos)
        stimData.append("startStim")
        # print("start")

    if (
        frame == 1140
    ):  # ca. after 5s + 15s (passed time + num of stim/time to apply them), log end of stimulation

        timeData.append(currentTime)
        ratingData.append(currentMousePos)
        stimData.append("stopStim")
        # print("end")

    elif event.getKeys(["escape"]):
        core.quit()

    # Do the drawing
    vasSeries.draw()
    vmTS.draw()
    win.flip()

# data storage
data2store = pd.DataFrame({"Cond": stimData, "Time": timeData, "Rating": ratingData})
data2store.to_csv(outFile, sep="\t", index=False)  # or comma-separated ","

# pause before continue is possible
grey.draw()
win.flip()
core.wait(2)

###
# transition phase from series 3 to 4
entered = False

while entered is False:
    intermezzo.draw()  # display intermezzo
    win.flip()

    if event.getKeys(keyList=["return", "c"]):
        entered = True

    elif event.getKeys(["escape"]):
        core.quit()
###
# name of file for fourth series
outFile = pth + expName + "_" + subj_id + "_" + bodypart + "4_" + sess + ".csv"

# other settings
recordedMousePos = np.zeros((5000, 2))

# clear tmp files
timeData = []
ratingData = []
stimData = []

# START PARADIGM 4
core.wait(2)

clock.reset()
while clock.getTime() < dur5s:
    instr.draw()  # display instructions for rating scale (0-100)
    win.flip()

    if event.getKeys(["escape"]):
        core.quit()

clock.reset()
while clock.getTime() < dur5s:
    alertFirst.draw()  # display alert first stim
    win.flip()

    if event.getKeys(["escape"]):
        core.quit()

# display cross and audio to present first stimulus
cross.draw()
win.flip()
sound_first.play()
core.wait(5)  # starts the moment the first sound starts

# first stim rating and cross afterwards = 10s
mouse.setPos(newPos=(0, 0))
vm = visual.CustomMouse(
    win,
    leftLimit=-0.6,
    rightLimit=0.6,  # starts and ends at scale ends
    topLimit=-0.2,
    bottomLimit=-0.2,  # you can only move mouse on line along scale
    newPos=[-50, 0],  # starting position
    showLimitBox=False,
    clickOnUp=True,
)  # clickOnUp does not matter, concerns mouse clicks
vm.pointer = fixSpot  # assign the fix spot to the vm pointer

ratingTimer = core.CountdownTimer(dur10s)
while ratingTimer.getTime() > 0:  # until timer is at 0
    vasFirst.reset()

    currentMousePos = vasFirst._getMarkerFromPos(
        vm.getPos()[0]
    )  # grabs current mouse position (rating)

    # Do the drawing
    vasFirst.draw()
    vm.draw()
    win.flip()

    if ratingTimer.getTime() < 0.001:  # if time runs out, just grab their rating
        currentMousePos = round(currentMousePos)  # log rating
        print("First stim rating: ", currentMousePos)

        # assemble data
        ratingData.append(currentMousePos)
        timeData.append("0")
        stimData.append("first")

        # data storage
        data2store = pd.DataFrame(
            {"Cond": stimData, "Time": timeData, "Rating": ratingData}
        )

if event.getKeys(["escape"]):
    core.quit()

# display alert for TS series
clock.reset()
while clock.getTime() < dur5s:
    alertSeries.draw()
    win.flip()

    if event.getKeys(["escape"]):
        core.quit()

# display cross and audio to present TS repetitive stimuli (n=15)
cross.draw()
win.flip()

mouse.setPos(newPos=(0, 0))
vmTS = visual.CustomMouse(
    win,
    leftLimit=-0.6,
    rightLimit=0.6,  # starts and ends at scale ends
    topLimit=-0.2,
    bottomLimit=-0.2,  # you can only move mouse on line along scale
    newPos=[-50, 0],  # starting position
    showLimitBox=False,
    clickOnUp=True,
)  # clickOnUp does not matter, concerns mouse clicks
vmTS.pointer = fixSpot

TSclock.reset()
for frame in range(
    1500
):  # 60 Hz are 60 frames/s, 1500 frames = 25s (previously: 1800 frames = 30s)
    vasSeries.reset()

    currentMousePos = vasSeries._getMarkerFromPos(
        vmTS.getPos()[0]
    )  # grabs current mouse position (rating)
    currentTime = TSclock.getTime()  # grabs time since globalClock was created

    currentTime = round(currentTime, 3)
    currentMousePos = round(currentMousePos)

    # round Rating to integer/whole number, round Time to 3 decimals in terminal window
    print("Time: {}, Rating: {}".format(round(currentTime, 3), round(currentMousePos)))

    timeData.append(currentTime)
    ratingData.append(currentMousePos)
    stimData.append("ts")

    if frame == 180:  # after 3s (=180 frames) start play sound
        sound_TS.play()
        # print("sound")

    if (
        frame == 300
    ):  # after 5s (=300 frames), 300+120 f, log start stimuli. The sound has 1 extra sec in beginning

        timeData.append(currentTime)
        ratingData.append(currentMousePos)
        stimData.append("startStim")
        # print("start")

    if (
        frame == 1140
    ):  # ca. after 5s + 15s (passed time + num of stim/time to apply them), log end of stimulation

        timeData.append(currentTime)
        ratingData.append(currentMousePos)
        stimData.append("stopStim")
        # print("end")

    elif event.getKeys(["escape"]):
        core.quit()

    # Do the drawing
    vasSeries.draw()
    vmTS.draw()
    win.flip()

# data storage
data2store = pd.DataFrame({"Cond": stimData, "Time": timeData, "Rating": ratingData})
data2store.to_csv(outFile, sep="\t", index=False)  # or comma-separated ","

grey.draw()
win.flip()
core.wait(2)

######
# end TS
win.close()
core.quit()
