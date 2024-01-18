from picamera2 import Picamera2, Preview
import time



class CameraController():
    def __init__(self):
        #Camera
        try:
            self.picam = Picamera2()
            self.cam_config = self.picam.create_preview_configuration()
            self.picam.configure(config)
            self.picam.start()
        except Exception as e:
            print(e)
            exit()

        self.picam_image_filename = "camera_imgs/cam_img.jpg"
        


    def camera_poll(self):
        while True:
            try:
                # Take picture
                self.picam.capture_file(self.picam_image_filename)
                print("Picture taken")
            except KeyboardInterrupt:
                break
            time.sleep(0.5)
        
        
    
    def start(self):
        self.camera_poll()

if __name__ == '__main__':
    camera_controller = CameraController()
    camera_controller.start()