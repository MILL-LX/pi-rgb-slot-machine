import sys
import time

from display import Display
import util

def main():
    display = Display()

    panel_images = util.test_images_for_display(display, num_panels=2) # TODO - replace with a call to generate panels for each animation frame      

    while True:
        try:
            display_image = util.display_image_from_panel_images(panel_images)
            display.setImage(display_image, x_offset=0, y_offset=0)

            panel_images.reverse()
            time.sleep(0.2)
        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == "__main__":
    main()