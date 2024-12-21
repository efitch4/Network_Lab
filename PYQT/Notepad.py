from PyQt6.QtWidgets import QStyleFactory, QInputDialog,QFileDialog,QMenu,QMenuBar,QTextEdit,QMainWindow,QWidget,QStackedLayout,QPushButton,QVBoxLayout,QTextEdit,QComboBox,QFormLayout,QHBoxLayout,QGridLayout,QMessageBox,QVBoxLayout,QApplication,QLabel,QPushButton,QLineEdit,QCheckBox,QMainWindow
import sys
from PyQt6.QtGui import QPixmap,QFont,QIcon,QTextCursor,QColor
import math
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
    
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Notepad")
        self.setGeometry(100,100,400,300)

        self.current_file = None


        self.edit_field = QTextEdit()
        self.setCentralWidget(self.edit_field)

        # Create a menubar

        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        #Creating file menu 
        fileMenu = QMenu("File",self)
        menubar.setNativeMenuBar(False)
        menubar.addMenu(fileMenu)

        #Create actions
        new_action = QAction("New",self)
        fileMenu.addAction(new_action)
        new_action.triggered.connect(self.new_file)

        open_action = QAction("Open",self)
        fileMenu.addAction(open_action)
        open_action.triggered.connect(self.open_file)

        save_action = QAction("Save",self)
        fileMenu.addAction(save_action)
        save_action.triggered.connect(self.save_file)

        save_as_action = QAction("Save As",self)
        fileMenu.addAction(save_as_action)
        save_as_action.triggered.connect(self.save_file_as)

        #Creating the edit menu

        editmenu = QMenu("Edit",self)
        menubar.addMenu(editmenu)

        undo_action = QAction("Undo",self)
        editmenu.addAction(undo_action)
        undo_action.triggered.connect(self.edit_field.undo)


        redo_action = QAction("Redo",self)
        editmenu.addAction(redo_action)
        redo_action.triggered.connect(self.edit_field.redo)

        cut_action = QAction("Cut",self)
        editmenu.addAction(cut_action)
        cut_action.triggered.connect(self.edit_field.cut)

        paste_action = QAction("Paste",self)
        editmenu.addAction(paste_action)
        paste_action.triggered.connect(self.edit_field.paste)

        copy_action = QAction("Copy",self)
        editmenu.addAction(copy_action)
        copy_action.triggered.connect(self.edit_field.copy)

        find_action = QAction("Find",self )
        editmenu.addAction(find_action)
        find_action.triggered.connect(self.find_text)


    def new_file(self):
        print("Creating new file")

    def open_file(self):
        print("Creating new file")
        file_path,_ = QFileDialog.getOpenFileName(self,"Open File","All Files(*);; Python Files(*.py)")
        with open(file_path,"r") as file:
            text = file.read()
            self.edit_field.setText(text)
    
    def save_file_as(self):
        print("Saving File")
        file_path,_ = QFileDialog.getSaveFileName(self,"Save File","","All Files(*);; Python File")
        if file_path:
            with open(file_path,"w") as file:
                file.write(self.edit_field.toPlainText())
            self.current_file = file_path


    def save_file(self):
        print("Saving a file ")
        if self.current_file:
            with open(self.current_file,"w") as file:
                file.write(self.edit_field.toPlainText())
        else:
            self.save_file_as()


    def find_text(self):
        print("Finding text")
        search_text,ok = QInputDialog.getText(self,"Find text","Search for")
        if ok:
                all_words=[]
                self.edit_field.moveCursor(QTextCursor.MoveOperation.Start)
                highlight_color = QColor(Qt.GlobalColor.yellow)

                while(self.edit_field.find(search_text)):
                     selection = QTextEdit.ExtraSelection()
                     selection.format.setBackground(highlight_color)

                     selection.cursor = self.edit_field.textCursor()
                     all_words.append(selection)
                self.edit_field.setExtraSelections(all_words)



app = QApplication(sys.argv)
app.setStyle("Windows")
print(QStyleFactory.keys())
print(app.style().name())
window = Window()
window.show()
sys.exit(app.exec())
