import sys
import time

from display import Display
from util import test_image_for_display

def main():
    display = Display()
    test_image = test_image_for_display(display, num_panels=2)
    display.setImage(test_image, x_offset=0, y_offset=0)

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == "__main__":
    main()