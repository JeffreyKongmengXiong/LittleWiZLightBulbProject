import asyncio, time
import cv2
import numpy as np
import pprint

from skimage import io
from pywizlight import wizlight, PilotBuilder
from PIL import ImageGrab
from statistics import mode

def mostFrequent(List):
    counter = 0
    num = List[0] 
      
    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency> counter): 
            counter = curr_frequency 
            num = i 
  
    return num 

def average(List):
    counter = 0
    num = List[0]
    return num

async def main():
    img = io.imread('https://i.stack.imgur.com/DNM65.png')[:, :, :-1]
    average = img.mean(axis=0).mean(axis=0)
    # get light
    light = wizlight("10.0.0.245")
    step = 50
    num_pixel = 1080//step * 1920//step
    img = ImageGrab.grab()
    imgNP = np.array(img)

    im_arr = np.frombuffer(img.tobytes(), dtype=np.uint8)
    im_arr = im_arr.reshape((img.size[1], img.size[0], 3))
    r = g = b = 0
    pixelArray = []
    count = 0
    acount = 0
    totalr = 0
    totalg = 0
    totalb = 0
    totala = 0
    diff = 30
    for y in range(0, 1080, step):
        for x in range(0, 1920, step):
            px = im_arr[y][x]
            if ((px[0] > px[1] + diff) or ((px[0] < px[1] - diff))):
                count += 1
                totalr += px[0]
                totalg += px[1]
                totalb += px[2]
            elif ((px[0] > px[2] + diff) or ((px[0] < px[2] - diff))):
                count += 1
                totalr += px[0]
                totalg += px[1]
                totalb += px[2]
            elif ((px[1] > px[0] + diff) or ((px[1] < px[0] - diff))):
                count += 1
                totalr += px[0]
                totalg += px[1]
                totalb += px[2]
            elif ((px[1] > px[2] + diff) or ((px[1] < px[2] - diff))):
                count += 1
                totalr += px[0]
                totalg += px[1]
                totalb += px[2]
            elif ((px[2] > px[0] + diff) or ((px[2] < px[0] - diff))):
                count += 1
                totalr += px[0]
                totalg += px[1]
                totalb += px[2]
            elif ((px[2] > px[1] + diff) or ((px[2] < px[1] - diff))):
                count += 1
                totalr += px[0]
                totalg += px[1]
                totalb += px[2]
            acount += 1
            totala += (px[0] + px[1] + px[2])/3
    r = totalr / count * 1.2
    if (r > 255):
        r = 255
    g = totalg / count * 1.2
    if (g > 255):
        g = 255
    b = totalb / count * 1.2
    if (b > 255):
        b = 255
    bright = totala / acount * 2.5
    if (bright > 255):
        bright = 255
    # bright = 255
    averageColor = [r, g, b, bright]
    print(averageColor)
    await light.turn_on(PilotBuilder(rgb = (r, g, b)))
    await light.turn_on(PilotBuilder(brightness = bright))

async def listener():
    while True:
        await main()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(listener())
