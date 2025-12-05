from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QInputDialog, QTableWidgetItem, QTableWidget
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
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

        # Initialize timer variables BEFORE creating UI
        self.time_elapsed = 0
        self.start_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._updateTimer)
        self.scoreboard_window = None


        self.game_manager = GameManager(gui=self)  # Pass self reference
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

        self.questionBrowser = QWebEngineView()
        main_layout.addWidget(self.questionBrowser)
        
        # Add different sections
        self._createMenuBar()
        main_layout.addWidget(self._createQuestionArea("Fråga"))
        main_layout.addWidget(self._createAnswerArea())
        main_layout.addWidget(self._createButtonArea())
        main_layout.addWidget(self._createTimerArea())
        main_layout.addWidget(self._createPointArea())
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def _createMenuBar(self):
        """Create the application menu bar.
        
        Adds menu items for Preferences, Levels, Subjects, Start Game, and See Scores.
        """
        menuBar = self.menuBar()
        self.preferencesMenu = QMenu("&Preferences", self)
        self.levelMenu = QMenu("&Levels", self)
        self.subjectMenu = QMenu("&Subjects", self)
        self.startGameMenu = QMenu("&Start Game", self)
        self.seeScoresMenu = QMenu("&See Scores", self)
        self.endGameMenu = QMenu("&End Game", self)
        menuBar.addMenu(self.preferencesMenu)
        menuBar.addMenu(self.levelMenu)
        menuBar.addMenu(self.subjectMenu)
        menuBar.addMenu(self.startGameMenu)
        menuBar.addMenu(self.seeScoresMenu)
        menuBar.addMenu(self.endGameMenu)
        self.endGameMenu.setEnabled(False)  # Disabled initially

        newGameAction = self.startGameMenu.addAction("New Game")
        newGameAction.triggered.connect(self.game_manager.start_game)
        # Adding subjects to menu
        self.selectAlgebra = self.subjectMenu.addAction("Algebra")
        self.selectEquations = self.subjectMenu.addAction("Equations")
        self.selectCalculus = self.subjectMenu.addAction("Calculus")
        # Setting subjects to checkable
        self.selectAlgebra.setCheckable(True)
        self.selectEquations.setCheckable(True)
        self.selectCalculus.setCheckable(True)
        # Adding levels to menu
        self.selectEasy = self.levelMenu.addAction("Easy")
        self.selectHard = self.levelMenu.addAction("Hard")
        # Setting levels to checkable
        self.selectEasy.setCheckable(True)
        self.selectHard.setCheckable(True)
        # Connect to update game manager when changed
        self.selectAlgebra.triggered.connect(self.update_selected_subjects)
        self.selectEquations.triggered.connect(self.update_selected_subjects)
        self.selectCalculus.triggered.connect(self.update_selected_subjects)

        self.endGame = self.endGameMenu.addAction("Quit game")
        self.endGame.triggered.connect(self.game_manager.finish_game)

        self.selectEasy.triggered.connect(self.update_selected_difficulty)
        self.selectHard.triggered.connect(self.update_selected_difficulty)





    def _createQuestionArea(self, question):
        """Create the question display area with LaTeX rendering.
        
        Args:
            question (str): The LaTeX math question to display.
            
        Returns:
            QWebEngineView: The web view widget containing the rendered question.
        """
        self.questionWidget = QWebEngineView()
        self.questionWidget.setMinimumHeight(150)  # Set minimum height
        self.questionWidget.setEnabled(False)  # Disabled until game starts
        
        # Load initial empty question
        self.update_question_display(question)
        
        return self.questionWidget
    
    def update_question_display(self, latex_question):
        """Update the question display with LaTeX rendering.
        
        Args:
            latex_question (str): LaTeX formatted question string.
        """
        html = f"""
        <html>
        <head>
            <script>
                window.MathJax = {{
                    tex: {{inlineMath: [['$','$'], ['\\\\(','\\\\)']]}}
                }};
            </script>
            <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        </head>
        <body style="font-size: 30px; padding: 20px; text-align: center; font-family: Arial;">
            <p><b>Question:</b></p>
            <p>\\({latex_question}\\)</p>
        </body>
        </html>
        """
        self.questionWidget.setHtml(html)
    
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
        self.answerInput.setEnabled(False)  # Disabled until game starts
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
        self.skipButton.clicked.connect(self.on_skip)
        
        button_layout.addStretch()
        button_layout.addWidget(self.submitButton)
        button_layout.addWidget(self.skipButton)
        button_layout.addStretch()
        
        button_widget.setLayout(button_layout)
        self.submitButton.setEnabled(False)  # Disabled until game starts
        self.skipButton.setEnabled(False)    # Disabled until game starts
        return button_widget
    
    def _createTimerArea(self):
        """Create the timer area.

        Returns:
            QLabel: Label widget displaying the elapsed time.
        """
        self.timerWidget = QLabel(f"Time: {self.time_elapsed}s")
        self.timerWidget.setAlignment(Qt.AlignCenter)
        font = self.timerWidget.font()
        font.setPointSize(20)
        self.timerWidget.setFont(font)
        
        return self.timerWidget
    
    def _createPointArea(self):
        """Create the points display area.

        Returns:
            QLabel: Label widget displaying the current points.
        """
        self.pointsWidget = QLabel(f"Points: 0")
        font = self.pointsWidget.font()
        font.setPointSize(20)
        self.pointsWidget.setFont(font)
        
        return self.pointsWidget
    
    def _updateTimer(self):
        """Update the timer display by counting up."""
        self.time_elapsed += 1
        self.timerWidget.setText(f"Time: {self.time_elapsed}s")

    def _startTimer(self):
        """Start the question timer."""
        import time
        self.start_time = time.time()  # Store when timer started
        self.time_elapsed = 0  # Reset to 0
        self.timerWidget.setText(f"Time: {self.time_elapsed}s")
        self.timer.start(1000)  # Timer ticks every second (1000ms)
        
    def _stopTimer(self):
        """Stop the timer and return elapsed time."""
        self.timer.stop()
        return self.time_elapsed  # Return elapsed seconds
    
    def _restart_timer(self, elapsed_time):
        self.start_time = elapsed_time
        self.timer.start(1000)
    
    def on_submit(self):
        """Handle the submit button click."""
        user_answer = self.answerInput.text()
        elapsed = self._stopTimer()  # Get elapsed time
        self.game_manager.check_answer(user_answer, elapsed)  # Pass it to game manager

    def on_skip(self):
        self.game_manager.next_question()

    def update_selected_subjects(self):
        """Update the game manager with selected subjects."""
        selected_subjects = []
        if self.selectAlgebra.isChecked():
            selected_subjects.append("algebra")
        if self.selectEquations.isChecked():
            selected_subjects.append("equations")
        if self.selectCalculus.isChecked():
            selected_subjects.append("calculus")

        self.game_manager.set_subjects(selected_subjects)

    def update_selected_difficulty(self):
        current_difficulty = None
        if self.selectEasy.isChecked():
            current_difficulty = "easy"
        if self.selectHard.isChecked():
            current_difficulty = "hard"
        self.game_manager.set_difficulty(current_difficulty)


    def show_save_score_dialog(self):
        """Show dialog to save player's score.
        
        Returns:
            str or None: Player's name if they chose to save, None if cancelled.
        """
        name, ok = QInputDialog.getText(
            self,
            "Spara Resultat",
            "Namn:",
            QLineEdit.Normal,
            ""
        )
        
        if ok and name:
            # User clicked "Spara" and entered a name
            return name
        else:
            # User clicked "Spara inte" or cancelled
            return None
        

    def open_scoreboard(self):
        if self.scoreboard_window is None:
            self.scoreboard_window = Scoreboard()
        self.scoreboard_window.show()
        self.scoreboard_window.raise_()


class Scoreboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scoreboard")
        self.resize(700, 400)

        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        layout.addWidget(self.table)
        

        self.load_scores()

    def load_scores(self):
        import sqlite3
        conn = sqlite3.connect("scores.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, score, difficulty, subject, date
            FROM scores ORDER BY score DESC
        """)
        rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Name", "Score", "Difficulty", "Subject", "Date"]
        )

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

        self.table.resizeColumnsToContents()

