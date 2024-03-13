from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

class Display:
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

    def width(self):
        return self.matrix.width
    
    def height(self):
        return self.matrix.height

    def setImage(self, image: Image.Image):
        self.matrix.Clear() 
        self.matrix.SetImage(image.convert("RGB"))

    def setScaledImage(self, image: Image.Image):
        scaled_image = image.thumbnail((self.matrix.width,self.matrix.height))
        self.setImage(scaled_image)  

    def clear(self):
        self.matrix.Clear()