from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QAction, qApp, QMainWindow
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore
import sys
import json

class Pencere(QWidget):

    def __init__(self):
    
        super().__init__()
        self.init_ui()
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.updateText)
        timer.start(5000)

    def init_ui(self):

        self.kelime_str = QLabel("Kelime:")
        self.kelime = QLineEdit()

        self.ip1_str = QLabel("İpucu 1:")
        self.ip1 = QLineEdit()

        self.ip2_str = QLabel("İpucu 2:")
        self.ip2 = QLineEdit()

        self.ip3_str = QLabel("İpucu 3:")
        self.ip3 = QLineEdit()

        self.ekle = QPushButton("Ekle")
        self.yazi_alani = QLabel("")

        v_box = QVBoxLayout()
        
        v_box.addWidget(self.kelime_str)
        v_box.addWidget(self.ip1_str)
        v_box.addWidget(self.ip2_str)
        v_box.addWidget(self.ip3_str)

        v_box2 = QVBoxLayout()
        
        v_box2.addWidget(self.kelime)
        v_box2.addWidget(self.ip1)
        v_box2.addWidget(self.ip2)
        v_box2.addWidget(self.ip3)

        h_box = QHBoxLayout()
        h_box.addLayout(v_box)
        h_box.addLayout(v_box2)

        h_box2 = QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.ekle)
        h_box2.addStretch()

        h_box3 = QHBoxLayout()
        h_box3.addStretch()
        h_box3.addWidget(self.yazi_alani)
        h_box3.addStretch()



        v_box3 = QVBoxLayout()
        v_box3.addLayout(h_box)
        v_box3.addLayout(h_box3)
        v_box3.addLayout(h_box2)

        self.ekle.clicked.connect(self.click)
        self.setWindowTitle("İpucu Ekleyici")
        self.setWindowIcon(QIcon("logo_json.png"))
        self.setMinimumHeight(170)
        self.setMaximumHeight(170)
        self.setMinimumWidth(350)
        self.setMaximumWidth(350)
        self.setLayout(v_box3)
        self.show()
    
    def click(self):
        with open("ipucu.json","r+", encoding="utf-8") as file:
            self.icerik = file.read()
            self.json_text = json.loads(self.icerik)
            
            self.json_file = json.dumps(self.json_text, indent = 4, ensure_ascii = False)


        kelime = self.kelime.text()
        ipucu1 = self.ip1.text()
        ipucu2 = self.ip2.text()
        ipucu3 = self.ip3.text()

        if kelime == "" or ipucu1 == "" or ipucu2 == "" or ipucu3 == "":
            self.yazi_alani.setText("Lütfen boş bırakmayın!")
            return False

        text = (""" 
        ,"%s" : {
            "1" : "%s",
            "2" : "%s",
            "3" : "%s"
        }
""" % (kelime, ipucu1, ipucu2, ipucu3))

        with open("ipucu.json", "w", encoding="utf-8") as file:
            file.write(self.json_file[:-4]  + text + "\t}\n" + "}")
            self.yazi_alani.setText("Başarı ile eklendi.")

    def updateText(self):
        self.yazi_alani.setText("")

app = QApplication(sys.argv)
window = Pencere()
sys.exit(app.exec_())