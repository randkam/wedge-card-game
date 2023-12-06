import random
import pickle
gamestate= 0
setupLength = 800
setupWidth = 800
cardvalue = ["ACE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN","JACK", "QUEEN", "KING"]
ante = 5
bet = 0
startingMoney = 100
card1 = None
card2 = None
gameround = 0
card1val = None
card2val = None
player1name = ""
player2name = ""
name1 = False
name2 = True
player1score = -1
player2score = -1
scores = []
scorestate = 0




def setup():
    global font1, font2, cardsprite, gamebackground, betbutton, font0, startscreen, menubutton, backbutton, quitbutton, restartbutton, helpbutton, player1name, player2name, name1, name2, scoresbutton, font4, rules,t, file, readfile, scores, passbutton, namescreenbackground, leaderboardbackground
    size(setupLength, setupWidth)
    font0 = loadFont("ArialNarrow-15.vlw")
    font1 = loadFont("Algerian-45.vlw")
    font2 = loadFont("Garamond-22.vlw")
    font3 = loadFont("FranklinGothic-DemiItalic-12.vlw")
    font4 = loadFont("Jokerman-Regular-48.vlw")
    cardsprite = loadImage("cardssprite.png")
    gamebackground = loadImage("gamescreen.jpg")
    betbutton = Button(10,200, 80,80, "Bet!", 255, font2)
    passbutton = Button(10,300, 80,80, "pass!", 255, font2)
    backbutton = Button(250, 250, 150, 50, "back", 255,font2)
    quitbutton = Button(250, 315, 150, 50, "quit",255, font2)
    menubutton = Button(730, 20, 50, 50, "menu", 255, font3)
    restartbutton = Button(250, 380, 150, 50, "restart",255, font2)
    helpbutton = Button(250, 445, 150, 50, "help/rules",255, font2)
    scoresbutton = Button(250, 510, 150, 50, "scores",255, font2)
    startscreen = loadImage("startscreen.png")
    rules = loadImage("rules.png")
    namescreenbackground = loadImage("namescreen (2).png")
    leaderboardbackground = loadImage("3.png")

class Card:
  def __init__(self, suit, cardname, x, y, override = False):
    self.suit = suit
    self.cardname = cardname
    self.x = x
    self.y = y
    self.w = 49
    self.h = 64
    self.selection = 0    
    self.selected = False
    if override:
        self.selected = True
        
    self.Lbutton = Button(self.x, self.y-30, 15, 30, "L", 255, font0)
    self.Hbutton = Button(self.x+self.w-20, self.y-30, 15, 30, "H", 255, font0)
  def getValue(self):
    nametoVal = {"ACE":[1,14] , "TWO":[2],"THREE":[3], "FOUR" : [4], "FIVE" : [5], "SIX": [6], "SEVEN": [7], "EIGHT":[8], "NINE": [9], "TEN":[10], "JACK": [11], "QUEEN": [12], "KING": [13] }
    val = nametoVal[self.cardname]
    if len(val) > 1 and self.selected:
        return [val[self.selection]]
    return val
  def display(self):
    val = self.getValue()
    if len(val) > 1:
        tmp = cardsprite.get(0,self.h * self.suit,self.w,self.h)
        self.Lbutton.display()
        self.Hbutton.display()
    else:
        num = val[0]
        if num == 14:
            num = 1
        tmp = cardsprite.get(49 * (num-1),(self.h * self.suit),self.w,self.h)
        
    image(tmp, self.x, self.y)

class Button:
    def __init__(self, x, y, w, h, t, c, font):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.t = t
        self.c = c
        self.font = font
    def display(self):
        if self.hovered():
            fill(150)
        else:
            fill(self.c)
        rect(self.x, self.y, self.w, self.h)
        fill(0)
        textFont(self.font)
        text(self.t, self.x + (self.w/4), self.y + (self.h/2))
    def hovered(self):
        if mouseX >= self.x and mouseX <= self.x + self.w and mouseY >= self.y and mouseY <= self.y + self.h:
            return True
        return False
      
class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.bet = 0
    def checkbet(self, bet):
        if bet > self.money or bet < 0:
            return False
        self.bet = bet
        return True
    def take(self, amount):
        if self.money - amount < 0:
            self.bet = 0
            return False
        self.money -= amount
        return True
    def give(self, amount):
        self.money += amount
        

      
def draw():
    global cardsprite, gamebackground, delayAmount, startscreen
    if gamestate == 0:
        startScreen()
    if gamestate == 1:
        namescreen()
    elif gamestate == 2:
        background(gamebackground)
        gameScreen()
    elif gamestate == 3:
      pausescreen()
    elif gamestate == 4:
        helpscreen()
    elif gamestate == 5:
        scoreboard()
    
def scoreboard():
    global readfile, scores, player1, player2, scorestate, tab
    background(leaderboardbackground)
    if scorestate == 0:
        scores = []
        readfile = open("scores.txt", "rb")     
        scores = pickle.load(readfile)        
        readfile.close()
        
        if player1score >= 0 and player2score >= 0:
            replaced1 = False
            replaced2 = False
            
            for i in range(len(scores)):
                if scores[i][0] == player1.name: 
                    if scores[i][1] < player1score:
                        scores[i][1] = player1score
                    replaced1 = True
                
                elif scores[i][0] == player2.name:
                    if scores[i][1] < player2score:
                        scores[i][1] = player2score
                    replaced2 = True
                
            if not replaced1:
                scores.append([player1.name, player1score])
                replaced1 = True
            if not replaced2:
                scores.append([player2.name, player2score])
                replaced2 = True
        
            scores.sort(key=lambda obj: int(obj[1]), reverse = True)
            writefile = open("scores.txt", "wb")
        
            pickle.dump(scores, writefile)
            print(scores)
            writefile.close()
            scorestate = 1
        elif player1score > 0 or player2score > 0:
            print("EMERGENCY 1")
    
    y = 265
    if len(scores) > 0:
        for n in scores:
            y +=30
            fill(255)
            textFont(font2)
            text(str(n[0]) +":", 200, y)
            text(str(n[1]) + " $", 500,y )
    else:
        textFont(font1)
        text("scores list is currently empty:(", 300,300)
    menubutton.display()
    

  
def namescreen():
    global  player1, player2, bank, player
    background(namescreenbackground)
    textFont(font0)
    fill(155)
    text(player1name, 400, 270)
   
    text(player2name, 400, 368)
    player1 = Player(player1name, startingMoney)
    player2 = Player(player2name, startingMoney)
    bank = Player("Bank", startingMoney)
    player = None

def startScreen():
    background(startscreen)
    
def pausescreen():
    background(gamebackground)
    backbutton.display()
    quitbutton.display()
    restartbutton.display()
    helpbutton.display()
    scoresbutton.display()
def helpscreen():
    background(rules)
    menubutton.display()
    
    
def gameScreen():
    global gamestate, font1, setupLength, gamebackground, ante, bet, gameround, card1, card2, player, font2, card3, card1val, card2val, card3val, delayAmount, menubutton, quitbutton, backbutton, player1, player2, bank, player, player2name, player1score, player2score, t
    if gameround == 0:
        player1score = -1
        player2score = -1
        if player is None or player.name == player2name:
            player = player1
        else:
            player = player2
           

        card1 = Card(random.randint(0,3), cardvalue[random.randint(0,12)], 300, 400)
        card2 = Card(random.randint(0,3), cardvalue[random.randint(0,12)], 340, 400)
        if card1.cardname == "ACE" and card2.cardname == "ACE":
            card1.selected = True
            card1.selection = 0
            card2.selected = True
            card2.selection = 1
        card3 = Card(random.randint(0,3), cardvalue[random.randint(0,12)], 350, 500, True)
       
        player.take(5)
        bank.give(5)
        
        gameround = 1 
        if player1.money <=0 or player2.money<=0 or bank.money<=0:
            gameround = 4 
    
    if gameround == 1:
        betbutton.display()
        passbutton.display()
        
    if gameround == 2 or gameround == 3:
        card1val = card1.getValue()[0]
        card2val = card2.getValue()[0]
        card3val = card3.getValue()[0]
        
        card3.display()

        if (card1val< card3val < card2val) or (card2val < card3val < card1val):
            if gameround == 2:
                player.money += player.bet
                bank.money -= player.bet
            text("you won the round", 150,300)
            text("click to continue", 150,500)
            
        else:
            if gameround == 2:
                player.money -= player.bet
                bank.money += player.bet
            text("you lost the round",150,300)
            text("click to continue", 150,500)
        player.bet = 0
        
        if gameround == 2:
            gameround = 3   
    if gameround == 4:
            textFont(font2)
            fill(255)
            if player1.money <=0:
                text("game over,"+ player1.name +  " has gone bankrupt ", 250,300)
            if player2.money <=0:
                text("game over,"+ player2.name +  " has gone bankrupt ", 250,300)
            if bank.money <=0:
                text("game over, bank has gone bankrupt", 250,300) 
            player1score = player1.money
            player2score = player2.money

        
    menubutton.display()
    textFont(font2)
    fill(255)
    text(player.name + "'s Turn", 0, 50)    
    text("{}'s Money: {}".format(player1.name, player1.money), 500, 50)
    text("{}'s Money: {}".format(player2.name, player2.money), 500, 75)
    text("{}'s Money: {}".format(bank.name, bank.money), 500, 100)
    
    textFont(font1)
    fill(255)
    text("bet:", 10,190)
    text(player.bet, 110, 190)
    card1.display()
    card2.display()

    
def mousePressed():
    global gamestate, gameround, card1val, card2val, card1, card2, menubutton, player, player1, player2, bank, scorestate, name1, name2, player1name, player2name
    if gamestate == 0:
            gamestate = 1
    elif gamestate == 2 or gamestate == 4 or gamestate==5:
        if menubutton.hovered():
            gamestate = 3
        if gameround == 1:
            if betbutton.hovered() or passbutton.hovered():
                canproceed = True
                if passbutton.hovered():
                    bet = 0
                    gameround = 0
                else:
                    
                    if card1.cardname == "ACE":
                        if card1.selected == False:
                            canproceed = False
                    
                    if card2.cardname == "ACE":
                        if card2.selected == False:
                            canproceed = False
                    if canproceed:
                        gameround = 2
                        
            if card1.Lbutton.hovered():
                card1.selection = 0
                card1.selected = True
            elif card1.Hbutton.hovered():
                card1.selection = 1
                card1.selected = True
                
            if card2.Lbutton.hovered():
                card2.selection = 0
                card2.selected = True
            elif card2.Hbutton.hovered():
                card2.selection = 1
                card2.selected = True
                
        elif gameround == 3:
            gameround = 0
        elif gameround == 4:
            gamestate == 5
            
    if gamestate == 3 :
        if backbutton.hovered():
            gamestate = 2
        elif quitbutton.hovered():
            exit()
        elif restartbutton.hovered():
            gamestate = 0
            gameround = 0
            player1.money = startingMoney
            player2.money = startingMoney
            bank.money = startingMoney
            player = None   
            player1name = ""
            player2name = ""
            name1 = False
            name2 = True
        elif helpbutton.hovered(): 
            gamestate = 4
        elif scoresbutton.hovered():
            gamestate = 5
            scorestate = 0        
def mouseWheel(event):
    global player
    if gamestate == 2 and gameround == 1:
        if event.getCount() > 0: 
           bet = player.bet - 5
           player.checkbet(bet)
        else:
            bet = player.bet + 5
            player.checkbet(bet)
       
def keyReleased():
    global player1name, name1, name2, player2name, gamestate
    if gamestate == 1:
        if name1 == False:
            if key != "\n":
                if key == "\b":
                    if (player1name) !="":
                        player1name = player1name[:-1]
                else:
                    if len(str(key)) == 1:
                        player1name += key
            elif key == "\n":
                name1 = True
                name2 = False
        elif name2 == False:
            if key != "\n":
                if key == "\b":
                    if len(player2name) != "":
                        player2name =  player2name[:-1]
                else:
                    if len(str(key)) == 1:
                        player2name += key
                    
            elif key == "\n":
                name2 = True
                gamestate = 2
                






                   
