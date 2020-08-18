from Classes import Button, InputBox,Menu,pygame, University

black,white = (0,0,0), (255,255,255)
screen = pygame.display.set_mode((1000, 800))
titlefont = pygame.font.Font(None, 100)
smallfont = pygame.font.Font(None, 30)

title = titlefont.render("University Budget Calculator", True, black)
exceptiontxt = smallfont.render("University not found", True, black)
uniinpt = InputBox(280,500,500,50,[white,black],pygame.font.Font(None, 45))
notFound = False
mode = 0

while True:
    for event in pygame.event.get():
        if uniinpt.handle_event(event,False,25):
            unifname = uniinpt.text.lower()
            try:
                unifile = open(unifname+'.txt', 'r')
                
                mode = 1
            except:
                notFound = True
    screen.fill(white)
    if mode == 0:
        uniinpt.active = True
        uniinpt.draw(screen)
        if notFound:
            screen.blit(exceptiontxt, (300, 560))
        screen.blit(title, (100,100))
    if mode >= 1:
        uniclass = University(unifile)
        screen.blit(uniclass.rendersect[mode-1], (100,100))
        
    pygame.display.update()

