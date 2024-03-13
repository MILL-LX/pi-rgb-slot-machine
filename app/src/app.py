import sys
import time

from display import Display
from util import test_image_for_display

def main():
    display = Display()
    test_image = test_image_for_display(display, 2)
    display.setImage(test_image)

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == "__main__":
    main()