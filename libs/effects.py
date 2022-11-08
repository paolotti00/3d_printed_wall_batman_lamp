import math
import machine
import neopixel
import time
import math
from libs.bpm_reader import BMPReader

# close all pixels
def clear(np):
    n=np.n
    for i in range(n):
        np[i] = (0, 0, 0)
        np.write()


def bounce(np, r, g, b, wait):
    n=np.n
    for i in range(4 * n):
        for j in range(n):
            np[j] = (r, g, b)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(wait)


def cycle(np, r, g, b, wait):
    n=np.n
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (r, g, b)
        np.write()
        time.sleep_ms(wait)

# rainbow effect
def wheel(pos):
    #  Input a value 0 to 255 to get a color value.
    #  The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def rainbow_cycle(np, wait):
    n=np.n
    for j in range(255):
        for i in range(n):
            rc_index = (i * 256 // n) + j
            np[i] = wheel(rc_index & 255)
        np.write()
        time.sleep_ms(wait)


def print_img(np,img_url):
    img = BMPReader(img_url)
    pixel_grid = img.get_pixels()
    i = 0
    for row in range(img.height):
        for col in range(img.width):
            # The Unicorn Hat arranges its pixels starting top-right and alternates
            # back and forth with each row so we need to reverse the even rows
            if row % 2 == 0:
                col = img.width - 1 - col
            np[i] = pixel_grid[row][col]
            i += 1
    write_fade_in(np)

def write_fade_in(np):
    brightness_step_division = [24,22,20,18,16,14,12,10,8,6,4,2,1]
    #iterate step division
    for i, step_division in enumerate (brightness_step_division):
        new_np=neopixel.NeoPixel(np.pin, np.n)
        #print('--------')
        #print("step division = " + str(step_division))
        #iterate original np tuple
        for j,tuple in enumerate(np):
            #print('--------')
            #print("tuple j = "+str(j) + " tuple = " + str(tuple))
            tuple_item_list=[]
            #interate single np tuple element
            for z,tuple_item in enumerate(tuple):
                #print ("tuple_item z = "+str(z) + " item = " + str(tuple_item)) 
                if(tuple_item!=0):
                    tuple_item_list.append(math.ceil(tuple_item/step_division))
                else:
                     tuple_item_list.append(0)
                #print ("tuple_item_list z = "+str(z) + " item = " + str(tuple_item_list[z]))
            new_np[j]=tuple_item_list
            #for x,new_tuple in enumerate(new_np):
                #print("new tuple " + str(new_tuple))
        #print("---------write--------")
        time.sleep_ms(30)
        new_np.write()

