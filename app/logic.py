import time
from sympy.parsing.latex import parse_latex
from questions import QUESTIONS


class GameManager:
    def __init__(self, gui=None):
        """Initialize the game manager.
        
        Args:
            gui (MainWindow): Reference to the main window GUI.
        """
        self.gui = gui
        self.questions = QUESTIONS
        self.current_question = None
        self.correct_answer = None
        self.selected_subjects = ["algebra"] # default value

    def set_subjects(self, subjects):
        """Set the selected subjects for the game.
        
        Args:
            subjects (list): List of subject names (e.g., ["algebra", "equations"])
        """
        self.selected_subjects = subjects
        print(f"Selected subjects: {subjects}")

    def start_game(self):
        """Start a new game and initialize game state by enabling and disabling relevant UI components."""
        print("Game started")
        if self.gui:
            self.gui.questionWidget.setEnabled(True)
            self.gui.answerInput.setEnabled(True)
            self.gui.submitButton.setEnabled(True)
            self.gui.skipButton.setEnabled(True)
            self.gui.levelMenu.setEnabled(False)
            self.gui.subjectMenu.setEnabled(False)
            self.gui.startGameMenu.setEnabled(False)
            self.gui.seeScoresMenu.setEnabled(False)
            self.gui.endGameMenu.setEnabled(True)
        self.next_question()
            

    def next_question(self):
        """Load and display the next question from selected subjects."""
        import random
        
        if not self.selected_subjects:
            print("No subjects selected!")
            return
            
        # Pick a random subject from selected ones
        subject = random.choice(self.selected_subjects)
        
        # Pick a random difficulty (you can make this selectable too)
        difficulty = "easy"
        
        # Pick a random question
        questions_list = self.questions[subject][difficulty]
        question_data = random.choice(questions_list)
        
        self.current_question = question_data["question"]
        self.correct_answer = question_data["answer"]
        
        if self.gui:
            self.gui.questionWidget.setText(self.current_question)
            self.gui.answerInput.clear()
            self.gui._startTimer()
        

    def check_answer(self, answer, elapsed_time):
        """Check the user's answer.
        
        Args:
            answer (str): The user's answer
            elapsed_time (int): Time taken to answer in seconds
        """
        parsed_answer = parse_latex(answer)
        print(f"Checking answer: {answer}")
        print(f"Time taken: {elapsed_time} seconds")
        print(f"Parsed answer: {parsed_answer}")
        self.next_question()