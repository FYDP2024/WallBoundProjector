import time
import pygame
from pygameConsts import *
import os
import glob

class DisplayController():
    def __init__(self):
        #Display
        try:
            #Initalize Pygame
            pygame.init()

            #Create Window with custom title
            pygame.display.set_caption("Wall Mounting Helper")
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            #screen = pygame.display.set_mode((1200,800))
            self.WIDTH, self.HEIGHT = self.screen.get_size()
            self.CENTER_X, self.CENTER_Y = self.WIDTH // 2, self.HEIGHT // 2


            self.img = ""
            self.img_path = ""
        except Exception as e:
            print(e)
            exit()

        self.picam_image_filename = "camera_imgs/cam_img.jpg"
        


    def camera_poll(self):
        last_time = 0
        while True:
            try:
                self.screen.fill(BLACK)

                if self.img != "":
                    self.screen.blit(img, (self.CENTER_X-self.img.get_width()//2,self.CENTER_Y-self.img.get_height()//2))
                
                pygame.display.update()
        
                file_time = os.path.getctime(self.img_path)
                if last_time < file_time:
                    print("got a more recent pic")
                    self.img = pygame.image.load(self.img_filename)
                    last_time = file_time
            except KeyboardInterrupt:
                
                pygame.quit()
                
                break
            time.sleep(0.5)
        
        
    
    def start(self):
        self.camera_poll()

if __name__ == '__main__':
    camera_controller = CameraController()
    camera_controller.start()