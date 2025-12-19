import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import neopixel

print("=== Starting NeoKey Trinkey ===")

try:
    # Wait for USB to initialize
    time.sleep(1)
    print("USB delay complete")
    
    pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
    print("NeoPixel initialized")
    
    button = digitalio.DigitalInOut(board.SWITCH)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.DOWN  # Changed from Pull.UP
    print("Button configured with Pull.DOWN")
    print(f"Initial button reading: {button.value} (False=not pressed, True=pressed)")
    
    print("Initializing keyboard...")
    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)
    print("Keyboard initialized")
    
    print("=== Ready! Press the button to launch GitHub. ===")
    
    button_pressed = False
    pixel.fill((0, 0, 50))
    print("LED set to blue")
    
except Exception as e:
    print(f"ERROR during setup: {e}")
    import traceback
    traceback.print_exception(e)
    while True:
        time.sleep(1)

print("Entering main loop...")
print(f"Initial button state: {button.value} (False=not pressed, True=pressed)")

try:
    while True:
        # With Pull.DOWN: False = not pressed, True = pressed
        if button.value and not button_pressed:
            button_pressed = True
            print("*** BUTTON PRESSED! ***")
            pixel.fill((0, 255, 0))
            
            try:
                # Step 1: Open Run dialog with Win+R
                print("Opening Run dialog...")
                kbd.press(Keycode.GUI, Keycode.R)
                kbd.release_all()
                time.sleep(0.7)  # Wait for Run dialog
                
                # Step 2: Type "firefox" and press Enter
                print("Launching Firefox...")
                layout.write("firefox")
                time.sleep(0.2)
                kbd.press(Keycode.ENTER)
                kbd.release_all()
                time.sleep(1.5)  # Wait for Firefox to open
                
                # Step 3: Focus address bar with Ctrl+L
                print("Focusing address bar...")
                kbd.press(Keycode.CONTROL, Keycode.L)
                kbd.release_all()
                time.sleep(0.4)
                
                # Step 4: Type GitHub URL and press Enter
                print("Typing GitHub URL...")
                layout.write("https://github.com/MAX-P0W3R") # CHANGE THIS TO YOUR USERNAME
                time.sleep(0.2)
                print("Pressing Enter...")
                kbd.press(Keycode.ENTER)
                kbd.release_all()
                print("*** Command sent! ***")
            except Exception as e:
                print(f"ERROR sending keys: {e}")
            
            time.sleep(0.5)
            pixel.fill((0, 0, 50))
            
        elif not button.value and button_pressed:
            button_pressed = False
            print("Button released.")
        
        time.sleep(0.01)
        
except Exception as e:
    print(f"ERROR in main loop: {e}")
    import traceback
    traceback.print_exception(e)
    while True:
        time.sleep(1)
