#<----------------------------------->
#Importation of the different librairies
from machine import Pin, I2C, ADC
from utime import sleep
from lcd1602 import LCD1602
from dht20 import DHT20
import machine,utime
#<////////////////////////////////////>
    
#<----------------------------------->
#Configuration of the different sensors, display and other, ...
I2c = I2C(1) # utilisation of the canal I2C (first pin) for the temperature sensor
dht20 = DHT20(I2c)
temperature = dht20.dht20_temperature()
Rotary_sensor = machine.ADC(2)  # it is for the variable resistance
i2c = I2C(0,scl=Pin(9), sda=Pin(8), freq=400000) #parameters of the display
display = LCD1602(i2c, 2, 16)
display.display()
buzzer = machine.PWM(machine.Pin(16)) #parameters of the buzzer
buzzer.freq(1046)
LED = machine.PWM(machine.Pin(18)) #parameters of the LED
LED.freq(1000)  
#<////////////////////////////////////>

#<----------------------------------->
#Initialization of the different set times
# It is used to manage the utlisation of the function
last_time = utime.ticks_ms() 
last_time_delete = last_time
last_time_temp = last_time
last_time_led = last_time
#<////////////////////////////////////>

#<----------------------------------->
#Initialization of the datas which will be incremented or changed
diviseur=1
etat = True
index_alarm = 0
efface = True
index_alarm_position = 0
affiche = True
#<////////////////////////////////////>


#<----------------------------------->
#Utilisation of the different sensors and transformation of the data
def sensors():
    new_time = utime.ticks_ms()
    resistance = Rotary_sensor.read_u16()
    temp=int(resistance/3120.761905)+15 # set the minimum temperature and define the tempertaure in fonction of the resistance
    ref_duty = int(0.9*resistance+6535)
    return new_time,temp,resistance, ref_duty
#<////////////////////////////////////>

#<----------------------------------->
#Function which subtracted the inital time and the currently time
def difference_time(new_time,last_time):
    return new_time-last_time
#<////////////////////////////////////>


#<----------------------------------->
#Function which clears the display
def display_clear(new_time, last_time_delete, efface):
    if 500 < (difference_time(new_time,last_time_delete)):
        display.clear() #clear the display
        last_time_delete = new_time
        efface = True #autorize the display of the alarm
        affiche = True #autorize the display of the ambient temperature
    else :
        affiche = False
    return last_time_delete, efface, affiche
#<////////////////////////////////////>

#<----------------------------------->
#Function which takes the temperature
def take_temperature(last_time_temp, temperature, new_time):
    temperature = dht20.dht20_temperature() #lecture of the temperature sensor
    last_time_temp = new_time
    return temperature, last_time_temp
#<////////////////////////////////////>

#<----------------------------------->
#Function which displays the abient temperature
def Display(affiche, temperature, display):
    if affiche:
        display.setCursor(0,0)
        display.print("Ambient:"+"{:.1f}".format(temperature))
#<////////////////////////////////////>


#<----------------------------------->
#Function which controls the LED
def Led(etat,ref_duty, new_time, last_time_led):
    if etat:
        LED.duty_u16(0)  # shut down the LED    
        etat = False # allow to change the status of the led
    else:
        LED.duty_u16(ref_duty) # intensity of the Led, it uses the PWM
        etat = True
    last_time_led = new_time
    return last_time_led, etat
#<////////////////////////////////////>

#<----------------------------------->
#Function which displays the alarm and controls the buzzer
def display_alarm_set(temperature, temp, efface, display, buzzer, index_alarm_position, index_alarm, resistance, diviseur):
    if temperature >=  int(resistance/3120.761905)+3+15:
        buzzer.duty_u16(12000)
        diviseur = 4 # change the frequence of the led
        if efface: 
            efface = False 
            if index_alarm_position%2==0 : # allow us to blink and move the word ALARM 
                display.setCursor(index_alarm,1) # it is used to move the display
                display.print("ALARM") 
            else :
                index_alarm+=1 #incrmnetation of the display
            if index_alarm ==11 : #it allows us to move to the intital position 
                index_alarm=0
                index_alarm_position+=1
    else :
        buzzer.duty_u16(0) # it is normal condition, no noice and it displays the temperature set
        display.setCursor(0,1)
        display.print("SET:"+"{:.1f}".format(temp))
        diviseur = 1 # change the frequence of the led
    return index_alarm_position, diviseur, efface
#<////////////////////////////////////>


#<----------------------------------->
#Infinty Loop
while True:
    
    new_time,temp,resistance, ref_duty = sensors() # lecture of sensors and transformation of the data
        
    last_time_delete, efface, affiche = display_clear(new_time, last_time_delete, efface) # clear the display


    if 1000 < (difference_time(new_time,last_time_temp)): #lecture of the tempertaure every second
        temperature, last_time_temp = take_temperature(last_time_temp, temperature, new_time)
    

    Display(affiche, temperature, display) # display the ambient temperature

    index_alarm_position, diviseur, efface = display_alarm_set(temperature, temp, efface, display,buzzer, index_alarm_position, index_alarm, resistance, diviseur)# it displays the second part of the display
       
    if 250/diviseur< difference_time(new_time,last_time_led ) : #change the status of the led 
        last_time_led, etat=Led(etat,ref_duty, new_time, last_time_led)

#<////////////////////////////////////>