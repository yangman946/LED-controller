import numpy as np
from PIL import ImageGrab
from utils import utilities
import asyncio
from tapo import ApiClient

class screen:
    def __init__(self, creds, s=1):
        self.c = creds
        self.U = utilities.Utils()
        self.sensitivity = s # how sensitive our audio is: greater s = greater sensitive
        self.tasks = []
        self.quit_event = asyncio.Event()
        self.client = ApiClient(self.c[0], self.c[1])

    def close(self):
        print("QUITTING")
        self.quit_event.set()
        for task in self.tasks:
            task.cancel()
        
        #self.A.close()
        self.tasks = []
        
        return
    
    def updateS(self, s):
        self.sensitivity = s

    async def start(self):
        self.quit_event = asyncio.Event()
        for i in self.c[2]:
            print(f"IP WORKING = {i}")
            #self.Proc = asyncio.create_task(self.main(i))
            self.tasks.append(asyncio.create_task(self.main(i)))
            
            #self.A.close()

        try:
            await asyncio.gather(*self.tasks)
        except asyncio.CancelledError:
            pass

    def average_color_and_brightness(self):
        # Capture the screen image
        b = (3010, 10, 4907, 1055)
        screen = ImageGrab.grab(b, all_screens=True)

        # Convert the image to numpy array for faster processing
        screen_np = np.array(screen)

        # Calculate average brightness
        brightness = np.mean(screen_np) * self.sensitivity

        # Calculate average color
        average_color = np.mean(screen_np, axis=(0, 1))

        # Convert average color from RGB to HSL
        average_color_hsl = self.U.rgb_to_hsl(average_color)

        # Map hue to a range between 0 and 100
        average_color_hsl = list(average_color_hsl)
        average_color_hsl[0] *= 360
        average_color_hsl[1] = max(1, min(100, average_color_hsl[1] * 100))

        return brightness, average_color_hsl

    async def main(self, ip):

        print("Turning device on...")

        try:
            device = await self.client.l900(ip)
            await device.on()
        except:
            return


        while not self.quit_event.is_set():
            try:
                brightness, (hue, saturation, _) = self.average_color_and_brightness()
                print("Average brightness:", brightness)
                print("Average color (HSL):", hue, saturation)

                brightness = max(1, min(10, brightness))
                hue = max(1, min(360, hue))

                # Set LED color
                await device.set_brightness(int(brightness))
                await device.set_hue_saturation(int(hue), int(saturation))

                # Add a delay to prevent excessive API requests
                await asyncio.sleep(0.5)  # Adjust the delay as needed
            except asyncio.CancelledError:
                break  # Exit the loop if cancelled

