from enum import Enum
import time

from PIL import Image, ImageDraw, ImageFont

from display import Display
import util

State = Enum('State', ['IDLE', 'RUNNING'])

class SlotMachine:
    def __init__(self, display: Display) -> None:
        print(f'Making a SlotMachine for a display with {display.num_panels} panels.')
        self.display = display
        self.state = State.IDLE

    def panel_image(self, character: str):
        display = self.display
        
        panel_width = display.width() // display.num_panels
        panel_height = display.height()

        image = Image.new("RGB", (panel_width, panel_height))
        draw = ImageDraw.Draw(image)

        font_size = min(panel_width, panel_height) // 3
        font = ImageFont.load_default()  # You can use a different font if you prefer
    
        text_width = draw.textlength(character, font=font)
        text_height = font_size
        
        x = (panel_width - text_width) // 2
        y = (panel_height - text_height) // 2
    
        draw.text((x, y), character, fill="white", font=font)

        return image

    
    def kick(self):
        self.state = State.RUNNING
        print(f'received kick signal')

        # panel_images = util.test_images_for_display(self.display) # TODO - replace with a call to generate panels for each animation frame      
        panel_images = [self.panel_image(c) for c in "MILL"]

        for i in range(10):
            display_image = util.display_image_from_panel_images(panel_images)
            self.display.setImage(display_image, x_offset=0, y_offset=0)

            # Rotate the array of panel images
            panel_images = panel_images[-1:] + panel_images[:-1]
            time.sleep(1)

        time.sleep(30)
        self.display.clear()
        print(f'cycle done')
        self.state = State.IDLE

