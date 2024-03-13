from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageDraw
import time

class Matrix:
    def __init__(self) -> None:
        self.brightness = 25
        self.fill_status = False
        self.zone_status = False
        self.border_status = False
        self.zone = 0
        self.currentColor = (0,0,0)

        self.options = RGBMatrixOptions()
        self.options.brightness = 25
        self.options.rows = 16
        self.options.cols = 32
        self.options.chain_length = 2
        self.options.parallel = 3
        # self.options.chain_length = 1
        # self.options.parallel = 1
        self.options.multiplexing = 4
        self.options.disable_hardware_pulsing = True #do not change!!!
        self.options.hardware_mapping = 'regular'
        self.options.drop_privileges=False
        # self.options.show_refresh_rate = True
        # self.options.pwm_bits=7
        # self.options.pwm_lsb_nanoseconds = 130
        # self.options.limit_refresh_rate_hz = 250
        self.matrix = RGBMatrix(options = self.options)

    def lightZone(self, rgb: tuple[int, int, int], zone: int) -> None:
        self.matrix.Clear()
        self.image = Image.new("RGB", (self.matrix.height,self.matrix.width))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0,0,int(self.matrix.width/3),self.matrix.height), fill=(rgb[0],rgb[1],rgb[2]))
        self.matrix.SetImage(self.image, zone*self.matrix.width/3, 0)
        self.image.close()

        self.zone_status = True
        self.zone = zone
        self.currentColor = rgb
        self.fill_status = False
        self.border_status = False

    def lightBorder(self, rgb: tuple[int, int, int]) -> None:
        self.matrix.Clear()
        print(f'Matrix width: {self.matrix.width} height: {self.matrix.width}')
        self.image = Image.new("RGB", (self.matrix.width,self.matrix.height))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0,0,int(self.matrix.width)-1,int(self.matrix.height)-1), outline=(rgb[0],rgb[1],rgb[2]), width=1)
        self.matrix.SetImage(self.image)
        self.image.save("image_teste.png", "png")
        self.image.close()

        self.border_status = True
        self.currentColor = rgb
        self.zone_status = False
        self.fill_status = False
    
    def fill(self, rgb: tuple[int, int, int]) -> None:
        self.matrix.Clear()
        self.matrix.Fill(rgb[0],rgb[1],rgb[2])

        self.fill_status = True
        self.currentColor = rgb
        self.zone_status = False
        self.border_status = False

    def clear(self):
        self.zone_status = False
        self.fill_status = False
        self.matrix.Clear()

    def blink(self, rgb: tuple[int, int, int], iterations: int, frequency: float):
        self.matrix.Clear()
        delay = 0.5/frequency
        for i in range(iterations):
            self.matrix.Fill(rgb[0],rgb[1],rgb[2])
            time.sleep(delay)
            self.matrix.Clear()
            time.sleep(delay)

    def applyImage(self, image: Image.Image):
        self.matrix.Clear()
        image.thumbnail((self.matrix.width,self.matrix.height))
        self.matrix.SetImage(image.convert("RGB"))

    def testImage(self, brightness: int):
        self.matrix.Clear()
        self.matrix.brightness = brightness
        test_image = Image.open("pikachu.jpg")
        print(test_image.size)
        #print(self.matrix.height)
        test_image.thumbnail((self.matrix.width,self.matrix.height), resample=Image.ANTIALIAS)
        self.matrix.SetImage(test_image.convert("RGB"))
        test_image.close()

    def setBrightness(self, brightness: int):
        self.brightness = brightness
        self.matrix.brightness = self.brightness
        
        # self.matrix.SetBrightness(brightness)

        if self.fill_status:
            print("New brightness, reloading fill.")
            self.fill(self.currentColor)
        elif self.zone_status:
            print("New brightness, reloading zone.")
            self.lightZone(self.currentColor, self.zone)
        elif self.border_status:
            print("New brightness, reloading border")
            self.lightBorder(self.currentColor)

    def clear(self):
        self.matrix.Clear()