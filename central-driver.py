import serial
import time
import logging

import board
import busio
import adafruit_adxl34x

from threading import Thread

import click

import numpy as np

import math_engine.zoom_transform

'''
Central raspberry pi device driver

1. thread for receiving images from the frontend
2. thread for receiving data from the sensors
3. thread for processing the images with the math engine
4. separate process for displaying the latest image

'''

def accelerometer_to_degrees(x, y, z):
    """
    Convert accelerometer readings (x, y, z) to pitch and roll in degrees.

    :param x: Acceleration in the X-axis.
    :param y: Acceleration in the Y-axis.
    :param z: Acceleration in the Z-axis.
    :return: Tuple containing (pitch, roll) in degrees.
    """
    pitch = np.arctan2(y, np.sqrt(x**2 + z**2))
    roll = np.arctan2(-x, z)

    # Convert radians to degrees
    pitch_degrees = np.degrees(pitch)
    roll_degrees = np.degrees(roll)

    return pitch_degrees, roll_degrees

class PolarisController():
    def __init__(self):
        try:
            self.test = ""

            # Distance measurement: (cm)
            self.distance = 0
            
            # Accelerometer measurements: 
            self.accelerometer_reading = (0,0,0)
            self.roll = 0
            self.pitch = 0
            self.yaw = 0

            # Camera data
            self.img_path = ""

            '''
            Init connections to the: 
                - distance sensor
                - accelerometer
                - camera
            '''
            self.lidar_ser = serial.Serial("/dev/ttyS0", 115200)
            i2c = busio.I2C(board.SCL, board.SDA)
            self.accelerometer = adafruit_adxl34x.ADXL345(i2c)


        except Exception as e:
            print(e)
            exit()


    def read_distance_sensor(self):
        
        counter = self.lidar_ser.in_waiting # count the number of bytes of the serial port
        if counter > 8:
            bytes_serial = self.lidar_ser.read(9)
            self.lidar_ser.reset_input_buffer()
            
            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # python3
                distance = bytes_serial[2] + bytes_serial[3]*256
                strength = bytes_serial[4] + bytes_serial[5]*256
                temperature = bytes_serial[6] + bytes_serial[7]*256 # For TFLuna
                temperature = (temperature/8) - 256
                logging.info("TF-Luna python3 portion")
                logging.info("Distance:"+ str(distance) + "cm")
                logging.info("Strength:" + str(strength))
                if temperature != 0:
                    logging.info("Chip Temperature:" + str(temperature)+ "℃")
                self.lidar_ser.reset_input_buffer()

                self.distance = distance
                
            # if bytes_serial[0] == "Y" and bytes_serial[1] == "Y":
            #     distL = int(bytes_serial[2].encode("hex"), 16)
            #     distH = int(bytes_serial[3].encode("hex"), 16)
            #     stL = int(bytes_serial[4].encode("hex"), 16)
            #     stH = int(bytes_serial[5].encode("hex"), 16)
            #     distance = distL + distH*256
            #     strength = stL + stH*256
            #     tempL = int(bytes_serial[6].encode("hex"), 16)
            #     tempH = int(bytes_serial[7].encode("hex"), 16)
            #     temperature = tempL + tempH*256
            #     temperature = (temperature/8) - 256
            #     print("TF-Luna python2 portion")
            #     print("Distance:"+ str(distance) + "cm\n")
            #     print("Strength:" + str(strength) + "\n")
            #     print("Chip Temperature:" + str(temperature) + "℃\n")
            #     self.lidar_ser.reset_input_buffer()

    def distance_sensor_poll(self):
        time.sleep(1)

        # collect last 10 distance readings and only update
        # when there is a change to the mode of the last 10

        while True:
            self.read_distance_sensor()
            time.sleep(0.1)
            logging.info(str(self.distance) + "cm")
    
    def accelerometer_poll(self):

        alpha = 0.51
        alpha_prime = 1-alpha

        prev_reading = None

        while True:
            #print("%f %f %f"%self.accelerometer.acceleration)

            acceleration = self.accelerometer.acceleration

            if prev_reading == None:
                self.roll = acceleration[0]
                self.pitch = acceleration[1]
                self.yaw = acceleration[2]

                self.accelerometer_reading = acceleration

                prev_reading = acceleration
            else:
                avg = (alpha * acceleration[0], alpha * acceleration[1], alpha * acceleration[2]) + (alpha_prime * prev_reading[0], alpha_prime * prev_reading[1], alpha_prime * prev_reading[2])

                self.roll = avg[0]
                self.pitch = avg[1]
                self.yaw = avg[2]

                self.accelerometer_reading = avg

                prev_reading = avg

            logging.info("%f %f %f"%acceleration)
            time.sleep(0.1)

    

    def display_readings(self):
        while True:
            click.clear()

            roll, pitch = accelerometer_to_degrees(self.accelerometer_reading[0],
                                                   self.accelerometer_reading[1],
                                                   self.accelerometer_reading[2])

            roll = round(roll,1)
            pitch = round(pitch,1)

            print("Distance: %d cm"%self.distance)
            print("Roll: %.1f"%roll)
            print("Pitch: %.1f"%pitch)
            
            time.sleep(0.1)


    def update_output_image(self):
        pass
        

    def start(self):
        Thread(target=self.distance_sensor_poll).start()
        Thread(target=self.accelerometer_poll).start()
        Thread(target=self.display_readings).start()

if __name__ == '__main__':
    polaris_controller = PolarisController()
    polaris_controller.start()



    
