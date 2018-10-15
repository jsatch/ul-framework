import sys, pygame

def se_encuentra_dentro(posx, posy, rect):
    if posx >= rect.left and posy >= rect.top:
        return True
    else:
        return False

def main ():
    pygame.init()

    size = width, height = 320, 240
    speed = [2, 2]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    ball = pygame.image.load("./imagenes/intro_ball.gif")
    ballrect = ball.get_rect()
    puntaje = 0

    while 1:
        posx = 0
        posy = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                print("El puntaje fue de {}".format(puntaje))
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                posx, posy = pygame.mouse.get_pos()

        if se_encuentra_dentro(posx, posy, ballrect):
            puntaje = puntaje + 1

        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        screen.fill(black)
        screen.blit(ball, ballrect)
        pygame.display.flip()

if __name__ == "__main__":
    main()