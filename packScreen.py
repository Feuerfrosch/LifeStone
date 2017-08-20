# I experimented with a custom widget to kind of recreate the original card opening setup
#-> dragging a pack into a frame in which it is obliterated and the cards from within are shown
# This took way too much time, although I was able to draw from Jonathan's examples, this is why I didn't implement more custom widgets

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QObject, QPoint, QRect, pyqtSignal
from PyQt5.QtGui import QBrush, QPen, QColor, QFont, QPainter
from random import randint
import sys

# the class of the pack that must be dragged ##########################################################################

class Pack(QObject):
    PackMoved = pyqtSignal(QPoint)

    def __init__(self, xpos, ypos, width, length):
        super(Pack, self).__init__()
        self.length = length
        self.width = width
        self.pos = QPoint(xpos, ypos)
    def setPos(self, newpos):
        self.pos.setX(newpos.x() - (self.width / 2))
        self.pos.setY(newpos.y() - (self.length / 2))
        self.PackMoved.emit(self.pos)
    def x(self):
        return self.pos.x()
    def y(self):
        return self.pos.y()
    def bounds(self):
        return QRect(self.x(), self.y(), self.width, self.length)

# the class of the frame into which the pack must be dragged ##########################################################################

class Frame(QObject):
    def __init__(self, xpos, ypos, width, length):
        super(Frame, self).__init__()
        self.pos = QPoint(xpos, ypos)
        self.width = width
        self.length = length
    def x(self):
        return self.pos.x()
    def y(self):
        return self.pos.y()
    def bounds(self):
        return QRect(self.x(), self.y(), self.width, self.length)

# the main class of the custom widget ############################################################################

class PackOpeningGraph(QWidget):
    packAmountGlobal = 0
    usedPacks = 0
    commonCards = 0
    rareCards = 0
    epicCards = 0
    legendaryCards = 0 # these variables are for communication of values between the files main.py and packScreen.py

    def __init__(self, packAmount, parent=None):
        super(PackOpeningGraph, self).__init__(parent)
        PackOpeningGraph.packAmountGlobal = packAmount
        self.packBrush = QBrush(QColor(31, 207, 54))
        self.frameBrush = QBrush(QColor(8, 26, 47))
        self.backgroundBrush = QBrush(QColor(154, 114, 37))
        self.linePen = QPen(Qt.SolidLine)
        self.linePen.setWidth(2)
        self.framePen = QPen(Qt.white, Qt.SolidLine)
        self.currentPack = None
        self.dragStartPos = None
        self.startPosition = QPoint(50, 100)
        self.setMinimumSize(400, 200)
        self.pack = Pack(0,0,100,200) # instances of pack and frame, note that frame is slightly larger for visual comfort
        self.frame = Frame(340, 250, 110, 220)
        self.font = QFont("Arial", 18, QFont.Medium) # this didnt really work i found
        self.text = "1 Hearthstone\nCard Pack"
        self.frameText = "Drop it in\nhere to open"

        self.setGeometry(175, 0, 800, 800)
        self.setWindowTitle("Open Packs!")

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(self.linePen)
        qp.setBrush(self.backgroundBrush)
        qp.drawRect(self.rect())

        qp.setPen(self.framePen)
        qp.setBrush(self.frameBrush)
        qp.drawRect(self.frame.bounds())
        qp.drawText(self.frame.bounds(), Qt.AlignCenter, self.frameText)

        if PackOpeningGraph.packAmountGlobal >= 1: # if there is at least one card pack in the playes posession, draw one to be dragged
            qp.setPen(self.linePen)
            qp.setBrush(self.packBrush)
            qp.drawRect(self.pack.bounds())
            qp.drawText(self.pack.bounds(), Qt.AlignCenter, self.text)
        else:
            pass

    def mousePressEvent(self, event):
        mouseX = event.pos().x()
        mouseY = event.pos().y()
        self.currentPack = None

        p = self.pack.bounds()
        if mouseX > p.left() and mouseX < p.right() and mouseY > p.top() and mouseY < p.bottom():
            self.currentPack = self.pack
            self.dragStartPos = QPoint(self.pack.x(), self.pack.y())
        else:
            pass

    def mouseMoveEvent(self, event):
        if self.currentPack != None:
            w = self.width()
            h = self.height()
            mouse = event.pos()
            if  mouse.x() > 0 and mouse.x() < w and mouse.y() > 0 and mouse.y() < h:
                self.currentPack.setPos(mouse)
            else:
                self.currentPack.setPos(self.dragStartPos)
                self.dragStartPos = None
                self.currentPack = None
            self.update()

# this is where the action happens #####################################################

    def mouseReleaseEvent(self, event):
            mouseX = event.pos().x()
            mouseY = event.pos().y()
            f = self.frame.bounds()
            if mouseX > f.left() and mouseX < f.right() and mouseY > f.top() and mouseY < f.bottom():
                if self.currentPack != None: # if the mouse has a pack in hand and is within the bounds of the frame...
                    for i in range(0, 5):
                        i = randint(1, 100) #0 to 99 was too annoying for calculating
                        if i <= 5:
                            PackOpeningGraph.legendaryCards += 1
                        elif (i > 5) and (i <= 15):
                            PackOpeningGraph.epicCards += 1
                        elif (i > 15) and (i <= 50):
                            PackOpeningGraph.rareCards += 1
                        else:
                            PackOpeningGraph.commonCards += 1 # give the player 5 cards whose rarity is calculated with different percentage chances
                    PackOpeningGraph.packAmountGlobal -= 1 # reduce the amount of card packs by one
                    PackOpeningGraph.usedPacks += 1 # and increase the amount of used card packs by one
                    self.currentPack.setPos(self.startPosition) # it looks like the old card pack has disappeared and a new one has taken its place
                    self.update()
                    text = "Your total card earnings: \nCommon: %d\nRare: %d\nEpic: %d\nLEGENDARY: %d\n" %(PackOpeningGraph.commonCards, PackOpeningGraph.rareCards, PackOpeningGraph.epicCards, PackOpeningGraph.legendaryCards)
                    collectionPopUp = QMessageBox()
                    collectionPopUp.setText(text)
                    collectionPopUp.exec_() # lastly, show the player after every opening what they got in the pack
                else:
                    pass
            else:
                pass

            if self.currentPack != None:
                self.currentPack = None
