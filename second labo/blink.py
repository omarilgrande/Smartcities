import machine  
import utime 

# initialization of the different pins
Rotary_sensor = machine.ADC(0)
buzzer = machine.PWM(machine.Pin(16))
button = machine.Pin(20, machine.Pin.IN) 

# frequencies and time of play of every musical note
score = {"DO":[1046, 250],"MI" :[1318, 250], "FA" :[1397, 250], 
        "RE":[1175,250], "SOL" : [1568, 500], "LA" :[1760, 125],
        "SI":[1967, 500] } 

#<----------------------------------->
# the musical note of different music
avengers_theme = [ 
    "FA", "FA", "LA", "FA",
    "RE", "DO", "RE",
    "FA", "FA", "LA", "FA",
    "RE", "DO", "RE"
]

pirates_theme = [
    "RE", "MI", "FA", "SOL", "FA", "MI", "RE",
    "FA", "SOL", "LA", "SOL", "FA", "MI", "FA"
]

jurassic_park_theme = [
    "FA", "FA", "MI", "RE", "DO",
    "DO", "RE", "MI", "FA",
    "FA", "MI", "RE", "DO"
]

harry_potter_theme = [
    "SI", "MI", "SOL", "FA", "MI",
    "SI", "MI", "SOL", "FA", "RE",
    "SI", "MI", "SOL", "FA", "MI"
]

super_mario_theme = [
    "MI", "MI", "MI",
    "DO", "MI", "SOL",
    "SOL", "DO", "SOL", "MI",
    "LA", "SI", "LA", "SOL", "MI",
    "SOL", "LA", "FA", "SOL"
]

star_wars_theme_simplifie = [
    "SOL", "SOL", "SOL", "MI",
    "SI", "SOL", "MI", "SI", "SOL",
    "RE", "RE", "RE", "MI", "SI", "FA", "MI", "SI", "SOL"
]
#<////////////////////////////////////>


#<----------------------------------->
# A list of the different musical notes of music and the name of each music
nom_musique = [star_wars_theme_simplifie,super_mario_theme,harry_potter_theme,jurassic_park_theme, pirates_theme,avengers_theme]
nom_musique_prime = ["star_wars_theme_simplifie","super_mario_theme","harry_potter_theme","jurassic_park_theme", "pirates_theme","avengers_theme"]
#<////////////////////////////////////>

#<----------------------------------->
# function which is used to play the musicla notes
# score is the dictionnary which has the information of musical notes
# notes is the musical which is currently plays
# last hs information over time when the last musical note was played
# i is the  index incrementation of the muscial notes
# new is the time 
# if the difference of new - last is over the time of the notes we can change the muscal note
# resistance is the value of the Rotary Angle Sensor to determine the intensity of the song
def music_notes(score, notes, last, i) :
    new = utime.ticks_ms() 
    if score[notes][1]<(new - last):
        resistance = Rotary_sensor.read_u16() 
        intensity = int(resistance*0.30518)
        buzzer.freq(score[notes][0])
        buzzer.duty_u16(intensity)
        return utime.ticks_ms(), i+1
    return last, i
#<////////////////////////////////////>


#<----------------------------------->
ref_musique = 0
ancien_index =0
i = 0
changement = False
last = utime.ticks_ms()
last_button= utime.ticks_ms()
#<////////////////////////////////////>

#<----------------------------------->
# infinity loop to play the music
while True:

    # look to check the value of the button because the incrementation can be uncontrollable
    index = button.value()
    new_button = utime.ticks_ms()
    if  250 < (new_button-last_button) and index==1:
        changement = True
        if ref_musique ==5:
            ref_musique =0
        else :
            ref_musique +=1
        last_button= utime.ticks_ms()
    else :
        changement = False
    ancien_index = index

    # check the name of the music
    print(nom_musique_prime[ref_musique])

    # loop for the playins of an entire music
    while i != (len(nom_musique[ref_musique])) and button.value()!=1 and changement ==False:
        musique = nom_musique[ref_musique]
        Note = musique[i]
        last, i =music_notes(score, Note, last, i)
        
    i = 0
#<////////////////////////////////////>