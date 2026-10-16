#!/usr/bin/env python3
import sys
import os
import time

lib_path = os.path.abspath("./rpi-rgb-led-matrix/")
sys.path.insert(0, lib_path)

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


"""

https://github.com/hzeller/rpi-rgb-led-matrix


Done off camera:
    - cloned library
    - built library
    - installed python dependencies in venv
    - wired display to pi
    - got example running


Important RGB Matrix API Notes:

    Configuration and options notes:
        options = RGBMatrixOptions()
        options.rows = ROWS                       # physical rows on the panel
        options.cols = COLS                       # physical columns
        options.hardware_mapping = "regular"
        options.gpio_slowdown = 4                 # pi 4b reccomendation
        options.brightness = 50                   # pi 4b reccomendation
        options.drop_privileges = False

        self.matrix = RGBMatrix(options=options)
        self.canvas = self.matrix.CreateFrameCanvas()               # how to get the array to independently modify each pixel
        self.font = graphics.Font()                                 # how to get fonts
        self.font.LoadFont("./rpi-rgb-led-matrix/fonts/4x6.bdf")    # how to load fonts


    Clearing the canvas:    
        canvas.Clear()
    
    Update Display with canvas:
        canvas = matrix.SwapOnVSync(canvas) returns the previously displayed canvas and displays the new one

    Writing text from a font:
        graphics.DrawText(canvas, font, X, Y, R, G, B, f"TEXT STRING{}")


"""



ROWS = 16
COLS = 32
 
options = RGBMatrixOptions()
options.rows = ROWS
options.cols = COLS
options.hardware_mapping = "regular"
options.gpio_slowdown = 4
options.brightness = 50
options.drop_privileges = False
 
matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()
 
font = graphics.Font()
font.LoadFont("./rpi-rgb-led-matrix/fonts/4x6.bdf")
 
canvas.Clear()
 
# box outline around the whole panel
blue = graphics.Color(0, 0, 255)
graphics.DrawLine(canvas, 0, 0, COLS - 1, 0, blue)                  # top
graphics.DrawLine(canvas, 0, ROWS - 1, COLS - 1, ROWS - 1, blue)    # bottom
graphics.DrawLine(canvas, 0, 0, 0, ROWS - 1, blue)                  # left
graphics.DrawLine(canvas, COLS - 1, 0, COLS - 1, ROWS - 1, blue)    # right
 
# word in the middle
graphics.DrawText(canvas, font, 9, 10, graphics.Color(255, 255, 0), "HELLO")
 
canvas = matrix.SwapOnVSync(canvas)
 
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    matrix.Clear()
 
