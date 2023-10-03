import time
import ctypes

# Constants for mouse events
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

# Structure for input event
class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("union", ctypes.POINTER(ctypes.c_uint32))]

# Function to simulate a mouse click
def click(x, y):
    # Set mouse position
    ctypes.windll.user32.SetCursorPos(x, y)

    # Create mouse down event
    input_down = INPUT(0, ctypes.pointer((x << 16) | y))
    input_down.type = MOUSEEVENTF_LEFTDOWN
    ctypes.windll.user32.SendInput(1, ctypes.pointer(input_down), ctypes.sizeof(INPUT))

    # Create mouse up event
    input_up = INPUT(0, ctypes.pointer((x << 16) | y))
    input_up.type = MOUSEEVENTF_LEFTUP
    ctypes.windll.user32.SendInput(1, ctypes.pointer(input_up), ctypes.sizeof(INPUT))

if __name__ == "__main__":
    # Delay before starting the click
    time.sleep(5)

    # Coordinates to click (adjust as needed)
    click_x, click_y = 100, 100

    # Perform the click
    click(click_x, click_y)
