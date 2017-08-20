# If this seems messy and not well tidied up...well it was written in a total of 5 days,
# because my computer was in repair for at least a ******* month...
# Thanks for your understanding :)


# importing stuff - more than I need, but better be safe than sorry ######################################################
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint, QObject, QSize, QTimer, QUrl, QRect, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QPen, QBrush, QColor, QKeySequence, QPainter, QFont
from PyQt5.QtMultimedia import QSound
from random import randint, choice
from PyQt5.QtMultimedia import QSound
import sys
from packScreen import *

# setting up the main class of the application ##########################################################################

class Hearthstone(QMainWindow): # the most important variables are defined here with their starting values
    moneyCount = 1000
    rankCount = 25
    goldCount = 0
    commonCards = 100
    rareCards = 25
    epicCards = 0
    legendaryCards = 0
    packCount = 0
    adventureCount = 0
    freeToPlay = True
    brawlPlayed = False
    questPlayed = False
    welcomeGift = False

# the init function of the main class - setting up some sounds and timers that will be used later on, so that they can be used by other functions to not cause an AttributeError ##########################################################################

    def __init__(self):
        super(Hearthstone, self).__init__()
        self.initGUI()
        self.initMenu()
        self.theme = QSound("sounds/HearthstoneSoundtrack-MainTitle.wav")
        self.ping = QSound("sounds/WhatsApp_Original_Message.wav")
        self.sax = QSound("sounds/EpicSaxGuy-EpicSaxGuyCruzoRemix.wav")
        self.theme.play() # starting the app out with the hearthstone theme
        self.theme.setLoops(100) # hopefully nobody will play this long... (does this cause python to crash when I close the application? Possible..)

        self.moneyTimer = QTimer(self) # these timers are for use in the pay to win mode -> they make sure money is
        self.moneyTimer.timeout.connect(self.depleteMoney) # taken out of the players account and ranks and gold are put in regularly

        self.rankTimer = QTimer(self)
        self.rankTimer.timeout.connect(self.increaseRank)

        self.goldTimer = QTimer(self)
        self.goldTimer.timeout.connect(self.increaseGold)

    def initGUI(self):
        self.popUpFriendsTimer = QTimer(self)
        self.popUpFriendsTimer.timeout.connect(self.popUpFriends)
        self.popUpFinancesTimer = QTimer(self)
        self.popUpFinancesTimer.timeout.connect(self.popUpFinances)

        self.popUpFriendsTimer.start(30000) # this makes the 'whatsapp messages of friends' pop up, who worry about the player putting too much time into the game

        try:
            if self.moneyTimer.isActive() == True: # so that the money, rank and gold values keep changing when the player returns to the main screen in pay to win mode
                self.moneyTimer.stop()
                self.rankTimer.stop()
                self.goldTimer.stop()
                self.moneyTimer.start(10000)
                self.rankTimer.start(15000)
                self.goldTimer.start(5000)
            else:
                pass
        except AttributeError:
            pass

# setting up allllll the GUI elements of the main screen and their signal/slot relationships ##########################################################################

        self.soloBut = QPushButton("Adventure")
        self.soloBut.setMinimumSize(100, 80)
        self.soloBut.clicked.connect(self.playAdventure)
        self.playBut = QPushButton("Play")
        self.playBut.setMinimumSize(100, 80)
        self.playBut.clicked.connect(self.play)
        self.brawlBut = QPushButton("Tavern Brawl")
        self.brawlBut.setMinimumSize(100, 80)
        self.brawlBut.clicked.connect(self.playBrawl)
        self.questBut = QPushButton("Quest")
        self.questBut.setMinimumSize(50, 80)
        self.questBut.clicked.connect(self.playQuest)
        self.shopBut = QPushButton("Shop")
        self.shopBut.setMinimumSize(50, 80)
        self.shopBut.clicked.connect(self.showShop)
        self.packBut = QPushButton("Packs")
        self.packBut.setMinimumSize(50, 80)

        self.packScreen = PackOpeningGraph(self.packCount) # instance of the only other real custom widget class used in this app

        self.packBut.clicked.connect(self.updatePackOpenings)
        self.collectionBut = QPushButton("Collection")
        self.collectionBut.setMinimumSize(50, 80)
        self.collectionBut.clicked.connect(self.displayCollection)
        self.workBut = QPushButton("Work for a Month")
        self.workBut.setMinimumSize(100, 80)
        self.workBut.clicked.connect(self.work)

        mainBut_layout = QVBoxLayout()
        mainBut_layout.addWidget(self.soloBut)
        mainBut_layout.addStretch(2)
        mainBut_layout.addWidget(self.playBut)
        mainBut_layout.addStretch(2)
        mainBut_layout.addWidget(self.brawlBut)
        mainBut_layout.addStretch(2)
        mainBut_layout.addWidget(self.workBut)

        mainButtons = QGroupBox()
        mainButtons.setLayout(mainBut_layout)
        mainButtons.setMaximumSize(300, 370)

        leftBut_layout = QVBoxLayout()
        leftBut_layout.addWidget(self.questBut)
        leftBut_layout.addWidget(self.shopBut)

        leftButtons = QGroupBox()
        leftButtons.setLayout(leftBut_layout)
        leftButtons.setMaximumSize(300, 300)

        rightBut_layout = QVBoxLayout()
        rightBut_layout.addWidget(self.packBut)
        rightBut_layout.addWidget(self.collectionBut)

        rightButtons = QGroupBox()
        rightButtons.setLayout(rightBut_layout)
        rightButtons.setMaximumSize(300, 300)


        radios_layout = QHBoxLayout()
        self.f2p = QRadioButton("Free to Play")
        self.p2w = QRadioButton("Pay to Win")
        if Hearthstone.freeToPlay == True:
            self.f2p.setChecked(True)
        else:
            self.p2w.setChecked(True)
        self.f2p.clicked.connect(self.FreeToPlay)
        self.p2w.clicked.connect(self.PayToWin)
        radios_layout.addWidget(self.f2p)
        radios_layout.addStretch(2)
        radios_layout.addWidget(self.p2w)
        radiobuttons = QGroupBox()
        radiobuttons.setLayout(radios_layout)
        radiobuttons.setMaximumSize(300, 70)

        self.gold = QLineEdit()
        self.gold.setEnabled(False) # so that one cannot cheat!
        self.goldLabel = QLabel("Gold")
        self.goldLabel.setObjectName("gold")

        self.money = QLineEdit()
        self.money.setEnabled(False)
        self.moneyLabel = QLabel("Money")
        self.moneyLabel.setObjectName("money")

        self.rank = QLineEdit()
        self.rank.setEnabled(False)
        self.rankLabel = QLabel("Rank")
        self.rankLabel.setObjectName("rank")

        money_layout = QHBoxLayout()
        money_layout.addWidget(self.moneyLabel)
        money_layout.addWidget(self.money)

        moneyBox = QGroupBox()
        moneyBox.setLayout(money_layout)
        moneyBox.setMaximumSize(300, 70)

        rank_layout = QHBoxLayout()
        rank_layout.addWidget(self.rankLabel)
        rank_layout.addWidget(self.rank)

        rankBox = QGroupBox()
        rankBox.setLayout(rank_layout)
        rankBox.setMaximumSize(300, 70)

        gold_layout = QHBoxLayout()
        gold_layout.addWidget(self.goldLabel)
        gold_layout.addWidget(self.gold)

        goldBox = QGroupBox()
        goldBox.setLayout(gold_layout)
        goldBox.setMaximumSize(300, 70)

        grid = QGridLayout()
        grid.addWidget(moneyBox, 0, 0, 1, 2)
        grid.addWidget(rankBox, 0, 2, 1, 2)
        grid.addWidget(goldBox, 0, 4, 1, 2)
        grid.addWidget(mainButtons, 1, 2, 4, 2)
        grid.addWidget(leftButtons, 3, 0, 2, 1)
        grid.addWidget(rightButtons, 3, 5, 2, 1)
        grid.addWidget(radiobuttons, 4, 2, 1, 3)

        mainScreen = QWidget()
        mainScreen.setLayout(grid)
        mainScreen.setObjectName("main") # for the css

        self.setWindowTitle("Hearthstone")
        h = qApp.desktop().screenGeometry().height() - 100
        w = qApp.desktop().screenGeometry().width() - 350
        self.setGeometry(175, 0, w, h)
        self.setFixedSize(w, h)
        self.setCentralWidget(mainScreen)
        self.show()
        self.updateGoldCount() # so the numbers in the line edits up top are always accurate
        self.updateMoneyCount()
        self.updateRankCount()

    def updateGoldCount(self):
        try:
            self.gold.setText(str(Hearthstone.goldCount))
        except RuntimeError:
            pass

    def updateMoneyCount(self):
        try:
            self.money.setText(str(Hearthstone.moneyCount))
        except RuntimeError:
            pass

    def updateRankCount(self):
        try:
            if Hearthstone.rankCount <= 0:
                self.rank.setText("LEGEND") # In Hearthstone, rank 0 is called legend
            else:
                self.rank.setText(str(Hearthstone.rankCount))
        except RuntimeError:
            pass

    def updatePackOpenings(self): # this exists so if the player buys 2 packs and only uses one, the next time he visits the open packs screen, he only has one pack left
        Hearthstone.packCount -= PackOpeningGraph.usedPacks
        PackOpeningGraph.usedPacks = 0
        self.packScreen.show()

    def Save(self): # saves all important variable values in text files inside the repository
        Hearthstone.packCount -= PackOpeningGraph.usedPacks
        PackOpeningGraph.usedPacks = 0

        gold = open("SaveGame/gold.txt", "w")
        gold.write(str(Hearthstone.goldCount))
        gold.close

        rank = open("SaveGame/rank.txt", "w")
        rank.write(str(Hearthstone.rankCount))
        rank.close

        money = open("SaveGame/money.txt", "w")
        money.write(str(Hearthstone.moneyCount))
        money.close

        common = open("SaveGame/common.txt", "w")
        common.write(str(Hearthstone.commonCards))
        common.close

        rare = open("SaveGame/rare.txt", "w")
        rare.write(str(Hearthstone.rareCards))
        rare.close

        epic = open("SaveGame/epic.txt", "w")
        epic.write(str(Hearthstone.epicCards))
        epic.close

        legendary = open("SaveGame/legendary.txt", "w")
        legendary.write(str(Hearthstone.legendaryCards))
        legendary.close

        packs = open("SaveGame/packs.txt", "w")
        packs.write(str(Hearthstone.packCount))
        packs.close

        adventures = open("SaveGame/adventures.txt", "w")
        adventures.write(str(Hearthstone.adventureCount))
        adventures.close

    def Load(self): # loads all those important values into their respective variables
          gold = open("SaveGame/gold.txt")
          Hearthstone.goldCount = int(gold.read())
          gold.close

          rank = open("SaveGame/rank.txt")
          Hearthstone.rankCount = int(rank.read())
          rank.close

          money = open("SaveGame/money.txt")
          Hearthstone.moneyCount = int(money.read())
          money.close

          common = open("SaveGame/common.txt")
          Hearthstone.commonCards = int(common.read())
          common.close

          rare = open("SaveGame/rare.txt")
          Hearthstone.rareCards = int(rare.read())
          rare.close

          epic = open("SaveGame/epic.txt")
          Hearthstone.epicCards = int(epic.read())
          epic.close

          legendary = open("SaveGame/legendary.txt")
          Hearthstone.legendaryCards = int(legendary.read())
          legendary.close

          packs = open("SaveGame/packs.txt")
          Hearthstone.packCount = int(packs.read())
          packs.close

          adventures = open("SaveGame/adventures.txt")
          Hearthstone.adventureCount = int(adventures.read())
          adventures.close

          self.updateGoldCount() # so that the loaded numbers are showing
          self.updateMoneyCount()
          self.updateRankCount()
          self.packScreen = PackOpeningGraph(self.packCount) # it used to not show the loaded packs at first, I thought this might help..it didnt hurt, so...
          self.update() # always good to throw this in from time to time I heard...
          self.initGUI() # just to make really sure all is loaded, load up the main screen again

    def initMenu(self): # this sets up the menu bar at the very top of the screen and allows the player to save and load
        self.menubar = self.menuBar()
        saveAct = QAction("Save Game", self)
        loadAct = QAction("Load Game", self)
        saveAct.triggered.connect(self.Save)
        loadAct.triggered.connect(self.Load)
        self.makeMenu = self.menubar.addMenu("Save")
        self.makeMenu.addAction(saveAct)
        self.makeMenu.addAction(loadAct)

    def displayCollection(self): # shows the player the numbers of cards of different rarities they have in a pop up window
        Hearthstone.commonCards += PackOpeningGraph.commonCards # adds all cards obtained through pack openings to the cards already in the players collection
        Hearthstone.rareCards += PackOpeningGraph.rareCards
        Hearthstone.epicCards += PackOpeningGraph.epicCards
        Hearthstone.legendaryCards += PackOpeningGraph.legendaryCards
        PackOpeningGraph.commonCards = 0 # empties the variables for cards obtained through pack openings so that they arent constantly added on
        PackOpeningGraph.rareCards = 0
        PackOpeningGraph.epicCards = 0
        PackOpeningGraph.legendaryCards = 0
        text = "Your collection: \nCommon: %d\nRare: %d\nEpic: %d\nLEGENDARY: %d\n" %(Hearthstone.commonCards, Hearthstone.rareCards, Hearthstone.epicCards, Hearthstone.legendaryCards)
        collectionPopUp = QMessageBox()
        collectionPopUp.setText(text)
        collectionPopUp.exec_() # shows the pop up window

# the window for playing an adventure ##########################################################################

    def playAdventure(self):
        if Hearthstone.adventureCount >= 1: # you have to have bought at least one adventure!
            self.adventureTimer = QTimer(self)
            self.adventureTimer.setSingleShot(True)
            self.adventureTimer.timeout.connect(self.initGUI)

            self.helpTimer = QTimer(self)
            self.helpTimer.timeout.connect(self.updateProgressBar) # these timers are for the progress bar

            self.adventureProgress = QProgressBar()
            self.adventureProgress.setInvertedAppearance(True)
            self.adventureProgress.setMinimum(0)
            if self.f2p.isChecked() == True:
                self.adventureProgress.setMaximum(25000)
            elif self.p2w.isChecked() == True:
                self.adventureProgress.setMaximum(5000) # in pay to win mode, everything is a lot faster
            else:
                pass

            self.progressLabel = QLabel("Playing adventure.\nAcquiring:\n25 common cards\n15 rare cards\n10 epic cards\n5 legendary cards")
            if Hearthstone.freeToPlay == False:
                self.progressLabel.setStyleSheet("""
                    QLabel {
                        font-size: 18px;
                    	color: white;
                    	text-align : center;
                        font-family: "Apple Chancery";
                    }""") # so it looks different in pay to win mode - the white was most important for being readable with a background picture

            adventure_layout = QVBoxLayout()
            adventure_layout.addWidget(self.progressLabel)
            adventure_layout.addWidget(self.adventureProgress)

            adventureScreen = QWidget()
            adventureScreen.setLayout(adventure_layout)
            adventureScreen.setObjectName("adventure")

            self.setWindowTitle("Adventure")
            h = qApp.desktop().screenGeometry().height() - 550
            w = qApp.desktop().screenGeometry().width() - 1000
            self.setGeometry(20, 20, w, h)
            self.setFixedSize(w, h)
            self.setCentralWidget(adventureScreen)
            self.update()

            Hearthstone.commonCards += 25
            Hearthstone.rareCards += 15
            Hearthstone.epicCards += 10
            Hearthstone.legendaryCards += 5
            Hearthstone.adventureCount -= 1 # what a deal!

            if self.f2p.isChecked() == True:
                self.adventureTimer.start(25000)
            elif self.p2w.isChecked() == True:
                self.adventureTimer.start(5000) # faster...
            else:
                pass
            self.helpTimer.start(100)
        else:
            self.displayWarning()

    def updateProgressBar(self): # updates the progress bars progress depending on the helpTimer
        if (self.adventureTimer.remainingTime()) >= 1:
            self.adventureProgress.setValue(self.adventureTimer.remainingTime())
        else:
            pass

    def displayWarning(self): # in the case that the player should have 0 adventures
        text = "You must purchase an adventure first. Navigate to the shop to purchase an adventure!"
        warningPopUp = QMessageBox()
        warningPopUp.setText(text)
        warningPopUp.exec_()

# a lot of this is very similar to the playAdventure function ##########################################################################

    def playBrawl(self):
        if Hearthstone.brawlPlayed == False:
            self.brawlTimer = QTimer(self)
            self.brawlTimer.setSingleShot(True)
            self.brawlTimer.timeout.connect(self.initGUI)

            self.brawlHelpTimer = QTimer(self)
            self.brawlHelpTimer.timeout.connect(self.updateBrawlProgressBar)

            self.waitTilWednesday = QTimer(self)
            self.waitTilWednesday.setSingleShot(True)
            self.waitTilWednesday.timeout.connect(self.resetBrawl) # this is so the player cannot immediately play tavern brawl again, just like in the original

            self.brawlProgress = QProgressBar()
            self.brawlProgress.setInvertedAppearance(True)
            self.brawlProgress.setMinimum(0)
            if self.f2p.isChecked() == True:
                self.brawlProgress.setMaximum(25000)
            elif self.p2w.isChecked() == True:
                self.brawlProgress.setMaximum(5000)
            else:
                pass

            self.brawlProgressLabel = QLabel("Playing Tavern Brawl.\nAcquiring a card pack.")
            if Hearthstone.freeToPlay == False:
                self.brawlProgressLabel.setStyleSheet("""
                    QLabel {
                        font-size: 18px;
                    	color: white;
                    	text-align : center;
                        font-family: "Apple Chancery";
                    }""")

            brawl_layout = QVBoxLayout()
            brawl_layout.addWidget(self.brawlProgressLabel)
            brawl_layout.addWidget(self.brawlProgress)

            brawlScreen = QWidget()
            brawlScreen.setLayout(brawl_layout)
            brawlScreen.setObjectName("brawl")

            self.setWindowTitle("Tavern Brawl")
            h = qApp.desktop().screenGeometry().height() - 500
            w = qApp.desktop().screenGeometry().width() - 1000
            self.setGeometry(20, 20, w, h)
            self.setFixedSize(w, h)
            self.setCentralWidget(brawlScreen)
            self.update()

            Hearthstone.packCount += 1
            Hearthstone.brawlPlayed = True

            if self.f2p.isChecked() == True:
                self.brawlTimer.start(25000)
            elif self.p2w.isChecked() == True:
                self.brawlTimer.start(5000)
            else:
                pass
            self.brawlHelpTimer.start(100)
            self.waitTilWednesday.start(100000)
        else:
            self.displayBrawlWarning()

    def updateBrawlProgressBar(self):
        if (self.brawlTimer.remainingTime()) >= 1:
            self.brawlProgress.setValue(self.brawlTimer.remainingTime())
        else:
            pass

    def displayBrawlWarning(self):
        text = "It is not time for a new Tavern Brawl yet! Wait until Wednesday!"
        warningPopUp = QMessageBox()
        warningPopUp.setText(text)
        warningPopUp.exec_()

    def resetBrawl(self):
        Hearthstone.brawlPlayed = False # resets the brawl so it can be played again after the timer waitTilWednesday has run out

# a lot of this is similar to the last two functions, especially playBrawl ##########################################################################

    def playQuest(self):
        if Hearthstone.questPlayed == False:
            self.questTimer = QTimer(self)
            self.questTimer.setSingleShot(True)
            self.questTimer.timeout.connect(self.initGUI)

            self.questHelpTimer = QTimer(self)
            self.questHelpTimer.timeout.connect(self.updateQuestProgressBar)

            self.waitTilTomorrow = QTimer(self)
            self.waitTilTomorrow.setSingleShot(True)
            self.waitTilTomorrow.timeout.connect(self.resetQuest)

            self.questProgress = QProgressBar()
            self.questProgress.setInvertedAppearance(True)
            self.questProgress.setMinimum(0)
            if self.f2p.isChecked() == True:
                self.questProgress.setMaximum(25000)
            elif self.p2w.isChecked() == True:
                self.questProgress.setMaximum(5000)
            else:
                pass
            questGold = choice([40, 50, 60, 80, 100])
            self.questProgressLabel = QLabel("Playing Quest.\nAcquiring %d gold." % questGold)
            if Hearthstone.freeToPlay == False:
                self.questProgressLabel.setStyleSheet("""
                    QLabel {
                        font-size: 18px;
                    	color: white;
                    	text-align : center;
                        font-family: "Apple Chancery";
                    }""")

            quest_layout = QVBoxLayout()
            quest_layout.addWidget(self.questProgressLabel)
            quest_layout.addWidget(self.questProgress)

            questScreen = QWidget()
            questScreen.setLayout(quest_layout)
            questScreen.setObjectName("quest")

            self.setWindowTitle("Quest")
            h = qApp.desktop().screenGeometry().height() - 500
            w = qApp.desktop().screenGeometry().width() - 1000
            self.setGeometry(20, 20, w, h)
            self.setFixedSize(w, h)
            self.setCentralWidget(questScreen)
            self.update()

            Hearthstone.goldCount += questGold
            Hearthstone.questPlayed = True

            if self.f2p.isChecked() == True:
                self.questTimer.start(25000)
            elif self.p2w.isChecked() == True:
                self.questTimer.start(5000)
            else:
                pass
            self.questHelpTimer.start(100)
            self.waitTilTomorrow.start(50000)

        else:
            self.displayQuestWarning()

    def updateQuestProgressBar(self):
        if (self.questTimer.remainingTime()) >= 1:
            self.questProgress.setValue(self.questTimer.remainingTime())
        else:
            pass

    def displayQuestWarning(self):
        text = "It is not time for a new Quest yet! Wait until tomorrow!"
        warningPopUp = QMessageBox()
        warningPopUp.setText(text)
        warningPopUp.exec_()

    def resetQuest(self):
        Hearthstone.questPlayed = False

# still some is similar to the last 3 ##########################################################################

    def play(self):
        Hearthstone.commonCards += PackOpeningGraph.commonCards
        Hearthstone.rareCards += PackOpeningGraph.rareCards
        Hearthstone.epicCards += PackOpeningGraph.epicCards
        Hearthstone.legendaryCards += PackOpeningGraph.legendaryCards # same as in displayCollection -> adds all previously acquired cards to the players collection
        PackOpeningGraph.commonCards = 0
        PackOpeningGraph.rareCards = 0
        PackOpeningGraph.epicCards = 0
        PackOpeningGraph.legendaryCards = 0
        self.playTimer = QTimer(self)
        self.playTimer.setSingleShot(True)
        self.playTimer.timeout.connect(self.initGUI)
        self.playTimer.timeout.connect(self.displayDecision)

        self.playHelpTimer = QTimer(self)
        self.playHelpTimer.timeout.connect(self.updatePlayProgressBar)

        self.playProgress = QProgressBar()
        self.playProgress.setInvertedAppearance(True)
        self.playProgress.setMinimum(0)
        if self.f2p.isChecked() == True:
            self.playProgress.setMaximum(25000)
        elif self.p2w.isChecked() == True:
            self.playProgress.setMaximum(5000)
        else:
            pass

        self.playProgressLabel = QLabel("Playing a game versus\nan online opponent.")
        if Hearthstone.freeToPlay == False:
            self.playProgressLabel.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    color: white;
                    text-align : center;
                    font-family: "Apple Chancery";
                }""")

        play_layout = QVBoxLayout()
        play_layout.addWidget(self.playProgressLabel)
        play_layout.addWidget(self.playProgress)

        playScreen = QWidget()
        playScreen.setLayout(play_layout)
        playScreen.setObjectName("play")

        self.setWindowTitle("Ranked Game")
        h = qApp.desktop().screenGeometry().height() - 500
        w = qApp.desktop().screenGeometry().width() - 1000
        self.setGeometry(20, 20, w, h)
        self.setFixedSize(w, h)
        self.setCentralWidget(playScreen)
        self.update()

        self.chance = (Hearthstone.rankCount + 25) + Hearthstone.legendaryCards + (Hearthstone.epicCards * 0.25)
        if self.chance >= 99: # a calculation for the players percentage chance of winning
            self.chance = 98
        else:
            pass
        dieThrow = randint(0, 99)

        if self.chance >= dieThrow: # setting up the possible outcomes of the game
            if Hearthstone.rankCount == 0:
                self.decision = "victorious"
                Hearthstone.goldCount += 10
            else:
                Hearthstone.rankCount -= 1
                self.decision = "victorious"
                Hearthstone.goldCount += 10
        else:
            if Hearthstone.rankCount == 25: # cannot fall 'lower', numerically higher, than 25
                self.decision = "defeated"
            else:
                Hearthstone.rankCount += 1
                self.decision = "defeated"


        if self.f2p.isChecked() == True:
            self.playTimer.start(25000)
        elif self.p2w.isChecked() == True:
            self.playTimer.start(5000)
        else:
            pass
        self.playHelpTimer.start(100)

    def updatePlayProgressBar(self):
        if (self.playTimer.remainingTime()) >= 1:
            self.playProgress.setValue(self.playTimer.remainingTime())
        else:
            pass

    def displayDecision(self):
        text = "You were %s!" % self.decision
        if self.decision == "defeated":
            text = text + "\nBetter luck next time!\nMaybe you need more legendary cards."
        else:
            text = text + "\nGreat job!\nYou must have a large collection of powerful, expensive cards."
        warningPopUp = QMessageBox()
        warningPopUp.setText(text)
        warningPopUp.exec_()

# still similar... ##########################################################################

    def work(self):
        self.workTimer = QTimer(self)
        self.workTimer.setSingleShot(True)
        self.workTimer.timeout.connect(self.initGUI)

        self.workHelpTimer = QTimer(self)
        self.workHelpTimer.timeout.connect(self.updateWorkProgressBar)

        self.workProgress = QProgressBar()
        self.workProgress.setInvertedAppearance(True)
        self.workProgress.setMinimum(0)
        if self.f2p.isChecked() == True:
            self.workProgress.setMaximum(250000)
        elif self.p2w.isChecked() == True:
            self.workProgress.setMaximum(500000) # this actually takes longer in pay to win mode!
        else:
            pass

        self.workProgressLabel = QLabel("Working.\nAcquiring 1000 Dollars")

        work_layout = QVBoxLayout()
        work_layout.addWidget(self.workProgressLabel)
        work_layout.addWidget(self.workProgress)

        workScreen = QWidget()
        workScreen.setLayout(work_layout)
        workScreen.setObjectName("work")

        self.setWindowTitle("Work")
        h = qApp.desktop().screenGeometry().height() - 500
        w = qApp.desktop().screenGeometry().width() - 1000
        self.setGeometry(20, 20, w, h)
        self.setFixedSize(w, h)
        self.setCentralWidget(workScreen)
        self.update()

        Hearthstone.moneyCount += 1000

        if self.f2p.isChecked() == True:
            self.workTimer.start(250000)
        elif self.p2w.isChecked() == True:
            self.workTimer.start(500000)
        else:
            pass
        self.workHelpTimer.start(100)

    def updateWorkProgressBar(self):
        if (self.workTimer.remainingTime()) >= 1:
            self.workProgress.setValue(self.workTimer.remainingTime())
        else:
            pass

# sets up the shop and its GUI elements ##########################################################################

    def showShop(self):
        if Hearthstone.freeToPlay == True:
            self.buyPackBut = QPushButton("Only 100 Gold")
            self.buyPacksBut = QPushButton("Only 100 Dollars")
            self.buyAdventureBut = QPushButton("Only 3.500 Gold")
            self.buyAdventureMoneyBut = QPushButton("Or 350 Dollars")
        else:
            self.buyPackBut = QPushButton("Discounted: 50 Gold")
            self.buyPacksBut = QPushButton("Discounted: 50 Dollars")
            self.buyAdventureBut = QPushButton("Discounted: 1000 Gold")
            self.buyAdventureMoneyBut = QPushButton("Or 100 Dollars")

        self.buyPackBut.setObjectName("pack")
        self.buyPacksBut.setObjectName("packs")
        self.buyAdventureBut.setObjectName("adventuregold")
        self.buyAdventureMoneyBut.setObjectName("adventuremoney") # all for css

        self.buyPackLabel = QLabel("1 Card-Pack")
        if Hearthstone.freeToPlay == False: # guess i could have done this just like above...oops
            self.buyPackLabel.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    color: white;
                    font-family: "Apple Chancery";
                }""")
        self.buyPacksLabel = QLabel("50 Card-Packs")
        if Hearthstone.freeToPlay == False:
            self.buyPacksLabel.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    color: white;
                    font-family: "Apple Chancery";
                }""")
        self.buyAdventureLabel = QLabel("1 Adventure")
        if Hearthstone.freeToPlay == False:
            self.buyAdventureLabel.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    color: white;
                    font-family: "Apple Chancery";
                }""")
        self.buyPackBut.clicked.connect(self.buyPack)
        self.buyPacksBut.clicked.connect(self.buyPacks)
        self.buyAdventureBut.clicked.connect(self.buyAdventure)
        self.buyAdventureMoneyBut.clicked.connect(self.buyAdventureMoney)
        self.backLink = QPushButton("Go Back")
        self.backLink.setMaximumSize(100, 50)
        self.backLink.clicked.connect(self.initGUI)

        PackBox1 = QHBoxLayout()
        PackBox1.addWidget(self.buyPackLabel)
        PackBox1.addStretch(1)
        PackBox1.addWidget(self.buyPackBut)

        PackBox2 = QHBoxLayout()
        PackBox2.addWidget(self.buyPacksLabel)
        PackBox2.addStretch(1)
        PackBox2.addWidget(self.buyPacksBut)

        AdventureBox = QHBoxLayout()
        AdventureBox.addWidget(self.buyAdventureLabel)
        AdventureBox.addStretch(1)
        AdventureBox.addWidget(self.buyAdventureBut)
        AdventureBox.addStretch(1)
        AdventureBox.addWidget(self.buyAdventureMoneyBut)

        ShopLayout = QVBoxLayout()
        ShopLayout.addItem(PackBox1)
        ShopLayout.addStretch(2)
        ShopLayout.addItem(PackBox2)
        ShopLayout.addStretch(2)
        ShopLayout.addItem(AdventureBox)
        ShopLayout.addStretch(1)
        ShopLayout.addWidget(self.backLink)

        shopScreen = QWidget()
        shopScreen.setLayout(ShopLayout)
        shopScreen.setObjectName("shop")

        self.setWindowTitle("Shop")
        h = qApp.desktop().screenGeometry().height() - 500
        w = qApp.desktop().screenGeometry().width() - 900
        self.setGeometry(20, 20, w, h)
        self.setFixedSize(w, h)
        self.setCentralWidget(shopScreen)
        self.update()

    def buyAdventure(self): # all the possibilities when one wants to buy and adventure with gold, inluding current mode
        if Hearthstone.freeToPlay == True:
            if Hearthstone.goldCount >= 3500:
                Hearthstone.goldCount -= 3500
                Hearthstone.adventureCount += 1
            else:
                text = "You don't have enough gold!"
                warningPopUp = QMessageBox()
                warningPopUp.setText(text)
                warningPopUp.exec_()
        else:
            if Hearthstone.goldCount >= 1000:
                Hearthstone.goldCount -= 1000
                Hearthstone.adventureCount += 1
            else:
                text = "You don't have enough gold!"
                warningPopUp = QMessageBox()
                warningPopUp.setText(text)
                warningPopUp.exec_()

    def buyAdventureMoney(self): # same as above with money instead of gold
        if Hearthstone.freeToPlay == True:
            if Hearthstone.moneyCount >= 350:
                Hearthstone.moneyCount -= 350
                Hearthstone.adventureCount += 1
            else:
                text = "You don't have enough money!"
                warningPopUp = QMessageBox()
                warningPopUp.setText(text)
                warningPopUp.exec_()
        else:
            if Hearthstone.moneyCount >= 100:
                Hearthstone.moneyCount -= 100
                Hearthstone.adventureCount += 1
            else:
                text = "You don't have enough money!"
                warningPopUp = QMessageBox()
                warningPopUp.setText(text)
                warningPopUp.exec_()

    def buyPack(self): # same as two above except with a pack
        if Hearthstone.freeToPlay == True:
            if Hearthstone.goldCount >= 100:
                Hearthstone.goldCount -= 100
                Hearthstone.packCount += 1
            else:
                text = "You don't have enough gold!"
                warningPopUp = QMessageBox()
                warningPopUp.setText(text)
                warningPopUp.exec_()
        else:
            if Hearthstone.goldCount >= 50:
                Hearthstone.goldCount -= 50
                Hearthstone.packCount += 1
            else:
                text = "You don't have enough gold!"
                warningPopUp = QMessageBox()
                warningPopUp.setText(text)
                warningPopUp.exec_()

    def buyPacks(self): # same as above, just with 50 packs and money
        if Hearthstone.freeToPlay == True:
            if Hearthstone.moneyCount >= 100:
                Hearthstone.moneyCount -= 100
                Hearthstone.packCount += 50
            else:
                text = "You don't have enough money!"
                warningPopUp = QMessageBox()
                warningPopUp.setText(text)
                warningPopUp.exec_()
        else:
            if Hearthstone.moneyCount >= 50:
                Hearthstone.moneyCount -= 50
                Hearthstone.packCount += 50
            else:
                text = "You don't have enough money!"
                warningPopUp = QMessageBox()
                warningPopUp.setText(text)
                warningPopUp.exec_()

# the function that starts the craziness that is pay to win mode ##########################################################################

    def PayToWin(self):
        if Hearthstone.moneyCount > 0: # only possible if the player has at least some money
            if Hearthstone.freeToPlay == True: # and the mode is not yet engaged
                Hearthstone.freeToPlay = False
                self.popUpFriendsTimer.stop()
                self.popUpFinancesTimer.start(17500) # starts the pop up messages regarding a defficiency of finances on the players end

                styleSheet = open("css/p2w.css") # opens the main stlyesheet
                qApp.setStyleSheet(styleSheet.read())
                styleSheet.close()

                self.theme.stop()
                self.sax.play() # changes the music - FOR YOUR INFORMATION: THIS MUSIC IS COMMONLY PLAYED IN THE HEARTHSTONE COMMUNITY,
                self.sax.setLoops(100) # WHEN IMPRESSIVE FEATS SUCH AS MASSIVE COMBOS ARE SHOWN! THAT IS WHY I CHOSE IT TO REPRESENT
                if Hearthstone.welcomeGift == False: # THE PLAYER WHO SPENDS MONEY ON THE GAME TO BE AS GOOD AS POSSIBLE
                    text = "Congratulations for chosing to\nspend your money on this game!\nHave 5 complimentary adventures for your commitment."
                    congratsPopUp = QMessageBox()
                    congratsPopUp.setGeometry(500, 500, 500, 500)
                    congratsPopUp.setText(text)
                    congratsPopUp.exec_()
                    Hearthstone.adventureCount += 5 # the first time a player enters pay to win mode, he gets 5 adventures
                    Hearthstone.welcomeGift = True
                else:
                    pass

                Hearthstone.moneyCount -= 100 # so there can't be gold farming, 100 dollars are subtracted immediately upon selection of pay to win mode
                self.updateMoneyCount()

                self.moneyTimer.start(10000) # starts the constant subtraction/addition of values
                self.goldTimer.start(5000)
                self.rankTimer.start(15000)
            else:
                pass

        else:
            self.f2p.setChecked(True)

    def depleteMoney(self):
        try:
            Hearthstone.moneyCount -= 100
            if Hearthstone.moneyCount <= 0: # this happens when the player runs out of money before pressing the free to play button again
                self.moneyTimer.stop() # everything changes back into free to play mode
                self.rankTimer.stop()
                self.goldTimer.stop()
                self.popUpFriendsTimer.start(30000)
                self.popUpFinancesTimer.stop()
                qApp.setStyleSheet("")
                self.sax.stop()
                self.theme.play()
                self.theme.setLoops(100)
                Hearthstone.moneyCount = 0
                Hearthstone.freeToPlay = True
                self.f2p.setChecked(True)
                self.initGUI
                self.update()
                text = "It seems that you have run out of money...\nToo bad that we had to set you\nback to the free-to-play status."
                warningPopUp = QMessageBox()
                warningPopUp.setText(text)
                warningPopUp.exec_()
            else:
                pass
            self.updateMoneyCount()
            self.update()
        except RuntimeError: # I had some errors when the player was still in another window than the main screen when they ran out of money..
            self.popUpFriendsTimer.start(30000)
            self.popUpFinancesTimer.stop()
            qApp.setStyleSheet("")
            self.sax.stop()
            self.theme.play()
            self.theme.setLoops(100)
            self.moneyTimer.stop()
            self.rankTimer.stop()
            self.goldTimer.stop()
            Hearthstone.moneyCount = 0
            Hearthstone.freeToPlay = True
            text = "It seems that you have run out of money...\nToo bad that we had to set you\nback to the free-to-play status."
            warningPopUp = QMessageBox()
            warningPopUp.setText(text)
            warningPopUp.exec_()

    def increaseRank(self):
        Hearthstone.rankCount -= 1
        self.updateRankCount()
        self.update()

    def increaseGold(self):
        Hearthstone.goldCount += 100
        self.updateGoldCount()
        self.update()

# this connects to the free to play button being pressed and does basically all that depleteMoney does, when the player runs out of money ##########################################################################

    def FreeToPlay(self):
        if Hearthstone.moneyCount <= 0:
            self.moneyTimer.stop()
            self.rankTimer.stop()
            self.goldTimer.stop()
        else:
            pass
        self.popUpFriendsTimer.start(30000)
        self.popUpFinancesTimer.stop()
        qApp.setStyleSheet("")
        self.sax.stop()
        self.theme.play()
        self.theme.setLoops(100)
        try:
            self.moneyTimer.stop()
            self.rankTimer.stop()
            self.goldTimer.stop()
            Hearthstone.freeToPlay = True
            self.f2p.setChecked(True)
            text = "We are sad to see you\ngo back to that place.\nCome back some time."
            byePopUp = QMessageBox()
            byePopUp.setText(text)
            byePopUp.exec_()
            self.initGUI
            self.update()
        except AttributeError:
            pass

# randomly selects one of the 10 / 7 messages and makes them pop up ##########################################################################

    def popUpFriends(self):
        message = randint(0, 9)
        messages = ["Hey dude, why aren't you at the hockey game?", "Come on out here, man!", "This is your mother. You have not come out of your room for 3 days. What are you doing in there?!",
                    "I miss you, we should hang out again some time!", "Haven't seen you at school in some time, are you on vacation or something?", "You are playing Hearthstone again, aren't you?",
                    "The concert last night was awesome! Why didn't you come again?", "Dude! Did you sleep through the exam this morning?!", "The weather is nice out, want to go for a hike?",
                    "Last chance! If you want to come with me to Spain tomorrow, you gotta decide NOW!"]
        self.ping.play()
        text = messages[message]
        self.friendPopUp = QMessageBox()
        self.friendPopUp.setText(text)
        self.friendPopUp.setWindowTitle("New Message")
        self.friendPopUp.setGeometry(0, 0, 300, 200)
        self.friendPopUp.setObjectName("friend")
        self.friendPopUp.exec_()

    def popUpFinances(self):
        message = randint(0, 6)
        messages = ["Your credit card has been denied due to insuficcient funds.", "Dude, I like you, but I need you to pay the rent on time. Don't let me down..", "WHERE'S MY MONEY?!",
                    "Hey, just checking in about the 12$ you're still owing me. I'd appreciate them back.", "Dear customer, you just went over the limit of your bank account. Thus it was closed until further notice.",
                    "Dear, I'm so glad your mom and I can support you going to college. I hope the money lasts the month!", "Hey, just wanted to inform you that the interest for last month's loan went up to 8%, because I still don't have the money from you.."]
        self.ping.play()
        text = messages[message]
        self.financePopUp = QMessageBox()
        self.financePopUp.setText(text)
        self.financePopUp.setWindowTitle("New Message")
        self.financePopUp.setGeometry(0, 0, 300, 200)
        self.financePopUp.setObjectName("finance")
        self.financePopUp.exec_()

# starts the application! ##########################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Hearthstone()
    sys.exit(app.exec_())
