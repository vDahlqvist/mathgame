import time


class GameManager:
    def __init__(self, gui=None):
        """Initialize the game manager.
        
        Args:
            gui (MainWindow): Reference to the main window GUI.
        """
        self.gui = gui

    def start_game(self):
        """Start a new game and enable UI elements."""
        print("Game started")
        if self.gui:
            self.gui._startTimer()
            self.gui.questionWidget.setEnabled(True)
            self.gui.answerInput.setEnabled(True)
            self.gui.submitButton.setEnabled(True)
            self.gui.skipButton.setEnabled(True)

    def next_question(self):
        pass

    def check_answer(self, answer, elapsed_time):
        """Check the user's answer.
        
        Args:
            answer (str): The user's answer
            elapsed_time (int): Time taken to answer in seconds
        """
        print(f"Checking answer: {answer}")
        print(f"Time taken: {elapsed_time} seconds")