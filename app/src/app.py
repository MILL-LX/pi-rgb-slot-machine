import argparse
import sys
import time

from flask import Flask

from display import Display
from slot_machine import SlotMachine, State
import util

def parse_arguments():
    parser = argparse.ArgumentParser(description="Raspbetty Pi LED Matrix Slot Machine")
    parser.add_argument("--test-display", action="store_true", help="Test the display panel")
    parser.add_argument("--slot-machine", action="store_true", help="Run the slot machine")
    parser.add_argument("--num-panels", type=int, default=2, help="number of display panels")
    return parser.parse_args()

def run_display_test(display):
    panel_images = util.test_images_for_display(display) # TODO - replace with a call to generate panels for each animation frame      

    while True:
        try:
            display_image = util.display_image_from_panel_images(panel_images)
            display.setImage(display_image, x_offset=0, y_offset=0)

            panel_images = panel_images[::-1]
            time.sleep(0.2)
        except KeyboardInterrupt:
            sys.exit(0)

def run_slot_machine(display):
    machine = SlotMachine(display)

    app = Flask(__name__)
    @app.route('/kick', methods=['GET'])
    def kick():
        # TODO - consider async implementation
        if machine.state == State.IDLE:
            machine.kick()
            return 'SlotMachine was kicked successfully'
        else:
            return 'SlotMachine is busy'
        

    app.run(host='0.0.0.0', port=80)


def main():
    args = parse_arguments()

    display = Display(args.num_panels)

    if args.test_display: 
        run_display_test(display)
    elif args.slot_machine:
        run_slot_machine(display)
    else:
        print(f'KTHXBye')

if __name__ == "__main__":
    main()