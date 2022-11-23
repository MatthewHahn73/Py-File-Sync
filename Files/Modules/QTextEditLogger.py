import datetime
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

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
