from enum import Enum
import time

from display import Display
import util

State = Enum('State', ['IDLE', 'RUNNING'])

class SlotMachine:
    def __init__(self, display: Display) -> None:
        print(f'Making a SlotMachine for a display with {display.num_panels} panels.')
        self.display = display
        self.state = State.IDLE
    
    def kick(self):
        self.state = State.RUNNING
        print(f'received kick signal')

        panel_images = util.test_images_for_display(self.display) # TODO - replace with a call to generate panels for each animation frame      

        for i in range(10):
            display_image = util.display_image_from_panel_images(panel_images)
            self.display.setImage(display_image, x_offset=0, y_offset=0)

            # Rotate the array of panel images
            panel_images = panel_images[-1:] + panel_images[:-1]
            time.sleep(1)

        self.display.clear()
        print(f'cycle done')
        self.state = State.IDLE

