# fractoglyph
Anaglyphed Fractal Generator for CMU15112 Term Project

Welcome to Fractogyph! 

Fractoglyph is a two-dimensional fractal generator with anaglyphic three-dimensional features. Fractoglyph is an interface where users can create art from fractals. A user can generate a fractal by altering many features of the base case of the fractal and changing the level of the fractal. Some of these base case features include changing the shape, reflecting, creating between edge points, and adding outer normal lines. Consequently, there are thousands of different fractals that can be generated from different combinations of these options. There are numerous additional features to manipulate your fractal once it is completed. These include saving and storing fractals, graduating their colors between levels, and most importantly the three-dimensional anaglyphing of the fractal. Anaglyphing (3D) is when a stereoscopic effect is created by filtering the images from each eye in the brain with chromatically opposite colors. A common example is 3D movies with red-cyan glasses. In overlaying red/cyan images of the fractals, a depth effect can be given to the images, as well as a three-dimensionality depending on the “z-axis” angle of these lines. 

In order to run this project, save the file into a folder on your computer. Do not move the file from this folder, because the program will create a file of stored data that it will need to access while running. Open Fractoglyph into your editor of choice, and being exploring!

There are no libraries that need to be installed in order to run this project. As long as you make sure that you have an updated version of Python 3 and tkinter runs, you’re all set! 

Below is a detailed list of instructions and keyboard shortcuts for running the program: 

There are five main features in changing the appearance of you fractal. All of these are managed both with key-commands and buttons. You will notice that each button is not labelled, but rather displays the current state of the fractal for that parameter. This is helpful in seeing the different values for each of the parameters at the current time. These are controlled by the following commands:
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
            
Now that you have created your fractal, you can anaglyph it! In order to see the fractal in 3D, you will need a pair of red-cyan 3D glasses. In changing the depth with the keys below, you can either make the center of the fractal appear more sunken in with the edges protruding out of the screen, or make the center appear more forward, with the edges sunken in. Try moving your head around and notice how the fractal changes!
Press 'd' to begin analgyphing - this corresponds to the 'anaglyph fractal' button on the side panel
Press 'x'/'z' to change anaglyph depth of fractal
            
If you are not anaglyphing, you can also change the color and width of your fractal and gradiate it between levels. The base level will be colored in the first color, and the highest level line segments will be colored in the second color. All segments in between will gradiate between the two colors evenly.
Press 'c' to choose a first color for your fractal - this corresponds to the left most color button
Press 'v' to choose a second color for your fractal - this corresponds to the middle color button
Press 'b' to choose a background color for the screen - this corresponds to the right most color button
Press 'w'/'q' to change the line width of the fractal
            
Once you are done with your fractal, you can save it and come back to it later. Don't worry about closing the program, as long as the file remains in the same file directory, your fractals will still be there the next time you open it!
Press 's' to save your current fractal, followed by one of '123456', to specify the location to store it in
Press 'o' to open a fractal, followed by one of '123456', to specify the location to open from
Press 'e' to clear the fractal data
Press 't' to print the current keys that fractals are saved under
Press 'r' to reset your fractal
            
There are also keyboard shortcuts in place to check the current state of the fractal.
Press 'p' to print summary of fractal values. This will print in the console of the python editor
Press 'f' to display a summary of the fractal values on the screen. They will appear in the upper right corner of the screen. Enabling this feature will also keep track of the starting point to the fractal, which is denoted by a small red circle in the fractal.
            
You can reach an instructions page by clicking the round 'i' button in the lower-left hand corner. 


