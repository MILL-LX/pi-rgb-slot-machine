import subprocess

##############################################################################################
# Startup Functions
##############################################################################################
def is_raspberry_pi():
    try:
        with open('/sys/firmware/devicetree/base/model', 'r') as f:
            model = f.read()
            if 'Raspberry Pi' in model:
                return True
    except FileNotFoundError:
        pass
    return False

def has_active_network_interface():
    if not is_raspberry_pi():
        return True
    
    try:
        # Run 'ip' command to list network interfaces
        result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)

        # Check if the command succeeded and if there's any network interface listed
        return result.returncode == 0 and len(result.stdout.strip()) > 0
    except Exception as e:
        print("Error occurred while checking for active network interface:", e)
        return False

##############################################################################################
# Word List Utility Functions
##############################################################################################
def load_words(word_file_path):
    with open(word_file_path, 'r') as word_file:
        words = word_file.readlines()
    word_list = [word.rstrip('\n').upper() for word in words if len(word) == 5]
    return word_list
