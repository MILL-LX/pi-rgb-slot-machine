import util

if util.is_raspberry_pi():
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
else:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
    
from PIL import Image

class Display:
    def __init__(self, num_panels: int, emulate=False) -> None:
        self.num_panels = num_panels
        self.brightness = 25
        self.fill_status = False
        self.zone_status = False
        self.border_status = False
        self.zone = 0
        self.currentColor = (0,0,0)

        self.options = RGBMatrixOptions()
        self.options.brightness = 100
        self.options.rows = 16
        self.options.cols = 32
        self.options.chain_length = 4
        self.options.parallel = 3
        self.options.multiplexing = 4
        self.options.disable_hardware_pulsing = True #do not change!!!
        self.options.hardware_mapping = 'regular'
        self.options.drop_privileges=False
        # self.options.show_refresh_rate = True
        self.options.pwm_bits=4
        # self.options.pwm_lsb_nanoseconds = 130
        self.options.limit_refresh_rate_hz = 250
        self.matrix = RGBMatrix(options = self.options)
        self.matrix.Clear()

    def width(self):
        return self.matrix.width
    
    def height(self):
        return self.matrix.height

    def setImage(self, image: Image.Image, x_offset=0, y_offset=0):
        self.matrix.Clear() 
        self.matrix.SetImage(image.convert("RGB"), x_offset, y_offset, True)

    def setScaledImage(self, image: Image.Image, x_offset=0, y_offset=0):
        scaled_image = image.thumbnail((self.matrix.width,self.matrix.height))
        self.setImage(scaled_image, x_offset=x_offset, y_offset=y_offset)  

    def clear(self):
        self.matrix.Clear()

    def fill(self, color: tuple[int, int, int]):
        self.matrix.Fill(*color)