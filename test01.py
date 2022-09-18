from led_array import Led_array
from time import sleep
l = Led_array()

# l.set_pixel_rgb(1,1,255,255,255)
# 
# while True:
#     pass

message = "Hello World. "
hue = 1

# while True:
#     l.set_pixel_rgb(x=1,y=0,r=128,g=128,b=128)

while True or KeyboardInterrupt:
    l.show_message(message,0,hue)
    sleep(1)

while True or KeyboardInterrupt:
    for position in range(l.columns,-len(message*(5+1)),1):
        if hue <=1 or hue == 0:
            hue += 0.01
        else: hue = 0
        
        l.show_message(message, position, hue)
        sleep(0.1)
