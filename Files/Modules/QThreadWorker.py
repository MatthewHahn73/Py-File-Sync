from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class QThreadWorker(QObject):
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

