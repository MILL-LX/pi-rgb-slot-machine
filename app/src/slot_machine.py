from display import Display
from enum import Enum

State = Enum('State', ['IDLE', 'RUNNING'])

class SlotMachine:
    def __init__(self, display: Display, num_panels: int) -> None:
        print(f'Making a SlotMachine for a display with {num_panels} panels.')
        self.state = State.IDLE
    
    def kick():
        print(f'received kick signal')