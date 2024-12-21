from PyQt6.QtWidgets import QMenuBar,QMainWindow,QWidget,QStackedLayout,QPushButton,QVBoxLayout,QTextEdit,QComboBox,QFormLayout,QHBoxLayout,QGridLayout,QMessageBox,QVBoxLayout,QApplication,QLabel,QPushButton,QLineEdit,QCheckBox,QMainWindow
import sys
from PyQt6.QtGui import QPixmap,QFont,QIcon
import math
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
    
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Menu")
        self.setGeometry(100,100,400,300)

        toolbar = self.addToolBar("Main Toolbar")

        self.new_action = QAction(QIcon("icons/new.png"),"New")
        toolbar.addAction(self.new_action)

        self.open_action = QAction(QIcon("icons/open.png"),"Open")
        toolbar.addAction(self.open_action)

        toolbar.addSeparator()
        self.save_action = QAction(QIcon("icons/save.png"),"Save")
        toolbar.addAction(self.save_action)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())


        # label1 = QLabel("Name")
        # name_edit = QLineEdit()


        # label2 = QLabel("Age")   
        # age_edit = QLineEdit()

        # form_layout = QFormLayout()
        # self.setLayout(form_layout)

        # form_layout.addRow(label1,name_edit)
        # form_layout.addRow(label2,age_edit)


# form_layout = QFormLayout()
#         self.setLayout(form_layout)

#         self.name_edit = QLineEdit()
#         self.email_edit = QLineEdit()
#         self.phone_edit = QLineEdit()

#         self.subject_combo = QComboBox()
#         self.subject_combo.addItems(["Select Subject","Personal","Business"])

#         self.message_edit = QTextEdit()

#         submit_button = QPushButton("Submit")
#         submit_button.clicked.connect(self.submitClicked)

#         form_layout.addRow(QLabel("Name"),self.name_edit)
#         form_layout.addRow(QLabel("Email"),self.email_edit)
#         form_layout.addRow(QLabel("Phone Number"),self.phone_edit)
#         form_layout.addRow(QLabel("Subject"),self.subject_combo)
#         form_layout.addRow(QLabel("Message"),self.message_edit)
#         form_layout.addRow(submit_button)

#     def submitClicked(self):
#        name = self.name_edit.text()
#        email= self.email_edit.text()
#        phone = self.phone_edit.text()
#        subject = self.subject_combo.currentText() 
#        message =self.message_edit.toPlainText()

#        print(f"Name:{name}\n Email:{email}\n Phone:{phone}\n Subject:{subject} \n Message{message}")

#   combo_box = QComboBox()
#         combo_box.addItems(["Label","Form"])
#         combo_box.activated.connect(self.changePage)


#         #creating page 1
#         label = QLabel("This is the label page")



#         # creating page 2
#         form = QFormLayout()
#         form.addRow("",QLabel("This is a form page"))
#         page2_container = QWidget()
#         page2_container.setLayout(form)


#         #creating a stacked layout 
#         self.stacked_layout = QStackedLayout()
#         self.stacked_layout.addWidget(label)
#         self.stacked_layout.addWidget(page2_container)

#         main_layout = QVBoxLayout()
#         main_layout.addWidget(combo_box)
#         main_layout.addLayout(self.stacked_layout)

#         self.setLayout(main_layout)
   
#     def changePage(self,index):
#         self.stacked_layout.setCurrentIndex(index

    #   #Step 1: Create a menubar
    #     menubar = self.menuBar()

    #     #creating the menu items 
    #     file_menu = menubar.addMenu("File")

    #     #creaating an action
    #     self.new_action = QAction("New")
        
    #     #adding action to the menu
    #     file_menu.addAction(self.new_action)

    #     #Adding a seperator
    #     file_menu.addSeparator()


    #     #creating another action
    #     self.exit_action = QAction("Exit")
    #     file_menu.addAction(self.exit_action)

    #     #creating a new menu
    #     edit_menu = menubar.addMenu("Edit")

    #     self.copy_action = QAction("Copy")
    #     edit_menu.addAction(self.copy_action)

    #     self.cut_action = QAction("Cut")
    #     edit_menu.addAction(self.cut_action)

    #     self.paste_action = QAction("Paste")
    #     edit_menu.addAction(self.paste_action)

