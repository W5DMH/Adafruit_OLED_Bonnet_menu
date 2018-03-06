# Copyright (c) 2017 Adafruit Industries
# Author: James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import RPi.GPIO as GPIO
import sys
import time
import datetime
import os
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import subprocess
from time import sleep, strftime, localtime

from datetime import datetime, timedelta
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont



# Input pins:
L_pin = 27 
R_pin = 23 
C_pin = 4 
U_pin = 17 
D_pin = 22 

A_pin = 5 
B_pin = 6 


GPIO.setmode(GPIO.BCM) 

GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up


# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
x = 12

padding = -2
top = padding
bottom = height-padding
font = ImageFont.load_default()

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

def splash():
             disp.clear()
             draw.rectangle((0,0,width,height), outline=0, fill=0)
             draw.text((x, top+16),    "W5DMH PSKBeacon !",  font=font, fill=1)
             disp.image(image)
             disp.display()
             time.sleep(5)

splash()

#turn go to sleep timer on or off 
AUTO_OFF_LCD = 1


#set up a bit of a grid for mapping menu choices, each "V" variable is a   horizontal line
#each latindex is  
index = 0
latindex = 0 
filler = 0
va = 0
vb = 8
vc =16
vd = 24
ve = 32
vf = 40
vg = 48

def basemenu():
             disp.clear()    
             draw.text((x, top),       "System Status",  font=font, fill=1)
             draw.text((x, top+8),     "Beacon Settings", font=font, fill=1)
             draw.text((x, top+16),    "Beacon Status",  font=font, fill=1)
             draw.text((x, top+24),    "Hide Display",  font=font, fill=1) 
             draw.text((x, top+32),    "Reboot",  font=font, fill=1) 
             draw.text((x, top+40),    "Shutdown",  font=font, fill=1) 
             disp.image(image) 
             disp.display()   
             index = 0
def menuselect(): 
            if index == (va):
                 status()
            if index == (vb): 
                 beaconsettings()
            if index == (vc):
                 beaconstatus() 
            if index == (vd): 
                 closedisplay()
            if index == (ve): 
                 reboot()
            if index == (vf): 
                 shutdown()

            else: 
                 #Display image.
                 disp.image(image) 
                 disp.display()   
                 time.sleep(.01)         
def status(): 
            while GPIO.input(L_pin):
                 # Draw a black filled box to clear the image.
                 draw.rectangle((0,0,width,height), outline=0, fill=0)
                 # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126$
                 cmd = "hostname -I | cut -d\' \' -f1"
                 IP = subprocess.check_output(cmd, shell = True )
                 cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
                 CPU = subprocess.check_output(cmd, shell = True )
                 cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
                 MemUsage = subprocess.check_output(cmd, shell = True )
                 cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
                 Disk = subprocess.check_output(cmd, shell = True )

                 # Write two lines of text.

                 draw.text((x-6, top),       "IP: " + str(IP),  font=font, fill=255)
                 draw.text((x-6, top+8),     str(CPU), font=font, fill=255)
                 draw.text((x-6, top+16),    str(MemUsage),  font=font, fill=255)
                 draw.text((x-6, top+25),    str(Disk),  font=font, fill=255)

                 # Display image.
                 disp.image(image)
                 disp.display()
                 time. sleep (.01)                                     

def beaconsettings(): 
        print("beacon settings")

def beaconstatus(): 
        print("beacon status")

def closedisplay(): 
        disp.clear()
        disp.display()
        while GPIO.input(U_pin):
              time. sleep (.01)
def reboot():
       draw.rectangle((0,0,width,height), outline=0, fill=0)
       draw.text((x, top+16),    "Rebooting Now",  font=font, fill=1)
       disp.image(image) 
       disp.display()
       time.sleep(15)
       draw.rectangle((0,0,width,height), outline=0, fill=0)
       disp.image(image) 
       disp.display()
       os.system('reboot')
def shutdown(): #this will not function unless you start the script as sudo  
       draw.rectangle((0,0,width,height), outline=0, fill=0)
       draw.text((x, top+16),    "Shutting Down Now",  font=font, fill=1)
       disp.image(image) 
       disp.display()
       time.sleep(15)
       draw.rectangle((0,0,width,height), outline=0, fill=0)
       disp.image(image) 
       disp.display()
       os.system("shutdown now -h")
#setup the  go to sleep timer
lcdstart = datetime.now()


try:
    while 1:
#        basemenu()
        lcdtmp = lcdstart + timedelta(seconds=30)   
        if (datetime.now() > lcdtmp): 
            disp.clear()
            draw.rectangle((0,0,width,height), outline=0, fill=0)            
            disp.image(image) 
            disp.display()
        if GPIO.input(U_pin): # button is released
            filler = (0)
        else: # button is pressed:
            basemenu()
            draw.text((x-8, index),       "*",  font=font, fill=0)
            index = (index-8)
            draw.text((x-8, index),       "*",  font=font, fill=1)
            disp.image(image) 
            disp.display()    
            print("button up")
            lcdstart = datetime.now()
        if GPIO.input(L_pin): # button is released
            latindex = (latindex)
        else: # button is pressed:
            latindex =(latindex-1)
            disp.clear()
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            draw.text((x-8, index),       "*",  font=font, fill=1)
            basemenu()
            lcdstart = datetime.now()
        if GPIO.input(R_pin): # button is released
            filler =(0)
        else: # button is pressed:
            latindex =(latindex+1)            
            menuselect()
            lcdstart = datetime.now()
        if GPIO.input(D_pin): # button is released
            filler = (0)
        else: # button is pressed:
            basemenu() 
            draw.text((x-8, top),       "*",  font=font, fill=0)
            draw.text((x-8, index),       "*",  font=font, fill=0)
            index = (index +8)
            draw.text((x-8, index),       "*",  font=font, fill=1)
            disp.image(image) 
            disp.display()    
            print("button down")
            lcdstart = datetime.now()
        if GPIO.input(C_pin): # button is released
            filler = (0)
        else: # button is pressed:
            filler = (0)
        if GPIO.input(A_pin): # button is released
            filler = (0)
        else: # button is pressed:
            disp.clear()
            disp.display()
            sys.exit(0)
            #disp.display()
        if GPIO.input(B_pin): # button is released
            filler = (0)
        else: # button is pressed:
            menuselect ()
        if not GPIO.input(A_pin) and not GPIO.input(B_pin) and not GPIO.input(C_pin): 
            catImage = Image.open('happycat_oled_64.ppm').convert('1')
            disp.image(catImage)
        else:
            filler=(0)         
#        while GPIO.input(A_pin) and GPIO.input(B_pin) and GPIO.input(C_pin) and GPIO.input(U_pin) and GPIO.input(D_pin) and GPIO.input(L_pin) and GPIO.input(R_pin) :  
#                 lcdtmp = lcdstart + timedelta(seconds=30)   
#                 if (datetime.now() > lcdtmp): 
#                  disp.clear()
#                  draw.rectangle((0,0,width,height), outline=0, fill=0)            
#                  disp.image(image) 
#                  disp.display()
 

except KeyboardInterrupt: 
    GPIO.cleanup()

