import time
import board
import busio
import adafruit_vl6180x
import statistics

i2c = busio.I2C(board.SCL, board.SDA)

sensor = adafruit_vl6180x.VL6180X(i2c)

def distance():

    distance_meas = []

    for index in range(25):
        distance_meas.append(sensor.range)

    distance_var = statistics.mean(distance_meas)
    return distance_var 
    #already in mm

