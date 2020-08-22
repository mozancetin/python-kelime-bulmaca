from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QAction, qApp, QMainWindow
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore
import json
import sys
import os


class Game(QWidget):

    def __init__(self):

        super().__init__()
        self.dosya_ac()
        self.para = 30
        self.count = 2
        self.restart_count = 0
        self.level_count = 1
        self.bildi = False
        self.end = False
        self.init_ui()

    def dosya_ac(self):
        global data
        global ipuclari
        with open("ipucu.json", encoding="utf-8") as json_file:
            data = json.load(json_file)
        
        ipuclari = list()
        for i in data:
            for x in data[i].keys():
                ipuclari.append(x)

    def init_ui(self):


        self.gold = QLabel("Gold: ")
        self.gold_str = QLabel(str(self.para))
        self.level = QLabel("Level ")
        self.level_str = QLabel(str(self.level_count))

        self.i1 = QLabel("İpucu 1: ")
        self.i1_str = QLabel(data['kelime'][ipuclari[self.restart_count]]['1'])

        self.i2 = QLabel("İpucu 2: ")
        self.i2_str = QLabel("İpucu Kilitli!")

        self.i3 = QLabel("İpucu 3: ")
        self.i3_str = QLabel("İpucu Kilitli!")

        self.yazi_alani = QLineEdit()
        self.i_btn = QPushButton("İpucu Aç (-10g)")
        self.tahmin_btn = QPushButton("Tahmin Et")
        self.sonraki = QPushButton("Sonraki")

        self.text = QLabel("")


        h_box = QHBoxLayout()
        h_box.addWidget(self.gold)
        h_box.addWidget(self.gold_str)
        h_box.addStretch()
        h_box.addWidget(self.level)
        h_box.addWidget(self.level_str)

        v_box = QVBoxLayout()
        v_box.addWidget(self.i1)
        v_box.addStretch()
        v_box.addWidget(self.i2)
        v_box.addStretch()
        v_box.addWidget(self.i3)
        v_box.addStretch()

        v2_box = QVBoxLayout()
        v2_box.addWidget(self.i1_str)
        v2_box.addStretch()
        v2_box.addWidget(self.i2_str)
        v2_box.addStretch()
        v2_box.addWidget(self.i3_str)
        v2_box.addStretch()
        
        h2_box = QHBoxLayout()
        h2_box.addStretch()
        h2_box.addLayout(v_box)
        h2_box.addLayout(v2_box)
        h2_box.addStretch()

        v3_box = QVBoxLayout()
        v3_box.addLayout(h_box)
        v3_box.addStretch()
        v3_box.addLayout(h2_box)
        v3_box.addStretch()
        v3_box.addWidget(self.yazi_alani)

        h3_box = QHBoxLayout()
        h3_box.addWidget(self.i_btn)
        h3_box.addWidget(self.tahmin_btn)
        h3_box.addWidget(self.sonraki)

        h4_box = QHBoxLayout()
        h4_box.addStretch()
        h4_box.addWidget(self.text)
        h4_box.addStretch()

        v4_box = QVBoxLayout()
        v4_box.addLayout(v3_box)
        v4_box.addLayout(h3_box)
        v4_box.addLayout(h4_box)



        self.setLayout(v4_box)
        self.setWindowTitle("Kelime Bulmaca")
        self.setWindowIcon(QIcon("logo.png"))
        self.setMinimumHeight(250)
        self.setMaximumHeight(250)
        self.setMinimumWidth(350)
        self.setMaximumWidth(350)
        self.i_btn.clicked.connect(self.info)
        self.tahmin_btn.clicked.connect(self.guess)
        self.sonraki.clicked.connect(self.next)
        self.show()
    
    def info(self):
        if self.count == 4 or self.end == True:
            return False
        if self.para >= 10:
            self.para -= 10
            self.gold_str.setText(str(self.para))

            if self.count == 2:
                self.i2_str.setText(data['kelime'][ipuclari[self.restart_count]][str(self.count)])
                self.count += 1
            elif self.count == 3:
                self.i3_str.setText(data['kelime'][ipuclari[self.restart_count]][str(self.count)])
                self.count += 1

        else:
            self.text.setText("Yeterli Gold Yok!")
            



    def guess(self):
        kullanıcı_tahmini = self.yazi_alani.text().lower()
        if kullanıcı_tahmini == "" or self.bildi == True or self.end == True:
            return False
        if self.text.text() != "":
            self.text.setText("")
        kelime = ipuclari[self.restart_count]
        if kullanıcı_tahmini == kelime:
            self.bildi = True
            self.para += 5
            self.gold_str.setText(str(self.para))
            self.text.setText("Doğru bildin! Sonraki soruya geç")
        else:
            self.text.setText("Bilemedin. Tekrar dene.")
            return False


            
    def next(self):
        if self.bildi == False or self.end == True:
            return False
        if self.restart_count != len(ipuclari)-1:
            self.restart_count += 1
            self.bildi = False
            self.count = 2
            self.yazi_alani.clear()
            self.i1_str.setText(data['kelime'][ipuclari[self.restart_count]]['1'])
            self.i2_str.setText("İpucu Kilitli!")
            self.i3_str.setText("İpucu Kilitli!")
            if self.level_count != len(ipuclari)-1:
                self.level_count += 1
                self.level_str.setText(str(self.level_count))
            else:
                self.level_str.setText("MAX")
        else:
            self.text.setText("Tebrikler bitirdiniz.")
            self.end = True
            return False

        if self.text.text() != "":
            self.text.setText("")
        


app = QApplication(sys.argv)
menu = Game()
sys.exit(app.exec_())
