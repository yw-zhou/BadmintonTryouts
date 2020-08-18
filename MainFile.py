# --------------------------------------------------------------------
# Program: Final Project 
# Author: Yi Wei Zhou
# Date: 23/01/2019
# Description: A Badminton Tryout program where users can input players
# matches and generate ranks and other properties
# --------------------------------------------------------------------

from Classes import Button, InputBox,Menu,pygame,ScrollBar,Player,prosort

####################Defining Values###################################3
#all
screen = pygame.display.set_mode((1000, 800))
smallfont = pygame.font.Font(None, 42)
white,black,lightgrey,darkgrey,red = (255,255,255),(0,0,0),(200,200,200),(100,100,100),(255,0,0)
mode = 1
playerlist,total = [],10
done = False
#mode 1: Title Screen
titlefont = pygame.font.SysFont("Arial Black", 110)
title = ["Badminton", "Tryout", "Software"]
title = [titlefont.render(x, True, black) for x in title]
titlepos = [(100,80),(250,180),(400,280)]
startmn = Menu(2,1,300,600,[100,0],(300, 450),[lightgrey]*2,['text','Start','Load'],200,100,60)

#mode 2: Input Team Name
subfont = pygame.font.SysFont("Arial Black", 50)
insertnametxt = subfont.render("Team Name:", True, white)
teaminpt = InputBox(280,300,430,60,[white,black],pygame.font.Font(None, 60))
teammn = Menu(2,1,300,600,[80,0],(310, 400),[lightgrey]*2,['text','Back','OK'],150,60,40)
overlap = False
overlaptxt = smallfont.render("Already Exists or Slots Full",True, white)

#mode 3: Load Team Selection
readteams = open('Teams.txt','r')
teamloadlist = []
for x in range(6):
    teamloadlist.append(readteams.readline().strip())
readteams.close()
loadteammn = Menu(2,3,300,600,[100,50],(50, 50),[lightgrey]*6,['text']+teamloadlist,400,185,100)
backbtn = Button(100,40,darkgrey,None,(50,750))
backbtn.textfunc("Back",white)
load = False
loaddelmn = Menu(2,3,300,600,[455,185],(385, 60),[red]*6,['text']+['X']*6,50,50,40)
                   
#mode 4: Add players
addplayertxt = subfont.render("Add Player:", True, black)
nameinpt = InputBox(450,80,430,60,[black,darkgrey],pygame.font.Font(None, 60))
players,scroll,mousedown = [],0,False
playerscroll = ScrollBar(950,200,50,600,players,10)
startbtn,cancelbtn = Button(100,40,darkgrey,None,(800,150)),Button(100,40,darkgrey,None,(100,150))
startbtn.textfunc("Start",white)
cancelbtn.textfunc("Cancel",white)
playerclass = []
playerdel = 0

#mode 5: Add matches
txtlist =[subfont.render("Winner:", True, black),
          subfont.render("Loser:", True, black),
          subfont.render("Score:", True, black)]
inptlist = []
for i in range(2):
    temp = InputBox(50+400*i,80,300,60,[black,darkgrey],pygame.font.Font(None, 60))
    inptlist.append(temp)
inptlist.append(InputBox(820,80,80,60,[black,darkgrey],pygame.font.Font(None, 60)))
matches,onematch  = [],[0,0,0]
printmatch,printscore = [],[]
temp = ['','','']
inptlist[0].active = True
matchscroll = ScrollBar(950,200,50,600,printmatch,10)
ranksbtn,playerbtn = Button(200,40,darkgrey,None,(700,150)),Button(200,40,darkgrey,None,(50,150))
ranksbtn.textfunc("Generate Ranks",white)
playerbtn.textfunc("Edit Players",white)
savebtn = Button(150,40,darkgrey,None,(500,150))
savebtn.textfunc('Save',white)
deletemn = Menu(1,1,300,600,[0,20],(850, 210),[red]*1,['text']+['delete']*10,80,40,35)
savebool,savedtxt = True,smallfont.render("Saved", True, black)
notes = [smallfont.render("Player does not exist", True, black),
         smallfont.render("Match already recorded", True, black)]
noteind = -1
#mode 6: View Ranking
playername = []
rankedscroll = ScrollBar(950,200,50,600,playername,10)
ranktxt = titlefont.render('Ranks',True, black)
stend = [0,0]

def openteams():
    global teamloadlist
    full = True
    #opening the teams text file writing the names and making a team file
    if teaminpt.text not in teamloadlist or teaminpt.text == '':
        for i in range(len(teamloadlist)):
            if teamloadlist[i] == '':
                teamloadlist[i] = teaminpt.text
                full = False
                break
        if full: return (teaminpt.text, open(teaminpt.text,'w+'),2)   
        fi = open('Teams.txt','w')
        for team in teamloadlist:
            fi.write(team+'\n')
        fi.close()
        #If there is an overlap, tell the user
        return (teaminpt.text,open(teaminpt.text,'w+'),4)
    else: return (teaminpt.text, open(teaminpt.text,'w+'),2)
   
def makemenu(data):
    #using the data make a universal menu
    if len(data)>10:lend = 10
    else:lend = len(data)
    menua = Menu(1,len(data),300,600,[0,0],(0, 200),
                 [lightgrey,darkgrey]*(len(data)//2)+[lightgrey]*(len(data)%2),
                 ['text']+data[scroll:scroll+11],950,60,40)
    menub = Menu(1,lend,300,600,[0,20],(850, 210),
                 [red]*lend,['text']+['delete']*10,80,40,35)
    return (menua,menub)

def scrollaround (data,stend,data2 = None):
    #using the coordinates of the scroll bar update the menu to show the according data
    tempmn = Menu(1,len(data),300,600,[0,0],(0, 200),
                    [lightgrey,darkgrey]*(len(data)//2)+[lightgrey]*(len(data)%2),
                     ['text']+data[stend[0]:stend[1]],950,60,40)
    if data2 != None:
        tempmn.secondtext = data2[stend[0]:stend[1]]
        tempmn.secpad = 700
    return tempmn

#def findparent(data,item):
    

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            try:#ensures data written on file is there when the user closes
                #the program randomly
                teamfile.close()
            except:pass
            done = True
            break
        if mode == 2:
            if teaminpt.handle_event(event,False,20):
                #when clicking enter or ok on the team input
                #write the team in teams and make a new team file
                teamnametxt = subfont.render(teaminpt.text, True, black)
                teamname, teamfile, mode = openteams()
                players = []
                if mode ==2: overlap = True
        elif mode == 3:
            if backbtn.handle_event(event): mode = 1
        elif mode == 4:
            if nameinpt.handle_event(event,False,20):
                #when inputing player names, make them into objects
                players.append(str(len(players)+1+playerdel)+' ' + nameinpt.text)
                playerclass.append(Player(len(players), nameinpt.text))
                playerclass[-1].save(teamfile)
                if len(players)> 10: scroll += 1
                #make a menu for players and delete and a scroll bar that is
                #linked to the menu
                playermn,deletemn1 = makemenu(players)
                nameinpt.text = ''
                nameinpt.txt_surface = nameinpt.font.render('', True, nameinpt.color)
                playerscroll.newBar(players)
            elif playerscroll.handle_event(event):mousedown = True
            elif startbtn.handle_event(event):

                printmatch,printscore = [],[]
                scroll = 0
                #when start is pressed, if it is from load, make the menu for it
                if load:
                    for p in playerclass:
                        #using the names in the matches find its parent object
                        if len(p.matches) != 0:
                            for opp,match in p.matches.items():
                                temp1 = str(p.number)+' ' + p.name+' VS ' + str(opp.number)+' '+ opp.name
                                temp2 = str(opp.number)+' ' + opp.name+' VS ' + str(p.number)+' '+ p.name
                                if temp1 not in printmatch and temp2 not in printmatch:
                                    printmatch.append(str(p.number)+' ' + p.name+' VS ' + str(opp.number)+' '+ opp.name)
                                    printscore.append(str(match[0]) + ':' + str(match[1]))
                    
                    #create a match and delete menu and add a second text and padding
                    #for the score
                    if len(printmatch):
                        matchmn,deletemn = makemenu(printmatch)
                        printscore = [matchmn.font.render(score,True, white) for score in printscore]
                        matchmn.secondtext = printscore[scroll:scroll+10]
                        matchmn.secpad = 700
                        matchscroll.newBar(printmatch)
                        matchscroll.bar.pos = (matchscroll.x,matchscroll.y)
                mode,scroll = 5,0
                teamfile.close()
            elif cancelbtn.handle_event(event): mode = 1
        elif mode == 5:
            for r in range(3):
                #for the first and second box
                if r<= 1 and inptlist[r].handle_event(event,True,15) and inptlist[r].text != '':
                    onematch[r],noteind = int(inptlist[r].text),-1
                    if int(inptlist[r].text)<len(players)+1:
                        #put the player represented in the box and save the number
                        #temp[r] = players[onematch[r]-1]
                        for p in playerclass:
                            if onematch[r] == p.number:
                                temp[r] = str(p.number) + ' ' + p.name
                                break
                        inptlist[r].txt_surface = inptlist[r].font.render(temp[r], True, inptlist[r].color)
                        inptlist[r].active,inptlist[r+1].active = False,True
                        break
                    else: noteind = 0
                elif r == 2 and inptlist[2].handle_event(event,True,2) and inptlist[r].text != '' and int(inptlist[r].text) < total:
                    if temp[0] +' VS '+ temp[1] not in printmatch and temp[1] +' VS '+ temp[0] not in printmatch and temp[1] != temp[0]: 
                        onematch[2],noteind = int(inptlist[r].text),-1
                        matches.append(onematch)
                        savebool = False
                        #write the matches into each players properties and update the
                        #menu 
                        playerclass[onematch[0]-1].update(playerclass[onematch[1]-1],total,onematch[2])
                        playerclass[onematch[1]-1].update(playerclass[onematch[0]-1], onematch[2],total,'l')
                        printmatch.append(temp[0]+' VS '+temp[1])
                        onematch,temp = [0,0,0],['','','']
                        inptlist[2].active,inptlist[0].active = False, True
                        col = len(printmatch)
                        if col>10:
                            scroll += 1
                            col = 10
                        matchmn,deletemn = makemenu(printmatch)
                        printscore.append(matchmn.font.render(str(total)+':'+inptlist[2].text,True, white))
                        matchmn.secondtext = printscore[scroll:scroll+10]
                        matchmn.secpad = 700
                        for r in range(3):
                            #clear all input boxes
                            inptlist[r].text = ''
                            inptlist[r].txt_surface = inptlist[r].font.render('', True, inptlist[r].color)
                        matchscroll.newBar(printmatch)
                    else: noteind = 1
                elif matchscroll.handle_event(event):
                    mousedown = True
            if ranksbtn.handle_event(event):
                #generate ranks for each character and sort according to their points
                #display as a menu
                for p in playerclass:
                    p.generate_ranks()
                tempprop = [x.r1p for x in playerclass]
                playerranked,pointslist = prosort(playerclass, tempprop)
                for x in range(len(playerranked)):
                    playerranked[x].rank = x + 1
                playername = ['Ranked:' + str(x+1) + '     Player: ' + str(playerranked[x].number)+ ' '+ playerranked[x].name for x in range(len(playerranked))]
                rankedmn = Menu(1,len(playerranked),300,600,[0,0],(0, 200),
                                [lightgrey,darkgrey]*(len(playerranked)//2)+[lightgrey]*(len(playerranked)%2),
                                ['text']+playername[0:11],950,60,40)
                pointslist = [rankedmn.font.render(str(x),True,white) for x in pointslist]
                rankedmn.secondtext = pointslist[0:11]
                rankedmn.secpad = 700
                rankedscroll.newBar(playername)
                rankedscroll.bar.pos = (rankedscroll.x,rankedscroll.y)
                mode = 6
            elif playerbtn.handle_event(event):
                mode = 4
                teamfile = open(teamname, 'w')
            elif savebtn.handle_event(event):
                teamfile = open(teamname, 'w')
                savebool = True
                for p in playerclass:p.save(teamfile)
                teamfile.close()
        elif mode == 6:
            #scroll event during ranked
            if rankedscroll.handle_event(event):
                mousedown = True
            if backbtn.handle_event(event): mode = 5
        elif mode == 7:
            if profilescroll.handle_event(event):
                mousedown = True
            if backbtn.handle_event(event): mode = 6

        #################################################
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if mode == 1:
                if startmn.cellclicked(pos) == [0,0]: mode,load = 2,False #start
                elif startmn.cellclicked(pos) == [0,1]:
                    mode,load = 3,True
                    loadteammn = Menu(2,3,300,600,[100,50],(50, 50),[lightgrey]*6,['text']+teamloadlist,400,185,100)
            elif mode == 2:
                if teammn.cellclicked(pos) == [0,0]: mode = 1
                elif teammn.cellclicked(pos) == [0,1]:#if clicked start
                    teamnametxt = subfont.render(teaminpt.text, True, black)
                    teamname, teamfile, mode = openteams()
                    if mode ==2: overlap = True
            elif mode == 3:
                tempdelete = loaddelmn.cellclicked(pos)
                tempcell = loadteammn.cellclicked(pos)
                if tempdelete != None:
                    #check for which team to delete and deleting the team
                    teamloadlist[tempdelete[0]*2+tempdelete[1]]= ''
                    loadteammn = Menu(2,3,300,600,[100,50],(50, 50),[lightgrey]*6,['text']+teamloadlist,400,185,100)
                    writeteamfile = open('Teams.txt','w')
                    for team in teamloadlist:
                        writeteamfile.write(team+'\n')
                    writeteamfile.close()
                elif tempcell!= None:
                    #check for which team is clicked and read in that file
                    teamname = teamloadlist[tempcell[0]*2+tempcell[1]]
                    if teamname != '':
                        teamfile = open(teamname,'r')
                        playerclass= []
                        while True:
                            tempdata = teamfile.readline().strip()
                            if tempdata == '': break
                            else:
                                #make each item read in and create and save to an object and its properties
                                tempdata = eval(tempdata)
                                tempplayer = Player(tempdata[0],tempdata[1])
                                tempplayer.rank, tempplayer.matches,tempplayer.win,tempplayer.r1p= tempdata[2:]
                                playerclass.append(tempplayer)
                        if len(playerclass):
                            teamfile.close()
                            teamfile= open(teamname,'w')
                            #using the oppponents name in player matches find the object and establish
                            # the link
                            for p in playerclass:
                                tempdict = {}
                                if len(p.matches):
                                    for opp,match in p.matches.items():
                                        for p2 in playerclass:
                                            if opp == p2.name:
                                                tempdict[p2] = match
                                p.matches = tempdict
                                p.save(teamfile)
                            players = [str(x.number) + ' ' + x.name for x in playerclass]
                            #create the menu and scroll bar from information read
                            playermn,deletemn1 = makemenu(players)
                            playerscroll.newBar(players)
                            playerscroll.bar.pos = (playerscroll.x,playerscroll.y)
                        else: load = False
                        teamnametxt = subfont.render(teamname, True, black)
                        mode = 4
                
            elif mode == 4:
                d = deletemn1.cellclicked(pos)
                if d!= None:
                    #checks for which delete button is clicked and how it draws
                    #connection to which player
                    top = int(playermn.image[1][0])
                    if top == 1: top +=1
                    del players[top+d[0]-2]
                    playermn.image = ['text']+players
                    playerscroll.newBar(players)
                    playerdel += 1
                    playermn.processText()
                    
            elif mode == 5:
                d = deletemn.cellclicked(pos)
                if d!= None:
                    #checks for which delete button and finds the corresponding
                    #match
                    savebool = False
                    top = int(matchmn.image[1][0])
                    if top == 1: top +=1
                    temp = printmatch[top+d[0]-2].split()
                    #finds the 2 players associated with the match to delete it
                    #from their own match history. This will also take out the
                    #match effect on their points, win rates, and ranking
                    if len(temp) ==6:
                        if temp[2] == 'VS':temp = temp[:4] + [temp[-2]+' '+temp[-1]]
                        else: temp = [temp[0]] + [temp[1]+' '+temp[2]] + temp[3:]
                    elif len(temp) == 7:temp = [temp[0]] + [temp[1]+' '+temp[2]] + temp[3:5]+ [temp[-2]+' '+temp[-1]]
                    peop = [0,0]
                    for p in playerclass:
                        if p.name == temp[1]:peop[0] = p
                        elif p.name == temp[-1]:peop[1] = p
                    for i,p in enumerate(peop):
                        if i == 0: opp = peop[1]
                        else: opp = peop[0]
                        if p.matches[opp][0] == total:
                            p.win -= 1
                            p.ratio = p.win/len(p.matches)
                        del p.matches[opp]
                    del printmatch[top+d[0]-2]
                    del printscore[top+d[0]-2]
                    matchmn.secondtext = printscore[scroll:scroll+10]
                    matchmn.image = ['text']+printmatch
                    matchscroll.newBar(printmatch)
                    matchmn.processText()
            elif mode == 6:
                tempcell = rankedmn.cellclicked(pos)
                if tempcell!= None:
                    #check which player is clicked and open their profile showing
                    #their properties
                    plprofile = playerclass[tempcell[0]+stend[0]]
                    pltext = subfont.render(str(plprofile.number) + ' ' + plprofile.name, True, black)
                    playermatches,playerscore = [],[]
                    for opp, score in plprofile.matches.items():
                        playermatches.append(str(plprofile.number) + ' ' +plprofile.name + ' VS ' + str(opp.number) + ' ' + opp.name)
                        playerscore.append(str(score[0]) + ' : ' + str(score[1]))
                    plproperties = [plprofile.r1p,plprofile.win, plprofile.ratio,plprofile.rank]                
                    propnames = ['Points: ','Wins: ','Win Ratio: ','Rank: ']
                    plproperties = [subfont.render(propnames[i] + str(plproperties[i]),True, black) for i in range(4)]
                    if len(playermatches):
                        playermatchmn, x = makemenu(playermatches)
                        playerscore = [playermatchmn.font.render(x,True,white) for x in playerscore]
                        playermatchmn.secondtext = playerscore
                        playermatchmn.secpad = 700
                        profilescroll = ScrollBar(950,200,50,600,playermatches,10)
                        profilescroll.newBar(playermatches)
                        profilescroll.bar.pos = (profilescroll.x,profilescroll.y)
                    mode = 7
            elif mode == 7:pass
            elif mode == 8:pass
            elif mode == 9:pass
        if event.type == pygame.MOUSEBUTTONUP:
            mousedown = False
    screen.fill(white)
    ########################Drawing everything on the screen###################
    if mode == 1:
        for x in range(3):screen.blit(title[x],titlepos[x])
        startmn.draw(screen)
    elif mode == 2:
        pygame.draw.rect(screen,darkgrey,(250,200,500,300),0)
        screen.blit(insertnametxt,(280,210))
        teaminpt.active,teaminpt.color = True,teaminpt.actcolor
        teaminpt.draw(screen)
        teammn.draw(screen)
        if overlap: screen.blit(overlaptxt, (300,365))
    elif mode == 3:
        loadteammn.draw(screen)
        loaddelmn.draw(screen)
        backbtn.draw(screen,(50,730))
    elif mode == 4:
        nameinpt.active,nameinpt.color = True,nameinpt.actcolor
        screen.blit(teamnametxt,(10,10))
        screen.blit(addplayertxt,(100,80))
        nameinpt.draw(screen)
        pygame.draw.rect(screen,black,(950,200,50,600),1)
        if mousedown:
            pos = pygame.mouse.get_pos()
            playermn = scrollaround(players,playerscroll.update(pos))
        playerscroll.draw(screen)
        startbtn.draw(screen)
        cancelbtn.draw(screen)
        #screen.blit(starttxt,(815,155))
        if len(players)>0:
            playermn.draw(screen,50)
            deletemn1.draw(screen)
    elif mode == 5:
        for i in range(2):
            screen.blit(txtlist[i],(50+400*i, 10))
            inptlist[i].draw(screen)
        inptlist[-1].draw(screen)
        screen.blit(txtlist[-1],(740, 10))
        if mousedown:
            pos = pygame.mouse.get_pos()
            matchmn = scrollaround(printmatch,matchscroll.update(pos),printscore)
        matchscroll.draw(screen)
        ranksbtn.draw(screen)
        playerbtn.draw(screen)
        savebtn.draw(screen)
        if savebool: screen.blit(savedtxt,(370,160))
        if len(printmatch)>0:
            matchmn.draw(screen,50)
            deletemn.draw(screen)
        if noteind != -1:
            screen.blit(notes[noteind],(200,0))
    elif mode == 6:
        if mousedown:
            pos = pygame.mouse.get_pos()
            stend = rankedscroll.update(pos)
            rankedmn = scrollaround(playername,stend,pointslist)
        rankedmn.draw(screen,50)
        rankedscroll.draw(screen)
        screen.blit(ranktxt,(100,0))
        backbtn.draw(screen,(50,150))
    elif mode == 7:
        screen.blit(pltext, (50,25))
        if mousedown:
            pos = pygame.mouse.get_pos()
            stend = profilescroll.update(pos)
            playermatchmn = scrollaround(playermatches,stend,playerscore)
        if len(playermatches):
            playermatchmn.draw(screen,20)
        for i in range(4):
            screen.blit(plproperties[i], (550, 10 + i*40))
        backbtn.draw(screen,(50,150))
        profilescroll.draw(screen)
        

    pygame.display.update()
pygame.quit()
