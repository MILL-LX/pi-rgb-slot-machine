from enum import Enum
import time

from display import Display

State = Enum('State', ['IDLE', 'RUNNING'])

class SlotMachine:
    def __init__(self, display: Display) -> None:
        print(f'Making a SlotMachine for a display with {display.num_panels} panels.')
        self.state = State.IDLE
    
    def kick(self):
        self.state = State.RUNNING
        print(f'received kick signal')
        time.sleep(10)
        print(f'cycle done')
        self.state = State.IDLE
