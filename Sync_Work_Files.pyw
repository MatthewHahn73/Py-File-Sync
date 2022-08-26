import os
import logging
import datetime
import json
import qdarkgraystyle
from dirsync import sync
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#Fonts
Custom_Font = QFont("Arial Black", 9)
Custom_Font_Small = QFont("Arial Black", 8)

#Logging info
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class QTextEditLogger(logging.Handler, QObject):
    sigLog = pyqtSignal(str)
    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, logRecord):
        Datetime = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().strftime("%H:%M:%S"))
        Msg = str(logRecord.getMessage())
        if Msg != '':
            self.sigLog.emit(Datetime + ' - ' + Msg)
            
class Worker(QObject):
    Complete = pyqtSignal()

    def __init__(self, SO, OD, DD, LS, L):
        super().__init__()
        self.Sync_Object = SO
        self.Origin_Dir_ = OD
        self.Dest_Dir_ = DD
        self.Log_Setting = LS
        self.Log = L

    def Difference(self):
        self.Sync_Object.Report_Difference(self.Origin_Dir_, self.Dest_Dir_, self.Log_Setting) 
        self.Complete.emit()

    def Sync(self):
        self.Sync_Object.Sync_Files(self.Origin_Dir_, self.Dest_Dir_, self.Log_Setting)        
        self.Complete.emit()


class Sync_GUI(QMainWindow):
    Sync_Object = None
    Save_Setting = False
    Log_Setting = False

    def __init__(self):
        super().__init__()
        self.initUI()
        self.Sync_Object = Sync()

    def initUI(self, parent=None):
        super().__init__(parent)
        
        #Menu
        Menu_Bar = self.menuBar()
        Menu_Bar.setFont(Custom_Font_Small)
        Menu_Bar.setStyleSheet(
            'QMenuBar {'
                'border-bottom: 1px solid gray'
            '}'
        )

        #File Tab
        File_Tab = Menu_Bar.addMenu('File')
        Close_App = QAction('Close', self)
        Close_App.setFont(Custom_Font_Small)
        Clear_Logs = QAction('Clear Terminal Logs', self)
        Clear_Logs.setFont(Custom_Font_Small)
        Clear_Log_File = QAction('Clear Log File', self)
        Clear_Log_File.setFont(Custom_Font_Small)
        File_Tab.addAction(Clear_Logs)
        File_Tab.addAction(Clear_Log_File)
        File_Tab.addAction(Close_App)

        #Options Tab
        self.Options_Tab = Menu_Bar.addMenu('Options')
        self.Save_Directories = QAction('Save Directories', self)
        self.Save_Directories.setFont(Custom_Font_Small)
        self.Save_Directories.setCheckable(True)
        self.Save_Directories.triggered.connect(lambda: self.Toggle_Directories(self.Save_Directories.isChecked()))
        self.Display_Operations = QAction('Display All Logs', self)
        self.Display_Operations.setFont(Custom_Font_Small)
        self.Display_Operations.setCheckable(True)
        self.Display_Operations.triggered.connect(lambda: self.Toggle_Logs(self.Display_Operations.isChecked()))
        self.Options_Tab.addAction(self.Save_Directories)
        self.Options_Tab.addAction(self.Display_Operations)

        #App Body
        self.Layout = QGridLayout()

        #Set Top Grid
        self.Origin_Label = QLabel('Origin')
        self.Origin_Label.setFont(Custom_Font)
        self.Origin_Field = QLineEdit()
        self.Origin_Field.setText("")
        self.Origin_Field.setFont(Custom_Font)
        self.Origin_Field.setReadOnly(True)
        self.Origin_Field.setMinimumWidth(420)
        self.Origin_Field.setFixedHeight(28)
        self.Origin_Button = QPushButton('Browse', self)
        self.Origin_Button.setFixedWidth(90) 
        self.Origin_Button.setFixedHeight(27) 
        self.Origin_Button.setFont(Custom_Font)
        self.Origin_Button.clicked.connect(self.Open_File_Dialog_Origin)

        self.Dest_Label = QLabel('Target')
        self.Dest_Label.setFont(Custom_Font)
        self.Dest_Field = QLineEdit()
        self.Dest_Field.setText("")
        self.Dest_Field.setFont(Custom_Font)
        self.Dest_Field.setReadOnly(True)
        self.Dest_Field.setMinimumWidth(420)
        self.Dest_Field.setFixedHeight(28)
        self.Dest_Button = QPushButton('Browse', self)
        self.Dest_Button.setFixedWidth(90) 
        self.Dest_Button.setFixedHeight(27) 
        self.Dest_Button.setFont(Custom_Font)
        self.Dest_Button.clicked.connect(self.Open_File_Dialog_Target)
        
        #Set Bottom Grid
        self.LogEdit = QTextEdit()
        self.LogEdit.setFont(Custom_Font)
        self.LogEdit.setReadOnly(True)
        self.LogEdit.setStyleSheet(
            "QTextEdit { \
                padding-left: 5px; \
                    padding-top: 1px; \
            }"
        )
        Handler = QTextEditLogger()
        Handler.sigLog.connect(self.LogEdit.append)
        logger.addHandler(Handler)    
        self.ScrollArea = QScrollArea(self)
        self.ScrollArea.setWidget(self.LogEdit)
        self.ScrollArea.setWidgetResizable(True)

        self.Bottom_Layout = QHBoxLayout()
        self.Bottom_Layout.addStretch(2)
        self.Sync_Button = QPushButton('Sync', self)
        self.Sync_Button.setFixedWidth(90) 
        self.Sync_Button.setFixedHeight(27) 
        self.Sync_Button.setFont(Custom_Font)
        self.Sync_Button.clicked.connect(lambda: self.Validate_And_Run('Sync'))
        self.Report_Button = QPushButton('Preview', self)
        self.Report_Button.setFixedWidth(90) 
        self.Report_Button.setFixedHeight(27) 
        self.Report_Button.setFont(Custom_Font)
        self.Report_Button.clicked.connect(lambda: self.Validate_And_Run('Report'))
        self.Animation_Label = QLabel()
        self.Animation_Label.setText("Working...")
        self.Animation_Label.setFont(Custom_Font)
        self.Animation_Label.setFixedWidth(80) 
        self.Animation_Label.setFixedHeight(27) 
        self.Animation_Label.hide()
        self.Bottom_Layout.addWidget(self.Animation_Label, alignment=Qt.AlignRight)
        self.Bottom_Layout.addWidget(self.Report_Button, alignment=Qt.AlignRight)
        self.Bottom_Layout.addWidget(self.Sync_Button, alignment=Qt.AlignRight)
        
        self.Layout.addWidget(self.Origin_Label, 1, 1)
        self.Layout.addWidget(self.Origin_Field, 1, 2)
        self.Layout.addWidget(self.Origin_Button, 1, 3)
        self.Layout.addWidget(self.Dest_Label, 2, 1)
        self.Layout.addWidget(self.Dest_Field, 2, 2)
        self.Layout.addWidget(self.Dest_Button, 2, 3)
        self.Layout.addWidget(self.ScrollArea, 3, 1, 1, 3)
        self.Layout.addLayout(self.Bottom_Layout, 4, 1, 1, 3)

        widget = QWidget()
        widget.setLayout(self.Layout)
        self.setCentralWidget(widget)

        Close_App.triggered.connect(self.close)
        Clear_Logs.triggered.connect(self.LogEdit.clear)
        Clear_Log_File.triggered.connect(self.Clear_Log_File)
        
        #Icon Settings
        Icon_Name = "Icon.ico"
        Icon_Path = (os.path.dirname(os.path.realpath(__file__)) + "/Files/" + Icon_Name).replace("\\", "/")
        if not os.path.exists(Icon_Path): 
            logging.warning(Icon_Name + " couldn't be located")
            
        #Window Settings
        self.setWindowIcon(QIcon(Icon_Path))
        self.setWindowTitle('Sync v1.25b')
        self.setMinimumSize(600,325)
        self.show()
        self.Load_Settings()
        self.setFocus()

    def Open_File_Dialog_Origin(self):
        dir_ = QFileDialog.getExistingDirectory(None, 'Origin Directory', 'C:\\', QFileDialog.ShowDirsOnly)
        if dir_:
            self.Origin_Field.setText(dir_)
            self.Origin_Field.setStyleSheet('color: white;')
            
    def Open_File_Dialog_Target(self):
        dir_ = QFileDialog.getExistingDirectory(None, 'Target Directory', 'C:\\', QFileDialog.ShowDirsOnly)
        if dir_:
            self.Dest_Field.setText(dir_)
            self.Dest_Field.setStyleSheet('color: white;')

    def Create_Required_Files(self, File_Name):
        try: 
            Path = os.path.dirname(os.path.realpath(__file__)) + "\\Files"
            Full_Path = os.path.dirname(os.path.realpath(__file__)) + "\\Files\\" + File_Name
            if not os.path.exists(Path):      #If files folder doesn't exist, create one
                os.makedirs(Path)
            if not os.path.exists(Full_Path): #If file doesn't exist, create one
                with open(Full_Path, "w") as File:
                    pass
        except IOError as e:
            logging.error(e)

    def Load_Settings(self):
        try:
            self.Create_Required_Files("Settings.json")
            with open(os.path.dirname(os.path.realpath(__file__)) + "\\Files\\Settings.json", "r") as File:
                Settings = json.load(File)
                Save_Setting = Settings["SS"]
                Log_Setting = Settings["LS"]

                if(Save_Setting != "False"):
                    File_Split = Save_Setting.split(' - ')
                    self.Save_Directories.setChecked(True)
                    self.Save_Setting = True
                    self.Origin_Field.setText(File_Split[0])
                    if(os.path.exists(File_Split[0])):
                        self.Origin_Field.setStyleSheet('color: white;')
                    else:
                        self.Origin_Field.setStyleSheet('color: indianred;')
                    if(len(File_Split) >= 2):
                        self.Dest_Field.setText(File_Split[1])
                        if(os.path.exists(File_Split[1])):
                            self.Dest_Field.setStyleSheet('color: white;')
                        else:
                            self.Dest_Field.setStyleSheet('color: indianred;')
                if(Log_Setting != "False"):
                    self.Display_Operations.setChecked(True)
                    self.Log_Setting = True
        except IOError as e:
            logging.error(e)
        except:
            pass

    def Save_Settings(self):
        try:
            Save_Bool, Log_Bool = "False", "False"
            with open(os.path.dirname(os.path.realpath(__file__)) + "\\Files\\Settings.json", "w") as File:
                if self.Save_Directories.isChecked() \
                    and self.Origin_Field.text() != '' \
                    and self.Dest_Field.text() != '': 
                        OT = self.Origin_Field.text() if self.Origin_Field.text() != '' else ''
                        DT = self.Dest_Field.text() if self.Dest_Field.text() != '' else ''
                        Save_Bool = OT + ' - ' + DT
                if self.Display_Operations.isChecked(): 
                    Log_Bool = "True"
                Config = {
                    "SS" : Save_Bool,
                    "LS" : Log_Bool,
                }       
                File.write(json.dumps(Config))
        except IOError as e:
            logging.error(e)

    def Write_To_Log_File(self, Operation):
        try:
            self.Create_Required_Files("Logs.log")
            with open(os.path.dirname(os.path.realpath(__file__)) + "\\Files\\Logs.log", "a") as File:
                Datetime = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().strftime("%H:%M:%S"))
                File.write("----------------------------------------------------------------------------------\n")
                File.write("Date: " + Datetime + "\n")
                File.write("Origin Dir: " + self.Origin_Field.text() + "\n")
                File.write("Target Dir: " + self.Dest_Field.text() + "\n")
                File.write("Operation: " + Operation + "\n\n")
                File.write(self.LogEdit.toPlainText() + "\n\n")
                File.write("----------------------------------------------------------------------------------\n")
                File.write('\n\n')
        except IOError as e:
            logging.error(e)

    def Clear_Log_File(self):
        Log_Path = os.path.dirname(os.path.realpath(__file__)) + "\\Files\\Logs.log"
        try: 
            if not os.path.exists(Log_Path): 
                return
            with open(Log_Path, "w") as File:
                pass
            logging.info("Log File Cleared")
        except IOError as e:
            logging.error(e)

    def Validate_And_Run(self, Operation):
        if os.path.isdir(self.Dest_Field.text()) and os.path.isdir(self.Origin_Field.text()):
            Origin_Dir_ = self.Origin_Field.text()
            Dest_Dir_ = self.Dest_Field.text()
            self.LogEdit.clear()
            if Operation == "Sync":
                try:
                    if self.Sync_Object.Require_Syncing(Origin_Dir_, Dest_Dir_):
                        self.Toggle_Buttons(False)

                        #Start Thread to Sync
                        self.Sync_Thread = QThread()
                        self.Worker = Worker(self.Sync_Object, Origin_Dir_, Dest_Dir_, self.Log_Setting, self.LogEdit)
                        self.Worker.moveToThread(self.Sync_Thread)
                        self.Sync_Thread.started.connect(self.Worker.Sync)
                        self.Worker.Complete.connect(self.Sync_Thread.quit)
                        self.Sync_Thread.start()
                        self.Sync_Thread.finished.connect(lambda: self.Toggle_Complete('Sync Complete'))      
                    else:
                        logging.error('Syncing Not Required')
                except Exception as e:
                    logging.debug(e)
            elif Operation == "Report":
                try:
                    if self.Sync_Object.Require_Syncing(Origin_Dir_, Dest_Dir_):
                        self.Toggle_Buttons(False)

                        #Start Thread to Report
                        self.Sync_Thread = QThread()
                        self.Worker = Worker(self.Sync_Object, Origin_Dir_, Dest_Dir_, self.Log_Setting, self.LogEdit)
                        self.Worker.moveToThread(self.Sync_Thread)
                        self.Sync_Thread.started.connect(self.Worker.Difference)
                        self.Worker.Complete.connect(self.Sync_Thread.quit)
                        self.Sync_Thread.start()
                        self.Sync_Thread.finished.connect(lambda: self.Toggle_Complete('Preview Complete'))  
                    else:
                        logging.error('Syncing Not Required')
                except Exception as e:
                    logging.debug(e)
        else:
            if not os.path.isdir(self.Origin_Field.text()):
                logging.warning('Invalid Origin Directory')
            if not os.path.isdir(self.Dest_Field.text()):
                logging.warning('Invalid Target Directory')

    def Toggle_Buttons(self, Toggle):
        if Toggle:
            self.Sync_Button.show()
            self.Report_Button.show()
            self.Origin_Button.setEnabled(True)
            self.Dest_Button.setEnabled(True)
            self.Animation_Label.hide()
        else:
            self.Sync_Button.hide()
            self.Report_Button.hide()
            self.Origin_Button.setEnabled(False)
            self.Dest_Button.setEnabled(False)
            self.Animation_Label.show()
        self.setFocus()

    def Toggle_Complete(self, Msg):
        logging.info(Msg)
        self.Toggle_Buttons(True)
        self.Write_To_Log_File(Msg.split(" ")[0])

    def Toggle_Logs(self, Toggle):
        self.Log_Setting = Toggle 

    def Toggle_Directories(self, Toggle):
        self.Save_Setting = Toggle

    def closeEvent(self, event):
        self.Save_Settings()
        self.close()

class Sync():
    def __init__(self):
       pass
               
    def Require_Syncing(self, Host, Dest):
        return True
        
    def Sync_Files(self, Host, Dest, VB): 
        sync(Host, Dest, action='sync', verbose=VB, logger=logger, exclude=(r'^(?:.*[\\/])?[_.][^_].*$',)) #Excludes files and folders that start with . or _

    def Report_Difference(self, Host, Dest, VB):
        sync(Host, Dest, action='diff', verbose=VB, logger=logger, exclude=(r'^(?:.*[\\/])?[_.][^_].*$',)) #Excludes files and folders that start with . or _

if __name__ == '__main__':
    app = QApplication(os.sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    ex = Sync_GUI()
    os.sys.exit(app.exec_())