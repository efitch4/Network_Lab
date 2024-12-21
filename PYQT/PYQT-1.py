from PyQt6.QtWidgets import QWidget,QHBoxLayout,QGridLayout,QMessageBox,QVBoxLayout,QApplication,QLabel,QPushButton,QLineEdit,QCheckBox,QMainWindow
import sys
from PyQt6.QtGui import QPixmap,QFont
import math


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("My First PyQT Window")
        self.setGeometry(0,0,400,150)

        label1 = QLabel("Label 1")
        label2 = QLabel("Label 2")
        label3 = QLabel("Label 3")  

        button1 = QPushButton("Button 1")
        button2 = QPushButton("Button 2")
        button3=    QPushButton("Button 3")

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(label1,0,0)
        layout.addWidget(label2,0,1)
        layout.addWidget(label3,0,2)

        layout.addWidget(button1,1,0)
        layout.addWidget(button2,1,1)
        layout.addWidget(button3,1,2)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())




#   button1 = QPushButton("Button 1")
#         button2 = QPushButton("Button 2")
#         button3 = QPushButton("Button 3")
#         button4 = QPushButton("Button 4")
   
#         hbox1 = QHBoxLayout()
#         hbox1.addWidget(button1)
#         hbox1.addWidget(button2)

#         hbox2 = QHBoxLayout()
#         hbox2.addWidget(button3)
#         hbox2.addWidget(button4)

#         vbox =QVBoxLayout()
#         vbox.addLayout(hbox1)
#         vbox.addLayout(hbox2)

#         self.setLayout(vbox)




    #    # new code added to create a button
    #     button = QPushButton(self)
    #     button.setText("Click here")
    #     button.move(100,200)
    #     button.clicked.connect(self.buttonClicked)

    #     #adding label to display count
    #     self.label = QLabel(self)
    #     self.label.setText("0")
    #     self.label.move(100,150)
    #     self.label.adjustSize()


    # def initUI(self):  
    #     self.count = 0  
    #     self.setWindowTitle("My First PyQT Window")
    #     self.setGeometry(0,0,300,200)

    #     self.name_label = QLabel(self)
    #     self.name_label.setText("Enter you name")
    #     self.name_label.move(60,10)

    #     self.name = QLineEdit(self)
    #     self.name.resize(200,20)
    #     self.name.move(60,50)

    #     button = QPushButton(self)
    #     button.setText("Add")
    #     button.move(200,80)
    #     button.clicked.connect(self.buttonClicked)

    #     self.result_label = QLabel(self)
    #     self.result_label.setFixedSize(150,20)
    #     self.result_label.move(60,120)


    # def buttonClicked(self):
    #     print("Button clicked")
    #     print("Your name is :"+ self.name.text())
    #     self.result_label.setText("Your name is :"+ self.name.text())

#  def calculate_sum(self):
#         try:
#             num1 = float(self.num1_input.text())
#             num2 = float(self.num1_input.text())
#             result = num1 + num2

#             self.result_label.setText(f"Results: {result:.2f}")
#             self.result_label.resize(300,20)
#         except ValueError:
#             self.result_label.setText("Invalid Input, please enter numbers")



    #     sugar_checkbox = QCheckBox(self)
    #     sugar_checkbox.setText("Sugar")
    #     sugar_checkbox.move(20,40)
    #     sugar_checkbox.toggled.connect(self.sugar_checked)

    #     self.label = QLabel(self)
    #     self.label.setText("")
    #     self.label.resize(200,20)
    #     self.label.move(20,90)


    # def sugar_checked(self,checked): 
    #     if checked:
    #         self.label.setText("Sugar added")
    #     else:
    #         self.label.setText("Sugar not added")

   
    # # The total cost of coffe would be this variable 
    #     self.total_cost = 0 

    #     label = QLabel(self)
    #     label.setText("Select your options")
    #     label.resize(200,20)
    #     label.move(20,20)

    #     sugar_checkbox = QCheckBox(self)
    #     sugar_checkbox.setText("Sugar($ 0.5)")
    #     sugar_checkbox.move(20,40)
    #     sugar_checkbox.toggled.connect(self.sugar_checked)


    #     milk_checkbox = QCheckBox(self)
    #     milk_checkbox.setText("Milk ($ 1)")
    #     milk_checkbox.move(20,60)
    #     milk_checkbox.toggled.connect(self.milk_checked)

    #     self.result_label = QLabel(self)
    #     self.result_label.setText("Total cost is $0")
    #     self.result_label.resize(200,20)
    #     self.result_label.move(20,90)

    # def sugar_checked(self,checked):
    #     if checked:
    #         self.total_cost+=0.5
    #     else:
    #         self.total_cost-=0.5
    #     self.result_label.setText("Total cost: $" + str(self.total_cost))

    # def milk_checked(self,checked):
    #     if checked:
    #         self.total_cost+=1
    #     else:
    #         self.total_cost-=1
    #     self.result_label.setText("Total cost: $" + str(self.total_cost))


   
    #     button = QPushButton("Show Messagebox",self)
    #     button.setGeometry(150,80,200,40)
    #     button.clicked.connect(self.show_message_box)

    # def show_message_box(self):
    #     msg = QMessageBox()
    #     msg.setWindowTitle("Message box title")
    #     msg.setText("This is a simple QmessageBox")
    #     msg.setIcon(QMessageBox.Icon.Information)
    #     msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    #     msg.setDefaultButton(QMessageBox.StandardButton.Ok)
    #     result = msg.exec()

    #     if result == QMessageBox.StandardButton.Ok:
    #         print("Ok button is clicked")
    #     else:
    #         print("Cancel button is clicked")

# number_label = QLabel("Enter a number",self)
#         number_label.move(20,20)

#         self.number_input = QLineEdit(self)
#         self.number_input.move(200,20)

#         calculate_button = QPushButton("Find Root",self)
#         calculate_button.move(200,60)

#         self.result_label = QLabel("Result:",self)
#         self.result_label.move(20,100)

#         calculate_button.clicked.connect(self.calculate_square_root)

#     def calculate_square_root(self):
#         try:
#             number = float(self.number_input.text())
#             math.sqrt(number)
#             square_root = math.sqrt(number)
#             if square_root.is_integer():
#                 self.result_label.setText(f"Square root: {square_root}")
#             else:
#                 msg = QMessageBox.warning(self,"Not a perfrect square", "The number is not a perfrect square")
#         except ValueError:
#             QMessageBox.warning(self,"Invalid input", "Please enter a valid number" )

    # def initUI(self):  
    #     self.setWindowTitle("My First PyQT Window")
    #     self.setGeometry(0,0,400,150)
   
    #     label = QLabel("Name")
    #     name = QLineEdit()
    #     button = QPushButton("Add")

    #     layout= QVBoxLayout()
    #     layout.addWidget(label)
    #     layout.addWidget(name)
    #     layout.addWidget(button)
        
    #     self.setLayout(layout)