#!/usr/bin/env python3
import sys

# seed the pseudorandom number generator
from random import SystemRandom
from random import randint
# seed random number generator
SystemRandom(1) # fix seeding

# A Single Card
class Card:
    def __init__(self):
        self.suit = "Z"
        self.number = 0
    def Set(self,suitNumber,zeroBasedNumber,isBruce):
        if(suitNumber == 0) :
            self.suit = "A"
        elif(suitNumber == 1) :
            self.suit = "B"
        elif(suitNumber == 2) :
            self.suit = "C"
        elif(suitNumber == 3) :
            self.suit = "D"
        elif(suitNumber == 4) :
            self.suit = "E"
        else:
            self.suit = "E"
        self.number = zeroBasedNumber + 1
        if(isBruce):
            self.suit = "X"
            self.number = zeroBasedNumber + 1
    def Draw(self):
        print ("%s%d " % (self.suit, self.number),end ='')

# List of All Cards
class CardStack:
    def __init__(self):
        self.cardPresent = [ [False ,False ,False ,False ,False] ,
                    [False ,False ,False ,False ,False] ,
                    [False ,False ,False ,False ,False] ,
                    [False ,False ,False ,False ,False] ,
                    [False ,False ,False ,False ,False]]
        self.brucePresent = [False,False,False,False]
        self.displayCard = Card();
        self.cardList = []
        self.numberOfCards = 0

    def Pop(self):
        if (self.cardList[0] < 0):
            # Bruce card
            self.brucePresent[abs(self.cardList[0])-1] = False
        else:
            self.cardPresent[self.cardList[0]] = False
        self.cardList.pop()
        self.numberOfCards = self.numberOfCards - 1

    def EmptyStack(self):
        while self.IsEmpty() == False:
            self.cardList.pop()
        self.numberOfCards = 0
        for s in range (0,5):
            for i in range (0,5):
                self.cardPresent[s][i] = False
        for b in range (0,4):
            self.brucePresent[b] = False

    def Value(self):
        totalValue = 0
        for s in range(0,5):
            highestCard = -1
            for n in range(0,5):
                if (self.cardPresent[s][n] == True):
                    highestCard = n
            if(highestCard > -1):
                totalValue = totalValue + highestCard + 1
        return(totalValue)

    def AddCard(self,suitNumber,zeroBasedNumber,bruce):
        if(bruce == True):
            self.brucePresent[zeroBasedNumber] = True
            self.cardList.append(-1*(zeroBasedNumber + 1))
        else:
            self.cardPresent[suitNumber][zeroBasedNumber] = True
            self.cardList.append(suitNumber*5+zeroBasedNumber)
        self.numberOfCards = self.numberOfCards +1

    def AddCardByNum(self,number):
        if(number < 0):
            self.AddCard(0,abs(number)-1,True)
        else:
            self.AddCard((number//5),(number%5),False)

    def PopTopCard(self):
        if(self.numberOfCards > 0):
            self.numberOfCards = self.numberOfCards - 1
            card = self.cardList[0]
            if(card < 0):
                self.brucePresent[abs(card)-1] = False
            else:
                self.cardPresent[(card//5)][(card%5)]= False
            return(self.cardList.pop())
        else:
            print("No Cards")
            sys.exit(1)

    def Draw(self):
        for s in range(0,5):
            for n in range(0,5):
                if(self.cardPresent[s][n] == True):
                    self.displayCard.Set(s,n,False)
                    self.displayCard.Draw()
        for b in range(0,4):
            if(self.brucePresent[b] == True):
                self.displayCard.Set(0,b,True)
                self.displayCard.Draw()

    def DrawInOrder(self):
        for i in self.cardList:
            if(i<0):
                self.displayCard.Set(0,(abs(i)-1),True)
                self.displayCard.Draw()
            else:
                self.displayCard.Set((i//5),(i%5),False)
                self.displayCard.Draw()

    def HighestInSuit(self,iSuit):
        for i in range(4,-1,-1):
            if(self.cardPresent[iSuit][i] == True):
                return (i+1)
        return(-1)

    def SuitPresent(self,iSuit):
        for i in range(4,-1,-1):
            if(self.cardPresent[iSuit][i] == True):
                return(True)
        return(False)

    def Swap(self):
        iRand1 = randint(0,(len(self.cardList)-1))
        iRand2 = randint(0,(len(self.cardList)-1))
        iCardNum1 = self.cardList[iRand1]
        iCardNum2 = self.cardList[iRand2]
        self.cardList[iRand1] = iCardNum2
        self.cardList[iRand2] = iCardNum1

    def Shuffle(self):
        iRand = randint(0,100)
        for k in range (0,iRand):
            self.Swap()

    def NewGame(self):
        self.cardList.clear()
        iCardNum = 0
        for iSuit in range (0,5):
            for iCard in range (0,5):
                self.cardPresent[iSuit][iCard]= True
                self.cardList.append(iCardNum)
                iCardNum = iCardNum + 1
                self.numberOfCards = self.numberOfCards + 1
        for b in range (0,4):
            self.cardList.append((-1*(b+1)))
            self.brucePresent[b] = True
            self.numberOfCards = self.numberOfCards + 1

    def IsEmpty(self):
        if(len(self.cardList) == 0) :
            return(True)
        else:
            return(False)

    def DoubledSuit(self):
        for iSuit in range(0,5):
            thisSuitPresent = False
            for i in range(0,5):
                if(self.cardPresent[iSuit][i] == True):
                    if(thisSuitPresent == True):
                        return(iSuit)
                    else:
                        thisSuitPresent = True
        return(-1)

    def IsDoubled(self):
        if(self.DoubledSuit() < 0):
            return(False)
        else:
            return(True)

    def ClearDoubled(self):
        # Only works for one Double
        iSuit = self.DoubledSuit()
        lowCardSet = False
        lowCardPos = 0
        highCardPos = 0
        for i in range(0,len(self.cardList)):
            card = self.cardList[i]
            if((card//5) == iSuit):
                if(lowCardSet == False):
                    lowCardPos = i
                    lowCardSet = True
                else:
                    highCardPos = i
        for j in range(lowCardPos,(highCardPos+1)):
            #print ("J:",j)
            card = self.cardList[lowCardPos]
            self.cardList.pop(lowCardPos)
            if(card < 0):
                self.brucePresent[abs(card)-1] = False
            else:
                self.cardPresent[(card//5)][(card%5)] = False
            self.numberOfCards = self.numberOfCards -1
        #self.Draw()

class PlayerCardStack:
    def __init__(self):
        self.playerName = "Bozo"
        self.cardsInHand = CardStack()
    def SetName(self,name):
        self.playerName = name
    def EmptyStack(self):
        self.cardsInHand.EmptyStack()
    def StartGame(self,playerName):
        self.SetName(playerName)
        self.EmptyStack()
    def Draw(self):
        if(self.cardsInHand.IsEmpty()):
            print ("%s:" % (self.playerName))
        else :
            print ("%s:" % (self.playerName),end='')
            self.cardsInHand.Draw()
            print ("")
    def PrintPlayer(self):
        print ("Current Player is: %s" % self.playerName,end='')
        print ("\n",end='')
    def AddCard(self,suitNumber,zeroBasedNumber):
        self.cardsInHand.AddCard(suitNumber,zeroBasedNumber,False)
    def AddCardByNum(self,number):
        self.cardsInHand.AddCardByNum(number)
    def CountCards(self):
        iTotal = 0
        for iSuit in range(0,5):
            if(self.cardsInHand.SuitPresent(iSuit) == True):
                iTotal = iTotal + self.cardsInHand.HighestInSuit(iSuit)
        return(iTotal)
    def Score(self):
        score = self.CountCards()
        print("*** %s's Score is : %d" % (self.playerName,score))

class InPlayCardStack:
    def __init__(self):
        self.inPlayCards = CardStack()
    def EmptyStack(self):
        self.inPlayCards.EmptyStack()
    def StartGame(self):
        self.EmptyStack()
    def Draw(self):
        print ("Cards In Play:",end='')
        self.inPlayCards.DrawInOrder()
        print ("\n",end='')
    def AddCard(self,suitNumber,zeroBasedNumber,bruce):
        self.inPlayCards.AddCard(suitNumber,zeroBasedNumber,isBruce)
    def AddCardByNum(self,number):
        self.inPlayCards.AddCardByNum(number)
    def IsEmpty(self):
        return(self.inPlayCards.IsEmpty())
    def IsDoubled(self):
        return(self.inPlayCards.IsDoubled())
    def ClearDoubled(self):
        self.inPlayCards.ClearDoubled()
    def PopTopCard(self):
        return(self.inPlayCards.PopTopCard())

class DeckStack:
    def __init__(self):
        self.deck = CardStack()
    def StartGame(self):
        self.deck.NewGame()
        self.deck.Shuffle()
    def Draw(self):
        self.deck.DrawInOrder()
    def DrawInOrder(self):
        self.deck.DrawInOrder()
    def IsEmpty(self):
        return(self.deck.IsEmpty())
    def PopTopCard(self):
        return(self.deck.PopTopCard())

class Board:
    def __init__(self,numPlayers):
        self.deck = DeckStack()
        self.inPlay = InPlayCardStack()
        self.numPlayers = numPlayers
        self.currentPlayer = 0
        self.players = []
        for i in range(0,numPlayers):
            newPlayer = PlayerCardStack()
            self.players.append(newPlayer)

    def StartGame(self,playerNames):
        self.deck.StartGame()
        self.inPlay.EmptyStack()
        self.currentPlayer = 0
        for i in range(0,self.numPlayers):
            self.players[i].StartGame(playerNames[i])

    def Draw(self):
        self.inPlay.Draw()
        #self.deck.Draw()
        for i in range(0,self.numPlayers):
            self.players[i].Draw()

    def PrintCurrentPlayer(self):
            self.players[self.currentPlayer].PrintPlayer()

    def AdvancePlayer(self):
        self.currentPlayer = ((self.currentPlayer + 1)  % self.numPlayers)

    def PullCard(self):
        card = self.deck.PopTopCard()
        if(card < 0): # bruce
            print("*** Bruce ***")
            self.inPlay.AddCardByNum(card)
            self.inPlay.Draw()
            self.inPlay.EmptyStack()
            self.AdvancePlayer()
        else:
            self.inPlay.AddCardByNum(card)
            if(self.inPlay.IsDoubled() == True):
                print("*** Doubled ***")
                self.inPlay.Draw()
                self.inPlay.ClearDoubled()
                while (self.inPlay.IsEmpty() == False):
                    card = self.inPlay.PopTopCard()
                    self.inPlay.Draw()
                    self.players[self.currentPlayer].Draw()
                    self.players[self.currentPlayer].AddCardByNum(card)
                self.AdvancePlayer()

    def TakeCards(self):
        print("*** Cards Taken ***")
        while self.inPlay.IsEmpty() == False:
            card = self.inPlay.PopTopCard()
            self.players[self.currentPlayer].AddCardByNum(card)
        self.inPlay.EmptyStack()
        self.AdvancePlayer()

    def IsDeckEmpty(self):
        if(self.deck.IsEmpty() == True):
            return (True)
        else:
            return (False)

    def IsGameOver(self):
        if(self.inPlay.IsEmpty() == True) and (self.deck.IsEmpty() == True):
            return (True)
        else:
            return (False)

    def Score(self):
        for i in range(0,self.numPlayers):
            score = self.players[i].Score()

class Game:
    def __init__(self):
        self.board = Board(3)
    def StartGame(self):
        playersNames = ["Riley", "Craig", "Blaine"];
        self.board.StartGame(playersNames)
    def Play(self):
        done = False
        while (done == False):
            self.board.Draw()
            if self.board.IsDeckEmpty():
                self.board.TakeCards()
            else:
                self.board.PrintCurrentPlayer()
                str = input ("D (Draw) or T (Take Cards)")
                if(str == "d") or (str == "D"):
                #Draw a Cards
                    self.board.PullCard()
                elif (str == "t") or (str == "T"):
                    self.board.TakeCards()
            done = self.board.IsGameOver()
        print("*** Game Over ***")
        self.board.Draw()
        score = self.board.Score()


game = Game()
game.StartGame()
game.Play()
