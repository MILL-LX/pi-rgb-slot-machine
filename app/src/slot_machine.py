from enum import Enum
import random
import time

from PIL import Image, ImageDraw, ImageFont

from display import Display
from emoji import emoji_list
import image_util
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
        font_size = min(self.panel_width * 0.8, self.panel_height)
        self.emoji_font = ImageFont.truetype(font_path, size=font_size)

        self.words = util.load_words('./data/happy_words.txt')
        self.display_images_for_words = self.make_display_images_for_words()

        self.winning_words = util.load_words('data/winning_words.txt')

        self.display_images_for_emoji, self.emoji_quartets = self.make_display_images_for_emoji()
        
        self.state = State.IDLE

    def panel_image(self, character: str, font: ImageFont, text_color: tuple[int,int,int]):
        image = Image.new("RGB", (self.panel_width, self.panel_height))
        draw = ImageDraw.Draw(image)
    
        text_width = draw.textlength(character, font=font)

        text_bbox = draw.textbbox((0, 0), character, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]


        x = (self.panel_width - text_width) // 2
        y = (self.panel_height - text_height) // 2
    
        draw.text((x, y), character, fill=text_color, font=font)

        return image

    def make_display_images_for_words(self):
        words = self.words[:]
        random.shuffle(words)

        display_images = {}
        for word in words:
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            panel_images = [self.panel_image(c, self.word_font, (r,g,b)) for c in word]
            if not display_images.get(word):
                display_images[word] = image_util.display_image_from_panel_images(panel_images)

        return display_images
    
    def make_display_images_for_emoji(self):
        words_to_emoji_ratio = len(self.words) // (len(emoji_list) // self.display.num_panels)
        shuffled_emoji = emoji_list[:] * words_to_emoji_ratio
        random.shuffle(shuffled_emoji)
        emoji_quartets = [''.join(shuffled_emoji[i:i+4]) for i in range(0, len(shuffled_emoji), self.display.num_panels)]

        display_images = {}
        for quartet in emoji_quartets:
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            panel_images = [self.panel_image(c, self.emoji_font, (r,g,b)) for c in quartet]
            if not display_images.get(quartet):
                display_images[quartet] = image_util.display_image_from_panel_images(panel_images)

        return display_images, emoji_quartets

    def kick(self):
        self.state = State.RUNNING
        print(f'received kick signal')

        self.display.clear()

        final_word_index = random.randint(0, len(self.words) - 1)
        final_word = self.words[final_word_index]
        final_display_image = self.display_images_for_words[final_word]

        display_images = list(self.display_images_for_words.values())
        display_images.extend(self.display_images_for_emoji.values())
        random.shuffle(display_images)

        iterations = min(100, len(self.display_images_for_words))
        for display_image in display_images[:iterations]:
            self.display.setImage(display_image, x_offset=0, y_offset=0)
            time.sleep(0.1)
        self.display.setImage(final_display_image, x_offset=0, y_offset=0)

        # DEBUG - test by always adding the current word to the winning word list
        # self.winning_words.append(final_word)

        flash_delay = 0.08
        if final_word in self.winning_words:
            time.sleep(flash_delay)
            for flash_color in [(255,0,0),(0,255,0),(0,0,255),(255,255,255)] * 5:
                self.display.fill(flash_color)
                time.sleep(flash_delay)
                self.display.setImage(final_display_image, x_offset=0, y_offset=0)
                time.sleep(flash_delay)

        self.display.setImage(final_display_image, x_offset=0, y_offset=0)
                
        print(f'cycle done')
        self.state = State.IDLE

