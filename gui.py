from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QWidget, QVBoxLayout, QLabel, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
       
        def _createMenuBar(self):
            menuBar = self.menuBar()
            # Creating menus using a QMenu object
            preferencesMenu = QMenu("&Preferences", self)
            levelMenu = QMenu("&Levels", self)
            subjectMenu = QMenu("&Subjects", self)
            startGameMenu = QMenu("&Start Game", self)
            seeScoresMenu = QMenu("&See Scores", self)
            # Adding menus to the menu bar
            menuBar.addMenu(preferencesMenu)
            menuBar.addMenu(levelMenu)
            menuBar.addMenu(subjectMenu)
            menuBar.addMenu(startGameMenu)
            menuBar.addMenu(seeScoresMenu)

        def _createQuestionArea(self):
            self.questionWidget = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(self.questionWidget)



        _createMenuBar(self)
        _createQuestionArea(self)
