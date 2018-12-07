import os
import random
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QHBoxLayout, QLabel, QComboBox, QDialog, QListWidget, QTableWidget
from PyQt5.QtCore import QTimer, Qt, QPoint, QObject
import numpy as np
import datetime
import sys
import webbrowser


class okf_sorsolo(QtWidgets.QMainWindow):
    def read_namelist(self):
        elemek = self.namelist.toPlainText().split('\n')
        #emberek.append(elemek.split())
        return(elemek)

    def sorsolas(self):
        if len(self.read_namelist()) == 0:
            QMessageBox.warning(self,'Hiba','Nem hagyhatod üresen a versenyzők listáját!',buttons = QMessageBox.Ok)
        else:
            sor = 0
            versenyzok_oszlop = ''
            emberek_ures = 0
            oszlopok_ures = 0
            self.namelist_pairs.clear()
            elemek = self.read_namelist()
            paros_paratlan = len(elemek)%2
            if paros_paratlan%2 == 1: elemek.append('*BYE*')
            random.shuffle(elemek)
            parok = zip(*[iter(elemek)]*2)
            self.namelist_pairs.append('Első körös párosítás')
            self.namelist_pairs.append('------------------- ')
      
            for jatekos1, jatekos2 in parok:
                megszakitas = 0
                if jatekos1 == '' or jatekos2 == '':
                    QMessageBox.warning(self,'Hiba','Nem lehetnek a listában üres sorok!\nÚjra sorsolás engedélyezve', buttons = QMessageBox.Ok)
                    megszakitas = 1
                    self.sorsolas_button.setEnabled(True)
                    break
                else:
                    self.namelist_pairs.append(str(jatekos1.strip())+" vs "+str(jatekos2.strip()))
                    self.namelist_pairs.append(' ')
            if megszakitas == 0:
                self.tablazat.setRowCount(len(self.read_namelist()))
                self.tablazat.setColumnCount(6)
                self.tablazat.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.tablazat.verticalHeader().setVisible(False)
                self.tablazat.setHorizontalHeaderLabels(["Versenyző","Forduló 1", "Forduló 2", "Forduló 3", "Forduló 4", "Forduló 5"])
                flags = Qt.ItemFlags()
                flags != Qt.ItemIsEnabled
                for emberek_tablazatba in elemek:
                    if emberek_tablazatba == "*BYE*":
                        continue
                    else:
                        self.tablazat.setItem(sor,0,QtWidgets.QTableWidgetItem(emberek_tablazatba))
                        sor = sor + 1
                self.sorsolas_button.setEnabled(False)
             

    def kiertekeles_process(self):
        self.tablazat_2.clear()
        jatekos_vegeredmeny_sor = 0
        jatekosok_osszesen = self.read_namelist()
        ossz_jatekos_sor = self.tablazat.rowCount()
        #Eredmeny tablazat elokeszitese
        self.tablazat_2.verticalHeader().setVisible(False)
        self.tablazat_2.setColumnCount(2)
        self.tablazat_2.setRowCount(ossz_jatekos_sor)
        self.tablazat_2.setHorizontalHeaderLabels(["Versenyző","Összes pontszám"])
        self.tablazat_2.setColumnWidth(1,245)
        self.tablazat_2.setColumnWidth(0,245)
        for jatekos_eredmenyek in range(0,ossz_jatekos_sor):
            eredmeny_osszeg_2 = 0
            jatekos = self.tablazat.item(jatekos_eredmenyek,0).text()
            if jatekos == "unlock_parositas":
                self.sorsolas_button.setEnabled(True)
                break
            for jatekos_eredmenyek_fordulo in range(1,6):
                if self.tablazat.item(jatekos_eredmenyek,jatekos_eredmenyek_fordulo) is None or len(self.tablazat.item(jatekos_eredmenyek,jatekos_eredmenyek_fordulo).text()) == 0:
                    eredmeny_osszeg = 0
                else:
                    mehet = ''
                    try:
                        int(self.tablazat.item(jatekos_eredmenyek,jatekos_eredmenyek_fordulo).text())%2
                        mehet = 1
                    except ValueError:
                        QMessageBox.critical(self,'Hiba','Csak numerikus értéket adhatsz meg!',buttons = QMessageBox.Ok)
                        break
                    if mehet == 1:
                     eredmeny_osszeg = int(self.tablazat.item(jatekos_eredmenyek,jatekos_eredmenyek_fordulo).text())
                eredmeny_osszeg_2 = eredmeny_osszeg_2 + eredmeny_osszeg
            self.tablazat_2.setItem(jatekos_vegeredmeny_sor,1,QtWidgets.QTableWidgetItem(str(eredmeny_osszeg_2))) 
            self.tablazat_2.setItem(jatekos_vegeredmeny_sor,0,QtWidgets.QTableWidgetItem(jatekos))
            sorrendezo = QtWidgets.QTableWidgetItem()
            sorrendezo.setData(Qt.EditRole, QtCore.QVariant(eredmeny_osszeg_2))
            self.tablazat_2.setItem(jatekos_vegeredmeny_sor,1,sorrendezo)   
            self.tablazat_2.sortItems(1,order = Qt.DescendingOrder)
            jatekos_vegeredmeny_sor = jatekos_vegeredmeny_sor + 1
    
    def pontszammentes(self):
        today_file = datetime.date.today()
        current_time = str(datetime.datetime.now().time())
        current_time = current_time.replace(':','_')
        f = open('verseny_eredmenyek/'+'verseny_'+str(today_file)+'--'+str(current_time)+'.txt','w')
        ossz_jatekos_sor = self.tablazat.rowCount()
        for versenyzok in range(0,ossz_jatekos_sor):
            eredmeny_osszeg_2 = ""
            for pontszamok in range(0,6):
                if self.tablazat.item(versenyzok,pontszamok) is None:
                    eredmeny_osszeg = 0
                else:
                    eredmeny_osszeg = self.tablazat.item(versenyzok,pontszamok).text()
                    eredmeny_osszeg_2 = eredmeny_osszeg_2 +" "+ eredmeny_osszeg
            f.write(eredmeny_osszeg_2+"\n")
        f.close()
    def open_ot_kutya(self):
        webbrowser.open('https://otkutya.hu')
    def about(self):
        QMessageBox.about(self,'MirrorMatch 1.0.1.181207','A program azért készült,\nhogy gyorsítson egy-egy versenyen,\nvalamint a pontszámok menthetőek legyenek\n\nKód & Design:Bencsik Balázs\nE-Mail:bazsi@otkutya.hu\n\n\n 2018 © Otkutya.hu')
    
    def terminate(self):
        exit(0)

    def __init__(self):
        super(okf_sorsolo,self).__init__()
        uic.loadUi('main.ui',self)
        self.kiertekeles_button.clicked.connect(self.kiertekeles_process)
        self.sorsolas_button.clicked.connect(self.sorsolas)
        self.kilepes.triggered.connect(self.terminate)
        self.pontszamok_mentese.triggered.connect(self.pontszammentes)
        self.otkutyalink.triggered.connect(self.open_ot_kutya)
        self.actionTool.triggered.connect(self.about)
        
       

def main():
    #mentesi mappa létrehozása
    basedir = os.path.abspath(os.path.dirname(__file__))
    saved_folder = os.path.exists(basedir+'/verseny_eredmenyek')
    if saved_folder == False:
        os.mkdir(basedir+'/verseny_eredmenyek')

    app = QtWidgets.QApplication(sys.argv)
    window = okf_sorsolo()
    sshFile="gui_def.stylesheet"
    with open(sshFile,"r") as fh:
        window.setStyleSheet(fh.read())
    window.setWindowIcon(QtGui.QIcon(basedir+'/images/assets/logo.ico'))
    window.tablazat_2.setStyleSheet('QTableWidget{background: rgba(0,0,0,0.8);border: 0px solid cyan}')
    window.tablazat.setStyleSheet('QTableWidget{background: rgba(0,0,0,0.8);border: 0px solid cyan; text-align: center}')
    #window.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
#    qtmodern.windows.ModernWindow()
    window.show()

    sys.exit(app.exec_())

main()