import pygame



class spaceShips:
    def __init__(self , WIDTH , HEIGHT):
        self.spaceShipWidth , self.spaceShipHeight = 50 , 50
        self.vel = 10
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.images(WIDTH , HEIGHT)
        self.yellowScore = 0
        self.redScore = 0


    def images(self , WIDTH , HEIGHT):
        self.background = pygame.image.load('./AllPhotos/space.png')
        self.background = pygame.transform.scale(self.background , (WIDTH , HEIGHT))

        self.yellowSpaceShip = pygame.image.load('./AllPhotos/spaceship_yellow.png')
        self.redSpaceShip = pygame.image.load('./AllPhotos/spaceship_red.png')
        self.yellowSpaceShip = pygame.transform.rotate(pygame.transform.scale(self.yellowSpaceShip , (self.spaceShipWidth , self.spaceShipHeight)) , (90))
        self.redSpaceShip = pygame.transform.rotate(pygame.transform.scale(self.redSpaceShip , (self.spaceShipWidth , self.spaceShipHeight)) , (-90))

    def draw(self , WIN , yellow_x , red_x , yellow_y , red_y):
        self.hitBoxYellow = (yellow_x , yellow_y , self.spaceShipWidth , self.spaceShipHeight)
        self.hitBoxRed =  (red_x , red_y , self.spaceShipWidth , self.spaceShipHeight) 

        WIN.blit(self.yellowSpaceShip , ( yellow_x , yellow_y))
        # pygame.draw.rect(WIN , "yellow" , self.hitBoxYellow , 1)

        WIN.blit(self.redSpaceShip , ( red_x , red_y))
        # pygame.draw.rect(WIN , "red" ,self.hitBoxRed, 1)

    def redHit(self):
        self.yellowScore += 1
        print("Red Was Hitted")

    def yellowHit(self):
        self.redScore += 1
        print("Yellow Was Hitted")



class bullets:
    def __init__(self , x , y , WIDTH):
        self.x = x
        self.y = y
        self.width , self.height = 20 , 5
        self.end = WIDTH
        self.vel = 20

    def drawYellow(self , WIN):
        self.yellowMove()
        pygame.draw.rect(WIN , "yellow" , (self.x , self.y , self.width , self.height)  )

    def yellowMove(self):
        self.x = self.x + self.vel

    def drawRed(self , WIN):
        self.redMove()
        pygame.draw.rect(WIN , "red" , (self.x , self.y , self.width , self.height)  )

    def redMove(self):
        self.x = self.x - self.vel
        

def gameOver(winner , WIN , ship , yellow_bullet , red_bullet ):
    if winner == 'yellow':
        gameResult = pygame.image.load('./AllPhotos/winnerYellow.png')
        WIN.blit(gameResult , (((ship.WIDTH // 2) - (gameResult.get_width() //2)) ,  (ship.HEIGHT // 2) - (gameResult.get_height() // 2)))
    elif winner == 'red':
        gameResult = pygame.image.load('./AllPhotos/winnerRed.png')
        WIN.blit(gameResult , (((ship.WIDTH // 2) - (gameResult.get_width() //2)) ,  (ship.HEIGHT // 2) - (gameResult.get_height() // 2)))
    else:
        backgroundImage1 = pygame.image.load('./AllPhotos/walpaperStarting.jpg')
        backgroundImage1 = pygame.transform.scale(backgroundImage1 , (ship.WIDTH , ship.HEIGHT))
        backgroundImage2 = pygame.image.load('./AllPhotos/title.png')
        backgroundImage2 = pygame.transform.scale(backgroundImage2 , (600 , 400))
        WIN.blit(backgroundImage1 , (0,0))
        WIN.blit(backgroundImage2 , (150,-50))


    pygame.display.update()

    gameRestart = False
    while not(gameRestart):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_KP_ENTER]:
                gameRestart = True
                ship.yellowScore = 0
                ship.redScore = 0
                red_bullet.clear()
                yellow_bullet.clear()
                ship.yellow_x = ((ship.WIDTH // 2) * 0.20)
                ship.red_x = (ship.WIDTH // 2) + ((ship.WIDTH // 2)*0.70)
                ship.yellow_y = 100
                ship.red_y = 100



def drawWindow(WIN , yellow_x , red_x , yellow_y , red_y , ship , leftSection , rightSection , yellow_bullet , red_bullet , spaceShipBlast):
    global winner

    WIN.blit(ship.background , (0,0))

    pygame.draw.rect(WIN , (0,0,0) , leftSection , 5)
    pygame.draw.rect(WIN , (0,0,0) , rightSection , 5)
    text1 = pygame.font.SysFont('comicsans' , 30 , True)
    text2 = pygame.font.SysFont('comicsans' , 30 , True)

    font1 = text1.render("Score : " + str(ship.yellowScore), 1 , (0,0,0))
    font2 = text2.render("Score : " + str(ship.redScore) , 1 , (0,0,0))
    WIN.blit(font1 , (100 , 10))
    WIN.blit(font2 , (600 , 10))

    ship.draw(WIN , yellow_x , red_x , yellow_y , red_y)

    if ship.yellowScore == 10:
        gameOver('yellow' , WIN , ship , yellow_bullet , red_bullet )
    elif ship.redScore == 10:
        gameOver('red' , WIN , ship , yellow_bullet , red_bullet )
        

    for bullet in yellow_bullet:
        if bullet.x + bullet.width > ship.hitBoxRed[0] and bullet.y + bullet.height > ship.hitBoxRed[1] and bullet.y + bullet.height < ship.hitBoxRed[1] + ship.hitBoxRed[3]:
            ship.redHit()
            if bullet in yellow_bullet:
                yellow_bullet.remove(bullet)
            else:
                print("Error was occured : \n we ignored")

        if bullet.x + bullet.vel < bullet.end:
            bullet.drawYellow(WIN)
        else:
            if bullet in yellow_bullet:
                yellow_bullet.remove(bullet)
            else:
                print("Error was occured : \n we ignored")

    for bullet in red_bullet:
        if bullet.x < ship.hitBoxYellow[0] + ship.hitBoxYellow[3] and bullet.y + bullet.height > ship.hitBoxYellow[1] and bullet.y + bullet.height < ship.hitBoxYellow[1] + ship.hitBoxYellow[3]:
            ship.yellowHit()
            if bullet in red_bullet:
                red_bullet.remove(bullet)
            else:
                print("Error was occured : \n we ignored")

        if bullet.x + bullet.vel > 0:
            bullet.drawRed(WIN)
        else:
            if bullet in red_bullet:
                red_bullet.remove(bullet)
            else:
                print("Error was occured : \n we ignored")

    pygame.display.update()


def main():
    pygame.init()
    pygame.font.init()

    WIDTH , HEIGHT = 900 , 600
    FPS = 60
    yellow_bullet = []
    red_bullet = []
    winner = ''

    spaceShipBlast = pygame.mixer.Sound('./AllPhotos/Grenade+1.mp3')
    spaceShipShoot = pygame.mixer.Sound('./AllPhotos/Gun+Silencer.mp3')

    
    yellow_x = ((WIDTH // 2) * 0.20)
    red_x = (WIDTH // 2) + ((WIDTH // 2)*0.70)
    yellow_y = 100
    red_y = 100
    yShootLoop = 0
    rShootLoop = 0


    WIN = pygame.display.set_mode((WIDTH , HEIGHT))
    pygame.display.set_caption('Space Battle')

    leftSection = (0 , 0 ,WIDTH // 2 , HEIGHT)
    rightSection = ( WIDTH // 2 , 0 , WIDTH // 2  , HEIGHT)


    ship = spaceShips(WIDTH , HEIGHT)

    

    clock = pygame.time.Clock()

    gameOver(winner , WIN , ship , yellow_bullet , red_bullet)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    

        keys = pygame.key.get_pressed()

        if yShootLoop > 0:
            yShootLoop += 1
        if yShootLoop > 3:
            yShootLoop = 0

            
        if rShootLoop > 0:
            rShootLoop += 1
        if rShootLoop > 3:
            rShootLoop = 0

        


        if keys[pygame.K_UP] and red_y > 0 + 100:
            red_y = red_y - ship.vel
        if keys[pygame.K_DOWN] and red_y < HEIGHT - ship.spaceShipHeight - 10:
            red_y = red_y + ship.vel
        
        if keys[pygame.K_w] and yellow_y > 0 + 100:
            yellow_y = yellow_y - ship.vel
        if keys[pygame.K_s] and yellow_y < HEIGHT - ship.spaceShipHeight - 10:
            yellow_y = yellow_y + ship.vel

        if keys[pygame.K_LSHIFT] and yShootLoop == 0:
            spaceShipBlast.play()
            if len(yellow_bullet) < 3:
                y_bul = bullets(yellow_x , yellow_y , WIDTH)
                yellow_bullet.append(y_bul)
                yShootLoop = 1

        if keys[pygame.K_RSHIFT] and rShootLoop == 0:
            spaceShipShoot.play()
            if len(red_bullet) < 3:
                r_bul = bullets(red_x , red_y , WIDTH)
                red_bullet.append(r_bul)
                rShootLoop = 1
        
        drawWindow(WIN , yellow_x + (ship.spaceShipWidth / 2) , red_x - (ship.spaceShipWidth / 2) , yellow_y - (ship.spaceShipHeight / 2), red_y - (ship.spaceShipHeight / 2), ship , leftSection , rightSection , yellow_bullet , red_bullet , spaceShipBlast)


    pygame.quit()


if __name__ == '__main__':
    main()