from PIL import Image, ImageDraw

from display import Display

##############################################################################################
# Testing Functions
##############################################################################################
def test_image_for_panel(display: Display, num_panels: int, fill_color: tuple[int, int, int]):
    panel_width = display.width() // num_panels
    panel_height = display.height()

    image = Image.new("RGB", (panel_width, panel_height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, panel_width * panel_width, panel_height), fill=fill_color)

    return image 

def test_images_for_display(display: Display, num_panels: int):
    colors = [(255,0,0), (0,255,0),(0,0,255),(255,255,255)] # TODO - dynamically generate base on num_panels
    panel_images = [test_image_for_panel(display, num_panels, colors[panel_number]) for panel_number in range(num_panels)]
    return panel_images

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

##############################################################################################
# Image Utility Functions
##############################################################################################
def display_image_from_panel_images(panel_images):
    num_panels = len(panel_images)

    if num_panels == 0:
        raise ValueError("panel_images is empty")

    panel_width, panel_height = panel_images[0].size

    display_image = Image.new("RGB", (num_panels * panel_width, panel_height))

    current_x = 0
    for panel_image in panel_images:
        display_image.paste(panel_image, (current_x, 0))
        current_x += panel_width

    return display_image

