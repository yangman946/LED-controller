
import json
import os
import random
import colorsys

class Utils:



    def avg(self, list):
        return sum(list)/len(list)

    def clamp(self, num):
        return min(max(1, num), 360)
    
    def creds(self):
        json_dat = open(f"{os.getcwd()}/config.json")
        self.j = json.load(json_dat)
        return self.j
    
    # visualiser

    def bassDev(self, b, a):
        if b[-1] < 100 and not a:
            return 0
        return random.randint(-int(abs(b[0] - b[-1])), int(abs(b[-0] - b[-1])))/(15 if not a else 2)
    
    def clamp(self, num):
        return min(max(1, num), 360)
    
    def shake(self, a):
        yield(random.randint(-int(a), int(a))/50, random.randint(-int(a), int(a))/50)
        while True:
            yield (0, 0)

    def hue_to_rgb(self, hue):
        """
        Convert hue value (0-360) to RGB color.
        """
        hue %= 360  # Ensure hue is within 0-360 range
        c = 1.0
        x = (1.0 - abs((hue / 60.0) % 2 - 1.0)) * c
        m = 0.0
        r, g, b = 0.0, 0.0, 0.0

        if 0 <= hue < 60:
            r, g, b = c, x, 0
        elif 60 <= hue < 120:
            r, g, b = x, c, 0
        elif 120 <= hue < 180:
            r, g, b = 0, c, x
        elif 180 <= hue < 240:
            r, g, b = 0, x, c
        elif 240 <= hue < 300:
            r, g, b = x, 0, c
        elif 300 <= hue < 360:
            r, g, b = c, 0, x

        return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)
    
    # screen
    def rgb_to_hsl(self, rgb):
        r, g, b = rgb
        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        return h, s, l