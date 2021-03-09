# -*- coding: utf-8 -*-

"""-------------------------------------------------------------------------+++
Script EntryEditor.
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
Everything about actual code.
"""
class editfield( QtWidgets.QLineEdit ):
    """
    Default QLineEdit does not support number of characters.
    This QLineEdit can handle them.
    """
    
    """
    # chars that i want to add to the text
    # but which QLineEdit does not support by default
    MANUALLY_ADD = {
        QtCore.Qt.Key_Enter         : '\n',
        QtCore.Qt.Key_Tab           : '\t',
        }
    """
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( editfield, self ).__init__( parent, *args, **kwargs )
        
        self.returnPressed.connect( self.insertn )
        
    """---------------------------------------------------------------------+++
    Everything about communication with displayfield.
    """
    def set_displayfield( self, displayfield ):
        self.D = displayfield
        
    def insert( self, text ):
        # Manually insert text at current cursor position.
        t = self.text()
        iloc = self.cursorPosition()
        newtext = t[:iloc]+text+t[iloc:]
        self.setText(newtext)
        self.setCursorPosition( iloc+1 )
        
    def insertn( self ):
        self.insert('\n')
        
    """---------------------------------------------------------------------+++
    Everything about events.
    """
    """
    def keyPressEventExtended( self, ev ):
        key = ev.key()+1
        if key in self.MANUALLY_ADD: self.insert( self.MANUALLY_ADD[key] )
        ev.accept()
    """
    
class displayfield( QtWidgets.QWidget ):
    
    # text
    PARAS = [] # each paragraph
    LYTS = [] # QTextLayout for each paragraph
    SHAPES = [] # curves, along which i want to draw paragraphs
    
    # coordinates
    CARET_PREV = [0,0,0,0] # x,y,char,textchar -- prev pos of the caret
    CARET_LAST = [0,0,0,0] # x,y,char,textchar -- curr pos of the caret
    CARET_SLCT = False # i assume i'm not selecting anything with caret yet
    MOUSE_PREV = [0,0] # x,y - previous position of the mouse
    MOUSE_LAST = [0,0] # x,y - last position of the mouse
    MOUSE_SLCT = False # i assume i'm not selecting anything with mouse yet
    
    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( displayfield, self ).__init__( parent, *args, **kwargs )
        
        # gui
        self._init()
        self._init_staticwidgets()
        self._init_actions()
        
    """---------------------------------------------------------------------+++
    Everything about communication with editfield.
    """
    def set_editfield( self, editfield ):
        self.E = editfield
        self.E.textChanged.connect( self._editfield_textchanged )
        self.E.setMaximumHeight( 1 )
        self.E.setMaximumWidth( 1 )
        
    """---------------------------------------------------------------------+++
    Everything about actions.
    """
    def _action_save( self ):
        print('save')
        
    def _action_addfloating( self ):
        """
        https://forum.qt.io/topic/76737/any-suggestion-on-how-to-make-floating-qlabel-move-with-content-in-qtextedit/7
        """
        
        def get_selectedrect():
            """-------------------------------------------------------------+++
            Definitions.
            """
            cur = self.textCursor()
            qrect = self.cursorRect()
            
            metrix = QtGui.QFontMetrics( self.font() )
            half_charheight = metrix.height() // 2
            
            """-------------------------------------------------------------+++
            Actual code.
            """
            # get x
            x1 = cur.selectionStart()
            x2 = cur.selectionEnd()
            
            y1 = qrect.y() - half_charheight
            y2 = y1 #+qrect.height() - half_charheight
            
            #print( x1,y1,x2,y2 )
            
            """
            # get current positions
            cursor = self.textCursor()
            x1 = cursor.selectionStart()
            x2 = cursor.selectionEnd()
            
            #
            
            charw = metrix.averageCharWidth()
            
            y1 = metrix.height()
            """
            
            return ( x1,y1,x2,y2 )
        
        def newfloating( text ):
            lab = QtWidgets.QLabel( self )
            lab.setText( text )
            return lab
            
        x1,y1,x2,y2 = get_selectedrect()
        
        
        sta = newfloating( '↓' )
        sta.move( x1,y1 )
        sta.show()
        
        #qpoint = self.cursorRect()
        #print( qpoint )
        #x, y = qpoint.x(), qpoint.y()
        
        # floating end
        end = newfloating( '↑' )
        end.move( x2,y2 )
        end.show()
        
    """---------------------------------------------------------------------+++
    Everything about text layout.
    """
    def positionlayouts( self ):
        """Recalculates the way the text should be rendered."""
        """-----------------------------------------------------------------+++
        Definitions.
        """
        
        # sizes
        widgetwidth_pixels = self.width()
        
        # positions
        margins = [ 0,0,0,0 ]
        
        def placeline( line ):
            # set line coordinates
            line.setPosition( QtCore.QPointF(margins[0],margins[1]) )
            margins[1] += line.height()
        
        """-----------------------------------------------------------------+++
        Actual code.
        """
        
        # reset lyts
        self.LYTS = []
        
        # get new lyts
        for para in self.PARAS:
            # text layout
            lyt = QtGui.QTextLayout()
            lyt.setFont( self.DEFONT )
            lyt.setTextOption( self.TEXTOPTION )
            lyt.setText( para )
        
            lyt.beginLayout()
            
            while True:
                # create the line
                line = lyt.createLine()
                if not line.isValid(): break
                
                line.setLineWidth( widgetwidth_pixels )
                placeline( line )
                
            lyt.endLayout()
            
            self.LYTS.append( lyt )
            
    def set_text( self, text ):
        # fill the editor
        self.E.setText( text )
        
    def _editfield_textchanged( self ):
        # Accepts edits from editfield and displays them.
        
        text = self.E.text()
        
        # recalculate text layouts
        self.PARAS = text.split('\n')
        self.positionlayouts()
        
        # repaint
        self.update()
        
    def _textcaret_undercoords( self, x, y ):
        """Translates mouse coordinates to the text char position."""
        """-----------------------------------------------------------------+++
        Definitions.
        """
        # placeholder values that i will change and return
        text_char = 0
        neat_char = 0
        neat_x = 0
        neat_y = 0
        
        def getlytiloc():
            # Finds correct lyt iloc for these coordinates.
            if y<=0: return 0
            for iloc in range( len(self.LYTS) ):
                rect = self.LYTS[iloc].boundingRect()
                rx,ry,rw,rh = rect.x(),rect.y(),rect.width(),rect.height()
                if y>=ry and y<=ry+rh: return iloc
            return -1
        
        def getline( lyt ):
            # Finds correct line of the lyt for these coordinates.
            if y<=0: return lyt.lineAt(0)
            for lineiloc in range( lyt.lineCount() ):
                line = lyt.lineAt(lineiloc)
                # get line's vertical boundaries
                U = line.y()
                D = U + line.height()
                # the ly is on the line
                if y>=U and y<=D: return line
            return lyt.lineAt( lyt.lineCount()-1 )
        
        def valid( char, lyt ):
            # Checks whether this char position is valid.
            # Fixes invalid ones.
            if lyt.isValidCursorPosition(char): return char
            # this char is invalid, have to
            # fix unicode byte forbidden positioning
            # compare with previous char
            if char<self.CARET_PREV[2]: # i want to go left
                return lyt.previousCursorPosition(char)
            # i want to go right
            return lyt.nextCursorPosition(char)
        
        """-----------------------------------------------------------------+++
        Actual code.
        """
        # i assume, i clicked on a line
        # get that line
        lytiloc = getlytiloc()
        lyt = self.LYTS[lytiloc]
        line = getline( lyt )
        
        # i want to place the caret at the corr. line char
        
        # get valid char relative to the whole text in self.PARAS
        for pariloc in range(lytiloc):
            text_char+=len( self.PARAS[pariloc] ) + 1 # for skipped \n
        text_char += line.xToCursor(x)
        text_char = valid( text_char, lyt )
        # place the caret at the visual nonexistant line beginning
        # it is inherited from the previous line
        neat_char = text_char-line.textStart()
        neat_x, neat_y = line.cursorToX( neat_char )
        neat_x, neat_y = 0, line.y()
        
        #print( x,y,neat_char,text_char,lyt.text()[line.textStart():text_char] )
        
        return neat_x, neat_y, neat_char, text_char
        
    """---------------------------------------------------------------------+++
    Everything about events.
    """
    def mousePressEvent( self, ev ):
        # what i do with the mouse coords:
        self.MOUSE_PREV = self.MOUSE_LAST # overwrite previous press coords
        self.MOUSE_LAST = [ ev.x(), ev.y() ] # remember current press coords
        self.MOUSE_SLCT = True # i assume i want to select some text
        
        # what i do with the caret coords:
        lx,ly,lchar,textchar = self._textcaret_undercoords(ev.x(),ev.y()) # get them
        self.CARET_PREV = [lx,ly,lchar,textchar] # overwrite prev coords
        self.CARET_LAST = [lx,ly,lchar,textchar] # remember current coords
        self.CARET_SLCT = self.MOUSE_SLCT # i assume i want to select some text
        
        # what i do with E:
        self.E.setCursorPosition( textchar )
        
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
        lx,ly,lchar,textchar = self._textcaret_undercoords(ev.x(),ev.y())
        self.CARET_LAST = [lx,ly,lchar,textchar] # remember current coords
            
        # repaint the widget
        self.update()
        
        # focus on the editor
        self.E.setFocus()
        
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
            lx,ly,lchar,textchar = self._textcaret_undercoords(ev.x(),ev.y())
            self.CARET_LAST = [lx,ly,lchar,textchar] # remember current coords
        
            # what i do with E:
            self.E.setCursorPosition( textchar )
            selen = self.CARET_PREV[3]-textchar
            self.E.setSelection( textchar, selen )
                
            # repaint the widget
            self.update()
            
    def resizeEvent( self, ev ): 
        # recalculate text layouts
        self.positionlayouts()
        
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
        
        # repaint shapes
        for shape in self.SHAPES:
            painter.drawPath( shape )
        
        # repaint lyts
        for lyt in self.LYTS:
            lyt.draw( painter, QtCore.QPointF(0,0) )
        
        painter.end()
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init( self ):
        # i want to access mouse and keyboard input
        self.setMouseTracking( True )
        #self.setFocusPolicy( QtCore.Qt.StrongFocus )
        
    def _init_staticwidgets( self ):
        # default font
        self.DEFONT = QtGui.QFont( 'consolas', 10 )
        
        # default text option
        self.TEXTOPTION = QtGui.QTextOption()
        """
        self.TEXTOPTION.setFlags(
            QtGui.QTextOption.IncludeTrailingSpaces
            #|QtGui.QTextOption.ShowTabsAndSpaces
            #|QtGui.QTextOption.ShowLineAndParagraphSeparators
            #|QtGui.QTextOption.ShowDocumentTerminator
            |QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere
            )
        """
        
        # invisible text editor
        #self.E = QtWidgets.QLineEdit( self )
        #self.E.setObjectName( 'textedit' )
        #self.E.setVisible( False )
        
    def _init_actions( self ):
        # save current file
        save = QtWidgets.QAction( 'Save', self )
        save.setShortcut( 'Ctrl+S' )
        save.triggered.connect( self._action_save )
        
        # make new buoys
        buoy = QtWidgets.QAction( 'Draw buoys', self )
        buoy.setShortcut( 'Ctrl+T' )
        buoy.triggered.connect( self._action_addfloating )
        
        self.addAction( save )
        #self.addAction( buoy )

class centralwidget( QtWidgets.QWidget ):
    
    # the data i'm working with
    CURRENT_FILE_PATH = ''
    
    def __init__( self,
                  *args, **kwargs ):
        super( centralwidget, self ).__init__( *args, **kwargs )
        
        # gui
        self._init()
        self._init_staticwidgets()
        
    """---------------------------------------------------------------------+++
    Everything about i/o.
    """
    def loadfile( self, path ):
        """
        Loads current file and initializes text layout.
        No repainting.
        """
        self.CURRENT_FILE_PATH = path
        text = readf( self.CURRENT_FILE_PATH )
        self.D.set_text( text )
        
    """---------------------------------------------------------------------+++
    Everything about init.
    """
    def _init( self ):
        self.setObjectName( 'centralwidget' )
        
    def _init_staticwidgets( self ):
        
        # scrollarea
        #sa = QtWidgets.QScrollArea( self )
        #sa.setVerticalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOn )
        #salyt = QtWidgets.QVBoxLayout()
        #salyt.setContentsMargins( 0,0,0,0 )
        #sa.setLayout( salyt )
        
        # displayfield
        self.D = displayfield( self )
        self.D.setObjectName( 'displayfield' )
        #salyt.addWidget( self.D )
        #sa.setWidget( self.D )
        
        # editfield
        E = editfield( self )
        E.setObjectName( 'textedit' )
        #E.setMaximumHeight( 15 )
        
        # connect them↑ together
        self.D.set_editfield( E )
        E.set_displayfield( self.D )
        
        # layout
        lyt = QtWidgets.QVBoxLayout()
        lyt.setContentsMargins( 0,0,0,0 )
        
        # assemble
        lyt.addWidget( self.D )
        lyt.addWidget( E )
        
        self.setLayout( lyt )
    
#---------------------------------------------------------------------------+++
# конец 2021.03.06 → 2021.03.09
