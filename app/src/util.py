import subprocess

from PIL import Image, ImageDraw

from display import Display

##############################################################################################
# Startup Functions
##############################################################################################
def has_active_network_interface():
    try:
        # Run 'ip' command to list network interfaces
        result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)

        # Check if the command succeeded and if there's any network interface listed
        return result.returncode == 0 and len(result.stdout.strip()) > 0
    except Exception as e:
        print("Error occurred while checking for active network interface:", e)
        return False

##############################################################################################
# Testing Functions
##############################################################################################
def test_image_for_panel(display: Display, fill_color: tuple[int, int, int]):
    panel_width = display.width() // display.num_panels
    panel_height = display.height()

    image = Image.new("RGB", (panel_width, panel_height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, panel_width, panel_height), fill=fill_color)

    return image 

def test_images_for_display(display: Display):
    colors = [(255,0,0), (0,255,0),(0,0,255),(255,255,255)] # TODO - dynamically generate base on num_panels
    # colors = [(255,0,0), (255,0,0), (255,0,0), (255,0,0)] # TODO - dynamically generate base on num_panels
    panel_images = [test_image_for_panel(display, colors[panel_number]) for panel_number in range(display.num_panels)]
    return panel_images

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

##############################################################################################
# Word List Utility Functions
##############################################################################################
def load_words(word_file_path):
    with open(word_file_path, 'r') as word_file:
        words = word_file.readlines()
    word_list = [word.rstrip('\n').upper() for word in words if len(word) == 5]
    return word_list
