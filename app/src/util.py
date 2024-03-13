from PIL import Image, ImageDraw

from display import Display

def test_image_for_panel(display: Display, num_panels: int, fill_color: tuple[int, int, int]):
    panel_width = display.width() // num_panels
    panel_height = display.height()

    image = Image.new("RGB", (panel_width, panel_height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, panel_width * panel_width, panel_height), fill=fill_color)

    return image 

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