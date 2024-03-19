from enum import Enum
import random
import time

from PIL import Image, ImageDraw, ImageFont

from display import Display
from emoji import emoji_list
import util

State = Enum('State', ['IDLE', 'RUNNING'])

class SlotMachine:
    def __init__(self, display: Display) -> None:
        print(f'Making a SlotMachine for a display with {display.num_panels} panels.')
        self.display = display
        self.panel_width = display.width() // display.num_panels
        self.panel_height = display.height()

        font_path = 'fonts/MILL/Canada Type - Screener SC.ttf'
        font_size = min(self.panel_width, self.panel_height)
        self.word_font = ImageFont.truetype(font_path, size=font_size)

        font_path = 'fonts/Noto_Emoji/static/NotoEmoji-Regular.ttf'
        font_size = min(self.panel_width, self.panel_height)
        self.emoji_font = ImageFont.truetype(font_path, size=font_size)

        self.words = util.load_words()
        self.display_images_for_words = self.make_display_images_for_words()
        self.state = State.IDLE

    def panel_image(self, character: str, font: ImageFont, text_color: tuple[int,int,int]):
        image = Image.new("RGB", (self.panel_width, self.panel_height))
        draw = ImageDraw.Draw(image)
    
        text_width = draw.textlength(character, font=font)

        text_bbox = draw.textbbox((0, 0), character, font=font)
        text_height = text_bbox[3] - text_bbox[1]

        x = (self.panel_width - text_width) // 2
        y = (self.panel_height - text_height) // 2
    
        draw.text((x, y), character, fill=text_color, font=font)

        return image

    def make_display_images_for_words(self):
        words = self.words[:]
        random.shuffle(words)

        display_images = []
        for word in words:
            panel_images = [self.panel_image(c, self.word_font, (255,255,255)) for c in word]
            display_images.append(util.display_image_from_panel_images(panel_images))

        return display_images

    def kick(self):
        self.state = State.RUNNING
        print(f'received kick signal')

        self.display.clear()

        display_images = self.display_images_for_words

        for display_image in display_images:
            self.display.setImage(display_image, x_offset=0, y_offset=0)
            time.sleep(0.04)

        print(f'cycle done')
        self.state = State.IDLE

