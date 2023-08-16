"""
Created on Sun Aug 13 18:50:34 2023

@author: chrisrelyea
"""


"""
    audio files included, all from royalty-free sites:
    hat.mp3
    snare.mp3
    kick.mp3

    this project was inspired by KeyDrum by Moragoh on GitHub
    https://github.com/Moragoh/KeyDrum/tree/master/KeyBand_release


 """
    



import pygame, sys
import math
from pygame.locals import *


# Enter desired tempo here in BPM. This is quarter notes, each button is a sixteenth note
tempo = 160

# DO NOT EDIT: Converting tempo to milliseconds for use with pygame delay method
# not exact, since delay() requires an integer as the argument
tempo = math.floor((60000/tempo)/4)

# Variables for sound file names
hat = "hat.mp3"
snare = "snare.mp3"
kick = "kick.mp3"

# RGB values
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)

# Beats and playing status
beats = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
current_beat = 1
playing = False

# Initialize the window
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Roboto', 25)
labelfont = pygame.font.SysFont('Roboto', 40)
titlefont = pygame.font.SysFont('Roboto', 80)
playbeat = font.render('X: Loop on',False,(0,0,0))
stopbeat = font.render('Z: Loop off',False,(0,0,0))
hatlabel = labelfont.render('HHat',False,(0,0,0))
snarelabel = labelfont.render('Snare',False,(0,0,0))
kicklabel = labelfont.render('Kick',False, (0,0,0))
title = titlefont.render('PyDrummer', False, (0,0,0))
sig = font.render('Created by Chris Relyea, 2023', False, (0,0,0))

display = pygame.display.set_mode((950,480))
pygame.display.set_caption('PyDrummer')
display.fill(white)
display.blit(playbeat,(10,10))
display.blit(stopbeat,(120,10))
display.blit(hatlabel, (15,190))
display.blit(snarelabel, (15,290))
display.blit(kicklabel, (15,390))
display.blit(title, (600, 50))
display.blit(sig, (670, 105))

pygame.draw.line(display, (169,169,169), (300,160),(300,430),3)
pygame.draw.line(display, (169,169,169), (500,160),(500,430),3)
pygame.draw.line(display, (169,169,169), (700,160),(700,430),3)


# Clickable button object
class Button:
    def __init__(self, sound, beat):
        self.state = False
        self.beat = beat
        self.sound = sound

    def __str__(self):
        return (self.sound + " button at beat " + str(self.beat) + " activation is " + str(self.state))
    
    def toggle(self):
        state = self.state
        self.state = not state

    def getstate(self):
        return self.state
    
    def gettype(self):
        return self.sound
        
    
        
        
# Iitialize drum data arrays
hats = []
snares = []
kicks = []

for i in range(1,17):
    hats += [Button("hat",i)]
    snares += [Button("snare",i)]
    kicks += [Button("kick",i)]


''' 
    playNotes

    Input: current beat to be played

    Plays the sound of any hat, snare, or kick buttons that are
    activated for the current beat
'''

def playNotes(currentBeat):
    if hats[currentBeat].getstate():
        hatsound = pygame.mixer.Sound('hat.mp3')
        hatsound.set_volume(0.4)
        pygame.mixer.Channel(7).play(hatsound)
    if snares[currentBeat].getstate():
        snaresound = pygame.mixer.Sound('snare.mp3')
        snaresound.set_volume(0.4)
        pygame.mixer.Channel(6).play(snaresound)
    if kicks[currentBeat].getstate():
        kicksound = pygame.mixer.Sound('kick.mp3')
        kicksound.set_volume(0.4)
        pygame.mixer.Channel(5).play(kicksound)
    
                


# Set up moving metronome dot
markersurface = pygame.Surface((900,50))
markersurface.fill(white)
pygame.draw.circle(markersurface,red,(25,25),10)
display.blit(markersurface,(100,125))

# Set up buttons
for x in range(0,16):
    pygame.draw.circle(display,blue,(x*50 + 125 ,200),20,2) ##hats
    pygame.draw.circle(display,blue,(x*50 + 125 ,300),20,2) ##snares
    pygame.draw.circle(display,blue,(x*50 + 125 ,400),20,2) ##kicks
pygame.display.update()



'''
    getClickedButtonTypeAndIndex

    Input: current x and y mouse position

    Output: type (sound) of corresponding button and index within hat, snare
        or kick array as a tuple
'''

def getClickedButtonTypeAndIndex(xpos, ypos):

    index = (xpos - 105)/50
    index = math.ceil(index)
    if (index < 1) or (index > 16):
        return
    if (180 <= ypos <= 220):
        type = "hat"
    elif (280 <= ypos <= 320):
        type = "snare"
    elif (380 <= ypos <= 420):
        type = "kick"
    else:
        return
    return (type,index-1)

'''
    getCenterFromTypeAndIndex

    Input: type of sound (row of buttons) and index within that row

    Output: (x,y) tuple coordinates of the center of corresponding button
'''

def getCenterFromTypeAndIndex(type, index):
    xval = (index*50) + 125

    if type == "hat":
        yval = 200
    
    elif type == "snare":
        yval = 300

    else:
        yval = 400

    return (xval, yval)



'''
    visualToggle

    Input: button row and input in that row

    Toggles the appearance of the button
        If activated: solid blue circle
        If not activated: blue circle outline
'''
def visualToggle(array, index):
    center = getCenterFromTypeAndIndex(array[0].gettype(),index)
    if array[index].getstate(): ## is activated
        pygame.draw.circle(display, white, center, 20)
        pygame.draw.circle(display,blue,center,20,2)
        pygame.display.update()

    else:
        pygame.draw.circle(display,blue,center,20)
        pygame.display.update()


# Driver code
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Detect mouse click, toggle correct button
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_pos = pygame.mouse.get_pos()
            typeAndIndex = (getClickedButtonTypeAndIndex(current_pos[0],current_pos[1]))
            if typeAndIndex != None:
                if typeAndIndex[0] == "hat":
                    visualToggle(hats,typeAndIndex[1])
                    hats[typeAndIndex[1]].toggle()

                if typeAndIndex[0] == "snare":
                    visualToggle(snares,typeAndIndex[1])
                    snares[typeAndIndex[1]].toggle()

                if typeAndIndex[0] == "kick":
                    visualToggle(kicks,typeAndIndex[1])
                    kicks[typeAndIndex[1]].toggle()
                    

        

        # Event to check for pressed keys
        if event.type == pygame.KEYDOWN:
            broken = False
            if event.key == pygame.K_x:
                marker_xval = 25
                beat_index = 0
                while True:
                    if broken == True:
                        break
                    for event in pygame.event.get():
                        if broken == True:
                            break
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_z:
                                broken = True
                                break
                    playNotes(beat_index)
                    pygame.time.delay(tempo)
                    markersurface.fill(white)
                    if beats[beat_index] != 16:
                        marker_xval += 50
                        pygame.draw.circle(markersurface,red,(marker_xval,25),10)
                        beat_index += 1
                    else:
                        marker_xval = 25
                        pygame.draw.circle(markersurface,red,(marker_xval,25),10)
                        beat_index = 0
                    display.blit(markersurface,(100,125))
                    pygame.display.update()