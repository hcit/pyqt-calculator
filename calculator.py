#!/usr/bin/python
from __future__ import division
import sys
import re
from sympy import solve, symbols
from ButtonsSetUp import *
from math import *
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class screen(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(screen, self).__init__(parent)
        # File menu setup
        eq_mode = QtGui.QAction('&Equation Solver', self)
        eq_mode.setShortcut('ctrl+e')
        eq_mode.triggered.connect(self.screenSetup_eq)
        basic_mode = QtGui.QAction('&Basic', self)
        basic_mode.setShortcut('ctrl+b')
        basic_mode.triggered.connect(self.screenSetup_basic)
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('ctrl+q')
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.setGeometry(300,300, 320, 300)
        self.setWindowTitle('Calculator')
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Calculator')
        #button lists
        self.allButtons = []
        self.pushButtons = []
        self.eqButtons = []

        fileMenu.addAction(eq_mode)
        fileMenu.addAction(basic_mode)
        fileMenu.addAction(exitAction)
        #by default, basic mode is loaded
        self.screenSetup_basic()
        #ans - the intermediate result
        self.ans = ''
        self.show()
    
    def screenSetup_basic(self):
        if len(self.allButtons) != 0:
            #if buttons were already created but hidden to
            # display Equation Solver interface
            for button in self.allButtons:
                button.show()
            if len(self.eqButtons) != 0:
                #if Eq mode was previously selected
                for button in self.eqButtons:
                    button.hide()
            return
        self.input_line = QtGui.QLineEdit(self)
        self.input_line.setAlignment(Qt.AlignRight)
        self.input_line.move(10,35)
        self.input_line.setFixedHeight(50)
        self.input_line.setFixedWidth(300)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.input_line.setFont(font)
        putButtons(self)
        self.allButtons.append(self.input_line)

        for button in self.pushButtons:
            #connecting buttons to input their value
            button.clicked.connect(self.insertText)

        #connecting special buttons to their function
        self.allButtons[0].clicked.connect(self.clearScreen)
        self.allButtons[1].clicked.connect(self.delChar)
        self.allButtons[2].clicked.connect(self.putAns)
        self.allButtons[3].clicked.connect(self.evaluate)
        self.allButtons[3].setShortcut('return')


    def insertText(self):
        button = self.sender()
        if button.text() == 'sqrt':
            self.input_line.insert('sqrt(')
            return
        self.input_line.insert(button.text())

    def clearScreen(self):
        button = self.sender()
        try:
            self.input_line.clear()
            self.input_text.clear()
        except AttributeError:
            pass

    def delChar(self):
        button = self.sender()
        self.input_line.backspace()

    def putAns(self):
        button = self.sender()
        self.input_line.insert('ans')

    def evaluate(self):
        button = self.sender()
        if self.ans != '':
            try:
                ans = eval(str(self.ans))
            except ZeroDivisionError:
                self.input_line.setText('Inf')
                self.ans = '0'
                return
        self.ans = str(self.input_line.displayText())
        #replace for pow operand
        self.ans = self.ans.replace('^', '**')
        try:
            self.ans = eval(self.ans)
        except ZeroDivisionError:
            self.input_line.setText('Inf')
            return

        if self.ans == int(self.ans):
            #disp ans as an int
            self.ans = int(self.ans)
        self.ans = str(self.ans)
        self.input_line.setText(self.ans)

    def screenSetup_eq(self):
        for button in self.allButtons:
            button.hide()
        if len(self.eqButtons) != 0:
            for button in self.eqButtons:
                button.show()
            return
        self.input_line.hide()
        self.input_text = QtGui.QTextEdit(self)
        self.input_text.setFixedWidth(300)
        self.input_text.setFixedHeight(200)
        self.input_text.move(10,40)
        self.input_text.show()

        self.button_solve = QPushButton('Solve',self)
        self.button_solve.move(20, 250)
        self.button_solve.setShortcut('ctrl+s')
        self.button_solve.show()
        self.button_clear_eq = QPushButton('Clear', self)
        self.button_clear_eq.setShortcut('ctrl+c')
        self.button_clear_eq.move(200, 250)
        self.button_clear_eq.show()
        self.button_clear_eq.clicked.connect(self.clearScreen)

        self.eqButtons.append(self.input_text)
        self.eqButtons.append(self.button_solve)
        self.eqButtons.append(self.button_clear_eq)
        self.button_solve.clicked.connect(self.solve)

    def solve(self):
        button = self.sender()
        equation = str(self.input_text.toPlainText())
        equation = equation.replace('\n',', ')
        equation = equation.replace('=', ' - ')
        var_list = set(re.findall(r'[a-z]', equation))
        vars_ = ''
        for var in var_list:
            vars_ += str(var) + ','
        command = vars_ + ' = symbols(\'' + vars_ + '\')'
        exec(command)
        vars_ = ', [' + vars_ + '])'
        equation = 'res_dict = solve([' + equation + ']'
        exec(equation + vars_)
        result = ''
        for key in res_dict:
            result += str(key) + ' = ' + str(res_dict[key]) + '\n'
        self.input_text.setText(result)


def main():
    app = QtGui.QApplication(sys.argv)
    test = screen()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
