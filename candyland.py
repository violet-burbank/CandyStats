import random
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import scipy.stats as stats
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Rectangle

#full deck
fullDeck = ['red', 'orange', 'green', 'blue', 'yellow', 'purple'] * 4 + ['redred', 'blueblue', 'yellowyellow', 'purplepurple'] * 4 + ['orangeorange', 'greengreen']*3 + ['peppermint', 'berry', 'lolly', 'gumdrop', 'peanut', 'ice']
#board
board = {'red': (1, 7, 14, 21, 27, 33, 39, 46, 52, 58, 64, 71, 77, 83, 89, 96, 103, 109, 115, 121, 127, 133, 134), 'purple': (2, 8, 15, 22, 28, 34, 40, 47, 53, 59, 65, 72, 78, 84, 90, 97, 104, 110, 116, 122, 128, 134), 'yellow': (3, 10, 16, 23, 29, 35, 41, 48, 54, 60, 66, 73, 79, 85, 91, 98, 105, 111, 117, 123, 129, 134), 'blue': (4, 11, 17, 24, 30, 43, 49, 55, 61, 67, 74, 80, 86, 93, 99, 106, 112, 118, 124, 130, 134), 'orange': (5, 12, 18, 25, 31, 37, 44, 50, 56, 62, 68, 75, 81, 87, 94, 100, 107, 113, 119, 125, 131, 134), 'green':(6, 13, 19, 26, 32, 38, 45, 51, 57, 63, 70, 76, 82, 88, 95, 101,108, 114, 120, 126, 132, 134), 'berry': 9, 'peppermint': 20, 'gumdrop': 42, 'peanut': 69, 'lolly': 92, 'ice': 102}
#licorice spots
stick = [47, 86, 117]
#bridge spots
bridge = {5: 60, 35: 46}
#Each object is a player, with a location, a place after victory, and a boolean saying whether or not they are locked on licorice
class player:
    def __init__(self, order):
        #sq is the square the player is located
        self.square = 0
        #blocked is whether or not the player is blocked from their next turn
        self.blocked = False
        #place tells what place the player came in
        self.place = 0
        #order tells the order of players, where 0 is first, 1 is second etc.
        self.order = order
    #Gives the location and place of a player
    def __repr__(self):
        return str(self.square)+" "+str(self.place)
    #Moves the player based on the card drawn
    def move(self, card):
        tile = 0
        #If we have a single color, then we can just use the helper function findTile
        if(card in board.keys()):
            tile = self.findTile(card)
        else:
            #There are repeated colors sometimes, so we must move twice, depending on the color.
            if(card=="redred"):
                tile1 = self.findTile("red")
                self.square = tile1
                if(tile1<134):
                    tile = self.findTile("red")
                else:
                    tile = tile1
            elif(card=="blueblue"):
                tile1 = self.findTile("blue")
                self.square = tile1
                if(tile1<134):
                    tile = self.findTile("blue") 
                else:
                    tile = tile1
            elif(card=="yellowyellow"):
                tile1 = self.findTile("yellow")
                self.square = tile1
                if(tile1<134):
                    tile = self.findTile("yellow")
                else:
                    tile = tile1
            elif(card=="greengreen"):
                tile1 = self.findTile("green")
                self.square = tile1
                if(tile1<134):
                    tile = self.findTile("green")
                else:
                    tile = tile1
            elif(card=="orangeorange"):
                tile1 = self.findTile("orange")
                self.square = tile1
                if(tile1<134):
                    tile = self.findTile("orange")
                else:
                    tile = tile1
            elif(card=="purplepurple"):
                tile1 = self.findTile("purple")
                self.square = tile1
                if(tile1<134):
                    tile = self.findTile("purple")
                else:
                    tile = tile1 
        self.square = tile
        #if the player is on a bridge spot at the end, they get to move to the spot on the bridge.
        if(tile in bridge.keys()):
            self.square = bridge[tile]
        #If the person is stuck in licorice, theye lose their next turn.
        elif(tile in stick):
            self.blocked = True
        
#Tells if the player has won
    def checkWin(self):
        if self.square == 134:
            return True
        return False
#Finds what square the card is at
    def findTile(self, card):
        square = self.square
        if(type(board[card])==int):
            tile = board[card]
        else:
            tilePos = list(filter(lambda x: x > square, board[card]))
            tile = min(tilePos)
        return tile

# Tells the player's square
    def returnSquare(self):
        return self.square

#Sets what place the player came in
    def setPlace(self, pla):
        self.place = pla

    #Returns what place the player came in
    def getPlace(self):
        return self.place 

    #Returns what the order of the player was
    def getOrder(self):
        return self.order


class deck:
    def __init__(self):
        random.shuffle(fullDeck)
        self.shufDeck = fullDeck
    
    def __repr__(self):
        return str(self.shufDeck)
#Takes a turn, draws a card and takes one off the top of the deck
    def turn(self):
        if(self.shufDeck==[]):
            random.shuffle(fullDeck)
            self.shufDeck = fullDeck
        card = self.shufDeck[0]
        self.shufDeck = self.shufDeck[1:]
        return card
#Single player
def singlePlayGame():
    p1 = player(0)
    d = deck()
    card = ''
    counter = 0
    while(p1.checkWin()==False):
        card = d.turn()
        print(card)
        p1.move(card)
        print(p1.returnSquare())
        counter  = counter + 1
    return counter

#Returns some stats about multiple runnings of a single player game. N is the number of repitions done.
def singleStats(n):
    #Stores the info of n single games, based on how many cards were played.
    singleInfo = []
    for i in range(0, n):
        singleInfo.append(singlePlayGame())
    plt.hist(singleInfo, bins = list(range(0, 110, 10)))
    plt.title("Number of Cards Played (Single Player)")
    plt.xlabel("Number of Cards")
    plt.ylabel("Frequency")
    #We do a shapiro Wilk test to see whether or not the data is normally distributed
    wStat, p =  stats.shapiro(singleInfo)
    p = round(p, 5)
    mean = round(np.mean(singleInfo), 2)
    stDev = round(np.std(singleInfo), 2)
    numOutliers = len(outliers(singleInfo))
    print("Mean: "+str(mean)+" Standard Deviation: "+str(stDev) + " Shapiro Test P-Value: "+str(p)+" Number of Outliers: "+str(numOutliers))
    plt.show()
    '''After running this on n values of 10, 100, and 1000 we can see that the plot get more and more right skewed, and the p value from the shapiro test is increasingly
    decreasing as n increases. This means that the data gets less normal as we increase our trial size. Since our data is very not normal, we can't really do any t tests and so forth
    to investigate this. I might look further into how the location cards impact number of cards drawn, but first I want to see if the number of cards played with multiple players '''


#I wanted to see if taking out outliers would significantly change our data, so lets see:
def cleanSingleStats(n):
    singleInfo = []
    for i in range(0, n):
        singleInfo.append(singlePlayGame())
    singleInfo = clean(singleInfo)
    #After cleaning, we do the same routine as before
    plt.hist(singleInfo, bins = list(range(0, 110, 10)))
    plt.title("Number of Cards Played (Single Player)")
    plt.xlabel("Number of Cards")
    plt.ylabel("Frequency")
    #We do a shapiro Wilk test to see whether or not the data is normally distributed
    wStat, p =  stats.shapiro(singleInfo)
    p = round(p, 5)
    mean = np.mean(singleInfo)
    stDev = np.std(singleInfo)
    numOutliers = len(outliers(singleInfo))
    print("Mean: "+str(mean)+" Standard Deviation: "+str(stDev) + " Shapiro Test P-Value: "+str(p)+" Number of Outliers: "+str(numOutliers))
    plt.show()
    plt.boxplot(singleInfo)
    plt.show()
    '''This did very little to change my data. Everything was pretty much the same, except the range of the plots was much less and there was a way smaller number of outliers in the final
    return. This was pretty much what I expected, so there isn't really too much more to investigate here. While I am glad I explored a little bit, there isn't too much more to say.'''

#quick helper function to find the outliers of a data set.
def outliers(data):
    #Here are our first and third quartiles
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3-q1
    max = 1.5*iqr + q3
    min = q1 - 1.5 * iqr
    outliers = []
    for i in range(0, len(data)):
        if(data[i]<min or data[i]>max):
            outliers.append(data[i])
    return outliers

#Another quick helper that cleans data by removing outliers
def clean(data):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3-q1
    max = 1.5*iqr + q3
    min = q1 - 1.5 * iqr
    cleanData = []
    for i in range(0, len(data)):
        if(data[i]>min and data[i]<max):
            cleanData.append(data[i])
    return cleanData


#plays a game with n players
def nPlayGame(n):
    #List of players
    pList = []
    for i in range(0, n):
        pList.append(player(i))
    d = deck()
    #Dictionary storing how many moves it took each player to complete the game
    winners = {}
    #Keeps track of how many turns have passed
    counter = 0
    #Keeps track of which players turn it is 
    pTurn = 0
    #Tells what place we are at, 0 means no one has finished, 1 means one person has finished and etc.
    currentPlace = 0
    #gameplay
    while(not len(pList) == 0):
        card = d.turn()
        if(pTurn >= len(pList)):
                pTurn = 0
        pList[pTurn].move(card)
        if(pList[pTurn].checkWin()==True):
            pList[pTurn].setPlace(currentPlace)
            winners[pList[pTurn].getOrder()] = counter
            pList.remove(pList[pTurn])
            currentPlace = currentPlace + 1
        else:
            pTurn = pTurn + 1
        counter = counter + 1
    return winners

#this analyzes m number of n player games of candyland
def nPlayerStats(n, m):
    currentGame = {}
    winners = []
    losers = []
    firstWinCounts = []
    notfirstWinCounts = []
    for i in range(0, m):
        currentGame = nPlayGame(n)
        winners.append(min(currentGame, key=currentGame.get))
        losers.append(max(currentGame, key=currentGame.get))
        if(winners[i] == 0):
            firstWinCounts.append(currentGame[0])
        else:
            notfirstWinCounts.append(currentGame[winners[i]])

    winProps = list(map(lambda x: winners.count(x) / m, range(0,n)))
    loseProps = list(map(lambda x: losers.count(x) / m, range(0,n)))

    plt.ylim(0, 1)
    plt.ylabel("Proportion by Order")
    plt.xlabel("Wins / Losses")
    bars = []
    for i in range(0, n):
        bars.append(plt.bar(range(0, 2), (winProps[i], loseProps[i])))
    
    plt.legend(tuple(map(lambda x: bars[x][0], range(0, n))), tuple(map(lambda y: "Player "+str(y), range(0, n))))
    plt.xticks((0, 1), ('Wins', 'Losses'))

    plt.show()
    print(winProps)
    firstWinProp = winners.count(0) / m
    notFirstWinProp = 1 - firstWinProp
    return firstWinProp