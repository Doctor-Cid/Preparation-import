# -*- coding: utf-8 -*-
import sys, configparser, time, random, subprocess, codecs, os  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import QCoreApplication
 

import P_IForm  # Это наш конвертированный файл дизайна

def clearFoldersfiles(Path, Path2):
    for file in os.listdir(Path):
        Fname=Path2+file
        try:
            os.remove(Fname)
        except OSError as e: ## if failed, report it back to the user ##
            print("Error: %s - %s." % (e.filename, e.strerror))
    return True

def clearFolders(Path, Path2):
    for file in os.listdir(Path):
        Fname=Path2+file
        try:
            os.rmdir(Fname)
        except OSError as e: ## if failed, report it back to the user ##
            if e.errno==41:
                print(Path)
                print(Path2)
                Path3=Path+'/'+file
                Path4=Path2+file+'\\'
                print(Path3)
                print(Path4)
                if clearFoldersfiles(Path3, Path4)==True:
                    clearFolders(Path, Path2)    
            else:
                print("Error: %s - %s" % (e.filename, e.strerror))
    return True      
                
                
    
    

class mainMenuWindow(QtWidgets.QMainWindow, P_IForm.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.saveFTPDirName.clicked.connect(self.createINI)
        self.ConvertToCSV.clicked.connect(self.convertXLSX)
        self.putFilestoFTP.clicked.connect(self.PutToFTP)
        self.clearDirectory.clicked.connect(self.clrFolders)
        self.OpenCatalog.clicked.connect(self.OpenFolders)

    def createINI(self):
        f=open("CryptoSet.ini", "w")
        config=configparser.ConfigParser()
        config.add_section("FolderName")
        config.set("FolderName", "Name", self.lineEdit.text())
        config.write(f)
        f.close()
        self.textBrowser.setText('Имя сохранено!!!')

    def loadINI(self):
        if not os.path.exists("CryptoSet.ini"):
            self.ConvertToCSV.setEnabled(False)
            self.textBrowser.setText('''Файл конфигураци не обнаружен!!!!!
Просьба ввести наименование вашей папки на ФТП и нажать кнопку сохранить.
Наименование не должно содержать пробелов или спец символов.
Наименование должно совпадать с наименованием папки на ФТП.
''')
        else:
            f=open(r"CryptoSet.ini", "r")
            config=configparser.ConfigParser()
            config.read_file(f)
            try:
                g=config.get('FolderName', "Name")
            except NoSectionError:
                self.ConvertToCSV.setEnabled(False)
                self.textBrowser.setText('Некорректный конфигурационный файл!!!')
            if g=='':
                self.ConvertToCSV.setEnabled(False)
                self.textBrowser.setText('Некорректное имя папки!!!!\nИмя папки не должно быть: Пустым, содержать пробелы, не совпадать с именем Вашей папки на FTP')
            else:
                self.lineEdit.setText(g)
                self.ConvertToCSV.setEnabled(True)
            f.close()
    
    def convertXLSX(self):
        if os.listdir("Modules/Preparation_Import/ToFTP/assort")==[]:
            Fname=None
        else:
            for file in os.listdir("Modules/Preparation_Import/ToFTP/assort"):
                if file.endswith(".xlsx"):
                    Fname=file
                else:
                    Fname=None
                
        if Fname==None:
            self.textBrowser.setText('Нет файлов на экспорт')
        else:
            Fname=os.path.join(os.getcwd()+'\\Modules\\Preparation_Import\\ToFTP\\assort\\'+Fname)
            print(Fname)
            result=subprocess.run([sys.executable,"Modules/Preparation_Import/ConvertToFormat.py", Fname], capture_output=True, text=True)
            self.textBrowser.setText(result.stdout)
            try:
                os.remove(Fname)
            except OSError as e: ## if failed, report it back to the user ##
                self.textBrowser.setText("Error: %s - %s." % (e.filename, e.strerror))
            self.ConvertToCSV.setEnabled(False)
            self.putFilestoFTP.setEnabled(True)

    def PutToFTP(self):
        result=subprocess.run([sys.executable,"Modules/Preparation_Import/PutFilestoFTP.py", self.lineEdit.text()], capture_output=True, text=True)
        self.textBrowser.setText(result.stdout)
        print('wut!?')

    def clrFolders(self):
        assort=r"Modules/Preparation_Import/ToFTP/assort"
        assort1="Modules\\Preparation_Import\\ToFTP\\assort\\"
        images=r"Modules/Preparation_Import/ToFTP/images"
        images1=r"Modules\\Preparation_Import\\ToFTP\\images\\"
        if clearFoldersfiles(assort, assort1)==True:
            if clearFolders(images, images1)==True:
                self.textBrowser.setText('Папки Assort и Images полностью очищены!!!!')
        else:
            self.textBrowser.setText('Что то пошло не так!!!! Ошибка 1')
        
    def OpenFolders(self):
        self.textBrowser.setText('Открываю Папки Assort и Images!!!!')
        path=os.path.join(os.getcwd()+'\\Modules\\Preparation_Import\\ToFTP\\assort\\')
        path2=os.path.join(os.getcwd()+'\\Modules\\Preparation_Import\\ToFTP\\images\\')
        subprocess.run(['explorer', path])
        subprocess.run(['explorer', path2])

    def loadCleverWords(self):
        Phrase=random.randint(0,20)
        if Phrase==0:
            self.textBrowser.setText('Единственный случай, когда у вас слишком много топлива - это когда вы горите.\n-Неизвестный-')
        elif Phrase==1:
            self.textBrowser.setText('Истина в том, что нет ничего истинного. И если это утверждение истинно, то оно ложно.\n-Древний парадокс-')
        elif Phrase==2:
            self.textBrowser.setText('Не идите туда, где проложена тропинка. Идите туда, где её нет, и проложите свою.\n-Неизвестный-')
        elif Phrase==3:
            self.textBrowser.setText('Простота - это предел совершенства.\n-Леонардо да Винчи-')
        elif Phrase==4:
            self.textBrowser.setText('Мы видим то, что мы знаем.\n-Иоганн Гете-')
        elif Phrase==5:
            self.textBrowser.setText('Пилот, у которого нет страха, вероятно, не летал на пределе своего самолета\n-Джон Макбрайд-')
        elif Phrase==6:
            self.textBrowser.setText('Творчество - развлечение интеллекта.\n-Альберт Эйнштейн-')
        elif Phrase==7:
            self.textBrowser.setText('А мог бы остаться летать в космосе навсегда...\n-Юрий Гагарин-')
        elif Phrase==8:
            self.textBrowser.setText('Дайте мне рычаг достаточно большой и точку опоры на которую можно его поместить и я переверну мир.\n-Архимед-')
        elif Phrase==9:
            self.textBrowser.setText('Если вы хотите знать как вещи работают на самом деле, изучите их когда они разобраны.\n-Уильям Гибсон-')
        elif Phrase==10:
            self.textBrowser.setText('Для оптимиста, стакан наполовину полон. Для пессимиста, стакан наполовину пуст. Для инженера, стакан в два\nраза больше, чем он должен быть.\n-Неизвестный-')
        elif Phrase==11:
            self.textBrowser.setText('Это один маленький шаг для человека, но гигантский скачок для всего человечества.\n-Нил Армстронг-')
        elif Phrase==12:
            self.textBrowser.setText('Природа никогда не нарушает ее собственные законы.\n-Леонардо да Винчи-')
        elif Phrase==13:
            self.textBrowser.setText('Отрицая научные принципы, можно поддержать любой парадокс.\n-Галилео Галилей-')
        elif Phrase==14:
            self.textBrowser.setText('Наука - это упорядоченные знания. Мудрость - это упорядоченная жизнь.\n-Галилео Галилей-')
        elif Phrase==15:
            self.textBrowser.setText('Никогда не меняй удачу на умение.\n-Неизвестный-')
        elif Phrase==16:
            self.textBrowser.setText('Когда выдающийся, но пожилой учёный настаивает, что что-то возможно - он почти наверняка прав.\nКогда он настаивает что что-то невозможно - вероятнее всего он не прав.\n-Артур С. Кларк-')
        elif Phrase==17:
            self.textBrowser.setText('Авиация - отрасль инженерии, которая реже всего прощает ошибки.\n-Фриман Дайсон-')
        elif Phrase==18:
            self.textBrowser.setText('Мы покорили открытый космос, но не свой внутренний мир.\n-Джордж Карлин-')
        elif Phrase==19:
            self.textBrowser.setText('Ну выйдет человечество в космос — и что? На что ему космос, когда не дано вечности?\n-Сальвадор Дали-')
        elif Phrase==20:
            self.textBrowser.setText('Даже если вера в ложь помогает творить добро, в конечном счёте, это ведет к истине - что мы одинокая раса во тьме, \nстрашащаяся смеющихся игр разумных злобных сущностей, которых смертные нарекли бы богами\n-Император Человечества-')
       
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = mainMenuWindow()  # Создаём объект класса ExampleApp
    mainMenuWindow.loadCleverWords(window)
    mainMenuWindow.loadINI(window)
    
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
    
