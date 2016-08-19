#------------------------------------------------------------------------------------------------------
# File Name:    typingGame.py
# Author:       Kyle Parrish
# Date:         7/4/2014
# Description:  A simple typing program that puts the characters typed on the screen simialr to all word processors.
#
# Change log:
#       8.19.16	Initial Release
#------------------------------------------------------------------------------------------------------

# Basic imports for the game
import os,sys,datetime, sqlite3
import pygame
from random import randint
from pygame.locals import *

# Setup basic constants
# Screen height and width
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Colors, any of these can be used in the program
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MATRIX_GREEN = (0, 255, 21)
PINK = (255, 105, 180)

# Code taken from: http://code.activestate.com/recipes/521884-play-sound-files-with-pygame-in-a-cross-platform-m/
# global constants
FREQ = 44100   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 2   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples
FRAMERATE = 30 # how often to check if playback has finished

sounds = ["Typewrit-Intermed-538_hifi.ogg",
            "Typewrit-Bell-Patrick-8344_hifi.ogg"]

soundFiles = []

def blankScreen(screen):
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	screen.blit(background, (0,0))
	pygame.display.update()

def main():
	# define the current position that the text will go to
	currX = 0
	currY = 0
	
	# define the width and height of the text to be written
	textWidth = 0
	textHeight = 0

	# initialize the music player
	pygame.mixer.pre_init(44100,-16,2, 1024)
	pygame.init()
    
	# initialize the text font and size
	TEXT_FONT = pygame.font.Font('freesansbold.ttf', 48)

	# set up the game window and screen
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('Music Game')

    # create background
	background = pygame.Surface(screen.get_size())
	background = background.convert()

    #allocate all the sound files, this should make it work better...
	for file in sounds:
		tempsound = pygame.mixer.Sound(file)
		soundFiles.append(tempsound)

    # hide the mouse
    # not used while developing
    #pygame.mouse.set_visible(False)

    # set the background with the default color.
	screen.blit(background, (0,0))
	pygame.display.update()    

	# main loop
	while 1:
        # This needs to change to match the new way of checking that I found on the web
        # http://stackoverflow.com/questions/12556535/programming-pygame-so-that-i-can-press-multiple-keys-at-once-to-get-my-character

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				return
			elif event.type == KEYDOWN:
				keys = pygame.key.get_pressed()

				if keys[K_ESCAPE] and keys[K_LCTRL]:
					pygame.quit()
					sys.exit()
				elif keys[K_ESCAPE]:
					blankScreen(screen)
					currX = 0
					currY = 0
					soundFiles[1].play()
				else:
					#between 97='a' and 122='z'
					# to get the capital letter simply subtract 32 from the ascii
					# value of the pressed key (event.key gets the ascii value)
					if(event.key >= 97 and event.key <= 122):
						# set the text object to be the surface to blit to the screen
						text = TEXT_FONT.render(chr(event.key - 32) + chr(event.key), 1, PINK)
						# set the height and width
						textWidth = text.get_width()
						textHeight = text.get_height()

						# check to see if we need to wrap the text to the next line
						if(currX + textWidth >= SCREEN_WIDTH):
							currX = 0
							currY = currY + textHeight

						# If we are at the bottom of the screen, blank the screen
						# and put the new characters in the first position.
						if(currY + textHeight >= SCREEN_HEIGHT):
							currX = 0
							currY = 0
							blankScreen(screen)

						screen.blit(text, (currX, currY))
						updateScreen = True
						soundFiles[0].play()
					
						currX = currX + textWidth
				
		pygame.display.update()

if __name__ == '__main__': main()
