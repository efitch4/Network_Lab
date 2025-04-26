from PyQt6.QtWidgets import QMainWindow, QApplication,QStyleFactory,QLabel,QVBoxLayout


import sys
class Window(QMainWindow):

    def __init__(self): 
        super().__init__() 
        self.initUI 

    def initUI(self): 
        self.setGeometry(0,0,700,500) 
        label = QLabel("<h1>This is a label</h1>",self) 
        layout = QVBoxLayout() 
        layout.addWidget(label) 
        self.setLayout(layout) 

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()