import machine
import utime
 
 
 
LED = machine.Pin(16, machine.Pin.OUT) # pin 16
button = machine.Pin(20, machine.Pin.IN) #pin 20
on = 1
off = 0 # is used for the output off the led
last_time = utime.ticks_ms()
etat_led = "on" # is uted to discribe the functionning of the led
valeur_bouton=0
add_latence = 0
new_time_before = last_time
while True:
    index = button.value()
   
    new_time = utime.ticks_ms() # utlisation of ticks_ms is lore efficient than time.ns()
    Break = 250/(1+ valeur_bouton) + add_latence
    if index ==1 and new_time-new_time_before > 150:
        valeur_bouton= valeur_bouton+1 #change the state of the process
        new_time_before =new_time # allow us to modife properly the state of the process 
        #because it adds a break after a modification of the process
        add_latence= 250 # to have a latence beetween the transistion
   
    if valeur_bouton == 0 or valeur_bouton == 1:
       
        if etat_led == "off" and new_time-last_time >= Break:
           
            LED.value(on)
            etat_led = "on" # is used to change the state of the led
            last_time = utime.ticks_ms()
            add_latence = 0 # to come back with the initanal break
        elif new_time-last_time >= Break:
            add_latence = 0
            LED.value(off)
            etat_led = "off"
            last_time = utime.ticks_ms()
 
 
       
    elif valeur_bouton == 2:
        LED.value(off)
       
    else :
        valeur_bouton = 0 # to come back to the initial state of the process
