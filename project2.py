import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

class AdventureGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adventure Game - The GUI Edition")
        self.setGeometry(100, 100, 500, 300)

        self.layout = QVBoxLayout()
        self.story_label = QLabel("You wake up in a dark room with two doors. Do you go left or right?")
        self.layout.addWidget(self.story_label)

        self.button_left = QPushButton("Go Left")
        self.button_right = QPushButton("Go Right")
        self.layout.addWidget(self.button_left)
        self.layout.addWidget(self.button_right)

        self.button_left.clicked.connect(self.go_left)
        self.button_right.clicked.connect(self.go_right)

        self.setLayout(self.layout)

    def go_left(self):
        self.story_label.setText("You enter a library. A ghost whispers a riddle. Do you 'listen' or 'run'?")
        self.button_left.setText("Listen")
        self.button_right.setText("Run")
        self.button_left.clicked.disconnect()
        self.button_right.clicked.disconnect()
        self.button_left.clicked.connect(self.listen_ghost)
        self.button_right.clicked.connect(self.run_away)

    def go_right(self):
        self.story_label.setText("You find a trap door. Do you 'open' it or 'ignore' it?")
        self.button_left.setText("Open")
        self.button_right.setText("Ignore")
        self.button_left.clicked.disconnect()
        self.button_right.clicked.disconnect()
        self.button_left.clicked.connect(self.open_trapdoor)
        self.button_right.clicked.connect(self.ignore_trapdoor)

    def listen_ghost(self):
        self.story_label.setText("The ghost says: 'Seek the heart of the maze.' You feel wiser. You win!")
        self.button_left.setDisabled(True)
        self.button_right.setDisabled(True)

    def run_away(self):
        self.story_label.setText("You trip while running and fall into the void. Game over.")
        self.button_left.setDisabled(True)
        self.button_right.setDisabled(True)

    def open_trapdoor(self):
        self.story_label.setText("You climb down and find treasure. You win!")
        self.button_left.setDisabled(True)
        self.button_right.setDisabled(True)

    def ignore_trapdoor(self):
        self.story_label.setText("You sit and do nothing. Eventually, you're forgotten. Game over.")
        self.button_left.setDisabled(True)
        self.button_right.setDisabled(True)

app = QApplication(sys.argv)
game = AdventureGame()
game.show()
sys.exit(app.exec())
