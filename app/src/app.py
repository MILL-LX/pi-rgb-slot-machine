import argparse
import sys
import time

from display import Display
from slot_machine import SlotMachine
import util

def parse_arguments():
    parser = argparse.ArgumentParser(description="Raspbetty Pi LED Matrix Slot Machine")
    parser.add_argument("--test-display", action="store_true", help="Test the display panel")
    parser.add_argument("--slot-machine", action="store_true", help="Run the slot machine")
    parser.add_argument("--num-panels", type=int, default=2, help="number of display panels")
    return parser.parse_args()

def run_display_test(display, num_panels):
    panel_images = util.test_images_for_display(display, num_panels=num_panels) # TODO - replace with a call to generate panels for each animation frame      

    while True:
        try:
            display_image = util.display_image_from_panel_images(panel_images)
            display.setImage(display_image, x_offset=0, y_offset=0)

            panel_images = panel_images[::-1]
            time.sleep(0.2)
        except KeyboardInterrupt:
            sys.exit(0)

def run_slot_machine(display, num_panels):
    machine = SlotMachine(display, num_panels=num_panels)
    pass

def main():
    args = parse_arguments()

    display = Display()

    if args.test_display: 
        run_display_test(display, num_panels=args.num_panels)
    elif args.slot_machine:
        run_slot_machine(display, num_panels=args.num_panels)
    else:
        print(f'KTHXBye')


if __name__ == "__main__":
    main()