from matrix import Matrix
import sys
import time

myMatrix = Matrix()
color_rgb = None

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(
            "Unexpected number of arguments.\n\nArguments are: 'color' 'brightness' 'delay'."
        )
    else:
        color_string = sys.argv[1]
        bright = sys.argv[2]
        delay = sys.argv[3]
        if not bright.isdigit():
            sys.exit("Invalid brightness value.")
        else:
            bright = int(bright)
        if bright > 255 or bright < 0:
            sys.exit("Invalid brightness value.")
        if color_string == "red":
            color_rgb = (255, 0, 0)
        elif color_string == "green":
            color_rgb = (0, 255, 0)
        elif color_string == "blue":
            color_rgb = (0, 0, 255)
        elif color_string == "white":
            color_rgb = (255, 255, 255)
        elif color_string == "yellow":
            color_rgb = (255, 255, 0)
        else:
            sys.exit("Invalid color value.")
        if not delay.isdigit():
            sys.exit("Invalid delay value.")
        else:
            delay = int(delay)
        try:
            myMatrix.setBrightness(bright)
            while True:
                myMatrix.fill(color_rgb)
                print("on")
                time.sleep(delay)
                myMatrix.clear()
                print("off")
                time.sleep(delay)
        except KeyboardInterrupt:
            sys.exit(0)
