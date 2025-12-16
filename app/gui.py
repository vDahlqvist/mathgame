from PyQt5.QtWidgets import QMainWindow, QMenu, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QInputDialog, QTableWidgetItem, QTableWidget, QMessageBox
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

        # Initialize variables
        self.time_elapsed = 0
        self.start_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._updateTimer)
        self.scoreboard_window = None


        self.game_manager = GameManager(gui=self)
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
        self.levelMenu = QMenu("&Levels", self)
        self.subjectMenu = QMenu("&Subjects", self)
        self.startGameMenu = QMenu("&Start Game", self)
        self.seeScoresMenu = QMenu("&See Scores", self)
        self.endGameMenu = QMenu("&End Game", self)
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
        # Adding button for ending game
        self.endGame = self.endGameMenu.addAction("Quit game")
        self.endGame.triggered.connect(self.game_manager.finish_game)
        # Action for selecting difficulty
        self.selectEasy.triggered.connect(self.update_selected_difficulty)
        self.selectHard.triggered.connect(self.update_selected_difficulty)
        # Action for opening score menu
        self.seeScores = self.seeScoresMenu.addAction("Show Scores")
        self.seeScores.triggered.connect(self.open_scoreboard)





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
        """Update the timer display by counting up.
        
        Increments the elapsed time counter by 1 second and updates the
        timer display widget. This is called automatically by the QTimer
        every 1000ms (1 second).
        """
        self.time_elapsed += 1
        self.timerWidget.setText(f"Time: {self.time_elapsed}s")

    def _startTimer(self):
        """Start the question timer.
        
        Resets the elapsed time to 0, updates the display, and starts the QTimer
        to increment every 1000ms (1 second). Records the current time for reference.
        """
        import time
        self.start_time = time.time()  # Store when timer started
        self.time_elapsed = 0  # Reset to 0
        self.timerWidget.setText(f"Time: {self.time_elapsed}s")
        self.timer.start(1000)  # Timer ticks every second (1000ms)
        
    def _stopTimer(self):
        """Stop the timer and return elapsed time.
        
        Returns:
            int: The elapsed time in seconds since the timer was started.
        """
        self.timer.stop()
        return self.time_elapsed  # Return elapsed seconds
    
    def _restart_timer(self, elapsed_time):
        """Restart the timer from a specific elapsed time.
        
        Used when the player gives an incorrect answer and needs to try again
        without resetting the timer to zero.
        
        Args:
            elapsed_time (int): The elapsed time in seconds to continue from.
        """
        self.start_time = elapsed_time
        self.timer.start(1000)
    
    def on_submit(self):
        """Handle the submit button click.
        
        Retrieves the user's answer from the input field, stops the timer,
        and passes the answer to the game manager for validation.
        """
        user_answer = self.answerInput.text()
        elapsed = self._stopTimer()  # Get elapsed time
        self.game_manager.check_answer(user_answer, elapsed)  # Pass it to game manager

    def on_skip(self):
        """Handle the skip button click.
        
        Loads the next question without checking the current answer.
        """
        self.game_manager.next_question()

    def update_selected_subjects(self):
        """Update the game manager with selected subjects.
        
        Reads the checkbox states from the subject menu and passes the list of
        selected subjects to the game manager.
        """
        selected_subjects = []
        if self.selectAlgebra.isChecked():
            selected_subjects.append("algebra")
        if self.selectEquations.isChecked():
            selected_subjects.append("equations")
        if self.selectCalculus.isChecked():
            selected_subjects.append("calculus")

        self.game_manager.set_subjects(selected_subjects)

    def update_selected_difficulty(self):
        """Update the game manager with selected difficulty level.
        
        Reads the checkbox states from the level menu and passes the selected
        difficulty to the game manager.
        """
        current_difficulty = None
        if self.selectEasy.isChecked():
            current_difficulty = "easy"
        if self.selectHard.isChecked():
            current_difficulty = "hard"
        self.game_manager.set_difficulty(current_difficulty)


    def show_save_score_dialog(self):
        """Show dialog to save player's score with input validation.
        
        Displays an input dialog for the player to enter their name and save
        their score to the database. Validates that the name is not empty or
        whitespace-only and is within acceptable length limits (1-50 characters).
        If validation fails, shows an error message and prompts again in a loop
        until a valid name is entered or the user cancels.
        
        The validated name is trimmed of leading/trailing whitespace before saving.
        
        Returns:
            str or None: Player's trimmed name if they chose to save and name is valid,
                        None if cancelled.
        """
        while True:
            name, ok = QInputDialog.getText(
                self,
                "Save Result?",
                "Name:",
                QLineEdit.Normal,
                ""
            )
            
            if not ok:
                # User cancelled
                return None
            
            # Validate name
            if not name or not name.strip():
                QMessageBox.warning(
                    self,
                    "Invalid Name",
                    "Please enter a valid name (not empty or whitespace only)."
                )
                continue
            
            if len(name.strip()) > 50:
                QMessageBox.warning(
                    self,
                    "Invalid Name",
                    "Name must be 50 characters or less."
                )
                continue
            
            # Name is valid
            self.game_manager.save_score(name.strip())
            return name.strip()
        

    def open_scoreboard(self):
        """Open the scoreboard window.
        
        Creates a new Scoreboard window if one doesn't exist, then shows and
        raises it to the front. Reuses the existing window if already created.
        
        Note:
            The scoreboard window is not destroyed when closed by the user,
            so it maintains its state between opens.
        """
        if self.scoreboard_window is None:
            self.scoreboard_window = Scoreboard()
        self.scoreboard_window.show()
        self.scoreboard_window.raise_()


class Scoreboard(QWidget):
    """Window displaying the high scores table.
    
    This widget shows all saved scores from the database in a sortable table
    format, including player names, scores, difficulty, subject, and date.
    
    Attributes:
        table (QTableWidget): The table widget displaying score data.
    """
    
    def __init__(self):
        """Initialize the scoreboard window and load scores from the database."""
        super().__init__()
        self.setWindowTitle("Scoreboard")
        self.resize(700, 400)

        self.logic = GameManager()

        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        layout.addWidget(self.table)
        

        self.load_scores()

    def load_scores(self):
        """Load and display scores from the database.
        
        Queries the database for all scores via the GameManager, sorted by score
        in descending order, and populates the table widget with the results.
        Each row contains the player's name, score, difficulty, subject, and date.
        
        Note:
            If database errors occur, an empty list is returned and the table
            will be empty but the application will continue running.
        """

        rows = self.logic.get_scores()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Name", "Score", "Difficulty", "Subject", "Date"]
        )

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

        self.table.resizeColumnsToContents()

