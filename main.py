import pygame
from pygame.locals import *
import random
import sys
import time

FPS = 32
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 399
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

GAME_SPRITES = {}
GAME_SOUNDS = {}
NumbersToLetters = {
    1 : "A", 2 : "B", 3 : "C", 4 : "D", 5 : "E", 6 : "F", 7 : "G",8 : "H",9 : "I",10 : "J",11 : "K",12 : "L",13 : "M",14 : "N",15 : "O",16 : "P",17 : "Q",18 : "R",19 : "S",20 : "T",21 : "U",22 : "V",23 : "W",24 : "X",25 : "Y",26: "Z"
}

def getWord():
    file = open("Words.txt")
    strings = file.read()
    listOfWords = strings.split("\n")
    
    return listOfWords[random.randint(0, len(listOfWords) - 1)]

def welcomeScreen():
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key != K_ESCAPE:
                return
            elif event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        SCREEN.blit(GAME_SPRITES['Welcome Screen'],(0,0))
                    
        pygame.display.update()

        FPSCLOCK.tick(FPS)

def find(string, char):
    lst= []
    for i in range(len(string)):
        if string[i] == char.lower() or string[i] == char:
            lst.append(i)

    return lst

def sortByWord(letter, word):
    if letter.lower() in word:
        return find(word,letter)
    elif letter in word:
        return find(word, letter)

def listToString(lst):
    string = ""
    for element in lst:
        string += element

    return string
    

def mainGame():
    word = getWord()
    doneLettersList = []
    doneLettersList2 = []
    wordSame = False
    hangmanNo = 0

    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    previousButtonX = 250
    previousButtonY = 150
    totalUnderlineWidth = 0
    
    while True:
        clicked = False

        if len(doneLettersList2) == len(word):
            for i in doneLettersList2:
                if len(find(doneLettersList2, i)) == len(find(word, i)):
                    wordSame = True
                else:
                    wordSame = False

        if not wordSame and hangmanNo != 7:

            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = True
            
            SCREEN.blit(GAME_SPRITES['Background'],(0,0))
            SCREEN.blit(GAME_SPRITES['Hangman States'][hangmanNo],(10,30))

            # Blitting the buttons

            for button in GAME_SPRITES['Buttons']:
                if GAME_SPRITES["Buttons"].index(button) % 9 == 0:
                    previousButtonY += 60
                    previousButtonX = 250

                if NumbersToLetters[GAME_SPRITES["Buttons"].index(button) + 1] not in doneLettersList:
                    SCREEN.blit(button, (previousButtonX, previousButtonY))
                    rect = button.get_rect()
                    rect.move_ip(previousButtonX, previousButtonY)
                else:
                    rect = button.get_rect()
                    rect.move_ip(previousButtonX, previousButtonY)
                    del(rect)

                previousButtonX += 40
                
                if clicked:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    try:
                        if rect.left <= mouse_x <= rect.right and rect.top <= mouse_y <= rect.bottom :
                            print(f"You clicked {NumbersToLetters[GAME_SPRITES['Buttons'].index(button) + 1]}")

                            if NumbersToLetters[GAME_SPRITES["Buttons"].index(button) + 1].lower() in word or NumbersToLetters[GAME_SPRITES["Buttons"].index(button) + 1] in word:
                                doneLettersList.append(NumbersToLetters[GAME_SPRITES["Buttons"].index(button) + 1])

                                for i in find(word, NumbersToLetters[GAME_SPRITES["Buttons"].index(button) + 1]):
                                    doneLettersList2.append(NumbersToLetters[GAME_SPRITES["Buttons"].index(button) + 1])
                                GAME_SOUNDS["Win"].play()
                            else:
                                hangmanNo += 1
                                GAME_SOUNDS["Fail"].play()
                    except:
                        pass
            # Blitting the Character Underlines

            for letter in word:
                totalUnderlineWidth += (GAME_SPRITES["Character Underline"].get_width() + 40)

            previousUnderlineX = 430 - (totalUnderlineWidth // 4)

            for letter in word:
                SCREEN.blit(GAME_SPRITES["Character Underline"], (previousUnderlineX, 150))
                previousUnderlineX += 40

            # Blitting the Letters

            previousLetterX = (430 - (totalUnderlineWidth // 4)) + 5

            for letter in doneLettersList:
                if letter in word:
                    LetterIndexList = find(word, letter)
                else:
                    LetterIndexList = find(word, letter.lower())

                for i in LetterIndexList:
                    for j in range(i):
                        previousLetterX += 40
                    
                    textsurface = myfont.render(letter, False, (0, 0, 0))
                    SCREEN.blit(textsurface, (previousLetterX,140))
                    previousLetterX = (430 - (totalUnderlineWidth // 4)) + 7
            
            previousUnderlineX = 430 - (totalUnderlineWidth // 4)
            totalUnderlineWidth = 0

            doneLettersList.sort(key = lambda letter : sortByWord(letter, word))
            doneLettersList2.sort(key = lambda letter : sortByWord(letter, word))

            previousButtonX = 250
            previousButtonY = 150
            # previousUnderlineX = 250
                        
            pygame.display.update()

            FPSCLOCK.tick(FPS)

        elif hangmanNo == 7:
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    return

            font = pygame.font.SysFont('Comic Sans MS', 50)

            textsurface1 = myfont.render("Press any key to continue..", False, (255, 255, 255))
            SCREEN.blit(GAME_SPRITES["Background"], (0,0))
            textsurface = font.render("Game Over!", False, (255, 255, 255))
            SCREEN.blit(textsurface, (250,140))
            SCREEN.blit(textsurface1, (200,200))
            textsurface2 = myfont.render(f"The word was: {word}", False, (255, 255, 255))
            SCREEN.blit(textsurface2, (240, 240))

            pygame.display.update()
            FPSCLOCK.tick(FPS)

        else:
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    return

            font = pygame.font.SysFont('Comic Sans MS', 50)
            textsurface1 = myfont.render("Press any key to continue..", False, (255, 255, 255))
            SCREEN.blit(GAME_SPRITES["Background"], (0,0))
            textsurface = font.render("You Win!", False, (255, 255, 255))
            SCREEN.blit(textsurface, (250,140))
            SCREEN.blit(textsurface1, (200,200))

            pygame.display.update()
            FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Hangman")
    
    # Game Sprites
    GAME_SPRITES['Welcome Screen'] = pygame.image.load("assets/Welcome Screen.jpg").convert()
    GAME_SPRITES['Background'] = pygame.image.load("assets/Background3.jpg").convert()
    GAME_SPRITES['Character Underline'] = pygame.image.load("assets/Underline.png").convert_alpha()
    GAME_SPRITES['Buttons'] = (
        pygame.transform.scale(pygame.image.load("assets/Buttons/A.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/B.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/C.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/D.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/E.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/F.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/G.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/H.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/I.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/J.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/K.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/L.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/M.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/N.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/O.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/P.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/Q.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/R.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/S.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/T.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/U.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/V.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/W.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/X.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/Y.png").convert_alpha(),(40,40)),
        pygame.transform.scale(pygame.image.load("assets/Buttons/Z.png").convert_alpha(),(40,40)),
    )
    GAME_SPRITES['Hangman States'] = (
        pygame.image.load("assets/Hangmans/1.png").convert_alpha(),
        pygame.image.load("assets/Hangmans/2.png").convert_alpha(),
        pygame.image.load("assets/Hangmans/3.png").convert_alpha(),
        pygame.image.load("assets/Hangmans/4.png").convert_alpha(),
        pygame.image.load("assets/Hangmans/5.png").convert_alpha(),
        pygame.image.load("assets/Hangmans/6.png").convert_alpha(),
        pygame.image.load("assets/Hangmans/7.png").convert_alpha()
    )

    # Game Sounds
    GAME_SOUNDS['Background'] = pygame.mixer.Sound("assets/Sound/Background.mp3")
    GAME_SOUNDS['Fail'] = pygame.mixer.Sound("assets/Sound/Fail.mp3")
    GAME_SOUNDS['Game Over'] = pygame.mixer.Sound("assets/Sound/Game Over.wav")
    GAME_SOUNDS['Win'] = pygame.mixer.Sound("assets/Sound/Win.wav")

    GAME_SOUNDS["Background"].play(-1)

    while True:
        welcomeScreen()
        GAME_SOUNDS["Background"].set_volume(0.3)
        mainGame()