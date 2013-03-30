from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui

def putButtons(screen):
    names = [ '7', '8', '9', '/', 'C', 'del',
            '4', '5', '6', '*', '(', ')',
            '1', '2', '3', '-', 'sqrt', 'ans',
            '0', '.', '^', '+', '=']
    #available positions for buttons
    X = [10, 60, 110, 160, 210, 260]
    posY = [ 90, 140, 190, 240, 290]

    special_names = [ 'del', 'C', 'ans', '=']
    screen.pushButtons = []
    screen.allButtons = []
    x = -40
    y = 40
    j = 0
    for i in names:
        x = (x + 50) % 300
        if j % 6 == 0:
            y = y % 290 + 50
        button = QtGui.QPushButton(i, screen)
        if i == '=':
            button.resize(100,50)
        else:
            button.resize(50,50)
        if i not in special_names:
            screen.pushButtons.append(button)
        else:
            screen.allButtons.append(button)
        button.move(x,y)
        button.show()
        j += 1
    screen.allButtons.extend(screen.pushButtons)


