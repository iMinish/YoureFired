#globals (scoreboard vaiables)
totalAttackPlayer1 = 0
totalAttackPlayer2 = 0
totalAttackHuman = 0
totalAttackAI = 0


totalhitPlayer1 = 0
totalhitPlayer2 = 0
totalhitHuman = 0
totalhitAI = 0



totalMissedPlayer1 = 0
totalMissedPlayer2 = 0
totalMissedHuman = 0
totalMissedAI = 0


if __name__ == "__main__":
    import pygame
    import pygame.gfxdraw
    import math
    from pygame.locals import *
    import random
    from boats import Boat
    from executive import Executive
    from player import Player
    pygame.init()

    disp_width = 1080
    disp_height = 720

    #globals
    disp = pygame.display.set_mode((disp_width, disp_height))
    disp.fill((192, 192, 192))
    pygame.display.set_caption('Battleboats')
    clock = pygame.time.Clock()
    draw_once = True
    gameState = "welcome"
    winner = "null"
    difficulty = "null"
    num_destroyed = 0
    numberOfBoats = 0
    player1 = Player()
    player2 = Player()
    playerHuman = Player()
    playerAI = Player()
    placeNumber = 1
    spotsToCheck = [] #[[0 for x in range(2)] for y in range(placeNumber)]
    turn = 0
    grid = None
    leftGrid = None
    rightGrid = None

    # variables used when gameState = "gamePlay"
    checkbox = pygame.draw.rect(disp, (255, 255, 255), (533, 200, 15, 15))
    toggled = False

    rects_clicked1 = []
    rects_missed1 = []
    rects_hit1 = []
    opposing_ship1 = []
    my_ships1 = []

    rects_clicked2 = []
    rects_missed2 = []
    rects_hit2 = []
    opposing_ship2 = []
    my_ships2 = []
    #game = Executive()

    board_cleared = True

    #globals for AI in human vs AI
    rects_clickedAI = []
    rects_missedAI = []
    rects_hitAI = []
    opposing_shipAI = []
    my_shipsAI = []
    shipHitsAI = []

    #globals for human in human vs AI
    rects_clickedHuman = []
    rects_missedHuman = []
    rects_hitHuman = []
    opposing_shipHuman = []
    my_shipsHuman = []

def quitGame():
    """Closes the game window"""

    pygame.quit()
    quit()

def event_handler():
    """Checks for different pygame events"""

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
            quitGame()

def isPointInRect(x, y, rect):
    """Checks if a coordinate is within the bounds of a pygame.rect object
    Args:
    x (float): x coordinate to check
    y (float): y coordinate to check
    rect (pygame.Rect): object to see if x any y are in
    Returns:
        bool: True if x and y are in rect, False otherwise
    """

    if x < rect.x + rect.width and x > rect.x and y < rect.y + rect.height and y > rect.y:
        return True
    return False

def createRects(x, y):
    """Creates an 8x8 grid of squares
    Args:
    x (int): the x position for the top right corner of the grid to start at
    y (int): the y position for the top right corner of the grid to start at
    Returns:
        8x8 array of pygame.Rect objects
    """

    interval = (disp_width / 2) / 16
    divX = interval + x
    divY = interval + y
    rects = [[0 for x in range(8)] for y in range(8)]
    letter_label = pygame.font.SysFont('Ariel', 20)
    alphabet = "ABCDEFGHIJKLMNOP"
    numbers = "123456789"
    for i in range(0, 8):
        letter_label_display = letter_label.render(numbers[i], False, (0, 0, 0))
        disp.blit(letter_label_display, (divX - 12, divY + 7))
        for j in range(0, 8):
            if(i == 0):
                letter_label_display = letter_label.render(alphabet[j], False, (0, 0, 0))
                disp.blit(letter_label_display, (divX + 12, divY - 12))
            rects[i][j] = pygame.Rect(divX, divY, interval, interval)
            pygame.draw.rect(disp, (0, 0, 0), rects[i][j], 2)
            divX += interval
        divX = interval + x
        divY += interval
    pygame.display.update()
    return rects

def text_objects(text, font): #function used from https://pythonprogramming.net/pygame-start-menu-tutorial/
    """Creates a text object
    Args:
    text: the string to display
    font: the style of the text
    """

    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()

def showboat1(rects):
    """Shows player 1's own boats after pressing the toggle button
    Args:
    rects: (8x8 array of pygame.Rect objects): the grid to check on
    """

    for i in range(0, 8):
        for j in range(0, 8):
            if(i, j) in my_ships1:
                pygame.draw.rect(disp, (0, 0, 0), rects[i][j])
                pygame.display.update(rects[i][j])

def showboat2(rects):
    """Shows player 2's own boats after pressing the toggle button
    Args:
    rects: (8x8 array of pygame.Rect objects): the grid to check on
    """
    for i in range(0, 8):
        for j in range(0, 8):
            if(i, j) in my_ships2:
                pygame.draw.rect(disp, (0, 0, 0), rects[i][j])
                pygame.display.update(rects[i][j])

def showboatHuman(rects):
    """Shows player human's own boats after pressing the toggle button
    Args:
    rects: (8x8 array of pygame.Rect objects): the grid to check on
    """
    for i in range(0, 8):
        for j in range(0, 8):
            if(i, j) in my_shipsHuman:
                pygame.draw.rect(disp, (0, 0, 0), rects[i][j])
                pygame.display.update(rects[i][j])

def showboatAI(rects):
    """Shows player AI's own boats after pressing the toggle button
    Args:
    rects: (8x8 array of pygame.Rect objects): the grid to check on
    """
    for i in range(0, 8):
        for j in range(0, 8):
            if(i, j) in my_shipsAI:
                pygame.draw.rect(disp, (0, 0, 0), rects[i][j])
                pygame.display.update(rects[i][j])

def trackRects1(rects):
    """Tracks when a single square in a grid is pressed by the mouse for player 1
    Args:
        rects: (8x8 array of pygame.Rect objects): the grid to check on
    """

    global winner
    newPress = True
    mouseX = 0
    mouseY = 0

    #scoreboard global variables
    global totalAttackPlayer1
    global totalhitPlayer1
    global totalMissedPlayer1
    hit_text = pygame.font.SysFont('Consolas', 40)
    if pygame.mouse.get_pressed() == (1, 0, 0) and newPress:
        newPress = False
        mouseX, mouseY = pygame.mouse.get_pos()
        for i in range(0, 8):
            for j in range(0, 8):
                if isPointInRect(mouseX, mouseY, rects[i][j]) and (i, j) in opposing_ship1 and not (i, j) in rects_clicked1: #clicked on square containing ship
                    rects_hit1.append((i, j))
                    #print("in 1")
                    print("Player1 hit a ship!") #TESTER COMMENT
                    player2.addToHitList(i, j)
                    rects_clicked1.append((i, j))
                    pygame.draw.rect(disp, (255, 0, 0), rects[i][j])
                    pygame.display.update(rects[i][j])
                    hit_text_display = hit_text.render("HIT!", False, (255, 0, 0))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    pygame.time.delay(500)
                    hit_text_display = hit_text.render("HIT!", False, (192, 192, 192))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    print(rects_clicked1)
                    print("destroyed", player1.shipsDestroyed()) # NOT SURE IF THIS IS UPDATING CORRECTLY
                    #scoreboard total attacked update
                    totalAttackPlayer1 = totalAttackPlayer1 + 1
                    #scoreboard total hit update
                    totalhitPlayer1 = totalhitPlayer1 + 1
                    if player2.shipsDestroyed() == numberOfBoats:
                        winner = "Player 1"
                        gameState = "winner"
                        winState()
                    setupGamePlay2() # Fixed fire until miss
                elif isPointInRect(mouseX, mouseY, rects[i][j]) and not (i, j) in rects_clicked1: #clicked on a square and missed
                    rects_missed1.append((i, j))
                    #print("in 2")
                    print("Player1 missed!") #TESTER COMMENT
                    rects_clicked1.append((i, j))
                    pygame.draw.rect(disp, (0, 0, 255), rects[i][j])
                    pygame.display.update(rects[i][j])
                    hit_text_display = hit_text.render("MISS!", False, (0, 0, 255))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    pygame.time.delay(500)
                    hit_text_display = hit_text.render("MISS!", False, (192, 192, 192))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    print(rects_clicked1)
                    setupGamePlay2() # Fixed fire until hit
                    #scoreboard total attacked update
                    totalAttackPlayer1 = totalAttackPlayer1 + 1
                    #scoreboard total missed update
                    totalMissedPlayer1 = totalMissedPlayer1 + 1

def trackRects2(rects):
    """Tracks when a single square in a grid is pressed by the mouse for player 2
    Args:
        rects (8x8 array of pygame.Rect objects): the grid to check on
    """

    global winner
    newPress = True
    mouseX = 0
    mouseY = 0
    global totalAttackPlayer2
    global totalhitPlayer2
    global totalMissedPlayer2
    hit_text = pygame.font.SysFont('Consolas', 40)
    if pygame.mouse.get_pressed() == (1, 0, 0) and newPress:
        newPress = False
        mouseX, mouseY = pygame.mouse.get_pos()
        for i in range(0, 8):
            for j in range(0, 8):
                if isPointInRect(mouseX, mouseY, rects[i][j]) and (i, j) in opposing_ship2 and not (i, j) in rects_clicked2:
                    rects_hit2.append((i, j))
                    player1.addToHitList(i, j)
                    rects_clicked2.append((i, j))
                    pygame.draw.rect(disp, (255, 0, 0), rects[i][j])
                    pygame.display.update(rects[i][j])
                    hit_text_display = hit_text.render("HIT!", False, (255, 0, 0))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    pygame.time.delay(500)
                    hit_text_display = hit_text.render("HIT!", False, (192, 192, 192))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    print(rects_clicked2)
                    print("destroyed", player2.shipsDestroyed())
                    #scoreBoard total attacked update
                    totalAttackPlayer2 = totalAttackPlayer2 + 1
                    #scoreboard total hit update
                    totalhitPlayer2 = totalhitPlayer2 + 1
                    if player1.shipsDestroyed() == numberOfBoats:
                        winner = "Player 2"
                        gameState = "winner"
                        winState()
                    setupGamePlay1() # Fixed fire until miss
                elif isPointInRect(mouseX, mouseY, rects[i][j]) and not (i, j) in rects_clicked2:
                    rects_missed2.append((i, j))
                    rects_clicked2.append((i, j))
                    pygame.draw.rect(disp, (0, 0, 255), rects[i][j])
                    pygame.display.update(rects[i][j])
                    hit_text_display = hit_text.render("MISS!", False, (0, 0, 255))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    pygame.time.delay(500)
                    hit_text_display = hit_text.render("MISS!", False, (192, 192, 192))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    print(rects_clicked2)
                    pygame.time.delay(250)
                    setupGamePlay1() # Fixed fire until hit
                    #scoreBoard total attacked update
                    totalAttackPlayer2 = totalAttackPlayer2 + 1
                    #scoreboard total missed update
                    totalMissedPlayer2 = totalMissedPlayer2 + 1
    elif pygame.mouse.get_pressed() != (1, 0, 0):
        newPress = True

def trackRectsHuman(rects):
    """Tracks when a single square in a grid is pressed by the mouse for player human
    Args:
        rects: (8x8 array of pygame.Rect objects): the grid to check on
    """

    global winner
    newPress = True
    mouseX = 0
    mouseY = 0
    global totalAttackHuman
    global totalhitHuman
    global totalMissedHuman
    hit_text = pygame.font.SysFont('Consolas', 40)
    if pygame.mouse.get_pressed() == (1, 0, 0) and newPress:
        newPress = False
        mouseX, mouseY = pygame.mouse.get_pos()
        for i in range(0, 8):
            for j in range(0, 8):
                if isPointInRect(mouseX, mouseY, rects[i][j]) and (i, j) in opposing_shipHuman and not (i, j) in rects_clickedHuman: #clicked on square containing ship
                    rects_hitHuman.append((i, j))
                    playerAI.addToHitList(i, j)
                    rects_clickedHuman.append((i, j))
                    pygame.draw.rect(disp, (255, 0, 0), rects[i][j])
                    pygame.display.update(rects[i][j])
                    hit_text_display = hit_text.render("HIT!", False, (255, 0, 0))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    pygame.time.delay(500)
                    hit_text_display = hit_text.render("HIT!", False, (192, 192, 192))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    print(rects_clickedHuman)
                    print("destroyed", playerHuman.shipsDestroyed())
                    #scoreBoard total attacked update
                    totalAttackHuman = totalAttackHuman + 1
                    #scoreBoard total hit update
                    totalhitHuman = totalhitHuman + 1
                    if playerAI.shipsDestroyed() == numberOfBoats:
                        winner = "Player Human"
                        gameState = "winner"
                        winState()
                    setupGamePlayAI()
                elif isPointInRect(mouseX, mouseY, rects[i][j]) and not (i, j) in rects_clickedHuman: #clicked on a square and missed
                    rects_missedHuman.append((i, j))
                    print("in 2")
                    rects_clickedHuman.append((i, j))
                    pygame.draw.rect(disp, (0, 0, 255), rects[i][j])
                    pygame.display.update(rects[i][j])
                    hit_text_display = hit_text.render("MISS!", False, (0, 0, 255))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    pygame.time.delay(500)
                    hit_text_display = hit_text.render("MISS!", False, (192, 192, 192))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    print(rects_clickedHuman)
                    setupGamePlayAI()
                    #scoreBoard total attacked update
                    totalAttackHuman = totalAttackHuman + 1
                    #scoreBoard total Missed update
                    totalMissedHuman = totalMissedHuman + 1

#def fireAdjacent(shipHitsAI):
    #shipHitAI is an array passed in with the current spot we want to hit

    #if("""able to fire above""")
        #return CP above the passed in CP
    #elif("""able to fire to the right""")
        #return CP to the right of passed in CP
    #elif("""able to fire below""")
        #return CP below the passed in CP
    #elif("""able to fire to the left""")
        #return CP to the left of passed in CP
    #else:


def trackRectsAI(rects, difficulty):
    """Allows the AI to fire
    Args:
        rects (8x8 array of pygame.Rect objects): the grid to check on
        difficulty (string): difficulty setting for AI
    """

    global winner
    newPress = True
    mouseX = 0
    mouseY = 0
    #scoreboard variables for AI
    global totalAttackAI
    global totalhitAI
    global totalMissedAI
    global shipHitsAI

    hit_text = pygame.font.SysFont('Consolas', 40)

    if (difficulty == "easy"):
        xCoord = random.randint(0, 7)
        yCoord = random.randint(0, 7)
        for i in range(0, 8):
            for j in range(0, 8):
                if (xCoord, yCoord) in opposing_ship2 and not (xCoord, yCoord) in rects_clickedAI:
                    rects_hit2.append((i, j))
                    player1.addToHitList(i, j)
                    rects_clicked2.append((i, j))
                    pygame.draw.rect(disp, (255, 0, 0), rects[i][j])
                    pygame.display.update(rects[i][j])
                    hit_text_display = hit_text.render("HIT!", False, (255, 0, 0))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    pygame.time.delay(500)
                    hit_text_display = hit_text.render("HIT!", False, (192, 192, 192))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    print(rects_clickedAI)
                    print("destroyed", playerAI.shipsDestroyed())
                    #scoreBoard total attacked update
                    totalAttackAI = totalAttackAI + 1
                    #scoreBoard total hit update
                    totalhitAI = totalhitAI + 1
                    if playerHuman.shipsDestroyed() == numberOfBoats:
                        winner = "Player AI"
                        gameState = "winner"
                        winState()
                    setupGamePlayHuman()
                elif not (xCoord, yCoord) in rects_clicked2:
                    rects_missed2.append((i, j))
                    rects_clicked2.append((i, j))
                    pygame.draw.rect(disp, (0, 0, 255), rects[i][j])
                    pygame.display.update(rects[i][j])
                    hit_text_display = hit_text.render("MISS!", False, (0, 0, 255))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    pygame.time.delay(500)
                    hit_text_display = hit_text.render("MISS!", False, (192, 192, 192))
                    disp.blit(hit_text_display, (480, 540))
                    pygame.display.update()
                    print(rects_clickedAI)
                    pygame.time.delay(250)
                    setupGamePlayHuman()
                    #scoreBoard total attacked update
                    totalAttackAI = totalAttackAI + 1
                    #scoreBoard total Missed update
                    totalMissedAI = totalMissedAI + 1
    elif (difficulty == "medium"):
            if (shipHitsAI):
                xCoord, yCoord = fireAdjacent(shipHitsAI) #NEED TO CREATE THIS FUNCTION STILL
            else:
                xCoord = random.randint(0,7)
                yCoord = random.randint(0,7)
            for i in range(0, 8):
                for j in range(0, 8):
                    if (xCoord, yCoord) in opposing_shipAI and not (xCoord, yCoord) in rects_clickedAI:
                        rects_hitAI.append((i, j))
                        playerHuman.addToHitList(i, j)
                        rects_clickedAI.append((i, j))
                        pygame.draw.rect(disp, (255, 0, 0), rects[i][j])
                        pygame.display.update(rects[i][j])
                        hit_text_display = hit_text.render("HIT!", False, (255, 0, 0))
                        disp.blit(hit_text_display, (480, 540))
                        pygame.display.update()
                        pygame.time.delay(500)
                        hit_text_display = hit_text.render("HIT!", False, (192, 192, 192))
                        disp.blit(hit_text_display, (480, 540))
                        pygame.display.update()
                        print(rects_clickedAI)
                        print("destroyed", playerAI.shipsDestroyed())
                        #scoreBoard total attacked update
                        totalAttackAI = totalAttackAI + 1
                        #scoreBoard total hit update
                        totalhitAI = totalhitAI + 1
                        if playerHuman.shipsDestroyed() == numberOfBoats:
                            winner = "Player AI"
                            gameState = "winner"
                            winState()
                        #if sunk, remove ship's coords from global shipList
                        checkIfSunk = playerHuman.getShipList()
                        isSunk = False
                        for currentShip in checkIfSunk:
                            shipsCoords = currentShip.getCoordinates()
                            if (currentShip.checkDestroyed() and ((xCoord,yCoord) in shipsCoords)): #CHECK
                                isSunk = True
                                for coord in shipCoords:
                                    shipHitsAI.remove(coord) #CHECK

                        #else, add coord to global list
                        if (isSunk == False):
                            shipHitsAI.append()
                        setupGamePlayHuman()

                    elif not (xCoord, yCoord) in rects_clickedAI:
                        rects_missedAI.append((i, j))
                        rects_clickedAI.append((i, j))
                        pygame.draw.rect(disp, (0, 0, 255), rects[i][j])
                        pygame.display.update(rects[i][j])
                        hit_text_display = hit_text.render("MISS!", False, (0, 0, 255))
                        disp.blit(hit_text_display, (480, 540))
                        pygame.display.update()
                        pygame.time.delay(500)
                        hit_text_display = hit_text.render("MISS!", False, (192, 192, 192))
                        disp.blit(hit_text_display, (480, 540))
                        pygame.display.update()
                        print(rects_clickedAI)
                        pygame.time.delay(250)
                        setupGamePlayHuman()
                        #scoreBoard total attacked update
                        totalAttackAI= totalAttackAI + 1
                        #scoreBoard total Missed update
                        totalMissedAI = totalMissedAI + 1

    elif (difficulty == "hard"):
        print("in hard mode") #testing purposes
        cont = 1
        for (i, j) in opposing_shipAI:
            if (not (i, j) in rects_clickedAI):
                print("inside line 553") #testing purposes
                rects_hitAI.append((i, j))
                playerHuman.addToHitList(i, j)
                rects_clickedAI.append((i, j))
                pygame.draw.rect(disp, (255, 0, 0), rects[i][j])
                pygame.display.update(rects[i][j])
                hit_text_display = hit_text.render("HIT!", False, (255, 0, 0))
                disp.blit(hit_text_display, (480, 540))
                pygame.display.update()
                pygame.time.delay(500)
                hit_text_display = hit_text.render("HIT!", False, (192, 192, 192))
                disp.blit(hit_text_display, (480, 540))
                pygame.display.update()
                print(rects_clickedAI)
                print("destroyed", playerAI.shipsDestroyed())
                #scoreBoard total attacked update
                totalAttackAI = totalAttackAI + 1
                #scoreBoard total hit update
                totalhitAI = totalhitAI + 1
                if playerHuman.shipsDestroyed() == numberOfBoats:
                    winner = "Player AI"
                    gameState = "winner"
                    winState()
                    cont = 0
                    break
                print("about to cont")
                setupGamePlayHuman()
                cont = 0
                break
            if (cont == 0):
                break
            print("BROKEN")


    elif pygame.mouse.get_pressed() != (1, 0, 0):
        newPress = True

def printRects1(rects):
    """Draws the squares on the board that have been hit or missed for player 1
    Args:
        rects (8x8 array of pygame.Rect objects): the grid to check on
    """

    for i in range(0, 8):
        for j in range(0, 8):
            if (i, j) in rects_hit1:
                pygame.draw.rect(disp, (255, 0, 0), rects[i][j])
                pygame.display.update(rects[i][j])
            if (i, j) in rects_missed1:
                pygame.draw.rect(disp, (0, 0, 255), rects[i][j])
                pygame.display.update(rects[i][j])

def printRects2(rects):
    """Draws the squares on the board that have been hit or missed for player 2
    Args:
        rects (8x8 array of pygame.Rect objects): the grid to check on
    """

    for i in range(0, 8):
        for j in range(0, 8):
            if (i, j) in rects_hit2:
                pygame.draw.rect(disp, (255, 0, 0), rects[i][j])
                pygame.display.update(rects[i][j])
            if (i, j) in rects_missed2:
                pygame.draw.rect(disp, (0, 0, 255), rects[i][j])
                pygame.display.update(rects[i][j])

def printRectsHuman(rects):
    """Draws the squares on the board that have been hit or missed for player human
    Args:
        rects (8x8 array of pygame.Rect objects): the grid to check on
    """

    for i in range(0, 8):
        for j in range(0, 8):
            if (i, j) in rects_hitHuman:
                pygame.draw.rect(disp, (255, 0, 0), rects[i][j])
                pygame.display.update(rects[i][j])
            if (i, j) in rects_missedHuman:
                pygame.draw.rect(disp, (0, 0, 255), rects[i][j])
                pygame.display.update(rects[i][j])

def printRectsAI(rects):
    """Draws the squares on the board that have been hit or missed for player AI, only used for testing
    Args:
        rects (8x8 array of pygame.Rect objects): the grid to check on
    """

    for i in range(0, 8):
        for j in range(0, 8):
            if (i, j) in rects_hitAI:
                pygame.draw.rect(disp, (255, 0, 0), rects[i][j])
                pygame.display.update(rects[i][j])
            if (i, j) in rects_missedAI:
                pygame.draw.rect(disp, (0, 0, 255), rects[i][j])
                pygame.display.update(rects[i][j])

def track_toggle():
    """Tracks when the toggle square is pressed by the mouse"""

    global toggled
    newPress = True
    mouseX = 0
    mouseY = 0

    if pygame.mouse.get_pressed() == (1, 0, 0) and newPress:
        newPress = False
        mouseX, mouseY = pygame.mouse.get_pos()
        if isPointInRect(mouseX, mouseY, pygame.Rect(533, 200, 15, 15)):
            if not toggled:
                checkbox = pygame.draw.rect(disp, (0, 0, 0), (533, 200, 15, 15))
                pygame.display.update(pygame.Rect(533, 200, 15, 15))
                toggled = True
                pygame.time.delay(250)
            else:
                checkbox = pygame.draw.rect(disp, (255, 255, 255), (533, 200, 15, 15))
                pygame.display.update(pygame.Rect(533, 200, 15, 15))
                toggled = False
                pygame.time.delay(250)

    elif pygame.mouse.get_pressed() != (1, 0, 0):
        newPress = True

def clear_board(rects):
    """Clears the board of all squares - intended to be used after showing the players own boats
    Args:
        rects (8x8 array of pygame.Rect objects): the grid to check on
    """

    for i in range(0, 8):
        for j in range(0, 8):
            pygame.draw.rect(disp, (192, 192, 192), rects[i][j])
            pygame.display.update(rects[i][j])

def trackPlacement(rects):
    """ tracks the placement of boats on the placeBoats screens for player 1 and 2
    Args:
        rects (8x8 array of pygame.Rect objects): grid to check on
    """

    global turn
    global placeNumber
    global spotsToCheck
    global player1
    global player2
    global playerHuman
    global playerAI
    global opposing_ship1
    global opposing_ship2
    global opposing_shipHuman
    global opposing_shipAI
    global my_ships1
    global my_ships2
    global my_shipsHuman
    global my_shipsAI
    newPress = True
    mouseX = 0

    mouseY = 0
    if pygame.mouse.get_pressed() == (1, 0, 0) and newPress:
        newPress = False
        mouseX, mouseY = pygame.mouse.get_pos()
        for i in range(0, 8):
            for j in range(0, 8):
                if isPointInRect(mouseX, mouseY, rects[i][j]) and (i,j) not in spotsToCheck and len(spotsToCheck) < placeNumber:
                    spotsToCheck.append((i,j))
                    pygame.draw.rect(disp, (0, 0, 0), rects[i][j])
                    pygame.display.update(rects[i][j])

    elif pygame.mouse.get_pressed() != (1, 0, 0) and len(spotsToCheck) == placeNumber:
        newPress = True
        print("spotsToCheck:", spotsToCheck)
        B = Boat()
        replace = []
        overlap = False
        for i in range(len(spotsToCheck)):
            if spotsToCheck[i] in player1.getCoordinateList() and turn % 2 == 0:
                overlap = True
                replace.append(spotsToCheck[i])
            elif spotsToCheck[i] in player2.getCoordinateList() and turn % 2 != 0:
                overlap = True
                replace.append(spotsToCheck[i])
            elif spotsToCheck[i] in playerHuman.getCoordinateList():
                overlap = True
                replace.append(spotsToCheck[i])

        if B.validPlace(spotsToCheck) and overlap == False:
            print("Boat Placed")
            placeNumber += 1
            updateBoatToPlaceText(placeNumber)
            if gameState == "placeBoats1":
                player1.placeShip(B)
                for i in range(len(B.getCoordinates())):
                    my_ships1.append(B.getCoordinates()[i])
                    opposing_ship2.append(B.getCoordinates()[i])
                print("Myships", my_ships1)
            elif gameState == "placeBoats2":
                player2.placeShip(B)
                for i in range(len(B.getCoordinates())):
                    my_ships2.append(B.getCoordinates()[i])
                    opposing_ship1.append(B.getCoordinates()[i])
            elif gameState == "placeBoatsHuman":
                playerHuman.placeShip(B)
                for i in range(len(B.getCoordinates())):
                    my_shipsHuman.append(B.getCoordinates()[i])
                    opposing_shipAI.append(B.getCoordinates()[i])

        else:
            print("Error placing boat")
            for i in spotsToCheck:
                pygame.draw.rect(disp, (192, 192, 192), rects[i[0]][i[1]])
                pygame.draw.rect(disp, (0, 0, 0), rects[i[0]][i[1]], 2)
                pygame.display.update(rects[i[0]][i[1]])
                if overlap == True and i in replace:
                    pygame.draw.rect(disp, (0, 0, 0), rects[i[0]][i[1]])
                    pygame.display.update(rects[i[0]][i[1]])
        spotsToCheck = []
    elif len(spotsToCheck) != placeNumber:
        for i in spotsToCheck:
            pygame.draw.rect(disp, (192, 192, 192), rects[i[0]][i[1]])
            pygame.draw.rect(disp, (0, 0, 0), rects[i[0]][i[1]], 2)
            pygame.display.update(rects[i[0]][i[1]])
        spotsToCheck = []

def trackPlayButton(): #PLAY VS HUMAN
    """ Tracks if the Play button on the welcome screen has been pressed. If it has, setupPlaceBoats(1) is called"""
    global gameState

    if pygame.mouse.get_pressed() == (1, 0, 0):
        mouseX, mouseY = pygame.mouse.get_pos()
        if isPointInRect(mouseX, mouseY, pygame.Rect(disp_width * .33, disp_height * .43, 370, 75)) and not numberOfBoats == 0:
            print("PLAY VS HUMAN CLICKED\n")
            setupPlaceBoats(1)

def trackPlayButton_AI(): #PLAY VS AI
    """ Tracks if the PLAY VS AI button on the welcome screen has been pressed. If it has, ????????????????"""
    global gameState
    global difficulty

    if pygame.mouse.get_pressed() == (1, 0, 0):
        mouseX, mouseY = pygame.mouse.get_pos()
        if isPointInRect(mouseX, mouseY, pygame.Rect(disp_width * .08, disp_height * .55, 260, 75)) and not numberOfBoats == 0: # PLAY VS EASY AI
            print("PLAY VS EASY AI CLICKED\n")
            difficulty = "easy"
            setupPlaceBoatsHuman() # need to change to handle which AI we are playing against

        if isPointInRect(mouseX, mouseY, pygame.Rect(disp_width * .35, disp_height * .55, 330, 75)) and not numberOfBoats == 0: # PLAY VS MEDIUM AI
            print("PLAY VS MEDIUM AI CLICKED\n")
            difficulty = "medium"
            setupPlaceBoatsHuman() # need to change to handle which AI we are playing against

        if isPointInRect(mouseX, mouseY, pygame.Rect(disp_width * .7, disp_height * .55, 270, 75)) and not numberOfBoats == 0: # PLAY VS HARD AI
            print("PLAY VS HARD AI CLICKED\n")
            difficulty = "hard"
            setupPlaceBoatsHuman() # need to change to handle which AI we are playing against

def getSize():
    """Handles the user interface of selecting the size of the boats
    Args:
    None
    Returns:
    size - Number of boats
    """
    global draw_once
    global numberOfBoats
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)

    if draw_once == True:
        pygame.draw.rect(disp, black, (disp_width * .33 , disp_height * .30, 70, 70))
        pygame.draw.rect(disp, black, (disp_width * .33 + 85, disp_height * .30, 70, 70))
        pygame.draw.rect(disp, black, (disp_width * .33 + 170, disp_height * .30, 70, 70))
        pygame.draw.rect(disp, black, (disp_width * .33 + 255, disp_height * .30, 70, 70))
        pygame.draw.rect(disp, black, (disp_width * .33 + 340, disp_height * .30, 70, 70))
        pygame.display.update()
        draw_once = False
    largeText = pygame.font.Font('freesansbold.ttf', 65)
    blackText = pygame.font.Font('freesansbold.ttf', 65)
    medText = pygame.font.Font('freesansbold.ttf', 48)
    smallText = pygame.font.Font('freesansbold.ttf', 36)
    TextSurf, TextRect = text_objects("1", largeText)
    TextSurf2, TextRect2 = text_objects("2", largeText)
    TextSurf3, TextRect3 = text_objects("3", largeText)
    TextSurf4, TextRect4 = text_objects("4", largeText)
    TextSurf5, TextRect5 = text_objects("5", largeText)
    TextRect.center = ((disp_width * .36), (disp_height * .35))
    TextRect2.center = ((disp_width * .36 + 85), (disp_height * .35))
    TextRect3.center = ((disp_width * .36 + 170), (disp_height * .35))
    TextRect4.center = ((disp_width * .36 + 255), (disp_height * .35))
    TextRect5.center = ((disp_width * .36 + 340), (disp_height * .35))
    disp.blit(TextSurf, TextRect)
    disp.blit(TextSurf2, TextRect2)
    disp.blit(TextSurf3, TextRect3)
    disp.blit(TextSurf4, TextRect4)
    disp.blit(TextSurf5, TextRect5)

    if pygame.mouse.get_pressed() == (1, 0, 0):
        mouseX, mouseY = pygame.mouse.get_pos()
        if isPointInRect(mouseX, mouseY, pygame.Rect(disp_width * .33, disp_height * .30, 70, 70)):
            numberOfBoats = 1
            pygame.draw.rect(disp, green, (disp_width * .33, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 85, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 170, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 255, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 340, disp_height * .30, 70, 70))
            TextSurf, TextRect = text_objects("1", largeText)
            TextSurf2, TextRect2 = text_objects("2", largeText)
            TextSurf3, TextRect3 = text_objects("3", largeText)
            TextSurf4, TextRect4 = text_objects("4", largeText)
            TextSurf5, TextRect5 = text_objects("5", largeText)
            pygame.display.update()
        elif isPointInRect(mouseX, mouseY, pygame.Rect(disp_width * .33 + 85, disp_height * .30, 70, 70)):
            numberOfBoats = 2
            pygame.draw.rect(disp, black, (disp_width * .33, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, green, (disp_width * .33 + 85, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 170, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 255, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 340, disp_height * .30, 70, 70))
            TextSurf, TextRect = text_objects("1", largeText)
            TextSurf2, TextRect2 = text_objects("2", largeText)
            TextSurf3, TextRect3 = text_objects("3", largeText)
            TextSurf4, TextRect4 = text_objects("4", largeText)
            TextSurf5, TextRect5 = text_objects("5", largeText)
            pygame.display.update()
        elif isPointInRect(mouseX, mouseY, pygame.Rect(disp_width * .33 + 170, disp_height * .30, 70, 70)):
            numberOfBoats = 3
            pygame.draw.rect(disp, black, (disp_width * .33, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 85, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, green, (disp_width * .33 + 170, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 255, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 340, disp_height * .30, 70, 70))
            TextSurf, TextRect = text_objects("1", largeText)
            TextSurf2, TextRect2 = text_objects("2", largeText)
            TextSurf3, TextRect3 = text_objects("3", largeText)
            TextSurf4, TextRect4 = text_objects("4", largeText)
            TextSurf5, TextRect5 = text_objects("5", largeText)
            pygame.display.update()
        elif isPointInRect(mouseX, mouseY, pygame.Rect(disp_width * .33 + 255, disp_height * .30, 70, 70)):
            numberOfBoats = 4
            pygame.draw.rect(disp, black, (disp_width * .33 , disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 85, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 170, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, green, (disp_width * .33 + 255, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 340, disp_height * .30, 70, 70))
            TextSurf, TextRect = text_objects("1", largeText)
            TextSurf2, TextRect2 = text_objects("2", largeText)
            TextSurf3, TextRect3 = text_objects("3", largeText)
            TextSurf4, TextRect4 = text_objects("4", largeText)
            TextSurf5, TextRect5 = text_objects("5", largeText)
            pygame.display.update()
        elif isPointInRect(mouseX, mouseY, pygame.Rect(disp_width * .33 + 340, disp_height * .30, 70, 70)):
            numberOfBoats = 5
            pygame.draw.rect(disp, black, (disp_width * .33, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 85, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 170, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, black, (disp_width * .33 + 255, disp_height * .30, 70, 70))
            pygame.draw.rect(disp, green, (disp_width * .33 + 340, disp_height * .30, 70, 70))
            TextSurf, TextRect = text_objects("1", largeText)
            TextSurf2, TextRect2 = text_objects("2", largeText)
            TextSurf3, TextRect3 = text_objects("3", largeText)
            TextSurf4, TextRect4 = text_objects("4", largeText)
            TextSurf5, TextRect5 = text_objects("5", largeText)
            pygame.display.update()

    pygame.display.update()


def trackQuitButton():
    """ Tracks if the Quit button on the welcome screen has been pressed. If it has, quitGame() is called"""

    if pygame.mouse.get_pressed() == (1, 0, 0):
        mouseX, mouseY = pygame.mouse.get_pos()
        if isPointInRect(mouseX, mouseY, pygame.Rect(disp_width * .45, disp_height * .68, 120, 75)):
            print("QUIT CLICKED\n")
            quitGame()

def updateBoatToPlaceText(size):
    """ Every time this is called, the text that says "Boat size to place..." on gameState = "placeBoats1"
        or gameState = "placeBoats2" will get redrawn with the new size shown
    Args:
        size (int): should corresponds to size of current boat to place (e.g. global placeNumber)
    """

    disp.fill((192, 192, 192), (350, 150, 200, 40))
    pygame.draw.rect(disp, (192, 192, 192), (570, 150, 50, 50))
    pygame.display.update((350, 150, 200, 40))
    font = pygame.font.SysFont("Times New Roman", 30)
    text = font.render("Boat size to place: " + str(size), True, (0, 0, 0))
    disp.blit(text, (350, 150))
    pygame.display.update()

def showSwitchPlayers(originalTime):
    """ Displays the screen that tells players to switch. Gives players three seconds to do so.
    Args:
        originalTime (pygame.time.get_ticks()): represents the original time (in systicks, represented as int)
                                                that this method was called. It is used agains the current
                                                time in systics to see if three seconds has passed
    """

    global placeNumber
    global gameState

    disp.fill((192, 192, 192))
    player_switch = pygame.font.SysFont('Consolas', 40)
    player_switch_display = player_switch.render("Player 2's Turn in ", False, (0, 0, 0))
    count3 = player_switch.render("3", False, (0, 0, 0))
    count2 = player_switch.render("2", False, (0, 0, 0))
    count1 = player_switch.render("1", False, (0, 0, 0))
    disp.blit(player_switch_display, (300, 100))
    pygame.display.update()
    pygame.time.delay(500)
    disp.blit(count3, (500, 150))
    pygame.display.update()
    pygame.time.delay(500)
    disp.blit(count2, (500, 200))
    pygame.display.update()
    pygame.time.delay(500)
    disp.blit(count1, (500, 250))
    pygame.display.update()
    pygame.time.delay(500)

    setupPlaceBoats(2)

def setupWelcome():
    """ Sets up initial graphics and variables for the welcome state """

    l_blue = (80, 171, 250)
    white = (255, 255, 255)
    black = (0, 0, 0)
    pygame.display.set_caption('Battleboats')
    disp.fill(l_blue)
    largeText = pygame.font.Font('freesansbold.ttf', 65)
    TextSurf, TextRect = text_objects("Welcome to Battleboats", largeText)
    medText = pygame.font.Font('freesansbold.ttf', 42)
    smallText = pygame.font.Font('freesansbold.ttf', 36)
    TextSurf, TextRect = text_objects("Welcome to Battleboats", largeText)

    select_text = pygame.font.SysFont('Consolas', 26)
    select_text_display = select_text.render("Select the number of boats", False, (0, 0, 0))
    disp.blit(select_text_display, (375, disp_height * .25))

    TextRect.center = ((disp_width / 2), (disp_height * .15))

    TextSurf2, TextRect2 = text_objects("PLAY VS HUMAN", medText)
    TextRect2.center = ((disp_width / 2), (disp_height / 2))

    TextSurf6, TextRect6 = text_objects("VS EASY AI", medText) # new code - rob
    TextRect6.center = ((disp_width * .2), (disp_height * .6)) # new code - rob

    TextSurf7, TextRect7 = text_objects("VS MEDIUM AI", medText) # new code - rob
    TextRect7.center = ((disp_width * .5), (disp_height * .6)) # new code - rob

    TextSurf8, TextRect8 = text_objects("VS HARD AI", medText) # new code - rob
    TextRect8.center = ((disp_width * .82), (disp_height * .6)) # new code - rob

    TextSurf3, TextRect3 = text_objects("QUIT", medText)
    TextRect3.center = ((disp_width / 2), (disp_height * .75))

    #makes buttons interactive
    mouse = pygame.mouse.get_pos()
    if disp_width * .33 + 100 > mouse[0] > disp_width * .33 and disp_height * .43 + 50 > mouse[1] > disp_height * .43: # PLAY VS HUMAN IS CLICKABLE
        pygame.draw.rect(disp, white, (disp_width * .33, disp_height * .43, 370, 75))
    elif disp_width * .08 + 100 > mouse[0] > disp_width * .08 and disp_height * .55 + 50 > mouse[1] > disp_height * .55: # PLAY VS EASY AI IS CLICKABLE
        pygame.draw.rect(disp, white, (disp_width * .08, disp_height * .55, 260, 75))
    elif disp_width * .35 + 100 > mouse[0] > disp_width * .35 and disp_height * .55 + 50 > mouse[1] > disp_height * .55: # PLAY VS MEDIUM AI IS CLICKABLE
        pygame.draw.rect(disp, white, (disp_width * .35, disp_height * .55, 330, 75))
    elif disp_width * .7 + 100 > mouse[0] > disp_width * .7 and disp_height * .55 + 50 > mouse[1] > disp_height * .55: # PLAY VS HARD AI IS CLICKABLE
        pygame.draw.rect(disp, white, (disp_width * .7, disp_height * .55, 270, 75))
    elif disp_width * .45 + 100 > mouse[0] > disp_width * .45 and disp_height * .68 + 50 > mouse[1] > disp_height * .68: # QUIT IS CLICKABLE
        pygame.draw.rect(disp, white, (disp_width * .45, disp_height * .68, 120, 75))
    else:
        pygame.draw.rect(disp, l_blue, (disp_width * .33, disp_height * .43, 370, 75)) #BACKGROUND of PLAY VS HUMAN
        pygame.draw.rect(disp, l_blue, (disp_width * .08, disp_height * .55, 260, 75)) #BACKGROUND of PLAY VS EASY AI
        pygame.draw.rect(disp, l_blue, (disp_width * .35, disp_height * .55, 330, 75)) #BACKGROUND of PLAY VS MEDIUM AI
        pygame.draw.rect(disp, l_blue, (disp_width * .7, disp_height * .55, 270, 75)) #BACKGROUND of PLAY VS HARD AI
        pygame.draw.rect(disp, l_blue, (disp_width * .45, disp_height * .68, 120, 75)) #BACKGROUND of QUIT
        pygame.draw.rect(disp, black, (disp_width * .33, disp_height * .43, 370, 75), 5) # PLAY VS HUMAN BOX
        pygame.draw.rect(disp, black, (disp_width * .08, disp_height * .55, 260, 75), 5) # PLAY VS EASY AI BOX
        pygame.draw.rect(disp, black, (disp_width * .35, disp_height * .55, 330, 75), 5) # PLAY VS MEDIUM AI BOX
        pygame.draw.rect(disp, black, (disp_width * .7, disp_height * .55, 270, 75), 5) # PLAY VS HARD AI BOX
        pygame.draw.rect(disp, black, (disp_width * .45, disp_height * .68, 120, 75), 5) # QUIT BOX
    TextRect.center = ((disp_width / 2), (disp_height / 6))
    disp.blit(TextSurf, TextRect) # WELCOME TO BATTLEBOATS
    disp.blit(TextSurf2, TextRect2) # PLAY VS HUMAN
    disp.blit(TextSurf6, TextRect6) # PLAY VS EASY AI
    disp.blit(TextSurf7, TextRect7) # PLAY VS MEDIUM AI
    disp.blit(TextSurf8, TextRect8) # PLAY VS HARD AI
    disp.blit(TextSurf3, TextRect3) # QUIT

    pygame.display.update()

def setupPlaceBoats(whichPlayer):
    """ Sets up initial graphics and variables for the placeBoats state
    Args:
        whichPlayer (int): 1 -> setup the placeBoats state for player 1, 2 -> setup the placeBoates satate for player 2
    """

    global gameState
    global grid
    global placeNumber
    global spotsToCheck

    placeNumber = 1
    spotsToCheck = []
    disp.fill((192, 192, 192))

    font = pygame.font.SysFont("Times New Roman", 40)
    text = font.render("Player " + str(whichPlayer) + ": " + "Place your " + str(numberOfBoats) + " boats", True, (0, 0, 0))
    disp.blit(text, (350, 100))

    updateBoatToPlaceText(1)

    grid = createRects(350, 200)

    pygame.display.update()
    pygame.time.delay(100)
    gameState = "placeBoats" + str(whichPlayer)

def setupPlaceBoatsHuman():
    """ Sets up initial graphics and variables for the placeBoats state for Human in human vs AI
    Args:
        None
    """

    global gameState
    global grid
    global placeNumber
    global spotsToCheck

    placeNumber = 1
    spotsToCheck = []
    disp.fill((192, 192, 192))

    font = pygame.font.SysFont("Times New Roman", 40)
    text = font.render("Player " + "Human" + ": " + "Place your " + str(numberOfBoats) + " boats", True, (0, 0, 0))
    disp.blit(text, (350, 100))

    updateBoatToPlaceText(1)

    grid = createRects(350, 200)

    pygame.display.update()
    pygame.time.delay(100)
    gameState = "placeBoatsHuman"

def setupPlaceBoatsAI():
    #places AI boats
    global my_shipsAI
    global opposing_shipHuman

    for i in range(1,numberOfBoats+1):
        B = Boat()
        goodCoords = 0
        while (goodCoords == 0):
            overlap = False
            spotsToCheck = []
            spotsToCheck = generateBoatLocation(i)
            for x in range(len(spotsToCheck)):
                if spotsToCheck[x] in playerAI.getCoordinateList():
                    overlap = True
            if (overlap == False):
                goodCoords = 1

        if B.validPlace(spotsToCheck) and goodCoords == 1:
            print("AI Boat Placed")
            print(B.getCoordinates()) #for testing only
            if gameState == "None":
                playerAI.placeShip(B)
                for x in range(len(B.getCoordinates())):
                    my_shipsAI.append(B.getCoordinates()[x])
                    opposing_shipHuman.append(B.getCoordinates()[x])

def generateBoatLocation(boatLength):
    #helper function for placing AI boats
    boatDirection = random.randint(0,1)
    returnCoords = []
    if (boatDirection == 0): #generate vertical coordinates
        bottomCoord = random.randint(boatLength - 1,7)
        colCoord = random.randint(0,7)
        returnCoords.append((bottomCoord,colCoord))
        if (boatLength > 1):
            for x in range(1,boatLength): #CHECK
                returnCoords.append((bottomCoord-x,colCoord))
        return returnCoords
    elif (boatDirection == 1): #generate horizontal getCoordinates
        rowCoord = random.randint(0,7)
        rightCoord = random.randint(boatLength - 1,7)
        returnCoords.append((rowCoord,rightCoord))
        if (boatLength > 1):
            for x in range(1,boatLength):
                returnCoords.append((rowCoord,rightCoord-x))
        return returnCoords

def setupGamePlay1():
    """ Sets up initial graphics and variables for the gamePlay state """

    global leftGrid
    global rightGrid
    global gameState

    disp_width = 1080
    disp_height = 720
    disp = pygame.display.set_mode((disp_width, disp_height))
    disp.fill((192, 192, 192))
    pygame.display.set_caption('Battleboats')
    player_turn = pygame.font.SysFont('Consolas', 40)

    player_switch = pygame.font.SysFont('Consolas', 40)
    player_switch_display=player_switch.render("Player 1's Turn in ", False, (0, 0, 0))
    count3 = player_switch.render("3", False, (0, 0, 0))
    count2 = player_switch.render("2", False, (0, 0, 0))
    count1 = player_switch.render("1", False, (0, 0, 0))
    disp.blit(player_switch_display, (320, 100))
    pygame.display.update()
    pygame.time.delay(500)
    disp.blit(count3, (500, 150))
    pygame.display.update()
    pygame.time.delay(500)
    disp.blit(count2, (500, 200))
    pygame.display.update()
    pygame.time.delay(500)
    disp.blit(count1, (500, 250))
    pygame.display.update()
    pygame.time.delay(500)

    disp.fill((192, 192, 192))
    player_turn_display = player_turn.render("Player 1's Turn", False, (0, 0, 0))
    toggle = pygame.font.SysFont('Ariel', 20)
    toggle_display = toggle.render('SHOW MY BOATS', False, (0, 0, 0))
    checkbox = pygame.draw.rect(disp, (255, 255, 255), (533, 200, 15, 15))
    toggled = False
    board_cleared = True
    track_toggle()
    disp.blit(player_turn_display, (350, 100))
    disp.blit(toggle_display, (548, 200))
    leftGrid = createRects(200, 200)
    rightGrid = createRects(500, 200)
    gameState = "gamePlay1"

def setupGamePlay2():
    """ Sets up initial graphics and variables for the gamePlay state """

    global leftGrid
    global rightGrid
    global gameState

    disp_width = 1080
    disp_height = 720
    disp = pygame.display.set_mode((disp_width, disp_height))
    disp.fill((192, 192, 192))
    pygame.display.set_caption('Battleboats')
    player_turn = pygame.font.SysFont('Consolas', 40)

    player_switch = pygame.font.SysFont('Consolas', 40)
    player_switch_display = player_switch.render("Player 2's Turn in ", False, (0, 0, 0))
    count3 = player_switch.render("3", False, (0, 0, 0))
    count2 = player_switch.render("2", False, (0, 0, 0))
    count1 = player_switch.render("1", False, (0, 0, 0))
    disp.blit(player_switch_display, (320, 100))
    pygame.display.update()
    pygame.time.delay(500)
    disp.blit(count3, (500, 150))
    pygame.display.update()
    pygame.time.delay(500)
    disp.blit(count2, (500, 200))
    pygame.display.update()
    pygame.time.delay(500)
    disp.blit(count1, (500, 250))
    pygame.display.update()
    pygame.time.delay(500)

    disp.fill((192, 192, 192))
    player_turn_display = player_turn.render("Player 2's Turn", False, (0, 0, 0))
    toggle = pygame.font.SysFont('Ariel', 20)
    toggle_display = toggle.render('  SHOW MY BOATS', False, (0, 0, 0))
    checkbox = pygame.draw.rect(disp, (255, 255, 255), (533, 200, 15, 15))
    toggled = False
    board_cleared = True
    track_toggle()
    disp.blit(player_turn_display, (350, 100))
    disp.blit(toggle_display, (548, 200))
    leftGrid = createRects(200, 200)
    rightGrid = createRects(500, 200)
    gameState = "gamePlay2"

def setupGamePlayHuman():
    """ Sets up initial graphics and variables for the gamePlay state """

    global leftGrid
    global rightGrid
    global gameState

    disp_width = 1080
    disp_height = 720
    disp = pygame.display.set_mode((disp_width, disp_height))
    disp.fill((192, 192, 192))
    pygame.display.set_caption('Battleboats')
    player_turn = pygame.font.SysFont('Consolas', 40)

    player_switch = pygame.font.SysFont('Consolas', 40)
    player_switch_display = player_switch.render("Player Human's Turn in ", False, (0, 0, 0))
    count3 = player_switch.render("3", False, (0, 0, 0))
    count2 = player_switch.render("2", False, (0, 0, 0))
    count1 = player_switch.render("1", False, (0, 0, 0))
    disp.blit(player_switch_display, (320, 100))
    pygame.display.update()
    pygame.time.delay(500)
    disp.blit(count3, (500, 150))
    pygame.display.update()
    pygame.time.delay(500)
    disp.blit(count2, (500, 200))
    pygame.display.update()
    pygame.time.delay(500)
    disp.blit(count1, (500, 250))
    pygame.display.update()
    pygame.time.delay(500)

    disp.fill((192, 192, 192))
    player_turn_display = player_turn.render("Player Human's Turn", False, (0, 0, 0))
    toggle = pygame.font.SysFont('Ariel', 20)
    toggle_display = toggle.render('  SHOW MY BOATS', False, (0, 0, 0))
    checkbox = pygame.draw.rect(disp, (255, 255, 255), (533, 200, 15, 15))
    toggled = False
    board_cleared = True
    track_toggle()
    disp.blit(player_turn_display, (350, 100))
    disp.blit(toggle_display, (548, 200))
    leftGrid = createRects(200, 200)
    rightGrid = createRects(500, 200)
    print("game state becoming human") #testing
    gameState = "gamePlayHuman"

def setupGamePlayAI():
    global gameState
    gameState = "gamePlayAI"

def winState():
    """ Lets the player know that they won """
    l_blue = (80, 171, 250)
    white = (255, 255, 255)
    black = (0, 0, 0)
    disp.fill(l_blue)
    #Display the Winner of the game

    if(winner == "Player 1" or winner == "Player 2"):
        largeText = pygame.font.Font('freesansbold.ttf', 65)
        text = winner + " wins!"
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((disp_width / 2), (disp_height * .17))
        disp.blit(TextSurf, TextRect)
        #pygame.display.update()
        gameState = "winner"


        #Score board for Player 1
        largeText_2 = pygame.font.Font('freesansbold.ttf', 53)
        text_Player1 = "Player 1"
        TextSurf, TextRect = text_objects(text_Player1, largeText_2) #creates text surface variable and text rectangle variable
        TextRect.center = ((disp_width / 4.2),(disp_height * .39)) # modifies the center of text rectangle based on pygame GUI window
        disp.blit(TextSurf, TextRect)
        #pygame.display.update() # updates pygame window
        gameState = "winner"

        largeTextForScore = pygame.font.Font('freesansbold.ttf', 42)

        text_Player1_Attack = "Total Attacked: " + (str(totalAttackPlayer1))
        TextSurf, TextRect = text_objects(text_Player1_Attack, largeTextForScore) #creates text surface variable and text rectangle variable
        TextRect.center = ((disp_width / 4), (disp_height * .55)) # modifies the center of text rectangle based on pygame GUI window
        disp.blit(TextSurf, TextRect)
        #pygame.display.update() # updates pygame window
        gameState = "winner"


        hit1 = ((totalhitPlayer1 / totalAttackPlayer1) * 100)
        hit1Percentage = round(hit1, 2)
        missed1 = ((totalMissedPlayer1 / totalAttackPlayer1) * 100)
        missed1Percentage = round(missed1, 2)

        text_Player1_Hit = "Hit in %: " + str(hit1Percentage)
        TextSurf, TextRect = text_objects(text_Player1_Hit, largeTextForScore) #creates text surface variable and text rectangle variable
        TextRect.center = ((disp_width / 4), (disp_height * .65)) # modifies the center of text rectangle based on pygame GUI window
        disp.blit(TextSurf, TextRect)
        #pygame.display.update() # updates pygame window
        gameState = "winner"

        text_Player1_Miss = "Missed in %: " + str(missed1Percentage)
        TextSurf, TextRect = text_objects(text_Player1_Miss, largeTextForScore) #creates text surface variable and text rectangle variable
        TextRect.center = ((disp_width / 4), (disp_height * .75)) # modifies the center of text rectangle based on pygame GUI window
        disp.blit(TextSurf, TextRect)
        #pygame.display.update() # updates pygame window
        gameState = "winner"



        #Score board for Player 2
        text_Player2 = "Player 2"
        TextSurf, TextRect = text_objects(text_Player2, largeText_2) #creates text surface variable and text rectangle variable
        TextRect.center = ((disp_width / 1.3), (disp_height * .39)) # modifies the center of text rectangle based on pygame GUI window
        disp.blit(TextSurf, TextRect)
        #pygame.display.update() # updates pygame window
        gameState = "winner"


        text_Player2_Attack = "Total Attacked: " + (str(totalAttackPlayer2))
        TextSurf, TextRect = text_objects(text_Player2_Attack, largeTextForScore) #creates text surface variable and text rectangle variable
        TextRect.center = ((disp_width / 1.3), (disp_height * .55)) # modifies the center of text rectangle based on pygame GUI window
        disp.blit(TextSurf, TextRect)
        #pygame.display.update() # updates pygame window
        gameState = "winner"

        if(totalAttackPlayer2 > 0):
            hit2 = ((totalhitPlayer2 / totalAttackPlayer2) * 100)
            hit2Percentage = round(hit2, 2)
            missed2 = ((totalMissedPlayer2 / totalAttackPlayer2) * 100)
            missed2Percentage = round(missed2, 2)

            text_Player2_Hit = "Hit in %: " + str(hit2Percentage)
            TextSurf, TextRect = text_objects(text_Player2_Hit, largeTextForScore) #creates text surface variable and text rectangle variable
            TextRect.center = ((disp_width / 1.3), (disp_height * .65)) # modifies the center of text rectangle based on pygame GUI window
            disp.blit(TextSurf, TextRect)
            #pygame.display.update() # updates pygame window
            gameState = "winner"

            text_Player2_Miss = "Missed in %: " + str(missed2Percentage)
            TextSurf, TextRect = text_objects(text_Player2_Miss, largeTextForScore) #creates text surface variable and text rectangle variable
            TextRect.center = ((disp_width / 1.3), (disp_height * .75)) # modifies the center of text rectangle based on pygame GUI window
            disp.blit(TextSurf, TextRect)
            pygame.display.update() # updates pygame window
            gameState = "winner"
        else:
            text_Player2_Hit = "Hit in %: " + "none"
            TextSurf, TextRect = text_objects(text_Player2_Hit, largeTextForScore) #creates text surface variable and text rectangle variable
            TextRect.center = ((disp_width / 1.3), (disp_height * .65)) # modifies the center of text rectangle based on pygame GUI window
            disp.blit(TextSurf, TextRect)
            #pygame.display.update() # updates pygame window
            gameState = "winner"

            text_Player2_Miss = "Missed in %: " + "none"
            TextSurf, TextRect = text_objects(text_Player2_Miss, largeTextForScore) #creates text surface variable and text rectangle variable
            TextRect.center = ((disp_width / 1.3), (disp_height * .75)) # modifies the center of text rectangle based on pygame GUI window
            disp.blit(TextSurf, TextRect)
            pygame.display.update() # updates pygame window
            gameState = "winner"

    if(winner == "Player Human" or winner == "Player AI"):
        largeText = pygame.font.Font('freesansbold.ttf', 65)
        text = winner + " wins!"
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((disp_width / 2), (disp_height * .17))
        disp.blit(TextSurf, TextRect)
        #pygame.display.update()
        gameState = "winner"


        #Score board for Player Human
        largeText_2 = pygame.font.Font('freesansbold.ttf', 53)
        text_Player1 = "Player Human"
        TextSurf, TextRect = text_objects(text_Player1, largeText_2) #creates text surface variable and text rectangle variable
        TextRect.center = ((disp_width / 4.2), (disp_height * .39)) # modifies the center of text rectangle based on pygame GUI window
        disp.blit(TextSurf, TextRect)
        #pygame.display.update() # updates pygame window
        gameState = "winner"

        largeTextForScore = pygame.font.Font('freesansbold.ttf', 42)

        text_Player1_Attack = "Total Attacked: " + (str(totalAttackHuman))
        TextSurf, TextRect = text_objects(text_Player1_Attack, largeTextForScore) #creates text surface variable and text rectangle variable
        TextRect.center = ((disp_width / 4), (disp_height * .55)) # modifies the center of text rectangle based on pygame GUI window
        disp.blit(TextSurf, TextRect)
        #pygame.display.update() # updates pygame window
        gameState = "winner"


        hit1 = ((totalhitHuman / totalAttackHuman) * 100)
        hit1Percentage = round(hit1, 2)
        missed1 = ((totalMissedHuman / totalAttackHuman) * 100)
        missed1Percentage = round(missed1, 2)

        text_Player1_Hit = "Hit in %: " + str(hit1Percentage)
        TextSurf, TextRect = text_objects(text_Player1_Hit, largeTextForScore) #creates text surface variable and text rectangle variable
        TextRect.center = ((disp_width / 4), (disp_height * .65)) # modifies the center of text rectangle based on pygame GUI window
        disp.blit(TextSurf, TextRect)
        #pygame.display.update() # updates pygame window
        gameState = "winner"

        text_Player1_Miss = "Missed in %: " + str(missed1Percentage)
        TextSurf, TextRect = text_objects(text_Player1_Miss, largeTextForScore) #creates text surface variable and text rectangle variable
        TextRect.center = ((disp_width / 4), (disp_height * .75)) # modifies the center of text rectangle based on pygame GUI window
        disp.blit(TextSurf, TextRect)
        #pygame.display.update() # updates pygame window
        gameState = "winner"



        #Score board for Player AI
        text_Player2 = "Player AI"
        TextSurf, TextRect = text_objects(text_Player2, largeText_2) #creates text surface variable and text rectangle variable
        TextRect.center = ((disp_width / 1.3), (disp_height * .39)) # modifies the center of text rectangle based on pygame GUI window
        disp.blit(TextSurf, TextRect)
        #pygame.display.update() # updates pygame window
        gameState = "winner"


        text_Player2_Attack = "Total Attacked: " + (str(totalAttackAI))
        TextSurf, TextRect = text_objects(text_Player2_Attack, largeTextForScore) #creates text surface variable and text rectangle variable
        TextRect.center = ((disp_width / 1.3), (disp_height * .55)) # modifies the center of text rectangle based on pygame GUI window
        disp.blit(TextSurf, TextRect)
        #pygame.display.update() # updates pygame window
        gameState = "winner"

        if(totalAttackAI > 0):
            hit2 = ((totalhitPlayer2 / totalAttackAI) * 100)
            hit2Percentage = round(hit2, 2)
            missed2 = ((totalMissedPlayer2 / totalAttackAI) * 100)
            missed2Percentage = round(missed2, 2)

            text_Player2_Hit = "Hit in %: " + str(hit2Percentage)
            TextSurf, TextRect = text_objects(text_Player2_Hit, largeTextForScore) #creates text surface variable and text rectangle variable
            TextRect.center = ((disp_width / 1.3), (disp_height * .65)) # modifies the center of text rectangle based on pygame GUI window
            disp.blit(TextSurf, TextRect)
            #pygame.display.update() # updates pygame window
            gameState = "winner"

            text_Player2_Miss = "Missed in %: " + str(missed2Percentage)
            TextSurf, TextRect = text_objects(text_Player2_Miss, largeTextForScore) #creates text surface variable and text rectangle variable
            TextRect.center = ((disp_width / 1.3), (disp_height * .75)) # modifies the center of text rectangle based on pygame GUI window
            disp.blit(TextSurf, TextRect)
            pygame.display.update() # updates pygame window
            gameState = "winner"
        else:
            text_Player2_Hit = "Hit in %: " + "none"
            TextSurf, TextRect = text_objects(text_Player2_Hit, largeTextForScore) #creates text surface variable and text rectangle variable
            TextRect.center = ((disp_width / 1.3), (disp_height * .65)) # modifies the center of text rectangle based on pygame GUI window
            disp.blit(TextSurf, TextRect)
            #pygame.display.update() # updates pygame window
            gameState = "winner"

            text_Player2_Miss = "Missed in %: " + "none"
            TextSurf, TextRect = text_objects(text_Player2_Miss, largeTextForScore) #creates text surface variable and text rectangle variable
            TextRect.center = ((disp_width / 1.3), (disp_height * .75)) # modifies the center of text rectangle based on pygame GUI window
            disp.blit(TextSurf, TextRect)
            pygame.display.update() # updates pygame window
            gameState = "winner"

if __name__ == "__main__":
    setupWelcome()

    while True:
        event_handler()
        if gameState == "welcome":
            trackPlayButton()
            trackPlayButton_AI()
            getSize()
            num_destroyed = numberOfBoats
            if numberOfBoats <= 5 and numberOfBoats > 0:
                trackPlayButton()
                trackPlayButton_AI()
            trackQuitButton()

        elif gameState == "placeBoats1":
            if placeNumber <= numberOfBoats:
                trackPlacement(grid)
            else:
                gameState = "None"
                turn +=1
                showSwitchPlayers(pygame.time.get_ticks())

        elif gameState == "placeBoats2":
            if placeNumber <= numberOfBoats:
                trackPlacement(grid)
            else:
                gameState = "None"
                setupGamePlay1()

        elif gameState == "placeBoatsHuman":
            if placeNumber <= numberOfBoats:
                trackPlacement(grid)
            else:
                gameState = "None"
                turn +=1
                setupPlaceBoatsAI()
                setupGamePlayHuman()

        elif gameState == "gamePlay1":
            if player2.shipsDestroyed() == num_destroyed:
                winner = "Player 1"
                gameState = "winner"
                winState()
            printRects1(leftGrid)
            printRects2(rightGrid)
            trackRects1(leftGrid)
            track_toggle()

            sunk_text = pygame.font.SysFont('Consolas', 30)
            sunk_text_display = sunk_text.render("Battleboats you've sunk:", False, (0, 0, 0))
            disp.blit(sunk_text_display, (340, 590))
            pygame.display.update()
            largeText = pygame.font.Font('freesansbold.ttf', 30)
            i = 0
            for index in range(0, numberOfBoats):
                if player2.getShip(index).checkDestroyed():
                    num = largeText.render("1x" + str(index + 1), False, (255, 0, 0))
                    disp.blit(num, ((disp_width * .34 + i), (disp_height * .90)))
                    pygame.display.update()
                else:
                    destroyed_num = largeText.render("1x" + str(index + 1), False, (255, 255, 255))
                    disp.blit(destroyed_num, ((disp_width * .34 + i), (disp_height * .90)))
                    pygame.display.update()
                i = i + 87

            if toggled and board_cleared:
                showboat1(rightGrid)
                board_cleared = False
            if not toggled and not board_cleared:
                clear_board(rightGrid)
                rightGrid = createRects(500, 200)
                board_cleared = True

        elif gameState == "gamePlay2":
            if player1.shipsDestroyed() == num_destroyed:
                winner = "Player 2"
                gameState = "winner"
                winState()
            printRects2(leftGrid)
            printRects1(rightGrid)
            trackRects2(leftGrid)
            track_toggle()

            sunk_text = pygame.font.SysFont('Consolas', 30)
            sunk_text_display = sunk_text.render("Battleboats you've sunk:", False, (0, 0, 0))
            disp.blit(sunk_text_display, (340, 590))
            pygame.display.update()
            largeText = pygame.font.Font('freesansbold.ttf', 30)
            i = 0
            for index in range(0,numberOfBoats):
                if player1.getShip(index).checkDestroyed():
                    num = largeText.render("1x" + str(index + 1), False, (255, 0, 0))
                    disp.blit(num, ((disp_width * .34 + i), (disp_height * .90)))
                    pygame.display.update()
                else:
                    destroyed_num = largeText.render("1x" + str(index + 1), False, (255, 255, 255))
                    disp.blit(destroyed_num, ((disp_width * .34 + i), (disp_height * .90)))
                    pygame.display.update()
                i = i + 87

            if toggled and board_cleared:
                showboat2(rightGrid)
                board_cleared = False
            if not toggled and not board_cleared:
                clear_board(rightGrid)
                rightGrid = createRects(500, 200)
                board_cleared = True
        elif gameState == "gamePlayHuman":
            print("GAME STATE HUMAN")
            if playerAI.shipsDestroyed() == num_destroyed:
                winner = "Player Human"
                gameState = "winner"
                winState()
            printRectsHuman(leftGrid)
            printRectsAI(rightGrid)
            trackRectsHuman(leftGrid)
            track_toggle()

            sunk_text = pygame.font.SysFont('Consolas', 30)
            sunk_text_display = sunk_text.render("Battleboats you've sunk:", False, (0, 0, 0))
            disp.blit(sunk_text_display, (340, 590))
            pygame.display.update()
            largeText = pygame.font.Font('freesansbold.ttf', 30)
            i = 0
            for index in range(0,numberOfBoats):
                if playerAI.getShip(index).checkDestroyed():
                    num = largeText.render("1x" + str(index + 1), False, (255, 0, 0))
                    disp.blit(num, ((disp_width * .34 + i), (disp_height * .90)))
                    pygame.display.update()
                else:
                    destroyed_num = largeText.render("1x" + str(index + 1), False, (255, 255, 255))
                    disp.blit(destroyed_num, ((disp_width * .34 + i), (disp_height * .90)))
                    pygame.display.update()
                i = i + 87

            if toggled and board_cleared:
                showboatHuman(rightGrid)
                board_cleared = False
            if not toggled and not board_cleared:
                clear_board(rightGrid)
                rightGrid = createRects(500, 200)
                board_cleared = True
        elif gameState == "gamePlayAI":
            if playerHuman.shipsDestroyed() == num_destroyed:
                winner = "Player AI"
                gameState = "winner"
                winState()
            print("callingTrackRectsAI") #for testing
            trackRectsAI(leftGrid, difficulty)

        elif gameState == "winner":
            winState()
        clock.tick(30)
