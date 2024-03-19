import argparse
import sys
import time

from flask import Flask

from display import Display
from slot_machine import SlotMachine, State
import image_util
import util

def parse_arguments():
    parser = argparse.ArgumentParser(description="Raspbetty Pi LED Matrix Slot Machine")
    parser.add_argument("--test-display", action="store_true", help="Test the display panel")
    parser.add_argument("--slot-machine", action="store_true", help="Run the slot machine")
    parser.add_argument("--num-panels", type=int, default=4, help="number of display panels")
    return parser.parse_args()

def run_display_test(display, seconds:int=0, check_network:bool=False):
    panel_images = image_util.test_images_for_display(display) # TODO - replace with a call to generate panels for each animation frame      

    start_time = time.time()
    while True:
        try:
            display_image = image_util.display_image_from_panel_images(panel_images)
            display.setImage(display_image, x_offset=0, y_offset=0)

            # display_image.save("image_teste.png", "png")
            # display_image.close()

            # Rotate the array of panel images
            panel_images = panel_images[-1:] + panel_images[:-1]
            time.sleep(0.1)


            # We stop if we are checking for a network connection and we have one.
            # Otherwise, we respect the time limit and stop if the specified seconds have elapsed.
            if check_network and util.has_active_network_interface():
                return
            elif seconds > 0:
                elapsed = time.time() - start_time
                if elapsed > seconds:
                    return
            
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
        run_display_test(display, seconds=10, check_network=True)
        run_slot_machine(display)
    else:
        print(f'KTHXBye')

if __name__ == "__main__":
    main()