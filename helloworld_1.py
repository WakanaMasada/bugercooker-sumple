# UART Control
#
# This example shows how to use the serial port on your OpenMV Cam. Attach pin
# P4 to the serial input of a serial LCD screen to see "Hello World!" printed
# on the serial LCD display.

import sensor, image, time, pyb
thresholds = [(23, 62, -32, 43, -64, -19)]
x_data=0
y_data=0
x_datalowbyte=0
x_datahighbyte=0
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 300)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False)
#must be turned off for color tracking
clock = time.clock()
goaldata=[]

from pyb import UART

# Always pass UART 3 for the UART number for your OpenMV Cam.
# The second argument is the UART baud rate. For a more advanced UART control
# example see the BLE-Shield driver.
uart = UART(1, 115200, timeout_char = 1000)
led = pyb.LED(2) # Red LED = 1, Green LED = 2, Blue LED = 3, IR LEDs = 4.

while(True):
    led.off()
    clock.tick()
    x_data=400
    #x0=160
    #y0=120
    img = sensor.snapshot()
    for blob in img.find_blobs(thresholds, pixels_threshold=200, area_threshold=200):
        #img.draw_rectangle(blob.rect())
        #img.draw_cross(blob.cx(), blob.cy())
        #x_data=blob.cx()
        goaldata.append(str(blob))

    if len(goaldata)==0:
        x_data=400
    elif len(goaldata)==1:
        goaldata=goaldata[0]
        goaldata=goaldata.split(",")
        x_data = int(goaldata[5][6:])
    else:
        pixs=[]
        for i in range(len(goaldata)):
            goaldata_split=goaldata[i].split(",")
            pixs.append(int(goaldata_split[4][10:]))
        num=pixs.index(max(pixs))
        goaldata=goaldata[num]
        goaldata=goaldata.split(",")
        x_data=int(goaldata[5][6:])
        #y_data=int(goaldata[6][6:])
    goaldata.clear()
    #img.draw_line(160, 120, x_data, y_data, color = (255, 0, 0), thickness = 2)
    #print("fps=%d" % clock.fps()),
    #print(" x=%d" % x_data),

    if x_data>255:
        x_datalowbyte=255
        x_datahighbyte=x_data-255
    else:
        x_datalowbyte=x_data
        x_datahighbyte=0
    uart.writechar(255)
    uart.writechar(x_datalowbyte)
    uart.writechar(x_datahighbyte)
