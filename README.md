rasphack-watchout
=================

   "Watch Out!" ~ Project for Raspberry Hackathon 2013.
   The main purpose of the project is to detect human activity in an area and take user defined actions on different situations.
   It may notify the owner, enable an alarm, inform the police or even perform mechanical actions on the humans identified. 
   
   It is based on image processing and face recognition done with Raspberry Pi development board. As the main library, OpenCV is used for doing all the heavy-lifting.
   The mechanical part is linked to an Arduino development board. The communication between Raspberry PI and Arduino is done via SPI.
   The Arduino development board can control different analogic senzors, motors, actuators, GSM-GPRS device. 
   
   
   Usage: python pyfirmata/facedetect --cascade face.xml 0

