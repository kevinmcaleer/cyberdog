from plasma import plasma2040, WS2812
from pimoroni import RGBLED
from time import sleep 
from fonts import *
import math

class Led_array:
    lights_per_col = 36
    columns = 8
    NUM_LEDS = lights_per_col * columns
    hue = 1.0
    saturation = 0.25
    brightness = 0.25
    FPS = 60
    speed = 10
    led_strip = WS2812(NUM_LEDS, 0,0, plasma2040.DAT)
    led_strip.start(FPS)
    offset = 0
    gap = 2

    def hsv2rgb(self, hue, sat, val):
        """ Returns the RGB of Hue Saturation and Brightness values """
    
        i = math.floor(hue * 6)
        f = hue * 6 - i
        p = val * (1 - sat)
        q = val * (1 - f * sat)
        t = val * (1 - (1 - f) * sat)

        offset = 0

        r, g, b = [
            (val, t, p),
            (q, val, p),
            (p, val, t),
            (p, q, val),
            (t, p, val),
            (val, p, q),
        ][int(i % 6)]
        r = int(r*255)
        g = int(g*255)
        b = int(b*255)
        
        return r, g, b
    
    def rgb2hsv(self, r:int, g:int, b:int):
        """ Returns the Hue Saturation and Value of RGB values """
        h = 0
        s = 0
        v = 0
        # constrain the values to the range 0 to 1
        r_normal, g_normal, b_normal,  = r / 255, g / 255, b / 255
        cmax = max(r_normal, g_normal, b_normal)
        cmin = min(r_normal, g_normal, b_normal)
        delta = cmax - cmin
        
        # Hue calculation
        if(delta ==0):
            h = 0
        elif (cmax == r_normal):
            h = (60 * (((g_normal - b_normal) / delta) % 6))
        elif (cmax == g_normal):
            h = (60 * (((b_normal - r_normal) / delta) + 2))
        elif (cmax == b_normal):
            h = (60 * (((r_normal - g_normal) / delta) + 4))
        
        # Saturation calculation
        if cmax== 0:
            s = 0
        else:
            s = delta / cmax
            
        # Value calculation
        v = cmax

        return h, s, v 
    
    def clear(self):
        for col in range(self.columns+1):
            for row in range(7):
                self.set_pixel_rgb(col, row, 0, 0, 0)

    def set_pixel_rgb(self,y,x, r,g,b):
        """ Set the pixel at x,y to the current colour """

        # work out if row is odd or even
        if x % 2 == 0: # even
            position = y + ((x* self.lights_per_col)) 
        else: # odd
            position = (((x+1)* (self.lights_per_col)) - y )-1 
        self.led_strip.set_rgb(position,r,g,b)

    def set_pixel_hsv(self, x,y, h,s,v):
        """ Set the pixel at x,y to the current colour """

         # work out if row is odd or even
        if x % 2 == 0: # even
            position = y + ((x* self.lights_per_col))
        else: # odd
            position = (((x+1)* (self.lights_per_col)) - y )-1 # This works but is back to front
        self.led_strip.set_hsv(position,h,s,v)   

    def display_character_old (self, character,pos):
        print(f'character: {character}')
        r,g,b = self.hsv2rgb(self.hue, self.saturation, self.brightness)
        for row in range(0,5):
            length = len(character[0])

            for col in range (0,length):
                x = col+self.offset+pos
                y = row+1
                
                # clear gap
                if x+1 < self.lights_per_col and x+1 > -1:
                    self.set_pixel_rgb(x+1, y, 0, 0, 0)
                
                # write pixel
                if x < self.lights_per_col and x > -1:
                    if character[row][col] == '1':
                        self.set_pixel_rgb(x, y, r, g, b)
                        
                    else:
                        self.set_pixel_rgb(x, y, 0, 0, 0)
        
        self.offset += len(character[0]) + self.gap
       
    def display_character(self, character,x_pos, scale=2):
        font_height = 5
        r,g,b = self.hsv2rgb(self.hue, self.saturation, self.brightness)

        # Get the length of this character (characters can be different widths)
        char_width = len(character[0])

        # Work our way though the character rows
        for current_row in range(0, (font_height) * scale):
            
            # Work our way though the character columns
            for current_col in range (0, char_width):

                #  set the x and y position of the pixel to light up
                x = current_col + self.offset + x_pos
                y = current_row 

                # clear previously lit pixel
                if x +1 < self.columns and x +1 > -1:
                    self.set_pixel_rgb(x+1, y, 0, 0, 0)
                
                # write the new pixel
                if x < self.columns and x > -1:
                    actual_row = (current_row // scale) 
                    print(f'actual_row: {actual_row}, x: {x}, y: {y}, current_row: {current_row}, current_col: {current_col}, pixel: {character[actual_row][current_col]}')
                    if character[actual_row][current_col] == '1':
                        self.set_pixel_rgb(x, y, r, g, b)
                    else:
                        self.set_pixel_rgb(x, y, 0, 0, 0)
                    if character[actual_row][current_col] == '1':
                        self.set_pixel_rgb(x, y, r, g, b)    # Draw the pixel
                    else:
                        self.set_pixel_rgb(x, y, 0, 0, 0)    # Clear the pixel
            sleep(0.01)    
        
        # move the offset along by the width of the character + the gap
        self.offset += char_width + self.gap
    
    def show_message(self, message, position, hue:None):
        """ Shows the message on the display, at the
            position provided, using the Hue value
            specified """
        if hue is None:
            hue = 1.0
        self.hue = hue    
        for character in message:
            print(character)
            if character == 'a':
                self.display_character(a, position)
            if character == 'b':
                self.display_character(b, position)
            if character == 'c':
                self.display_character(c, position)
            if character == 'd':
                self.display_character(d, position)
            if character == 'e':
                self.display_character(e, position)
            if character == 'f':
                self.display_character(f, position)
            if character == 'g':
                self.display_character(g, position)
            if character == 'h':
                self.display_character(h, position)
            if character == 'i':
                self.display_character(i, position)
            if character == 'j':
                self.display_character(j, position)
            if character == 'k':
                self.display_character(k, position)
            if character == 'l':
                self.display_character(l, position)
            if character == 'm':
                self.display_character(m, position)
            if character == 'n':
                self.display_character(n, position)
            if character == 'o':
                self.display_character(o, position)
            if character == 'p':
                self.display_character(p, position)
            if character == 'q':
                self.display_character(q, position)
            if character == 'r':
                self.display_character(r, position)
            if character == 's':
                self.display_character(s, position)
            if character == 't':
                self.display_character(t, position)
            if character == 'u':
                self.display_character(u, position)
            if character == 'v':
                self.display_character(v, position)
            if character == 'w':
                self.display_character(w, position)
            if character == 'x':
                self.display_character(x, position)
            if character == 'y':
                self.display_character(y, position)
            if character == 'z':
                self.display_character(z, position)
            if character == ' ':
                self.display_character(space, position)
            if character == '1':
                self.display_character(one, position)
            if character == '2':
                self.display_character(two, position)
            if character == '3':
                self.display_character(three, position)
            if character == '4':
                self.display_character(four, position)
            if character == '5':
                self.display_character(five, position)
            if character == '6':
                self.display_character(six, position)
            if character == '7':
                self.display_character(seven, position)
            if character == '8':
                self.display_character(eight, position)
            if character == '9':
                self.display_character(nine, position)
            if character == '0':
                self.display_character(zero, position)
            if character == '.':
                self.display_character(fullstop, position)
            if character == '@':
                self.display_character(at, position)
            if character == '!':
                self.display_character(exclaimation, position)
            if character == '#':
                self.display_character(pound, position)
            if character == '"':
                self.display_character(speech, position)
            if character == '$':
                self.display_character(dollar, position)
            if character == '%':
                self.display_character(percentage, position)
            if character == '&':
                self.display_character(amplesand, position)
            if character == '(':
                self.display_character(left_bracket, position)
            if character == ')':
                self.display_character(right_bracket, position)
            if character == '?':
                self.display_character(question, position)
            if character == '^':
                self.display_character(carat, position)
            if character == '_':
                self.display_character(underscore, position)
            if character == '<':
                self.display_character(left_arrow, position)
            if character == '>':
                self.display_character(right_arrow, position)
            if character == '/':
                self.display_character(forward_slash, position)
            if character == '\\':
                self.display_character(back_slash, position)
            if character == '=':
                self.display_character(plus, position)
            if character == '-':
                self.display_character(minus, position)
            if character == ':':
                self.display_character(colon, position)
            if character == ';':
                self.display_character(semicolon, position)
            if character == '=':
                self.display_character(equals, position)
            if character == '~':
                self.display_character(tilde, position)
            if character == "'":
                self.display_character(single_quote, position)
            if character == '|':
                self.display_character(pipe, position)
            if character == 'A':
                self.display_character(A, position)
            if character == 'B':
                self.display_character(B, position)
            if character == 'C':
                self.display_character(C, position)
            if character == 'D':
                self.display_character(D, position)
            if character == 'E':
                self.display_character(E, position)
            if character == 'F':
                self.display_character(F, position)
            if character == 'G':
                self.display_character(G, position)
            if character == 'H':
                self.display_character(H, position)
            if character == 'I':
                self.display_character(I, position)
            if character == 'J':
                self.display_character(J, position)
            if character == 'K':
                self.display_character(K, position)    
            if character == 'L':
                self.display_character(L, position)
            if character == 'M':
                self.display_character(M, position)
            if character == 'N':
                self.display_character(N, position)
            if character == 'O':
                self.display_character(O, position)
            if character == 'P':
                self.display_character(P, position)
            if character == 'Q':
                self.display_character(Q, position)
            if character == 'R':
                self.display_character(R, position)
            if character == 'S':
                self.display_character(S, position)
            if character == 'T':
                self.display_character(T, position)
            if character == 'U':
                self.display_character(U, position)
            if character == 'V':
                self.display_character(V, position)
            if character == 'W':
                self.display_character(W, position)
            if character == 'X':
                self.display_character(X, position)
            if character == 'Y':
                self.display_character(Y, position)
            if character == 'Z':
                self.display_character(Z, position)
            if character == '}':
                self.display_character(smiley, position)
                
        self.offset = 0