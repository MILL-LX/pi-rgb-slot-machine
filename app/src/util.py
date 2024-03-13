from PIL import Image, ImageDraw

from display import Display

def test_image_for_display(display: Display, num_panels: int):
    image = Image.new("RGB", (display.width(), display.height()))
    draw = ImageDraw.Draw(image)
    
    panel_width = display.width() // num_panels
    panel_height = display.height()
    x = 0
    y = 0

    colors = [(255,0,0), (0,255,0),(0,0,255),(255,255,255)]
    for panel in range(num_panels):
        x = panel_width * panel
        draw.rectangle((x, y, panel_width * panel_width, panel_height), fill=colors[panel])
    return image    