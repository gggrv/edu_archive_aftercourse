# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script main.
"""

# embedded in python
import sys
# pip install
from PyQt5 import QtCore, QtGui, QtWidgets
# same folder
import EntryEditor

"""-------------------------------------------------------------------------+++
Everything about aid.
"""
def readf( path ):
    with open( path, 'r', encoding='utf-8' ) as f:
        return f.read()
    
def savef( path, text ):
    with open( path, 'w', encoding='utf-8' ) as f:
        f.write(text)
    
def appef( path, text ):
    with open( path, 'a', encoding='utf-8' ) as f:
        f.write(text)

"""-------------------------------------------------------------------------+++
Everything about actual code.
"""
class mainwindow( QtWidgets.QMainWindow ):
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( mainwindow, self ).__init__( parent, *args, **kwargs )
        
        # gui
        self._init()
        self._init_staticwidgets()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init_staticwidgets( self ):
        w = EntryEditor.centralwidget( self )
        self.setCentralWidget( w )
        
        w.loadfile( 'test.txt' )
        
    def _init( self ):
        self.setObjectName( 'mainwindow' )
        self.setWindowTitle( 'AAAAAAAAAA' )
        
"""-------------------------------------------------------------------------+++
autorun
"""
def autorun():
    app = QtWidgets.QApplication( sys.argv )
    w = mainwindow()
    w.show()
    
    sys.exit( app.exec_() )

if __name__ == '__main__':
    autorun()
    
#---------------------------------------------------------------------------+++
# конец 2021.03.06 → 2021.03.06
