from PIL import Image, ImageDraw

from display import Display

def test_image_for_display(display: Display):
    image = Image.new("RGB", (display.matrix.width,display.matrix.height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,int(display.matrix.width)-1,int(display.matrix.height)-1), outline=(255,255,255), width=1)
    return image