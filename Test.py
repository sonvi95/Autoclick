import threading
import mouse
import keyboard

a = mouse.MoveEvent(1,1,12)
print(type(a))
if type(a) is mouse._mouse_event.MoveEvent:
    print(a)