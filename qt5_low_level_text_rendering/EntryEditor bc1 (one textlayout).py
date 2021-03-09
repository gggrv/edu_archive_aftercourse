# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script EntryEditor bc1 (one textlayout).

Obsolete version, it will not work with main.pyw.
The difference with the modern EntryEditor.py:
here I use only one QTextLayout. I forced it display and handle \n.
"""

# embedded in python
# pip install
from PyQt5 import QtCore, QtGui, QtWidgets
# same folder

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
Everything about supplimentary code.
"""
class textlayout( QtGui.QTextLayout ):
    """Custom QtGui.QTextLayout. Just in case."""
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( textlayout, self ).__init__( parent, *args, **kwargs )
        
    """---------------------------------------------------------------------+++
    Everything about subclassing.
    """
    """
    def createLine( self ):
        pass
    """

"""-------------------------------------------------------------------------+++
Everything about actual code.
"""
class centralwidget( QtWidgets.QWidget ):
    
    # the data i'm working with
    CURRENT_FILE_PATH = ''
    CURRENT_FILE_DATA = ''
    
    #
    CARET_PREV = [0,0,0] # x,y,char -- prev pos of the caret
    CARET_LAST = [0,0,0] # x,y,char -- curr pos of the caret
    CARET_SLCT = False # i assume i'm not selecting anything with caret yet
    MOUSE_PREV = [0,0] # x,y - previous position of the mouse
    MOUSE_LAST = [0,0] # x,y - last position of the mouse
    MOUSE_SLCT = False # i assume i'm not selecting anything with mouse yet
    
    # text layout stuff
    _CARET_WIDTH = 1 # caret width in pixels
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( centralwidget, self ).__init__( parent, *args, **kwargs )
        
        # gui
        self._init()
        self._init_staticwidgets()
        self._init_actions()
        
    """---------------------------------------------------------------------+++
    Everything about actions.
    """
    def _action_save( self ):
        self.ENTRY_DATA = self.toPlainText()
        savef( self.CURRENT_FILE, self.ENTRY_DATA )
        
    """---------------------------------------------------------------------+++
    Everything about text layout.
    """
    def _textlayout_restruct( self, lyt ):
        """Recalculates the way the text should be rendered."""
        """-----------------------------------------------------------------+++
        Definitions.
        """
        
        painter = QtGui.QPainter()
        
        # metrics
        #fm = painter.fontMetrics()
        
        # sizes
        widgetwidth_pixels = self.width()
        
        # positions
        margins = [ 0,0,0,0 ]
        
        # very important placeholder for lineinfo
        self._FAKELINEINFO = [] # coords of existing and imaginary QTextLines, [top,height,iloc in textlayout]
        
        # other
        br = '\n'
        textlength = len( self.CURRENT_FILE_DATA )
        
        def placeline( line, skip ):
            # set line coordinates
            
            # remember line info
            lineiloc = [self.TEXTLYT.lineCount()-1,-1][skip]
            self._FAKELINEINFO.append(
                [
                    margins[1], # top
                    line.height(),
                    lineiloc # iloc in textlayout
                    ]
                )
            
            # skip adding the actual line
            # because pyqt5 dies when QTextLine with zero contents appears
            if not skip:
                line.setPosition( QtCore.QPointF(margins[0],margins[1]) )
                
            margins[1] += self._FAKELINEINFO[-1][1] # line.height()
            
        def brcount( text ):
            brcount = 0
            for letter in text:
                if not letter=='\n': break
                brcount+=1
            return brcount
        
        """-----------------------------------------------------------------+++
        Actual code.
        """
        
        lyt.beginLayout()
        
        while True:
            # create the line
            line = lyt.createLine()
            if not line.isValid(): break
            
            # what will be displayed on this line?
            line.setLineWidth( widgetwidth_pixels )
            
            sta = line.textStart()
            end = sta + line.textLength()
            if end>=textlength:
                placeline( line, False )
                break
            text = self.CURRENT_FILE_DATA[ sta:end ]
            
            # where is br and how many of them are there?
            # https://stackoverflow.com/questions/40076670/qtextlayout-manual-line-breaking
            if br in text:
                chars_tillbr = text.find(br) # where is it
                brs = brcount( text[chars_tillbr:] ) # how many consequently
                
                # cut the line here
                line.setLineWidth( chars_tillbr )
                line.setNumColumns( chars_tillbr )
                
                # set line coordinates
                placeline( line, False )
                
                # add empty lines
                for _ in range(brs//2):
                    placeline( line, True )
                
                continue
            
            # there was no br
            placeline( line, False )
            
        lyt.endLayout()
        
    def _textcaret_undercoords( self, x, y ):
        """Translates mouse coordinates to the text char position."""
        """-----------------------------------------------------------------+++
        Definitions.
        """
        # placeholder values that i will change and return
        neat_char = 0
        neat_x = 0
        neat_y = 0
        
        def getlineinfo():
            # Gets info of the line i've just clicked on
            for lineinfo in self._FAKELINEINFO:
                top, height, iloc = lineinfo
                # get line's vertical boundaries
                U, D = top, top+height
                # the ly is on the line
                if y>=U and y<=D: return lineinfo
            raise NotImplementedError
        
        def valid( char ):
            # Checks whether this char position is valid.
            # Fixes invalid ones.
            if self.TEXTLYT.isValidCursorPosition(char): return char
            # this char is invalid, have to
            # fix unicode byte forbidden positioning
            # compare with previous char
            if char<self.CARET_PREV[2]: # i want to go left
                return self.TEXTLYT.previousCursorPosition(char)
            # i want to go right
            return self.TEXTLYT.nextCursorPosition(char)
        
        """-----------------------------------------------------------------+++
        Actual code.
        """
        # i assume, i clicked on a line
        # get that line
        lineinfo = getlineinfo()
        
        # that line exists
        if lineinfo[2]>=0:
            line = self.TEXTLYT.lineAt( lineinfo[2] )
            # i want to place the caret at the corr. line char
            
            # get valid char relative to the whole text in self.TEXTLYT
            text_char = valid( line.xToCursor(x) )
            # place the caret at the visual nonexistant line beginning
            # it is inherited from the previous line
            neat_char = text_char-line.textStart()
            neat_x, neat_y = line.cursorToX( neat_char )
            neat_x, neat_y = 0, lineinfo[0]
            
            print( x,y,'→',neat_x,neat_y,neat_char,self.TEXTLYT.text()[line.textStart():text_char])
            
        # that line does not exist yet (it's empty)
        else:
            # place the caret at the visual nonexistant line beginning
            # it is inherited from the previous line
            neat_char = 0
            neat_x = 0
            neat_y = lineinfo[0]
        
        return neat_x, neat_y, neat_char
        
    def _textcaret_undercoords( self, x, y ):
        """Translates mouse coordinates to the text char position."""
        """-----------------------------------------------------------------+++
        Definitions.
        """
        # placeholder values that i will change and return
        neat_char = 0
        neat_x = 0
        neat_y = 0
        
        def getlineinfo():
            # Gets info of the line i've just clicked on
            for lineinfo in self._FAKELINEINFO:
                top, height, iloc = lineinfo
                # get line's vertical boundaries
                U, D = top, top+height
                # the ly is on the line
                if y>=U and y<=D: return lineinfo
            raise NotImplementedError
        
        def valid( char ):
            # Checks whether this char position is valid.
            # Fixes invalid ones.
            if self.TEXTLYT.isValidCursorPosition(char): return char
            # this char is invalid, have to
            # fix unicode byte forbidden positioning
            # compare with previous char
            if char<self.CARET_PREV[2]: # i want to go left
                return self.TEXTLYT.previousCursorPosition(char)
            # i want to go right
            return self.TEXTLYT.nextCursorPosition(char)
        
        """-----------------------------------------------------------------+++
        Actual code.
        """
        # i assume, i clicked on a line
        # get that line
        lineinfo = getlineinfo()
        
        # that line exists
        if lineinfo[2]>=0:
            line = self.TEXTLYT.lineAt( lineinfo[2] )
            # i want to place the caret at the corr. line char
            
            # get valid char relative to the whole text in self.TEXTLYT
            text_char = valid( line.xToCursor(x) )
            # place the caret at the visual nonexistant line beginning
            # it is inherited from the previous line
            neat_char = text_char-line.textStart()
            neat_x, neat_y = line.cursorToX( neat_char )
            neat_x, neat_y = 0, lineinfo[0]
            
            print( lineinfo[2],neat_char,self.TEXTLYT.text()[line.textStart():text_char])
            
        # that line does not exist yet (it's empty)
        else:
            # place the caret at the visual nonexistant line beginning
            # it is inherited from the previous line
            neat_char = 0
            neat_x = 0
            neat_y = lineinfo[0]
        
        return neat_x, neat_y, neat_char
        
    def loadfile( self, path ):
        """
        Loads current file and initializes text layout.
        No repainting.
        """
        self.CURRENT_FILE_PATH = path
        text = readf( self.CURRENT_FILE_PATH )
        self.CURRENT_FILE_DATA = text
        
        self.TEXTLYT.setText( self.CURRENT_FILE_DATA )
        self.TEXTLYT.setCacheEnabled( True )
        self._textlayout_restruct( self.TEXTLYT )
        
    """---------------------------------------------------------------------+++
    Everything about events.
    """
    def mousePressEvent( self, ev ):
        # what i do with the mouse coords:
        self.MOUSE_PREV = self.MOUSE_LAST # overwrite previous press coords
        self.MOUSE_LAST = [ ev.x(), ev.y() ] # remember current press coords
        self.MOUSE_SLCT = True # i assume i want to select some text
        
        # what i do with the caret coords:
        lx,ly,lchar = self._textcaret_undercoords(ev.x(),ev.y()) # get them
        self.CARET_PREV = [lx,ly,lchar] # overwrite prev coords
        self.CARET_LAST = [lx,ly,lchar] # remember current coords
        self.CARET_SLCT = self.MOUSE_SLCT # i assume i want to select some text
            
        # repaint the widget
        self.update()
        
    def mouseReleaseEvent( self, ev ):
        # what i do with the mouse coords:
        self.MOUSE_LAST = [ ev.x(), ev.y() ] # remember current rel. coords
        self.MOUSE_SLCT = False # i assume i want to stop selecting text
        
        # what i do with the caret coords:
        self.CARET_SLCT = self.MOUSE_SLCT # i assume i want to stop selecting
        
        # if did not move the mouse anywhere, the caret is at
        # correct position, so there is no need to recalc/repaint anything
        if self.MOUSE_LAST==self.MOUSE_PREV: return None
        # i did move the mouse
        # get current coords
        lx,ly,lchar = self._textcaret_undercoords(ev.x(),ev.y())
        self.CARET_LAST = [lx,ly,lchar] # remember current coords
            
        # repaint the widget
        self.update()
        
    def mouseMoveEvent( self, ev ):
        # i assume i want to select some text
        if self.MOUSE_SLCT and self.CARET_SLCT:
            # remember current coordinates
            self.MOUSE_LAST = [ ev.x(), ev.y() ]
            
            # what i do with the caret coords:
            # if did not move the mouse anywhere, the caret is at
            # correct position, so there is no need to recalc/repaint anything
            if self.MOUSE_LAST==self.MOUSE_PREV: return None
            # i did move the mouse
            # get current coords
            lx,ly,lchar = self._textcaret_undercoords(ev.x(),ev.y())
            self.CARET_LAST = [lx,ly,lchar] # remember current coords
                
            # repaint the widget
            self.update()
            
    def keyPressEvent( self, ev ):
        print( 'pr',ev.key(), chr(ev.key()) )
            
    def keyReleaseEvent( self, ev ):
        print( 're',ev.key() )
        
    def resizeEvent( self, ev ):
        
        # recalculate text layouts
        self._textlayout_restruct( self.TEXTLYT )
        
        ev.accept()
        
    def paintEvent( self, ev ):
        """
        https://doc.qt.io/qt-5/qtextlayout.html#details
        https://doc.qt.io/qtforpython-5/PySide2/QtGui/QTextLayout.html
        https://doc.qt.io/archives/qq/qq24-textlayouts.html
        https://www.learnpyqt.com/tutorials/bitmap-graphics/
        https://www.programcreek.com/python/example/82366/PyQt5.QtGui.QPainter
        https://doc.qt.io/qtforpython/overviews/qtwidgets-widgets-elidedlabel-example.html
        """
        """-----------------------------------------------------------------+++
        Definitions.
        """
        
        painter = QtGui.QPainter()
        
        """-----------------------------------------------------------------+++
        Actual code.
        """
        # repaint self
        QtWidgets.QWidget.paintEvent( self, ev )
        
        painter.begin( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing )
        
        # repaint text layout
        self.TEXTLYT.draw( painter, QtCore.QPointF(0,0) )
            
        """
        # repaint text caret
        lx,ly,lchar = self.CARET_LAST
        if self.CARET_SLCT: # the cursor is selecting something
            px = self.CARET_PREV[0]
            print( abs(lx-px) )
            self.TEXTLYT.drawCursor( painter, QtCore.QPointF(lx,ly),
                lchar, abs(lx-px) )
        else:
            self.TEXTLYT.drawCursor( painter, QtCore.QPointF(lx,ly), lchar )
        """
        
        painter.end() 
        
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init( self ):
        self.setObjectName( 'centralwidget' )
        
        # i want to access mouse and keyboard input
        self.setMouseTracking( True )
        self.setFocusPolicy( QtCore.Qt.StrongFocus )
        
    def _init_staticwidgets( self ):
        # font
        self.DEFONT = QtGui.QFont( 'consolas', 10 )
        
        # text layout
        self.TEXTLYT = textlayout()
        self.TEXTLYT.setFont( self.DEFONT )
        
        # it's text option
        to = QtGui.QTextOption()
        to.setFlags(
            QtGui.QTextOption.IncludeTrailingSpaces
            |QtGui.QTextOption.ShowTabsAndSpaces
            |QtGui.QTextOption.ShowLineAndParagraphSeparators
            |QtGui.QTextOption.ShowDocumentTerminator
            |QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere
            )
        self.TEXTLYT.setTextOption( to )
        
    def _init_actions( self ):
        # save current file
        save = QtWidgets.QAction( 'Save', self )
        save.setShortcut( 'Ctrl+S' )
        save.triggered.connect( self._action_save )
        
        self.addAction( save )
    
#---------------------------------------------------------------------------+++
# конец 2021.03.07 → 2021.03.09
