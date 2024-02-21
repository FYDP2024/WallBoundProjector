import serial
import time
import logging

import board
import busio
import adafruit_adxl34x

from threading import Thread

import click

import time
import pygame
import os
import cv2

import numpy as np

from math_engine.zoom_transform import zoom_transform
from math_engine.roll_transform import roll_transform
from math_engine.pitch_transform import pitch_transform
import math_engine.shared_transform as sharedtransform

from helpers.helpers import SimpleMovingAverage

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

            self.roll_offset = 2

            # Camera data
            self.img_path = ""

            # User input
            self.input_image_path = "test_frame.png"

            #Result Image
            self.valid_img = False
            self.result_img = []

            #pygame window

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

                return distance
                
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
        distance = SimpleMovingAverage(5)
        while True:


            distance.add_data_point(self.read_distance_sensor())
            self.distance = distance.calculate_sma()
            time.sleep(0.05)
            logging.info(str(self.distance) + "cm")
    
    def accelerometer_poll(self):


        roll = SimpleMovingAverage(5)
        pitch = SimpleMovingAverage(5)
        

        while True:
            #print("%f %f %f"%self.accelerometer.acceleration)

            acceleration = self.accelerometer.acceleration

            if acceleration != (0,0,0):

                roll.add_data_point(-1 * acceleration[1])
                pitch.add_data_point(acceleration[0])

                roll_degrees, pitch_degrees = accelerometer_to_degrees(
                    roll.calculate_sma(),
                    pitch.calculate_sma(),
                    10)

                self.roll = roll_degrees
                self.pitch = pitch_degrees

                

                logging.info("%f %f %f"%acceleration)
            time.sleep(0.05)

    

    def display_readings(self):
        while True:
            click.clear()

            

            roll = round(self.roll,1)
            pitch = round(self.pitch,1)

            print("Distance: %d cm"%self.distance)
            print("Roll: %.1f"%roll)
            print("Pitch: %.1f"%pitch)
            print("%f %f %f"%self.accelerometer.acceleration)
            
            time.sleep(0.1)


    def update_output_image_2(self):
        #read the input image
        #transform it
        #save it to the display image folder
        

        img_path = "sample_grid_smaller.png"

        loaded_input_image = sharedtransform.read_img(img_path) 
        last_dist = self.distance
        last_roll = 0
        last_pitch = 0
        while True:
            roll, pitch = self.roll, self.pitch

            roll = roll - self.roll_offset


            if (self.distance,roll,pitch) != (last_dist,last_roll,last_pitch):
                last_dist = self.distance
                last_roll = self.roll
                last_pitch = self.pitch
                #print("start transform")
                transformed_img = loaded_input_image
                
                
                transformed_img = roll_transform(-1 * roll, transformed_img)
                print(transformed_img.shape[0]," ",transformed_img.shape[1])
                transformed_img = pitch_transform(pitch/10.0, transformed_img)
                transformed_img = zoom_transform(self.distance/100, transformed_img)

                self.result_img = transformed_img
                self.valid_img = True
                cv2.imwrite("display_imgs/img.png", transformed_img)
                #print("end transform")
            time.sleep(0.1)

    def display_result_img(self):
        #take the result image and display it in a pygame window
        #result image is self.result_img

        try:
            #Initalize Pygame
            pygame.init()

            #Create Window with custom title
            pygame.display.set_caption("Wall Mounting Helper")
            screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
            #screen = pygame.display.set_mode((1200,800))
            WIDTH, HEIGHT = screen.get_size()
            CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

        except Exception as e:
            print(e)
            exit()

        

        last_time = 0
        while True:
            try:
                screen.fill((0,0,0))

                if self.valid_img:
                    res_img = pygame.image.frombuffer(self.result_img.tostring(), self.result_img.shape[1::-1], "BGR")
                
                    try:
                        screen.blit(res_img, (CENTER_X-res_img.get_width()//2,CENTER_Y-res_img.get_height()//2))
                    except:
                        pass

                pygame.display.update()
        
                
            except KeyboardInterrupt:
                
                pygame.quit()
                
                break
            time.sleep(0.1)

    # def update_output_image(self):

    #     #Display
    #     try:
    #         #Initalize Pygame
    #         pygame.init()

    #         #Create Window with custom title
    #         pygame.display.set_caption("Wall Mounting Helper")
    #         screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    #         #screen = pygame.display.set_mode((1200,800))
    #         WIDTH, HEIGHT = screen.get_size()
    #         CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

    #     except Exception as e:
    #         print(e)
    #         exit()

        

    #     self.picam_image_filename = "camera_imgs/cam_img.jpg"

    #     img_path = self.input_img_path

    #     loaded_input_image = sharedtransform.read_img(img_path) 
    #     image_to_display = zoom_transform.zoom_transform(self.distance, loaded_input_image)

    #     while True:
    #         try:
    #             screen.fill((0,0,0))

    #             if image_to_display != None:
    #                 try:
    #                     screen.blit(image_to_display, (CENTER_X-image_to_display.get_width()//2,CENTER_Y-image_to_display.get_height()//2))
    #                 except:
    #                     pass
    #             pygame.display.update()
        
            
    #         except KeyboardInterrupt:
                
    #             pygame.quit()
                
    #             break
    #         time.sleep(0.5)
        

    def start(self):
        Thread(target=self.distance_sensor_poll).start()
        Thread(target=self.accelerometer_poll).start()
        Thread(target=self.display_readings).start()
        Thread(target=self.update_output_image_2).start()
        Thread(target=self.display_result_img).start()

if __name__ == '__main__':
    polaris_controller = PolarisController()
    polaris_controller.start()



    
