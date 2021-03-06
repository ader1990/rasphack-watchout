#!/usr/bin/python
import pyfirmata #pt legatura cu Arduino # Creeaza un obiect Arduino pe portul specificat 
import random
import time
board = pyfirmata.Arduino('/dev/ttyACM0') #Pinii Arduino pt motoare (ca variabile) 
PIN_stanga_inainte = board.get_pin('d:5:p') #pinul digital 5 = pwm 
PIN_stanga_inapoi = board.get_pin('d:3:p') 
PIN_dreapta_inainte = board.get_pin('d:6:p') 
PIN_dreapta_inapoi = board.get_pin('d:9:p') # Pornim un thread Iterator care sa se ocupe de datele pe serial (pt analog) 
left=0;
right=0;
max_speed=900.0;

def mergi(stanga, dreapta): 
    if(stanga > 0):      
	    PIN_stanga_inapoi.write(0)      
	    PIN_stanga_inainte.write(stanga/max_speed) 
    else:      
	    PIN_stanga_inapoi.write(-stanga/max_speed)      
	    PIN_stanga_inainte.write(0)    
	    if(dreapta > 0):      
	        PIN_dreapta_inapoi.write(0)      
	        PIN_dreapta_inainte.write(dreapta/max_speed)    
	    else:      
	        PIN_dreapta_inapoi.write(-dreapta/max_speed)      
	        PIN_dreapta_inainte.write(0) 
#while (1):      
#    if(random.random()  < 0.5):
#        left+=random.random()*150/10;
#        mergi(-left,-left) #inainte
#        time.sleep(0.001)
#    else:           
#        right+=random.random()*150/10;
#        mergi(-right, right) #inainte
#        time.sleep(0.001)

