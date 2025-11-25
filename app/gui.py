from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from logic import GameManager

class MainWindow(QMainWindow):
    """Main window for the math game application.
    
    This class creates and manages the main user interface including the menu bar,
    question display area, answer input field, and control buttons.
    
    Attributes:
        questionWidget (QLabel): Label widget displaying the current math question.
        answerInput (QLineEdit): Input field for the user's answer.
        submitButton (QPushButton): Button to submit the answer.
        skipButton (QPushButton): Button to skip the current question.
    """
    
    def __init__(self):
        """Initialize the main window and create the user interface."""
        super().__init__()

        self.game_manager = GameManager()
        # Create the main layout first
        self._createUI()
        
    def _createUI(self):
        """Create and organize the main user interface layout.
        
        Sets up the central widget with a vertical layout containing the question area,
        answer input field, and button controls.
        """
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Add different sections
        self._createMenuBar()
        main_layout.addWidget(self._createQuestionArea("Fråga"))
        main_layout.addWidget(self._createAnswerArea())
        main_layout.addWidget(self._createButtonArea())
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def _createMenuBar(self):
        """Create the application menu bar.
        
        Adds menu items for Preferences, Levels, Subjects, Start Game, and See Scores.
        """
        menuBar = self.menuBar()
        preferencesMenu = QMenu("&Preferences", self)
        levelMenu = QMenu("&Levels", self)
        subjectMenu = QMenu("&Subjects", self)
        startGameMenu = QMenu("&Start Game", self)
        seeScoresMenu = QMenu("&See Scores", self)
        menuBar.addMenu(preferencesMenu)
        menuBar.addMenu(levelMenu)
        menuBar.addMenu(subjectMenu)
        menuBar.addMenu(startGameMenu)
        menuBar.addMenu(seeScoresMenu)

        newGameAction = startGameMenu.addAction("New Game")
        newGameAction.triggered.connect(self.game_manager.start_game)


    def _createQuestionArea(self, question):
        """Create the question display area.
        
        Args:
            question (str): The math question to display.
            
        Returns:
            QLabel: The label widget containing the question text.
        """
        self.questionWidget = QLabel(question)
        self.questionWidget.setAlignment(Qt.AlignCenter)
        font = self.questionWidget.font()
        font.setPointSize(30)
        self.questionWidget.setFont(font)
        return self.questionWidget
    
    def _createAnswerArea(self):
        """Create the answer input field.
        
        Returns:
            QLineEdit: The input field where users enter their answers.
        """
        self.answerInput = QLineEdit()
        self.answerInput.setPlaceholderText("Enter your answer...")
        self.answerInput.setAlignment(Qt.AlignCenter)
        font = self.answerInput.font()
        font.setPointSize(20)
        self.answerInput.setFont(font)
        return self.answerInput
    
    def _createButtonArea(self):
        """Create the button control area.
        
        Creates a horizontal layout with Submit and Skip buttons centered on the screen.
        
        Returns:
            QWidget: Widget containing the button layout.
        """
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        
        self.submitButton = QPushButton("Submit")
        self.submitButton.clicked.connect(self.on_submit)
        self.skipButton = QPushButton("Skip")
        
        button_layout.addStretch()
        button_layout.addWidget(self.submitButton)
        button_layout.addWidget(self.skipButton)
        button_layout.addStretch()
        
        button_widget.setLayout(button_layout)
        return button_widget
    
    def on_submit(self):
        """Handle the submit button click."""
        user_answer = self.answerInput.text()
        self.game_manager.check_answer(user_answer)

