import cv2
import pygame
import random
import time
import os

import handTracker as hT
from timer import Timer 

WIDTH, HEIGHT = (900, 400)
pygame.init()
FPS = 60
# 250x220
paper = pygame.image.load(os.path.join('Assets', 'paper.jpg'))
rock = pygame.image.load(os.path.join('Assets', 'rock.jpg'))
scissors = pygame.image.load(os.path.join('Assets', 'scissors.jpg'))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

# colors

YELLOW = (255, 235, 0)
BLACK = (0, 0, 0)

playerPosition = (300+25, 95)
computerPosition: tuple[int, int] = (300+325, 95)
playerTextPosition = (300+60, 10)
computerTextPosition = (300+350, 10)

detector = hT.HandDetector(detectionCon=0.8)
cap = cv2.VideoCapture(0)

interactions = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock"
}


def score(plChoice: str, compChoice: str) -> int:
    if not plChoice == compChoice:
        if interactions[plChoice] == compChoice:
            return 1
        else:
            return 0
    return -1


def draw(playerIMG=paper, computerIMG=rock, playerScore: int = 0, computerScore: int = 0):
    WIN.fill(YELLOW)
    WIN.blit(playerIMG, playerPosition)
    WIN.blit(computerIMG, computerPosition)
    WIN.blit(text("player : " + str(playerScore)), playerTextPosition)
    WIN.blit(text("computer : " + str(computerScore)), computerTextPosition)


def main():
    clock = pygame.time.Clock()
    run = True
    # if true computer chooses a random value
    compChose = False
    # range of the hand if this is passed the game restarts
    bound = 150

    playerScore = 0
    computerScore = 0
    # keeps track of fps
    previousTime = 0
    timer = Timer(3)

    computerChoice = scissors
    comChoiceStr = ''

    playerChoice = paper
    playerChoiceStr = ""

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        _, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        fingers = detector.countFingers(lmList, True)

        if timer.start:
            # font
            font = cv2.FONT_HERSHEY_SIMPLEX
            
            # org
            org = (300,300)
            
            # fontScale
            fontScale = 5
            
            # Blue color in BGR
            color = (255, 0, 0)
            
            # Line thickness of 2 px
            thickness = 2
            
            # Using cv2.putText() method
            
            img = cv2.putText(img, str(int(abs(timer.current-timer.start_time))), org, font, 
                            fontScale, color, thickness, cv2.LINE_AA)

        if compChose and not timer.start:
            
            compChose = False

            rand = random.randint(1, 3)
            computerChoice = scissors
            comChoiceStr = ''

            if rand == 1:
                computerChoice = rock
                comChoiceStr = "rock"
            elif rand == 2:
                computerChoice = paper
                comChoiceStr = 'paper'
            else:
                computerChoice = scissors
                comChoiceStr = 'scissors'

            # runs until a hand is found
            while not len(lmList):
                _, img = cap.read()
                img = detector.findHands(img)
                lmList = detector.findPosition(img)

            fingers = detector.countFingers(lmList, True)
            playerChoice = rock
            playerChoiceStr = ""

            if 0 <= fingers < 2:
                playerChoice = rock
                playerChoiceStr = "rock"
            elif 2 <= fingers < 4:
                playerChoice = scissors
                playerChoiceStr = "scissors"
            else:
                playerChoice = paper
                playerChoiceStr = "paper"

            if score(playerChoiceStr, comChoiceStr):
                playerScore += 1
            else:
                computerScore += 1

        if not fingers and len(lmList):
            if lmList[4][2] < bound:
                compChose = True
                timer.start_timer()

        # previousTime = showFPS(previousTime, img)

        timer.update()

        img = cv2.line(img,(0,bound), (1000,bound), (255,0,0), 1)
        # cv2.imshow("Image", img)
        draw(playerChoice, computerChoice, playerScore, computerScore)
        height, width, _ = img.shape

        img = pygame.image.frombuffer(img.tobytes(), (width, height), "BGR")
        WIN.blit(pygame.transform.scale(img,(300,400)), (0, 0))
        pygame.display.update()

        cv2.waitKey(1)

    pygame.quit()


def showFPS(prevTime, img):
    currentTime = time.time()
    fps = 1 / (currentTime - prevTime)
    prevTime = currentTime
    cv2.putText(img, str(int(fps)), (10, 70),
                cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 3)
    return prevTime


def text(txt: str):
    font = pygame.font.Font('freesansbold.ttf', 32)
    Txt = font.render(txt, True, BLACK)
    return Txt


if __name__ == '__main__':
    main()
