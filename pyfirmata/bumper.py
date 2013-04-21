#!/usr/bin/python
import pyfirmata #pt legatura cu Arduino # Creeaza un obiect Arduino pe portul specificat 
board = pyfirmata.Arduino('/dev/ttyACM0') #Pinii Arduino pt motoare (ca variabile) 
PIN_stanga_inainte = board.get_pin('d:5:p') #pinul digital 5 = pwm 
PIN_stanga_inapoi = board.get_pin('d:3:p') 
PIN_dreapta_inainte = board.get_pin('d:6:p') 
PIN_dreapta_inapoi = board.get_pin('d:9:p') # Pornim un thread Iterator care sa se ocupe de datele pe serial (pt analog) 
it = pyfirmata.util.Iterator(board) 
it.start() 
board.analog[0].enable_reporting() 
#A0 va trimite date 
#Primele date citite pot fi eronate si le ignor 
while board.analog[0].read() is None:
        pass
def mergi(stanga, dreapta): 
#functie pt controlul motoarelor(0..255)    
    if(stanga > 0):      
	    PIN_stanga_inapoi.write(0)      
	    PIN_stanga_inainte.write(stanga/255.0) 
	    #aici se opereaza in #0..1    
    else:      
	    PIN_stanga_inapoi.write(-stanga/255.0)      
	    PIN_stanga_inainte.write(0)    
	    if(dreapta > 0):      
	        PIN_dreapta_inapoi.write(0)      
	        PIN_dreapta_inainte.write(dreapta/255.0)    
	    else:      
	        PIN_dreapta_inapoi.write(-dreapta/255.0)      
	        PIN_dreapta_inainte.write(0) 
print 'Am pornit!' 
try:    
	while (1):      
	    if(board.analog[0].read() * 1024 < 400 ):
	       mergi(255,255) #inainte      
	    else:           
	        print 'Obstacol!'           
	        mergi(180,-180) 
	        #dreapta           
	        board.pass_time(0.8) 
	#timpul trebuie recalibrat pt 
	#90grade.
except: 
	#daca se intrerupe programul (Ctrl-C)  
	mergi(0,0) #stop motoare  
        board.exit() 
	#inchide pyFirmata, inclusiv Iteratorul
