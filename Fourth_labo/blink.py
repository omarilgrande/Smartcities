#<----------------------------------->
#Import of the different librairies
from ws2812 import WS2812
from machine import ADC
import utime
#<////////////////////////////////////>


#<----------------------------------->
#Initialisation of sensors
RGB = WS2812(20,1) #The first number defines the pin and the second number defines the number of LED RGB which are connected
#in this case, there is only one LED RGB
sound_sensor = ADC(0)#it defines the pin
#<////////////////////////////////////>


#<----------------------------------->
#Definition of differents functions which create a random combination to have an random color. The components of the color are a number between
#0 and 255 for the red, blue and green component. 
def red(led_value, average_noise) :
    #linear function which send back a number between 0 and 255, it depends on the average_noise and the Led_value. It returns a number for 
    #the red component
    color_red = int((average_noise-13000)*4.87*10**-3-(5*led_value)*2) 
    if 255>color_red and color_red>0 :
        return color_red 
    else : 
        return int((average_noise-13000)*4.87*10**-3)

def green(BPM_now, led_value):
    #linear function which send back a number between 0 and 255, it depends on the BPM_now and the Led_value. It returns a number for 
    #the green component
    color_green = int(0.853333*BPM_now-(led_value-2)*2)
    if 255>color_green and color_green >0:
        return color_green
    else : 
        return int(0.853333*BPM_now)

def blue (last_noise, led_value):
    #linear function which send back a number between 0 and 255, it depends on the last_noise and the Led_value. It returns a number for 
    #the blue component
    color_blue = int((last_noise-13000)*4.87*10**-3-(led_value+5)*2)
    if 255>color_blue and color_blue >0:
        return color_blue
    else :
        return int((last_noise-13000)*4.87*10**-3)
#<////////////////////////////////////>


#<----------------------------------->
#Initialisation of datas
BPM_now = 0
noise_list=[]
last_noise = 0
NO_noise = 13000 #if the lecture of the sensor is under this number, there is no noise
led_value = 0
last_time = utime.ticks_ms()          
last_time_writte = last_time
prise_de_mesure = True
average_noise= 0
BPM=[]
battement = False
#<////////////////////////////////////>


#<----------------------------------->
#Math functions
lissage = lambda average_noise, diff : (average_noise)*0.8+0.2*diff #average of the last and the new noise
peak = lambda average_noise : average_noise*0.95 #definition of the landing for the new noise
BPM_math = lambda new_time, last_time : 60000/(new_time-last_time)#calculate the value of the BPM
#<////////////////////////////////////>


#<----------------------------------->
#The first fifteen results of the sensors to make an average
while len(noise_list)!=15:
        noise=(sound_sensor.read_u16())
        if noise!=0:
            noise_list.append(noise)
#<////////////////////////////////////>


#<----------------------------------->
#Incrementation of the LED_value
def led(led_value):
    led_value = led_value+1
    if led_value>10:
        led_value= -10
    return led_value
#<////////////////////////////////////>


#<----------------------------------->
#Lecture of the sensor
def lecture(prise_de_mesure, noise_list):
    
    noise=(sound_sensor.read_u16())
    if noise!=0:
        del noise_list[0]#delete the last data of the noise
        noise_list.append(noise)#Add the new data of noise, if it is different of zero
        prise_de_mesure = False 
    return noise_list, prise_de_mesure
#<////////////////////////////////////>


#<----------------------------------->
#Lecture of the sensor
def moyenne(average_noise, noise_list, last_noise):
    for i in range(15):
        average_noise +=noise_list[i]
    average_noise = average_noise/15#It makes an average of the last fiftheen datas of noise
    diff = average_noise-last_noise
    average_noise=lissage(average_noise, diff)#It makes an average of the last average andthe new average
    return last_noise, average_noise
#<////////////////////////////////////>


#<----------------------------------->
#Lecture of the sensor
def BPM_function(average_noise, new_time, last_time, BPM):
    print("The average noise is : ",average_noise)
    BPM_now = BPM_math(new_time, last_time)#calculate the value of the BPM
    BPM.append(BPM_now)#Add the value of the currently BPM
    last_time= new_time
    last_noise = peak(average_noise) #Define the new landing to surpass for the new noise
    print("The currently BPM is : ", BPM_now)
    battement = True
    return battement, last_time, BPM, last_noise
#<////////////////////////////////////>


#<----------------------------------->
#Lecture of the sensor
def writting(last_time_writte, new_time, BPM):
    last_time_writte=new_time
    if len(BPM)!=0:
        bpm = sum(BPM)/len(BPM)#Calculate the average BPM
        BPM.clear()#Clear the list of the BPM
    else :
        bpm=0

    try:
        with open("bpm_log.txt", "a") as f: #The structure with close automaticaly the file
            f.write(f"{utime.localtime()}: {bpm:.1f} BPM\n")#Writte the data
            print("Valeur enregistrée dans bpm_log.txt")
    except Exception as e:
            print("Erreur d’écriture dans le fichier :", e)#Send the error to the terminal
            
    print("le BPM moyen est de ",bpm) 
    return last_time_writte 
#<////////////////////////////////////>


#<----------------------------------->
#Lecture of the sensor
def LED(battement, led_value, average_noise, BPM_now, last_noise):
    color = red(led_value, average_noise), green(BPM_now, led_value), blue(last_noise, led_value)#Calculate a random value of RGB
    RGB.pixels_fill(color)
    RGB.pixels_show()#Change the color of the RGB
    battement = False
    return battement
#<////////////////////////////////////>


#<----------------------------------->
#Infinty loop of reading
while True:
    #incrementation of the LED_value for the random color
    led_value = led(led_value)
    
    #Lectire of the noise sensor 
    while prise_de_mesure:
        noise_list, prise_de_mesure=lecture(prise_de_mesure, noise_list)
    
    #Allow taking the lecture of the noise
    prise_de_mesure = True 
    #Allow to make an average
    last_noise =average_noise
    #Reset the value of the average
    average_noise=0
    #utlisation of a function to make an average off the noise
    last_noise, average_noise = moyenne(average_noise, noise_list, last_noise)

    new_time = utime.ticks_ms()    
    
    if average_noise > last_noise and  new_time-last_time >200 and average_noise>NO_noise : #Allow to calculate the value of
        #the BPM if : the new noise is stronger than the last noise, there is a noise and the BPM is under 300BPM.
        battement, last_time, BPM, last_noise = BPM_function(average_noise, new_time, last_time, BPM)
        
    if new_time-last_time_writte>60000 :#Use the function every single minute
        last_time_writte = writting(last_time_writte, new_time, BPM)


    if battement:#If there is a BPM we change the color of the RGB
        battement = LED(battement, led_value, average_noise, BPM_now, last_noise)
#<////////////////////////////////////>