
from led_array import Led_array
from time import sleep
from plasma import plasma2040
from pimoroni import Button

button_a = Button(plasma2040.BUTTON_A)
button_b = Button(plasma2040.BUTTON_B)

l = Led_array()

hue = 0.1
saturation = 1.0
brightness = 0.35
# brightness = 1.0
glow_brightness = brightness
speed = 0.01
direction = False

off = False
chaser_num = 0

l.NUM_LEDS = 36*4
flash_count = 0

def cycle():
    # cycle through the colours
    global hue, chaser_num
    
    if chaser_num > l.NUM_LEDS:
        chaser_num = 0

    l.led_strip.set_hsv(chaser_num, hue, saturation, brightness)
    hue += 0.01
    if hue > 1.0:
        hue = 0.0
        
    sleep(speed*2)
    chaser_num += 1
    
def chaser():
    global chaser_num, hue
    
    if chaser_num > l.NUM_LEDS:
        chaser_num = 0
    l.led_strip.set_hsv(chaser_num,hue,saturation,brightness)
    if chaser_num > 0:
        l.led_strip.set_rgb(chaser_num-1,0,0,0)
        
    sleep(speed)
    chaser_num += 1
    hue += 0.001
    if hue > 1.0:
        hue = 0.0

def pulse():
    global hue, chaser_num, glow_brightness, direction
    
    if chaser_num > l.NUM_LEDS:
       chaser_num = 0
       
    if direction:
        for i in range(l.NUM_LEDS):
            l.led_strip.set_hsv(i,hue,saturation,glow_brightness)
            
        sleep(speed)
        glow_brightness += 0.01
        hue += 0.01
        if hue > 1.0:
            hue = 0.0
        if glow_brightness > 0.5:
                direction = False
        
    if not direction:
        for i in range(l.NUM_LEDS):
            l.led_strip.set_hsv(i,hue,saturation,glow_brightness)
            
        sleep(speed)
        glow_brightness -= 0.01
        hue += 0.01
        if hue > 1.0:
            hue = 0.0
        if glow_brightness < 0.0:
                direction = True
            

def rainbow():
    global hue
    
    for i in range(l.NUM_LEDS):
        l.led_strip.set_hsv(i, hue, saturation, brightness)
    hue += 0.01
    if hue > 1.0:
        hue = 0.0
    
    sleep(speed*8)
    
def flash_red():
    global flash_count
    if flash_count == 10:
        for i in range(l.NUM_LEDS):
            r,g,b, = l.hsv2rgb(1,1,0.5)
            l.led_strip.set_rgb(i, r, g, b)
        sleep(0.75)
        flash_count = 0
    else:
        flash_count += 1
        for i in range(l.NUM_LEDS):
            r,g,b, = l.hsv2rgb(1,0,0.0)
            l.led_strip.set_rgb(i, r, g, b)
    
#     sleep(speed/100000)

def red_and_blue():
    global flash_count
    rate = 3
    if flash_count >= rate:
        for i in range(l.NUM_LEDS):
            r,g,b, = l.hsv2rgb(1,1,0.5)
            l.led_strip.set_rgb(i, r, g, b)
        sleep(rate/10)
        flash_count = 0
    else:
        flash_count += 1
        for i in range(l.NUM_LEDS):
            r,g,b, = l.hsv2rgb(0.6,1,0.5)
            l.led_strip.set_rgb(i, r, g, b)


def glow():
    global glow_brightness, hue
    for i in range(l.NUM_LEDS):
        l.led_strip.set_hsv(i,hue,saturation,glow_brightness)
        
    sleep(speed)
    glow_brightness += 0.01
    hue += 0.01
    if hue > 1.0:
        hue = 0.0
    if glow_brightness > 0.5:
        glow_brightness = 0

def black():
    if off:
        for i in range(l.NUM_LEDS):
            l.led_strip.set_hsv(i, 0, 0, 0)
       
        sleep(speed)

def do_led_pattern(led_pattern):
    if led_pattern == 0:
        cycle()
    elif led_pattern == 1:
        chaser()
    elif led_pattern == 2:
        pulse()
    elif led_pattern == 3:
        rainbow()
    elif led_pattern == 4:
        glow()
    elif led_pattern == 5:
        flash_red()
    elif led_pattern == 6:
        red_and_blue() 
    elif led_pattern == 7:
        black()

led_pattern = 0

pattern = {0:'cycle',1:'chaser', 2:'pulse',3:'rainbow',4:'glow',5:'flash_red',6:'red and blue',7:'black'}

while True:
    # Check if buttons are pressed
    if button_a.read():    
        led_pattern += 1
        if led_pattern > 7:
            led_pattern = 0
        print(f'led_pattern: {led_pattern}, {pattern[led_pattern]}')
    if button_b.read():
        if off:
            off = False
        else:
            off = True
        black()

    if not off:
        do_led_pattern(led_pattern)
#     print(f'hue: {hue}, sat: {saturation}, val: {brightness}')
#     sleep(speed)
