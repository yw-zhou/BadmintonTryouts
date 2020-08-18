# --------------------------------------------------------------------
# Program: Classes list for Final Project and Pixel Art 
# Author: Yi Wei Zhou
# Date: 23/01/2019
# Description: Contains all the classes and functions that are imported
#  by MainFile
# --------------------------------------------------------------------

#imports and variable definitions 
import pygame, sys
pygame.init()

#sys.setrecursionlimit(2000)

#groups and object with an anchor so when moving the anchor, everything else
#will move accordingly
class Group ():
    def __init__(self,anchor, objects):
        self.needdraw,self.anchor = [],anchor
        for descript in objects: #gets the coordinates in relation to the anchor
            if descript[0] == 'inpt': descript[1].rect.x, descript[1].rect.y = anchor[0]+descript[2], anchor[1]+descript[3]
            elif descript[0] == 'btn':descript[1].pos = (anchor[0]+descript[2], anchor[1]+descript[3])
            else:self.needdraw.append(descript[1:])            
    def draw(self,screen,pos = None): #draws the group where the anchor is at the pos given
        if pos == None: pos = self.anchor
        for img in self.needdraw:
            screen.blit(img[0], (pos[0]+img[1],pos[1]+img[2]))
            
##puts an object at the centre of the screen (width only)
def stagecentre (objtype, obj,screen):
    w,h = screen.get_size()
    if objtype == 'img':
        width,height = obj.get_size()
    elif objtype == 'btn':
        width = obj.width
    elif objtype == 'rect':
        width = obj.w
    return (w-width)//2

#reads the file and returns a list of its contents
def readfile():
    filename = open('filenames.txt','r')
    namelst = []
    while True:
        name = filename.readline().strip()
        if name == '':break
        else: namelst.append(name)
    filename.close()
    return namelst
            
class Pixel():
    def __init__(self, width, height, colour,pos):
        self.width,self.height,self.colour,self.pos,self.outline,self.lcolour = width, height, colour,pos,1,(100,100,100)
        
    def draw(self,screen,pos = None):
        if pos!= None: self.pos = pos
        pygame.draw.rect(screen,self.colour,(self.pos[0],self.pos[1],self.width,self.height))
        pygame.draw.rect(screen,self.lcolour,(self.pos[0],self.pos[1],self.width,self.height),self.outline)

    def selectfill(self, colour,canfill):
        if colour != None: self.colour = colour  
        if not canfill:self.outline,self.lcolour = 2,(0,0,0)

class Button(Pixel):
    def __init__(self, width, height, colour, image,pos):
        Pixel.__init__(self, width, height, colour,pos)
        self.visible,self.font,self.text= True,pygame.font.Font(None, height-5),''
        if image!= None:self.image = pygame.transform.scale(image,(int(self.width*0.9),int(self.height*0.9)))
        else: self.image = image
    def draw(self,screen, pos = None):
        if self.visible:
            if self.colour != None:Pixel.draw(self,screen,pos)
            if self.text != '':
                if pos != None: self.tx,self.ty = pos
                screen.blit(self.text,(self.tx,self.ty))
            if self.image!= None:
                if pos != None:
                    self.pos = pos
                screen.blit(self.image,(self.pos[0]+int(self.width*0.05),self.pos[1]+int(self.height*0.05)))
    def handle_event(self,event):#if button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousepos = pygame.mouse.get_pos()
            if self.pos[0] <= mousepos[0]<= self.pos[0]+self.width and self.pos[1] <= mousepos[1]<= self.pos[1]+self.height:
                return True
        return False

    def selectfill(self):
        #outlines button for user to know which colour/tool is selected
        self.outline,self.lcolour = 2,(0,0,0)

    def centre (self,obj):
        #centres images and text if inputed
        if obj[0] == 'img':
            (owidth,oheight) = obj[1].get_size()
            return (self.pos[0] + (self.width - owidth)//2, self.pos[1] + (self.height - oheight)//2)
    def textfunc(self,txt,colour):
        #Allows for text to be on button and centered
        self.text = self.font.render(txt, True,colour)
        tw, th = self.font.size(txt)
        self.tx,self.ty = (self.pos[0] + (self.width - tw)//2, self.pos[1] + (self.height - th)//2)

class InputBox:
    def __init__(self, x, y, w, h, color = [(0,0,0),(100,100,100)],font = pygame.font.Font(None, 50), text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.x,self.y, self.h = x,y,h
        self.color,self.visible = color[1],True
        self.actcolor, self.inactcolor = color[0],color[1]
        self.text,self.font = text,font
        self.txt_surface = font.render(text, True, self.color)
        self.active,self.count = False,0
    def handle_event(self, event, onlynum = False,limit = 10000):
        if self.visible:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = self.actcolor if self.active else self.inactcolor
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]

                    elif event.key == pygame.K_RETURN:
                        return True
                    else:
                        if len(self.text) < limit:
                            if onlynum:
                                if event.key in [pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]:
                                    self.text += event.unicode
                            else:self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = self.font.render(self.text, True, self.color)
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
    def draw(self, screen):
        if self.visible:
            if self.active:
                self.count +=1
                if self.count%400<=200:
                    temp = self.txt_surface.get_width()
                    pygame.draw.line(screen, self.actcolor, (self.x+temp+10,self.y+5),(self.x+temp+10,self.y+self.h-5),2)
            screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
            pygame.draw.rect(screen, self.color, self.rect, 2)
        
class Grid():#abstract class
    def __init__(self, rows, columns,stagewidth,stageheight):
        self.rows,self.col,self.swidth,self.sheight,self.x,self.y= rows,columns,stagewidth,stageheight,0,0
        self.cwidth,self.cheight = self.swidth//self.rows, self.sheight//self.col
    def draw(self,screen):
        for r in range(self.rows):
            for c in range(self.col):
                pygame.draw.rect(screen,(255,255,255),(r*self.cwidth,c*self.cheight,self.cwidth,self.cheight))
                pygame.draw.rect(screen,(100,100,100),(r*self.cwidth,c*self.cheight,self.cwidth,self.cheight),1)
    def posclicked(self,pos):
        return (pos[0]//self.cwidth,pos[1]//self.cheight)
    def keysmove(self,side):
        if side == 'left':self.x-=1
        elif side == 'right':self.x+=1  
        elif side == 'up':self.y-=1   
        elif side == 'down':self.y+=1
        if self.x<0 or self.x>=self.rows: self.x = self.orix
        if self.y<0 or self.y>=self.col: self.y = self.oriy
        return (self.x,self.y)
                   
class Menu(Grid):
    #imports from parent grid class. Allows for a variety of possible inputs
    # including colour, image, text and more. 
    def __init__(self, rows, columns,stagewidth,stageheight,spacing=[0,0],cord = (0,0),colour = None,image = None,cwidth=None,cheight=None,size = 20):
        Grid.__init__(self, rows, columns,stagewidth,stageheight)
        self.spacing, self.cord, self.colour,self.image,self.txtsize = spacing, cord, colour,image,size
        self.buttons,self.text,self.visible = [],None,True
        self.secondtext,self.secpad = [], 0
        if cwidth != None: self.cwidth,self.cheight = cwidth, cheight
        if image == None: image = [None]*rows*columns
        elif image[0] == 'text':
            self.font = pygame.font.Font(None, self.txtsize)
            image += (rows*columns-len(image[1:]))*['']
            self.t,self.text = image[1:],[self.font.render(text, True, (255,255,255)) for text in image[1:]]
            image = [None]*rows*columns 
        if colour== None: colour = [(255,255,255)]*rows*columns
        for r in range(rows):
            self.buttons.append([Button(self.cwidth,self.cheight,colour[c*self.rows + r],image[c*self.rows + r],(cord[0] + r*self.cwidth+r*spacing[0],cord[1] + c*self.cheight+c*spacing[1])) for c in range(columns)])
    def draw(self,screen,centre = True):
        if self.visible:
            for r in range(self.rows):
                for c in range(self.col):
                    self.buttons[r][c].draw(screen)
                    if self.text!= None:
                        try:
                            temptext = self.text[c*self.rows+r]
                            centrex,centrey = (self.cwidth-temptext.get_width())//2, (self.cheight-temptext.get_height())//2
                            if centre==True:
                                screen.blit(temptext,(self.buttons[r][c].pos[0]+centrex,self.buttons[r][c].pos[1]+centrey))
                            else:
                                if len(self.secondtext)!= 0:
                                    if len(self.secondtext)>c*self.rows+r: 
                                        temp2text = self.secondtext[c*self.rows+r]
                                        screen.blit(temp2text,(self.buttons[r][c].pos[0]+self.secpad,self.buttons[r][c].pos[1]+centrey))
                                screen.blit(temptext,(self.buttons[r][c].pos[0]+centre,self.buttons[r][c].pos[1]+centrey))
                        except:pass
    def cellclicked(self,pos):
        #returns which button is clicked. Otherwise returns None
        if self.visible:
            for x, row in enumerate(self.buttons):
                for y, p in enumerate(row):
                    if p.pos[0]<=pos[0]<=p.pos[0] + p.width and p.pos[1]<=pos[1]<=p.pos[1] + p.height:
                        self.buttons[self.x][self.y].outline,self.buttons[self.x][self.y].lcolour = 1,(100,100,100)
                        self.buttons[x][y].selectfill()
                        self.x,self.y = x,y
                        return [y,x]
    def processText(self):
        font = pygame.font.Font(None, self.txtsize)
        self.t = self.image[1:]
        self.text = [font.render(text, True, (255,255,255)) for text in self.image[1:]]
    
class PixelArt (Grid):
    def __init__(self, rows, columns,stagewidth,stageheight,cord = (0,0),colour = None):
        Grid.__init__(self, rows, columns,stagewidth,stageheight)
        self.pixels,self.cord = [],cord
        if colour== None: colour = [(255,255,255)]*rows*columns
        for r in range(rows):
            self.pixels.append([Pixel(self.cwidth,self.cheight,colour[r*self.col + c],(r*self.cwidth+cord[0],c*self.cheight+cord[1])) for c in range(columns)])
        self.previous = self.pixels[0][0]
    def draw(self,screen):
        for r in range(self.rows):
            for c in range(self.col):
                self.pixels[r][c].draw(screen)
    def cellclicked(self,pos,colour=None):
        #figures out which cell is clicked and colours it.
        if self.cord[0] <= pos[0]<= self.cord[0] + self.swidth and self.cord[1] <= pos[1]<= self.cord[1] + self.sheight:
            for x,row in enumerate(self.pixels):
                for y,pix in enumerate(row):
                    if pix.pos[0]<=pos[0]<=pix.pos[0]+pix.width and pix.pos[1]<=pos[1]<=pix.pos[1]+pix.height:
                        cx,cy = x,y
            self.pixels[self.x][self.y].outline,self.pixels[self.x][self.y].lcolour = 1,(100,100,100)
            self.x,self.y = cx,cy
            if self.canfill:
                #if the entire screen is the same colour and you want to fill
                #instead of recursing through the whole screen. It will recognize
                #it and just fill the entire screen
                same = True
                for row in self.pixels:
                    if [p.colour for p in row].count(row[0].colour) != len(row):
                        same = False
                if same:
                    for row in self.pixels:
                        for p in row:
                            p.colour = colour
                    self.canfill = False
                    same = False    
                    return
                else:
                    self.fillin((cx,cy),self.pixels[cx][cy].colour, colour)
            self.pixels[cx][cy].selectfill(colour,self.canfill)
            self.canfill = False
            
    def keystrokes(self,side,colour=None):
        #move using key board
        self.pixels[self.x][self.y].outline,self.pixels[self.x][self.y].lcolour = 1,(100,100,100)
        (cx,cy) = self.keysmove(side)
        self.orix,self.oriy = self.x, self.y
        self.pixels[cx][cy].selectfill(colour,False)
        
    def fillin(self,cord,prevcolour, colour):
        #recursive function that tests the 4 sides of each pixel calling upon
        #itself if it is unfilled. 
        if prevcolour == colour: return
        x,y = cord[0],cord[1]
        self.pixels[x][y].selectfill(colour,self.canfill)
        if 0<x<self.rows and 0<y<self.col:
            if 0<=y-1<self.col:
                if self.pixels[x][y-1].colour == prevcolour:self.fillin((x,y-1),prevcolour,colour)
            if 0<=y+1<self.col:
                if self.pixels[x][y+1].colour == prevcolour:self.fillin((x,y+1),prevcolour,colour)
            if 0<=x-1<self.rows:
                if self.pixels[x-1][y].colour == prevcolour:self.fillin((x-1,y),prevcolour,colour)
            if 0<=x+1<self.rows:
                if self.pixels[x+1][y].colour == prevcolour:self.fillin((x+1,y),prevcolour,colour)
                
class ScrollBar():
    def __init__(self,x,y,width, height,data,dlength,colour = (0,0,0)):
        self.x,self.y,self.width,self.height,self.data,self.dl = x,y,width, height,data,dlength
        self.cl,self.visible = colour,True
        self.bar = Button(width,height,self.cl,None,(x,y))
    def newBar(self,data):
        #makes the bar smaller when there are more items in the list
        self.data = data
        if len(self.data)>10:h = self.height//len(self.data)*(self.dl)
        else: h = self.height
        y = (self.y + self.height) - h
        self.bar = Button(self.width,h,self.cl,None,(self.x,y))
    def draw(self,screen):
        if self.visible:
            pygame.draw.rect(screen,self.cl,(self.x,self.y,self.width,self.height),1)
            self.bar.draw(screen)
    def handle_event(self,event):
        #when user clicks the scroll bar
        if self.bar.handle_event(event):
            pos = pygame.mouse.get_pos()
            self.tempdiff = self.bar.pos[1] - pos[1]
            return True
    def update(self,pos):
        if self.visible:
            if len(self.data) != 0:
                #using the proportional distance between the mouse and the scroll
                # bar input the index the menu should change
                self.bar.pos = (self.x,pos[1]+self.tempdiff)
                if self.bar.pos[1]<self.y: self.bar.pos =(self.x,self.y)
                elif self.bar.pos[1]>self.y+self.height-self.bar.height:
                    self.bar.pos =(self.x,self.y+self.height-self.bar.height)
                tempscroll = (self.bar.pos[1]-self.y)//(self.height//len(self.data))
                return tempscroll,tempscroll+self.dl

class Player():
    def __init__(self, number, name):
        self.number,self.name, self.rank, self.matches = number, name, None, {}
        self.r1p,self.r2p,self.ratio,self.win = 0,0, 1,0
    def save(self,file):
        #writes all properties of the player in a designated file
        temp = {}
        for opp, match in self.matches.items():
            temp[opp.name] = match
        revert = self.matches
        self.matches = temp
        properties = [self.number,self.name,self.rank,self.matches, self.win, self.r1p]
        file.write(str(properties)+'\n')
        self.matches = revert
    def update(self, opp, score,oppscore, outcome = 'win'):
        #changes player properties based on inputed matches
        self.matches[opp] = [score,oppscore]
        if outcome == 'win':
            #print(self,self.win,self.matches)
            self.win += 1
        self.ratio = self.win/len(self.matches)
    def generate_ranks(self):
        #using algorithm generate its round 1 points
        self.r1p = self.win*100
        for opp, score in self.matches.items():
            self.r1p += int(score[0]*opp.ratio*10)
        divisor =len(self.matches)
        if divisor == 0: divisor = 1
        else: divisor *= 2
        self.r1p = self.r1p//divisor

        
            
def prosort(data, prop):
    #sorts objects according to one of its properties
    for num in range(len(prop)-1,0,-1):
        for i in range(num):
            if prop[i] <prop[i+1]:
                prop[i],prop[i+1] = prop[i+1],prop[i]
                data[i], data[i+1] = data[i+1],data[i]
    return data,prop

class University ():
    def __init__(self,file):
        self.file = file
        self.sections = []
        self.contents = []
        time = 0
        titlefont = pygame.font.Font(None, 60)
        while True:
           time += 1
           temp = file.readline()
           if temp == '***':
               break
           if time % 2:
               self.sections.append(eval(temp))
           else:self.contents.append(eval(temp))

        print(self.sections)
        self.rendersect = [titlefont.render(s, True, (0,0,0)) for s in self.sections]
        print(self.contents)
        
           
#Player(1,'Yiwei')
