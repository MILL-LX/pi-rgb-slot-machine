from enum import Enum
import random
import time

from PIL import Image, ImageDraw, ImageFont

from display import Display
import util

def load_words(word_file_path='./data/happy_words.txt'):
    with open(word_file_path, 'r') as word_file:
        words = word_file.readlines()
    word_list = [word.rstrip('\n').upper() for word in words if len(word) == 5]
    return word_list


State = Enum('State', ['IDLE', 'RUNNING'])

class SlotMachine:
    def __init__(self, display: Display) -> None:
        print(f'Making a SlotMachine for a display with {display.num_panels} panels.')
        self.display = display
        self.words = load_words()
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

        self.display.clear()

        # panel_images = util.test_images_for_display(self.display) 
        current_word = random.choice(self.words)
        words_minus_current_word = [word for word in self.words if word  != current_word]
        final_panel_images = [self.panel_image(c) for c in current_word]

        for i in range(101):
            current_word = random.choice(words_minus_current_word)
            panel_images = [self.panel_image(c) for c in current_word]
            display_image = util.display_image_from_panel_images(panel_images)
            self.display.setImage(display_image, x_offset=0, y_offset=0)

            # Rotate the array of panel images
            # panel_images = panel_images[-1:] + panel_images[:-1]
            time.sleep(0.03)

        display_image = util.display_image_from_panel_images(final_panel_images)

        print(f'cycle done')
        self.state = State.IDLE

