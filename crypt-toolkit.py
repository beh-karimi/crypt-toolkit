from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtCore import *

class XorTab(QWidget):
    def __init__(self):
        super(XorTab, self).__init__()
        self.lastType = 0
        self.modifying = False

        mainLay = QHBoxLayout()

        optLay = QVBoxLayout()
        optLay.setAlignment(Qt.AlignTop)
        optLay.setSpacing(0)
        optLaySizeWid = QWidget()

        self.optIOType = QButtonGroup(self)
        optIOTypeText = QLabel("Format:")
        font = optIOTypeText.font()
        font.setPointSize(15)
        optIOTypeText.setFont(font)
        optIOHex = QRadioButton("Hex")
        optIOHex.setChecked(True)
        optIOBin = QRadioButton("Binary")
        self.optIOType.addButton(optIOHex, 16)
        self.optIOType.addButton(optIOBin, 2)
        self.optIOType.idClicked.connect(self.change_type)
        optLay.addWidget(optIOTypeText)
        optLay.addWidget(optIOHex)
        optLay.addWidget(optIOBin)

        ioLay = QVBoxLayout()
        inp1Text = QLabel("Input 1: ")
        self.inp1 = QTextEdit()
        self.inp1.setAcceptRichText(False)
        self.inp1.textChanged.connect(self.inp_change)
        self.inp1.setTabChangesFocus(True)
        inp2Text = QLabel("Input 2: ")
        self.inp2 = QTextEdit()
        self.inp2.setAcceptRichText(False)
        self.inp2.textChanged.connect(self.inp_change)
        self.inp2.setTabChangesFocus(True)
        outText = QLabel("Output: ")
        self.out = QTextEdit()
        self.out.setAcceptRichText(False)
        self.out.setReadOnly(True)
        self.out.setTabChangesFocus(True)
        ioLay.addWidget(inp1Text)
        ioLay.addWidget(self.inp1)
        ioLay.addWidget(inp2Text)
        ioLay.addWidget(self.inp2)
        ioLay.addWidget(outText)
        ioLay.addWidget(self.out)
        
        mainLay.addLayout(optLay, 0)
        mainLay.addLayout(ioLay, 1)
        self.setLayout(mainLay)

    def change_type(self, type):
        if self.lastType != type:
            self.lastType = type
            self.modifying = True
            for w in (self.inp1, self.inp2):
                a = w.toPlainText()
                s = ""
                if type == 2:
                    for n in range(len(a)):
                        ss = bin(int(a[n], 16))[2:]
                        if len(ss)%4 != 0:
                            for n in range(4-len(ss)%4):
                                ss = "0" + ss
                        s += ss

                else:
                    for n in range(0, len(a), 4):
                        s += hex(int(a[n:n+4], 2))[2:]
                w.setText(s)
            self.modifying = False
            self.inp_change()



    def inp_change(self):
        if not self.modifying:
            base = self.optIOType.checkedId()
            a = self.inp1.toPlainText()
            b = self.inp2.toPlainText()
            s=""
            if len(a) > len(b):
                for i in range(len(b)):
                    if base==16:
                        s += hex(int(a[i],16) ^ int(b[i],16))[2:]
                    else:
                        s += bin(int(a[i],2) ^ int(b[i],2))[2:]
            else:
                for i in range(len(a)):
                    if base==16:
                        s += hex(int(a[i],16) ^ int(b[i],16))[2:]
                    else:
                        s += bin(int(a[i],2) ^ int(b[i],2))[2:]
            self.out.setText(s)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)

        tabs.addTab(XorTab() , "Xor")

        self.setCentralWidget(tabs)

app = QApplication([])

mainwindow = MainWindow()
mainwindow.show()

app.exec()
