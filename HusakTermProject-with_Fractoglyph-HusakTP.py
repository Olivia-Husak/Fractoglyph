################################################################################
################################################################################
# Olivia Husak
# ogh
# 12/6/18
# Term Project Final
################################################################################
################################################################################


import math
import string
import copy
from tkinter import *
import random
import shelve
from tkinter.colorchooser import *


################################################################################
################################################################################
# Initialization
################################################################################
################################################################################


class Struct(object): pass
data = Struct()
# Made data a global variable for fetching data in other files. 

savedDataFile = "fractog"
saveDataMode = False
openDataMode = False
clearDataMode = False

def init():
    global data
    data.mode = "splashScreen"
    data.phi = 0
    data.theta = 0
    data.breaks = 1
    data.shape = 1
    data.spikes = False
    data.numPoints = 3
    data.reflected = False
    data.extendedLines = False
    data.level = 1
    data.windowSize = 1200
    data.startX = data.width / 2 - 87.5
    data.startY = data.height / 2
    data.startR = 300
    data.zoom = 1.0
    data.zAxis = 0
    data.mirror = False
    data.barWidth = data.width // 7
    data.animate = False
    data.threeDee = False
    data.animateText = "Animate Fractal"
    data.anaglyphText = "Anaglyph Fractal"
    data.eta = 0
    data.zeta = 0
    data.startZ = 0
    data.color1 = "#000000"  #black
    data.color2 = "#000000"  
    data.background = "#ffffff"  #white
    data.lineWidth = 1
    data.displayParams = False

##########
# CITATION
# Mode template taken from 112 Website
# https://www.cs.cmu.edu/~112/notes/notes-animations-demos.html
##########

def mousePressed(event):
    global data
    # Decides which mousePressed to call based on current Game Mode
    if (data.mode == "splashScreen"):
        splashScreenMousePressed(event)
    elif (data.mode == "fractal"):
        fractalMousePressed(event)
    elif (data.mode == "instruction"):
        instructionMousePressed(event)


def keyPressed(event):
    global data
    # Decides which keyPressed to call based on current Game Mode
    if (data.mode == "splashScreen"):
        splashScreenKeyPressed(event)
    elif (data.mode == "fractal"):
        fractalKeyPressed(event)
    elif (data.mode == "instruction"):
        instructionKeyPressed(event)


def timerFired():
    global data
    # Decides which timerFired to call based on current Game Mode
    if (data.mode == "splashScreen"):
        splashScreenTimerFired()
    elif (data.mode == "fractal"):
        fractalTimerFired()
    elif (data.mode == "instruction"):
        instructionTimerFired()


def redrawAll(canvas):
    global data
    # Decides which redrawAll to call based on current Game Mode
    if (data.mode == "splashScreen"):
        splashScreenRedrawAll(canvas)
    elif (data.mode == "fractal"):
        fractalRedrawAll(canvas)
    elif (data.mode == "instruction"):
        instructionRedrawAll(canvas)


################################################################################
################################################################################
# splashScreen mode
# NOTE:
# I tried to make the pythagorean tree for HW bonus, but failed/ran out of time.
# I came back to the code for this splash screen and finished it and randomized
# the direction of growth. So mostly this is original for this project, and it
# was never used for anything else.
################################################################################
################################################################################


def rot(origin, point, angle):
    # Rotate a point in a tkinter window counterclockwise by a given angle
    # around a given origin.
    rad = math.radians(angle)
    ox, oy = origin
    px, py = point
    dx = px - ox
    dy = py - oy
    x = ox + dx * math.cos(rad) + dy * math.sin(rad)
    y = oy - dx * math.sin(rad) + dy * math.cos(rad)
    return (x, y)


def drawDot(canvas, point, color="black", size=3, outl=""):
    # Draws a dot on the canvas at location point = (x, y).
    px, py = point
    canvas.create_oval(px - size, py - size, px + size, py + size, fill=color,
                       outline=outl)


def splashScreenKeyPressed(event):
    global data
    if event.keysym == "space":
        data.mode = "fractal"
    if event.char == "i":
        data.mode = "instruction"


def splashScreenMousePressed(event):
    global data
    # print(event.x, event.y)
    if (event.x > 3 * data.width / 8) and (
            event.x < 5 * data.width / 8) and (event.y > 225) and (
            event.y < 275):
        data.mode = "fractal"
    if (event.x > 7 * data.width / 16) and (event.x < 9 * data.width / 16) and \
            (event.y > 280) and (event.y < 300):
        data.mode = "instruction"


def drawPythTree(canvas, p1, p2, theta, level=0, rand=False):
    # Draws a Pythagoras Tree on the baseline form point p1 to point p2 (which
    # are (x, y) tuple coordinates, Theta is the angle of the left point of
    # the triangle (so theta=45 generates the symmetric tree, theta<45 bends to
    # the left, and theta>45 bends to the right).
    if level > 0:
        if rand:
            angle = random.choice([theta, 90 - theta])
        else:
            angle = theta
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        coords = [p1, p2]
        coords.append((x2 + dy, y2 - dx))
        coords.append((x1 + dy, y1 - dx))
        coords.append((coords[2][0] - dx / 2, coords[2][1] - dy / 2))
        coords.append(rot(coords[4], coords[2], 2 * angle))
        # coords[0:4] is the square to be drawn as a polygon for this level.
        # coords[4] is the midpoint of the "top side" of the square, the
        # direction in which the tree grows.
        # coords[5] is the vertex of the growth triangle.
        canvas.create_polygon(coords[0:4], fill="", outline="black")
        drawPythTree(canvas, coords[3], coords[5], theta, level - 1, rand)
        drawPythTree(canvas, coords[5], coords[2], theta, level - 1, rand)


def splashScreenRedrawAll(canvas):
    global data
    canvas.create_text(data.width / 2 - 20, 125, text="Fractoglyph",
                       font="Times 150", fill="red")
    canvas.create_text(data.width / 2 + 20, 125, text="Fractoglyph",
                       font="Times 150", fill="cyan")
    canvas.create_text(data.width / 2, 125, text="Fractoglyph", font="Times 150")
    drawPythTree(canvas, (data.width / 2 - data.width // 20, data.height - 20),
                 (data.width / 2 + data.width // 20, data.height - 20),
                 35, 12, True)
    canvas.create_rectangle(3 * data.width / 8, 225, 5 * data.width / 8,
                            275, fill="white")
    canvas.create_rectangle(7 * data.width / 16, 280, 9 * data.width / 16, 300,
                            fill="white")
    canvas.create_text(data.width / 2, 250, text="E x p l o r e", font="Courier 30")
    canvas.create_text(data.width / 2, 290, text="Instructions",
                       font="Courier 18")


def splashScreenTimerFired():
    #timer fired is empty but the way the tree changes is because every time 
    #redrawall is called it generates a new random tree
    global data
    pass


################################################################################
################################################################################
# Instruction Mode
################################################################################
################################################################################


def instructionMousePressed(event):
    global data
    if event.x > 475 and event.x < 725 and event.y > 750 and event.y < 800:
        data.mode = "fractal"


def instructionKeyPressed(event):
    global data
    pass


def instructionTimerFired():
    global data
    pass


def instructions(canvas):
    global data
    keyShorts = """ 
    There are five main features in changing the appearance of you fractal. All of these are managed both with key-commands and buttons. You will notice that 
    each button is not labelled, but rather displays the current state of the fractal for that parameter. This is helpful in seeing the different values for 
    each of the parameters at the current time. These are controlled by the following commands: 
            Press 'k'/'l' to change the number of breaks in a point of the fractal- this corresponds to the top-most button on the screen
            Press 'y' to add outer normal spikes to each point in the fractal - this corresponds to the second top-most button on the screen
            Press 'm' to mirror fractal - this corresponds to the third top-most button on the screen
            Press '123456' to change shape of fractal - this corresponds to the fourth top-most button on the screen
            Press '.'/',' to change the level of the fractal - this corresponds to the fifth top-most button on the screen
            
    Once you have a fractal, there are different commands you can use to change its perspective and positioning. 
            Press '='/'-' keys to zoom fractal in and out - this corresponds to the navigation buttons in the bottom right corner of the screen
            Use the arrow keys to move fractal around the screen - this corresponds to the navigation buttons in the bottom right corner of the screen
            Press '['/']' to step the animation - this corresponds to the 'animate fractal' button on the side panel
            Press ';'/''' to rotate fractal
            
    Now that you have created your fractal, you can anaglyph it! In order to see the fractal in 3D, you will need a pair of red-cyan 3D glasses. In changing the 
    depth with the keys below, you can either make the center of the fractal appear more sunken in with the edges protruding out of the screen, or make the 
    center appear more forward, with the edges sunken in. Try moving your head around and notice how the fractal changes! 
            Press 'd' to begin analgyphing - this corresponds to the 'anaglyph fractal' button on the side panel
            Press 'x'/'z' to change anaglyph depth of fractal
            
    If you are not anaglyphing, you can also change the color and width of your fractal and gradiate it between levels. The base level will be colored in the 
    first color, and the highest level line segments will be colored in the second color. All segments in between will gradiate between the two colors evenly. 
            Press 'c' to choose a first color for your fractal - this corresponds to the left most color button
            Press 'v' to choose a second color for your fractal - this corresponds to the middle color button
            Press 'b' to choose a background color for the screen - this corresponds to the right most color button
            Press 'w'/'q' to change the line width of the fractal
            
    Once you are done with your fractal, you can save it and come back to it later. Don't worry about closing the program, as long as the file remains in the 
    same file directory, your fractals will still be there the next time you open it! 
            Press 's' to save your current fractal, followed by one of '123456', to specify the location to store it in 
            Press 'o' to open a fractal, followed by one of '123456', to specify the location to open from 
            Press 'e' to clear the fractal data
            Press 't' to print the current keys that fractals are saved under 
            Press 'r' to reset your fractal
            
    There are also keyboard shortcuts in place to check the current state of the fractal. 
            Press 'p' to print summary of fractal values. This will print in the console of the python editor 
            Press 'f' to display a summary of the fractal values on the screen. They will appear in the upper right corner of the screen. Enabling this feature
            will also keep track of the starting point to the fractal, which is denoted by a small red circle in the fractal. 
            
    You can return to this page at anytime by clicking the round 'i' button in the lower left-hand corner. Happy creating! 
                    """
    canvas.create_text(data.width/2, data.height/2, text = keyShorts, font = "Courier 12")


def instructionRedrawAll(canvas):
    global data
    if data.mode == "instruction": 
        data.background = "white"
        #otherwise if we change the fractal background and then come back to the
        #instructions page, the background color is different and text is 
        #illegible if too dark
    canvas.create_text(data.width / 2 - 12.5, 65, text="Instructions",
                       font="Times 80", fill="red")
    canvas.create_text(data.width / 2 + 12.5, 65, text="Instructions",
                       font="Times 80", fill="cyan")
    canvas.create_text(data.width / 2, 65, text="Instructions", font="Times 80")
    canvas.create_rectangle(data.width / 2 - 150, data.height - 100,
                            data.width / 2 + 150, data.height - 50)
    canvas.create_text(data.width / 2, data.height - 75, text="E x p l o r e",
                       font="Courier 30")
    instructions(canvas)


################################################################################
################################################################################
# Main Code for Fractal Generator
################################################################################
################################################################################


################################
# Anaglyphing Fractal Generator
################################

def draw3dLine(canvas, x1, y1, z1, x2, y2, z2):
    global data
    # Draws red-blue anaglyphic line between 3d points 1 and 2.
    # where z=0 appears in the plane of the screen, z<0 appears closer (pops
    # out of the screen) and z>0 appears farther away (sinks into the screen).
    zScale = 10 * data.level
    if z1 == 0 and z2 == 0:
        canvas.create_line(x1, y1, x2, y2, fill="black")
    else:
        canvas.create_line(x1 - z1 / zScale, y1, x2 - z2 / zScale, y2, fill="cyan")
        canvas.create_line(x1 + z1 / zScale, y1, x2 + z2 / zScale, y2, fill="red")


def draw3dSegments(canvas, point, zoom, segments):
    global data
    # Draws a line on a tkinter canvas based on a starting point (x, y, z) and one
    # or more segments in the form of a list of (r, theta, zeta).
    sx, sy, sz = point
    theta = 0
    eta = 0
    # Sets up the starting point for the line drawing
    for segment in segments:
        r, theta, eta = zoom * segment[0], math.radians(segment[1]) + theta, math.radians(segment[2]) + eta
        ex = sx + r * math.cos(theta)
        ey = sy - r * math.sin(theta)
        ez = sz + r * math.sin(eta)
        draw3dLine(canvas, sx, sy, sz, ex, ey, ez)
        sx, sy, sz = ex, ey, ez
    return sx, sy, sz


def fractal3dLine(level, startR, startTheta, startEta, phi, zeta, breaks, spikes):
    # Computes the segments of a 3d fractal line with x,y angle phi covering
    # distance r (in pixels) at initial x,y-angle startTheta and z-angle
    # startZeta (both in degrees)
    if level > 0:
        result = []
        lengthScaler = 4
        r = startR / (breaks + lengthScaler)
        # uses endR to compute the length of the
        # fractal line, and then scales it to approximate the original length
        # (StartR)
        result.extend(fractal3dLine(level - 1, r, startTheta, startEta, 
                                    phi, zeta, breaks, spikes))
        endR = r
        result.extend(fractal3dLine(level - 1, r, phi, zeta, phi, 
                                    zeta, breaks, spikes))
        endR += r * math.cos(math.radians(phi))
        currentTheta = phi
        phiBreak = -2 * phi / breaks
        zetaBreak = -2 * zeta / breaks
        for _ in range(breaks):
            if spikes:
            #added special conditions for spikes under 3D to make them appear
            #3D and not offset the geometry as they did previously
                if phiBreak <= 0:
                    spikeAngle = phiBreak / 2 + 90
                else:
                    spikeAngle = phiBreak / 2 - 90
                result.extend(fractal3dLine(level - 1, r, spikeAngle, 
                                            zeta, phi, zeta, breaks, spikes))
                result.extend(fractal3dLine(level - 1, r, 180, 
                                            (breaks + 1) * zetaBreak, 
                                            phi, zeta, breaks, spikes))
                result.extend(fractal3dLine(level - 1, r, spikeAngle, zeta, 
                                            phi, zeta, breaks, spikes))
            else:
                result.extend(fractal3dLine(level - 1, r, phiBreak, 
                                            zetaBreak, phi, zeta, breaks, 
                                            spikes))
            currentTheta += phiBreak
            endR += r * math.cos(math.radians(currentTheta))
        result.extend(fractal3dLine(level - 1, r, phi, 
                                    zeta, phi, zeta, breaks, spikes))
        endR += r

        if endR < startR / lengthScaler:
            # This caps the scaling of the resulting fractal line so that it
            # doesn't grow too big/tall when the fractal line compresses too
            # much.
            endR = startR / lengthScaler
        scaledResult = []
        rScale = startR / endR
        # Set up for the r-scaling
        for coord in result:
            # Create a new segments list that scales all the r values in
            # result by the factor rScale.
            scaledResult.append((coord[0] * rScale, coord[1], coord[2]))
        return scaledResult
    else:
        return [(startR, startTheta, startEta)]


#######################################
# Fractal Generator Without Anaglyphing
#######################################

# Singificantly changed from before/all new since only half made in tp1 and 
# not used in tp2. When not anaglyphing, can specify color1 to color2  
# gradation. Reworked functions from returning a list of points into a polygon
# to making each segemnt have a specific color based on its level and whether
# it is gradiated, and drawing lines joined together at points rather than a 
# whole polygon, since the polygon would only take one color.

def drawSegments(canvas, point, zoom, segments, colors, wid="1"):
    # Draws a line on a tkinter canvas based on a starting point (x, y) and one
    # or more segments in the form of a list of (r, angle).
    # colors are passed in as a list (with level # of elements)
    sx, sy = point
    theta = 0
    for segment in segments:
        r, theta = zoom * segment[0], math.radians(segment[1]) + theta
        ex = sx + r * math.cos(theta)
        ey = sy - r * math.sin(theta)
        canvas.create_line(sx, sy, ex, ey, fill=colors[segment[2]], width=wid, 
                            capstyle="round", joinstyle="round")
        sx, sy = ex, ey
    return sx, sy


def fractalLine(level, startR, startTheta, startColor, phi, breaks, spikes):
    # Computes the segments of a 2d fractal line with angle phi covering
    # distance r (in pixels) at initial angle theta (in degrees). 
    if level > 0:
        result = []
        lengthScaler = 4
        r = startR / (breaks + lengthScaler)
        # uses endR to compute the length of the
        # fractal line, and then scales it to approximate the original length
        # (StartR)
        result.extend(fractalLine(level - 1, r, startTheta, startColor, 
                                    phi, breaks, spikes))
        endR = r
        nextColor = max(startColor - 1, 0)
        result.extend(fractalLine(level - 1, r, phi, nextColor, 
                                    phi, breaks, spikes))
        endR += r * math.cos(math.radians(phi))
        currentAngle = phi
        phiBreak = - 2 * phi / breaks
        for _ in range(breaks):
            if spikes: 
                if phiBreak <= 0:
                    spikeAngle = phiBreak / 2 + 90
                else:
                    spikeAngle = phiBreak / 2 - 90
                result.extend(fractalLine(level - 1, r, spikeAngle, nextColor, 
                                            phi, breaks, spikes))
                result.extend(fractalLine(level - 1, r, 180, nextColor, phi, 
                                            breaks, spikes))
                result.extend(fractalLine(level - 1, r, spikeAngle, nextColor, 
                                            phi, breaks, spikes))
            else:
                result.extend(fractalLine(level - 1, r, phiBreak, nextColor, 
                                        phi, breaks, spikes))
            currentAngle += phiBreak
            endR += r * math.cos(math.radians(currentAngle))
        result.extend(fractalLine(level - 1, r, phi, startColor, phi, 
                                    breaks, spikes))
        endR += r

        if endR < startR / lengthScaler:
            # This caps the scaling of the resulting fractal line so that it doesn't
            # grow too big/tall when the fractal line compresses too much.
            endR = startR / lengthScaler

        scaledResult = []
        rScale = startR / endR
        # Set up for the r-scaling
        for coord in result:
            # Create a new segments list that scales all the r values in result by
            # the factor rScale.
            scaledResult.append((coord[0] * rScale, coord[1], coord[2]))
        return scaledResult
    else:
        return [(startR, startTheta, startColor)]
        
#################################################
# Saving, Storing, Clearing, and Opening Fractals
#################################################

##########
# CITATION
# https://docs.python.org/3/library/shelve.html
# This is also my own code below, I just used the python website to
# learn about this library so that I could use it to save and restore fractals.
# The only line that is copied is "with shelve.open(savedDataFile) as f:"
# and this line is also featured in to File IO section of the 112 website.

# Writing all of the below functions is my own work. 
##########

# these functions are called and manipulated in the MVC framework
# in keyPressed and mousePressed, as well as in button drawing functions

def saveData(location):
    global data, savedDataFile
    print("Saving data in location " + location + ".")
    with shelve.open(savedDataFile) as f:
        f[location] = data


def openData(location):
    global data, savedDataFile
    with shelve.open(savedDataFile) as f:
        if location in f:
            print("Opening data in location " + location + ".")
            data = f[location]
        else:
            print("No data in location " + location + ".")


def clearData(location):
    global data, savedDataFile
    with shelve.open(savedDataFile) as f:
        if location in f:
            print("Deleting data in location " + location + ".")
            del f[location]
        else:
            print("No data in location " + location + ".")


def keysSaved():
    global data, savedDataFile
    with shelve.open(savedDataFile) as f:
        return list(f.keys())


def getBgColorForButton(location):
    global savedDataFile
    with shelve.open(savedDataFile) as f:
        if location in f:
            tempData = f[location]
            return tempData.background
        else:
            return "gray95"


def getFgColorForButton(location):
    global savedDataFile
    with shelve.open(savedDataFile) as f:
        if location in f:
            tempData = f[location]
            return tempData.color1
        else:
            return "gray95"


def get3dForButton(location):
    global savedDataFile
    with shelve.open(savedDataFile) as f:
        if location in f:
            tempData = f[location]
            return tempData.threeDee
        else:
            return False


def testGCFB():
    for k in keysSaved():
        print(getBgColorForButton(k))
    print(getBgColorForButton("42"))


################
# Color Gradient
################

###########
# CITATION
# https://pypi.org/project/tkcolorpicker/
# This website taught me about the tkinter color picker and the function 
# askcolor, as used below in the getColor function. Thus, the second line in
# the getColor() function is not my original work. 

# https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
# I used this website's rgb_to_hex function to convert my colors so I could gradiate them
# And the hex_to_rgb function. 

#All the color gradiating is my own work. 
##########

def getColor():
    return askcolor()[-1]


def hexToRgb(hex):
    hex = hex.lstrip('#')
    return int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)


def rgbToHex(rgb):
    return "#%02x%02x%02x" % rgb


def generateColorGradient(color1, color2, steps):
    if steps < 1:
        steps = 1
    r1, g1, b1 = hexToRgb(color1)
    r2, g2, b2 = hexToRgb(color2)
    rStep = (r2 - r1) // steps
    gStep = (g2 - g1) // steps
    bStep = (b2 - b1) // steps
    gradient = [color1]
    r, g, b = r1, g1, b1
    for i in range(steps):
        r += rStep
        r = min(r, 255)
        # Make sure each r, g, and b are <= 255
        r = max(r, 0)
        # Make sure each r, g, and b are > 0
        g += gStep
        g = min(g, 255)
        g = max(g, 0)
        b += bStep
        b = min(b, 255)
        b = max(b, 0)
        gradient.append(rgbToHex((r, g, b)))
    return gradient


def drawDot(canvas, point, color="black", size=3, outl=""):
    # Draws a dot on the canvas at location point = (x, y). Color and size,
    # which is the radius of the dot in pixels, may also be specified.
    px, py = point
    canvas.create_oval(px - size, py - size, px + size, py + size, fill=color, 
                        outline=outl)

############################
# User Interface and Buttons
############################

def animationButton(canvas):
    global data
    canvas.create_rectangle(25 + 2, data.height - 290 + 2,
                            data.barWidth - 25 + 2, data.height - 265 + 2,
                            fill="dark grey", width=0)
    canvas.create_rectangle(25, data.height - 290, data.barWidth - 25,
                            data.height - 265, fill="white", width=0)
    canvas.create_text(data.barWidth / 2, data.height - 278,
                       text=data.animateText, font="Courier 12")


def anaglyphButton(canvas):
    global data
    canvas.create_rectangle(25 + 2, data.height - 325 + 2,
                            data.barWidth - 25 + 2, data.height - 300 + 2,
                            fill="dark grey", width=0)
    canvas.create_rectangle(25, data.height - 325, data.barWidth - 25,
                            data.height - 300, fill="white", width=0)
    canvas.create_text(data.barWidth / 2, data.height - 313,
                       text=data.anaglyphText, font="Courier 12")


def colorButton(canvas):
    global data
    canvas.create_rectangle(25 + 2, data.height - 385 + 2, 60 + 2,
                            data.height - 350 + 2, fill="dark grey", width=0)
    canvas.create_rectangle(25, data.height - 385, 60,
                            data.height - 350, fill="white", width=0)
    canvas.create_rectangle(70 + 2, data.height - 385 + 2, 105 + 2,
                            data.height - 350 + 2, fill="dark grey", width=0)
    canvas.create_rectangle(70, data.height - 385, 105,
                            data.height - 350, fill="white", width=0)
    canvas.create_rectangle(115 + 2, data.height - 385 + 2, 150 + 2,
                            data.height - 350 + 2, fill="dark grey", width=0)
    canvas.create_rectangle(115, data.height - 385, 150,
                            data.height - 350, fill="white", width=0)
    canvas.create_rectangle(25 + 5, data.height - 380, 55, data.height - 355,
                            fill=data.color1, width=1)
    canvas.create_rectangle(75, data.height - 380, 100, data.height - 355,
                            fill=data.color2, width=1)
    canvas.create_rectangle(120, data.height - 380, 145, data.height - 355,
                            fill=data.background, width=1)


def instructionIcon(canvas):
    global data
    radius = 10
    canvas.create_oval(25 - radius + 2, data.height - 25 - radius + 2,
                       25 + radius + 2, data.height - 25 + radius + 2,
                       fill="dark grey", width=0)
    canvas.create_oval(25 - radius, data.height - 25 - radius, 25 + radius,
                       data.height - 25 + radius, fill="white", width=0)
    canvas.create_text(25, data.height - 25, text="i", font="Courier 12")


def drawSquiggle(canvas, startPoint, color, threeDee):
    if threeDee:
        startX, startY = startPoint
        canvas.create_rectangle(startX+3, startY-7, startX+17, startY+5, 
                                fill="black", outline="")
        canvas.create_rectangle(startX+23, startY-7, startX+37, startY+5, 
                                fill="black", outline="")
        canvas.create_rectangle(startX+5, startY-5, startX+15, startY+3, 
                                fill="red", outline="")
        canvas.create_rectangle(startX+25, startY-5, startX+35, startY+3, 
                                fill="cyan", outline="")
        canvas.create_arc(startX+14, startY-5, startX+26, startY+5, 
                            style="arc", start="45", extent="90", width=2)
        canvas.create_line(startX-1, startY-10, startX+3, startY-6, 
                            fill="black", width=2)
        canvas.create_line(startX+37, startY-6, startX+41, startY-10, 
                            fill="black", width=2)
    else:
        drawSegments(canvas, startPoint, 1.0,
                     [(10, 0, 0),
                      (16, 60, 0),
                      (16, -120, 0),
                      (10, 60, 0)],
                     [color], 2)


def storeButton(canvas):
    global data
    canvas.create_rectangle(25 + 2, data.height - 240 + 2, 77 + 2, 
                            data.height - 188 + 2,
                            fill="dark grey", width=0)
    canvas.create_rectangle(25 + 2, data.height - 176 + 2, 77 + 2, 
                            data.height - 124 + 2,
                            fill="dark grey", width=0)
    canvas.create_rectangle(25 + 2, data.height - 112 + 2, 77 + 2,
                            data.height - 60 + 2,
                            fill="dark grey", width=0)
    canvas.create_rectangle(97 + 2, data.height - 240 + 2, 150 + 2, 
                            data.height - 188 + 2,
                            fill="dark grey", width=0)
    canvas.create_rectangle(97 + 2, data.height - 176 + 2, 150 + 2, 
                            data.height - 124 + 2,
                            fill="dark grey", width=0)
    canvas.create_rectangle(97 + 2, data.height - 112 + 2, 150 + 2, 
                            data.height - 60 + 2,
                            fill="dark grey", width=0)
    #uses data from the stored fractals to generate representative pictures on 
    #the keys that correspond to those saved fractals
    keys = keysSaved()
    canvas.create_rectangle(25, data.height - 240, 77, data.height - 188,
                            fill=getBgColorForButton("1"), width=0)
    if ("1" in keys): drawSquiggle(canvas, (32, data.height - 214), 
                                getFgColorForButton("1"), get3dForButton("1"))
    canvas.create_rectangle(25, data.height - 176, 77, data.height - 124,
                            fill=getBgColorForButton("3"), width=0)
    if ("3" in keys): drawSquiggle(canvas, (32, data.height - 150), 
                                getFgColorForButton("3"), get3dForButton("3"))
    canvas.create_rectangle(25, data.height - 112, 77, data.height - 60,
                            fill=getBgColorForButton("5"), width=0)
    if ("5" in keys): drawSquiggle(canvas, (32, data.height - 86), 
                                getFgColorForButton("5"), get3dForButton("5"))
    canvas.create_rectangle(97, data.height - 240, 150, data.height - 188,
                            fill=getBgColorForButton("2"), width=0)
    if ("2" in keys): drawSquiggle(canvas, (104, data.height - 214), 
                                getFgColorForButton("2"), get3dForButton("2"))
    canvas.create_rectangle(97, data.height - 176, 150, data.height - 124,
                            fill=getBgColorForButton("4"), width=0)
    if ("4" in keys): drawSquiggle(canvas, (104, data.height - 150), 
                                getFgColorForButton("4"), get3dForButton("4"))
    canvas.create_rectangle(97, data.height - 112, 150, data.height - 60,
                            fill=getBgColorForButton("6"), width=0)
    if ("6" in keys): drawSquiggle(canvas, (104, data.height - 86), 
                                getFgColorForButton("6"), get3dForButton("6"))


def storeButtonButtons(canvas):
    global data
    canvas.create_rectangle(25, data.height - 201, 77, data.height - 188,
                            fill="white", width=0)
    canvas.create_rectangle(97, data.height - 201, 150, data.height - 188,
                            fill="white", width=0)
    canvas.create_rectangle(25, data.height - 137, 77, data.height - 124,
                            fill="white", width=0)
    canvas.create_rectangle(97, data.height - 137, 150, data.height - 124,
                            fill="white", width=0)
    canvas.create_rectangle(25, data.height - 73, 77, data.height - 60,
                            fill="white", width=0)
    canvas.create_rectangle(97, data.height - 73, 150, data.height - 60,
                            fill="white", width=0)
    canvas.create_rectangle(64, data.height - 240, 77, data.height - 227,
                            fill="white", width=0)
    canvas.create_rectangle(64, data.height - 176, 77, data.height - 163,
                            fill="white", width=0)
    canvas.create_rectangle(64, data.height - 112, 77, data.height - 99,
                            fill="white", width=0)
    canvas.create_rectangle(137, data.height - 240, 150, data.height - 227,
                            fill="white", width=0)
    canvas.create_rectangle(137, data.height - 176, 150, data.height - 163,
                            fill="white", width=0)
    canvas.create_rectangle(137, data.height - 112, 150, data.height - 99,
                            fill="white", width=0)
    canvas.create_text(70.4, data.height - 234, text="X", font="Arial 10")
    canvas.create_text(70.4, data.height - 170, text="X", font="Arial 10")
    canvas.create_text(70.4, data.height - 106, text="X", font="Arial 10")
    canvas.create_text(143.4, data.height - 234, text="X", font="Arial 10")
    canvas.create_text(143.4, data.height - 170, text="X", font="Arial 10")
    canvas.create_text(143.4, data.height - 106, text="X", font="Arial 10")
    canvas.create_text(51, data.height - 195.5, text="save", font="Courier 11")
    canvas.create_text(51, data.height - 132.5, text="save", font="Courier 11")
    canvas.create_text(51, data.height - 67.5, text="save", font="Courier 11")
    canvas.create_text(123, data.height - 195.5, text="save", font="Courier 11")
    canvas.create_text(123, data.height - 132.5, text="save", font="Courier 11")
    canvas.create_text(123, data.height - 67.5, text="save", font="Courier 11")


def drawTriangle(canvas, startpoint, size, orientation, col="", outl="black", wid=1):
    x1, y1 = startpoint
    x2 = x1 + size * math.cos(math.radians(orientation + 30))
    y2 = y1 + size * math.sin(math.radians(orientation + 30))
    x3 = x1 + size * math.cos(math.radians(orientation - 30))
    y3 = y1 + size * math.sin(math.radians(orientation - 30))
    canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=col, outline=outl, 
                            width=wid)


def navButtons(canvas):
    drawTriangle(canvas, (1144, 775), 22, 0, "dark grey", "")
    drawTriangle(canvas, (1175, 744), 22, 90, "dark grey", "")
    drawTriangle(canvas, (1206, 775), 22, 180, "dark grey", "")
    drawTriangle(canvas, (1176, 806), 22, -90, "dark grey", "")
    drawTriangle(canvas, (1142, 772), 20, 0, "white", "black")
    drawTriangle(canvas, (1173, 742), 20, 90, "white", "black")
    drawTriangle(canvas, (1203, 772), 20, 180, "white", "black")
    drawTriangle(canvas, (1173, 803), 20, -90, "white", "black")
    canvas.create_rectangle(1154, 813, 1172, 830, fill="dark grey", outline="")
    canvas.create_rectangle(1152, 810, 1168, 826, fill="white", outline="black")
    canvas.create_line(1155, 818, 1165, 818)
    canvas.create_rectangle(1180, 813, 1198, 830, fill="dark grey", outline="")
    canvas.create_rectangle(1178, 810, 1194, 826, fill="white", outline="black")
    canvas.create_line(1181, 818, 1191, 818)
    canvas.create_line(1186, 813, 1186, 823)


def resetButton(canvas):
    global data
    canvas.create_rectangle(97 + 2, data.height - 35 + 2,
                            data.barWidth - 25 + 2, data.height - 15 + 2,
                            fill="dark grey", width=0)
    canvas.create_rectangle(97, data.height - 35,
                            data.barWidth - 25, data.height - 15,
                            fill="white", width=0)
    canvas.create_text(123.5, data.height - 25, text="reset",
                       font="Courier 12")


def createButton(canvas, startHeight):
    global data
    bigWidth = data.barWidth // 7 * 3
    startBig = data.barWidth // 7
    startSmall = data.barWidth - startBig * 2
    smallWidth = startBig
    smallGap = startBig * 2
    canvas.create_rectangle(startBig + 2, startHeight + 2,
                            startBig + 2 + bigWidth, startHeight + 2 + bigWidth,
                            fill="dark grey", width=0)
    canvas.create_rectangle(startBig, startHeight, startBig + bigWidth,
                            startHeight + bigWidth, fill="white", width=0)
    canvas.create_rectangle(startSmall + 2, startHeight + 2 + 10,
                            startSmall + 2 + smallWidth,
                            startHeight + 2 + smallWidth + 10, fill="dark grey",
                            width=0)
    canvas.create_rectangle(startSmall + 2, startHeight + 2 + smallGap - 10,
                            startSmall + 2 + smallWidth,
                            startHeight + 2 + smallWidth + smallGap - 10,
                            fill="dark grey", width=0)
    canvas.create_rectangle(startSmall, startHeight + 10,
                            startSmall + smallWidth,
                            startHeight + smallWidth + 10, fill="white",
                            width=0)
    canvas.create_rectangle(startSmall, startHeight + smallGap - 10,
                            startSmall + smallWidth,
                            startHeight + smallGap + smallWidth - 10,
                            fill="white", width=0)
    canvas.create_polygon(startSmall + 5, startHeight + smallWidth - 5 + 10,
                          startSmall + smallWidth / 2, startHeight + 5 + 10,
                          startSmall + smallWidth - 5,
                          startHeight + smallWidth - 5 + 10, fill="white",
                          outline="black")
    canvas.create_polygon(startSmall + 5,
                          startHeight + smallGap / 2 + smallWidth + 5 - 10,
                          startSmall + smallWidth / 2,
                          startHeight + smallGap / 2 + 2 * smallWidth - 5 - 10,
                          startSmall + smallWidth - 5,
                          startHeight + smallGap / 2 + smallWidth + 5 - 10,
                          fill="white", outline="black")


def sideBar(canvas):
    #gets the current state of the fractal and draws a verison of the current 
    #state of one state on its corresponding button, with all other states 
    #held at a base constant. 
    global data
    canvas.create_rectangle(0, 0, data.barWidth + 2, data.height, fill="grey50",
                            width=0)
    canvas.create_rectangle(0, 0, data.barWidth, data.height, fill="light grey",
                            width=0)
    for buttonHeight in range(25, 450, 85):
        createButton(canvas, buttonHeight)
    drawSegments(canvas, [37.5, 62.5], 1,
                 fractalLine(1, 50, 0, 0, 55, data.breaks, None),
                 ["black"])
    drawSegments(canvas, [37.5, 62.5 + 85], 1,
                 fractalLine(1, 50, 0, 0, 55, 1, data.spikes),
                 ["black"])
    if data.mirror:
        drawSegments(canvas, [37.5, 62.5 + 170], 1,
                     fractalLine(1, 50, 0, 0, -55, 1, False),
                     ["black"])
        drawSegments(canvas, [37.5, 62.5 + 170], 1,
                     fractalLine(1, 50, 0, 0, 55, 1, False),
                     ["black"])
    else:
        drawSegments(canvas, [37.5, 62.5 + 170], 1,
                     fractalLine(1, 50, 0, 0, 55, 1, False),
                     ["black"])
    if data.level < 3:
        drawSegments(canvas, [37.5, 62.5 + 340], 1,
                     fractalLine(data.level, 50, 0, 0, 55, 1, False),
                     ["black"])
    else:
        drawSegments(canvas, [37.5, 62.5 + 340], 1,
                     fractalLine(3, 50, 0, 0, 55, 1, False),
                     ["black"])
    if data.shape == 1:
        canvas.create_line(37.5, 62.5 + 255, 87.5, 62.5 + 255)
    elif data.shape == 2:
        canvas.create_line(37.5, 57.5 + 255, 87.5, 57.5 + 255)
        canvas.create_line(37.5, 67.5 + 255, 87.5, 67.5 + 255)
    iconStart = (37.5 + 5 * (data.shape - 3), 82.5 + 255)
    iconR = 76 - 9 * data.shape

    for shapeTheta in range(0, 360, 360 // data.shape):
        if data.shape > 2:
            iconStart = drawSegments(canvas, iconStart, 1.0,
                                     [(iconR, shapeTheta, 0)], ["black"], 1)


###############
# MVC Framework
###############

def fractalKeyPressed(event):
    global data, saveDataMode, openDataMode, clearDataMode
    if saveDataMode:
        if (event.keysym in "12345678"):
            saveData(event.keysym)
        else:
            print("Save command cancelled.")
        saveDataMode = False
        return
    if openDataMode:
        if (event.keysym in "12345678"):
            openData(event.keysym)
        else:
            print("Open command cancelled.")
        openDataMode = False
        return
    if clearDataMode:
        if (event.keysym in "12345678"):
            clearData(event.keysym)
        else:
            print("Clear command cancelled.")
        clearDataMode = False
        return
    if (event.keysym == "Right"):
        data.startX += 10
    elif (event.keysym == "Left"):
        data.startX -= 10
    elif (event.keysym == "Up"):
        data.startY -= 10
    elif (event.keysym == "Down"):
        data.startY += 10
    elif (event.keysym == "equal"):
        data.zoom *= 1.1
    elif (event.keysym == "minus"):
        data.zoom /= 1.1
    elif (event.keysym == "bracketright"):
        data.phi += 5
    elif (event.keysym == "bracketleft"):
        data.phi -= 5
    elif (event.keysym == "quoteright"):
        data.theta += 5
    elif (event.keysym == "semicolon"):
        data.theta -= 5
    elif (event.keysym == "l") and data.breaks < 9:
        data.breaks += 1
    elif (event.keysym == "k") and data.breaks > 1:
        data.breaks -= 1
    elif (event.keysym == "period") and data.level < 5:
        data.level += 1
    elif (event.keysym == "comma") and data.level > 1:
        data.level -= 1
    elif (event.keysym in "123456"):
        data.shape = int(event.keysym)
    elif (event.keysym == "x") and data.zeta < 90:
        data.zeta += 2
    elif (event.keysym == "z") and data.zeta > -90:
        data.zeta -= 2
    elif (event.keysym == "y"):
        data.spikes = not data.spikes
    elif (event.keysym == "m"):
        data.mirror = not data.mirror
    elif (event.keysym == "d"):
        data.threeDee = not data.threeDee
    elif (event.keysym == "f"):
        data.displayParams = not data.displayParams
    elif (event.keysym == "p"):
        print(" Shape: ", ["None", "Line", "Lines", "Triangle",
                           "Square", "Pentagon", "Hexagon", "None",
                           "Octagon", "Nonagon"][data.shape])
        print(" Level: ", data.level)
        print("   Phi: ", data.phi)
        print("  Zeta: ", data.zeta)
        print("Breaks: ", data.breaks)
        print("Spikes: ", data.spikes)
        print("Mirror: ", data.mirror)
    elif (event.keysym == "s"):
        saveDataMode = True
        print("Save Location?")
    elif (event.keysym == "o"):
        openDataMode = True
        print("Open Location?")
    elif (event.keysym == "e"):
        clearDataMode = True
        print("Clear Location?")
    elif (event.keysym == "t"):
        print(keysSaved())
    elif (event.keysym == "r"):
        print("Resetting.")
        init()
        data.mode = "fractal"
    elif (event.keysym == "c"):
        c = getColor()
        if c is not None:
            data.color1 = c
            print("Color1: ", data.color1)
    elif (event.keysym == "v"):
        c = getColor()
        if c is not None:
            data.color2 = c
            print("Color2: ", data.color2)
    elif (event.keysym == "b"):
        c = getColor()
        if c is not None:
            data.background = c
            print("Background: ", data.background)
    elif (event.keysym == "w") and data.lineWidth < 7:
        data.lineWidth += 1
    elif (event.keysym == "q") and data.lineWidth > 1:
        data.lineWidth -= 1


def fractalMousePressed(event):
    global data
    if event.x > 125 and event.x < 150 and event.y > 35 and event.y < 60 and data.breaks < 9:
        data.breaks += 1
    elif event.x > 125 and event.x < 150 and event.y > 65 and event.y < 90 and data.breaks > 0:
        data.breaks -= 1
    elif event.x > 125 and event.x < 150 and event.y > 120 and event.y < 145:
        data.spikes = True
    elif event.x > 125 and event.x < 150 and event.y > 150 and event.y < 175:
        data.spikes = False
    elif event.x > 125 and event.x < 150 and event.y > 205 and event.y < 230:
        data.mirror = True
    elif event.x > 125 and event.x < 150 and event.y > 235 and event.y < 260:
        data.mirror = False
    elif event.x > 125 and event.x < 150 and event.y > 290 and event.y < 315:
        if data.shape < 6:
            data.shape += 1
    elif event.x > 125 and event.x < 150 and event.y > 320 and event.y < 345:
        if data.shape > 1:
            data.shape -= 1
    elif event.x > 125 and event.x < 150 and event.y > 375 and event.y < 400 and data.level < 5:
        data.level += 1
    elif event.x > 125 and event.x < 150 and event.y > 405 and event.y < 430 and data.level > 1:
        data.level -= 1
    elif event.x > 25 and event.x < 150 and event.y > 560 and event.y < 585:
        if not data.animate:
            data.animate = True
            data.animateText = "Stop Animation"
        else:
            data.animate = False
            data.animateText = "Animate Fractal"
    elif event.x > 25 and event.x < 150 and event.y > 525 and event.y < 550:
        if not data.threeDee:
            data.threeDee = True
            data.anaglyphText = "Stop Anaglyph"
            data.zeta = 20
        else:
            data.threeDee = False
            data.anaglyphText = "Anaglyph Fractal"
    elif math.sqrt((event.x - 25) ** 2 + (event.y - 825) ** 2) <= 10:
        data.mode = "instruction"
    elif event.x > 25 and event.x < 60 and event.y > 465 and event.y < 500:
        c = getColor()
        if c is not None:
            data.color1 = c
            print("Color1: ", data.color1)
    elif event.x > 70 and event.x < 105 and event.y > 465 and event.y < 500:
        c = getColor()
        if c is not None:
            data.color2 = c
            print("Color2: ", data.color2)
    elif event.x > 115 and event.x < 150 and event.y > 465 and event.y < 500:
        c = getColor()
        if c is not None:
            data.background = c
            print("Background: ", data.background)
    elif event.x > 97 and event.x < 150 and event.y > 815 and event.y < 835:
        print("Resetting.")
        init()
        data.mode = "fractal"
    elif event.x > 1142 and event.x < 1162 and event.y > 762 and event.y < 782:
        data.startX -= 10
    elif event.x > 1182 and event.x < 1203 and event.y > 762 and event.y < 782:
        data.startX += 10
    elif event.x > 1162 and event.x < 1182 and event.y > 742 and event.y < 762:
        data.startY -= 10
    elif event.x > 1162 and event.x < 1182 and event.y > 782 and event.y < 803:
        data.startY += 10
    elif event.x > 1152 and event.x < 1168 and event.y > 810 and event.y < 826:
        data.zoom /= 1.1
    elif event.x > 1178 and event.x < 1194 and event.y > 810 and event.y < 826:
        data.zoom *= 1.1
    elif event.x > 25 and event.x < 77 and event.y > 650 and event.y < 662:
        saveData("1")
    elif event.x > 25 and event.x < 77 and event.y > 713 and event.y < 726:
        saveData("3")
    elif event.x > 25 and event.x < 77 and event.y > 778 and event.y < 791:
        saveData("5")
    elif event.x > 98 and event.x < 150 and event.y > 650 and event.y < 662:
        saveData("2")
    elif event.x > 98 and event.x < 150 and event.y > 713 and event.y < 726:
        saveData("4")
    elif event.x > 98 and event.x < 150 and event.y > 778 and event.y < 791:
        saveData("6")
    elif event.x > 64 and event.x < 77 and event.y > 610 and event.y < 623:
        clearData("1")
    elif event.x > 64 and event.x < 77 and event.y > 674 and event.y < 687:
        clearData("3")
    elif event.x > 64 and event.x < 77 and event.y > 738 and event.y < 751:
        clearData("5")
    elif event.x > 137 and event.x < 150 and event.y > 610 and event.y < 623:
        clearData("2")
    elif event.x > 137 and event.x < 150 and event.y > 674 and event.y < 687:
        clearData("4")
    elif event.x > 137 and event.x < 150 and event.y > 738 and event.y < 751:
        clearData("6")
    elif event.x > 25 and event.x < 77 and event.y > 610 and event.y < 650:
        openData("1")
    elif event.x > 25 and event.x < 77 and event.y > 674 and event.y < 713:
        openData("3")
    elif event.x > 25 and event.x < 77 and event.y > 738 and event.y < 778:
        openData("5")
    elif event.x > 97 and event.x < 150 and event.y > 610 and event.y < 650:
        openData("2")
    elif event.x > 97 and event.x < 150 and event.y > 674 and event.y < 713:
        openData("4")
    elif event.x > 97 and event.x < 150 and event.y > 738 and event.y < 778:
        openData("6")


def fractalTimerFired():
    global data
    if data.animate:
        data.phi += 3


def fractalRedrawAll(canvas):
    global data
    if data.displayParams:
        drawDot(canvas, (data.startX, data.startY), "red", 
                            2 + data.lineWidth, "")
        canvas.create_text(data.width - 20, 16, anchor="ne",
                           text=(" Shape: " + ["None", "Line", "Lines",
                                               "Triangle", "Square", "Pentagon",
                                               "Hexagon", "None", "Octagon",
                                               "Nonagon"][data.shape]))
        canvas.create_text(data.width - 20, 32, anchor="ne",
                           text=("Level: " + str(data.level)))
        canvas.create_text(data.width - 20, 48, anchor="ne",
                           text=("Phi: " + str(data.phi)))
        canvas.create_text(data.width - 20, 64, anchor="ne",
                           text=("Zeta: " + str(data.zeta)))
        canvas.create_text(data.width - 20, 80, anchor="ne",
                           text=("Breaks: " + str(data.breaks)))
        canvas.create_text(data.width - 20, 96, anchor="ne",
                           text=("Spikes: " + str(data.spikes)))
        canvas.create_text(data.width - 20, 112, anchor="ne",
                           text=("Mirror: " + str(data.mirror)))
    shapeTheta = 360 / data.shape
    # drawing the fractals based on different cases, if it is 3D and mirrored, 
    # 3D and not mirrored, not 3D and mirrored, and not 3D and not mirrored. 
    if data.threeDee:
        startPoint = (data.startX, data.startY, data.startZ)
        draw3dSegments(canvas, startPoint, data.zoom, fractal3dLine(data.level,
                        data.startR, data.theta, 0, data.phi, data.zeta, 
                        data.breaks, data.spikes))
        for i in range(data.shape):
            if data.mirror:
                draw3dSegments(canvas, startPoint, data.zoom,
                               fractal3dLine(data.level, data.startR,
                                             data.theta + int(i * shapeTheta),
                                             0, -data.phi, -data.zeta,
                                             data.breaks, data.spikes))
            startPoint = draw3dSegments(canvas, startPoint, data.zoom,
                                        fractal3dLine(data.level, data.startR,
                                            data.theta + int(i * shapeTheta),
                                            0, data.phi, data.zeta,
                                            data.breaks, data.spikes))
    else:
        startPoint = (data.startX, data.startY)
        for i in range(data.shape):
            if data.mirror:
                drawSegments(canvas, startPoint, data.zoom,
                             fractalLine(data.level, data.startR,
                                         data.theta + int(i * shapeTheta),
                                         data.level, -data.phi,
                                         data.breaks, data.spikes),
                             generateColorGradient(data.color1, data.color2, 
                                                    data.level), data.lineWidth)
            startPoint = drawSegments(canvas, startPoint, data.zoom,
                                      fractalLine(data.level, data.startR,
                                            data.theta + int(i * shapeTheta),
                                            data.level, data.phi,
                                            data.breaks, data.spikes),
                                      generateColorGradient(data.color1, 
                                                    data.color2, data.level),
                                                    data.lineWidth)
    if data.height == 850:
    # only at this height will buttons fit and be displayed nicely. Program 
    # will still work at other heights, see instructions for keyboard shortcuts
        sideBar(canvas)
        instructionIcon(canvas)
        animationButton(canvas)
        anaglyphButton(canvas)
        colorButton(canvas)
        storeButton(canvas)
        resetButton(canvas)
        storeButtonButtons(canvas)
        navButtons(canvas)


################################################################################
################################################################################
# CITATION
# Run Function copied from 112 Website
# It has been altered slightly to accomodate for different needs with global
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
################################################################################
################################################################################

def run(width=300, height=300):
    global data

    def redrawAllWrapper(canvas):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height, fill=data.background,
                                width=0)
        redrawAll(canvas)
        canvas.update()

    def mousePressedWrapper(event, canvas):
        mousePressed(event)
        redrawAllWrapper(canvas)

    def keyPressedWrapper(event, canvas):
        keyPressed(event)
        redrawAllWrapper(canvas)

    def timerFiredWrapper(canvas):
        timerFired()
        redrawAllWrapper(canvas)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas)

    # Set up data and call init
    data.width = width
    data.height = height
    data.timerDelay = 100  # milliseconds
    root = Tk()
    root.title("Fractoglyph! by Olivia Husak (2018)")
    root.resizable(width=False, height=False)  # prevents resizing window
    init()
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    root.bind("<Button-1>",
              lambda event: mousePressedWrapper(event, canvas))
    root.bind("<Key>", lambda event: keyPressedWrapper(event, canvas))
    timerFiredWrapper(canvas)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(1225, 850)