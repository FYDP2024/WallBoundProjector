import time
import pygame
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
            self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
            #screen = pygame.display.set_mode((1200,800))
            self.WIDTH, self.HEIGHT = self.screen.get_size()
            self.CENTER_X, self.CENTER_Y = self.WIDTH // 2, self.HEIGHT // 2


            self.img = ""
            self.img_path = "camera_imgs/cam_img.jpg"
        except Exception as e:
            print(e)
            exit()

        self.picam_image_filename = "camera_imgs/cam_img.jpg"
        


    def display_poll(self):
        last_time = 0
        while True:
            try:
                self.screen.fill((0,0,0))

                if self.img != "":
                    try:
                        self.screen.blit(self.img, (self.CENTER_X-self.img.get_width()//2,self.CENTER_Y-self.img.get_height()//2))
                    except:
                        pass
                pygame.display.update()
        
                file_time = os.path.getctime(self.img_path)
                if last_time < file_time:
                    print("got a more recent pic")
                    try:
                        self.img = pygame.image.load(self.img_path)
                    except:
                        pass
                    last_time = file_time
            except KeyboardInterrupt:
                
                pygame.quit()
                
                break
            time.sleep(0.5)
        
        
    
    def start(self):
        self.display_poll()

if __name__ == '__main__':
    display_controller = DisplayController()
    display_controller.start()
