import time
from sympy.parsing.latex import parse_latex
from questions import QUESTIONS
import random
import math


class GameManager:
    def __init__(self, gui=None, db=None):
        """Initialize the game manager.
        
        Args:
            gui (MainWindow): Reference to the main window GUI.
        """
        self.gui = gui
        self.db = db
        self.questions = QUESTIONS
        self.current_question = None
        self.correct_answer = None
        self.selected_subjects = ["algebra"]  # Default
        self.current_difficulty = "easy" # Default value
        self.current_points = 0
        self.questions_completed = 0

    def set_difficulty(self, difficulty):
        """Set the difficulty level for the game.
        
        Args:
            difficulty (str): Difficulty level ("easy" or "hard")
        """
        self.current_difficulty = difficulty
        print(f"Difficulty set to: {difficulty}")

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
        
        if not self.selected_subjects:
            print("No subjects selected!")
            return
            
        # Pick a random subject from selected ones
        subject = random.choice(self.selected_subjects)
        
        # Pick a random difficulty (you can make this selectable too)
        difficulty = self.current_difficulty
        
        # Pick a random question
        questions_list = self.questions[subject][difficulty]
        question_data = random.choice(questions_list)
        
        self.current_question = question_data["question"]
        self.correct_answer = question_data["answer"]
        
        if self.gui:
            # Use the new update method instead of setText
            self.gui.update_question_display(self.current_question)
            self.gui.answerInput.clear()
            self.gui._startTimer()

    def check_answer(self, answer, elapsed_time):
        """Check the user's answer.
        
        Args:
            answer (str): The user's answer
            elapsed_time (int): Time taken to answer in seconds
        """
        try:
            parsed_answer = parse_latex(answer)
            parsed_correct = parse_latex(self.correct_answer)
            
            is_correct = parsed_answer == parsed_correct # boolean returning true or false depending on if answer is correct or not
            
            print(f"User answer: {answer} -> {parsed_answer}")
            print(f"Correct answer: {self.correct_answer} -> {parsed_correct}")
            print(f"Time taken: {elapsed_time} seconds")
            print(f"Result: {'Correct!' if is_correct else 'Incorrect'}")

            if is_correct:
                self.calculate_points(elapsed_time, self.current_difficulty)
                self.questions_completed +=1
                if self.questions_completed >= 10:
                    self.finish_game() # if 10 questions have been answered, end round
                else:
                    self.next_question() # Load next question if correct answer
            elif not is_correct:
                if self.gui:
                    self.gui._restart_timer(elapsed_time)
                    self.gui.answerInput.clear()
            
            return is_correct
        except Exception as e:
            print(f"Error parsing answer: {e}")
            return False
        
    def calculate_points(self, elapsed_time, difficulty):
        """Update player's score based on time and difficulty.
        
        Args:
            elapsed_time (int): Time taken to answer
            difficulty (str): Question difficulty level
        """
        print(f"Updating points for difficulty: {difficulty}, time: {elapsed_time}s")
        base_easy = 50
        base_hard = 100
        k = 0.1
        multiplier = math.exp(-k * elapsed_time)
        if difficulty == "easy":
            points  = base_easy * multiplier
        if difficulty == "hard":
            points = base_hard * multiplier
        points = int(points) # Round to whole number
        print(f"Points for this question: {points}, with difficulty: {difficulty} and time: {elapsed_time}")
        self.update_points(points)
    
    def update_points(self, points):
        self.current_points = self.current_points + points
        if self.gui:
            self.gui.pointsWidget.setText(f"Points: {self.current_points}")

    def finish_game(self):
        if self.gui:
            self.gui.questionWidget.setEnabled(False)
            self.gui.answerInput.setEnabled(False)
            self.gui.submitButton.setEnabled(False)
            self.gui.skipButton.setEnabled(False)
            self.gui.levelMenu.setEnabled(True)
            self.gui.subjectMenu.setEnabled(True)
            self.gui.startGameMenu.setEnabled(True)
            self.gui.seeScoresMenu.setEnabled(True)
            self.gui.endGameMenu.setEnabled(False)
            self.gui._stopTimer()

            player_name = self.gui.show_save_score_dialog()

            if player_name:
                print(f"Saving score for {player_name}: {self.current_points} points, at {self.current_difficulty} difficulty, in {self.selected_subjects}")
                # call score saving function here
            else:
                print("score not saved")
        
    def save_score(self, player_name):
        self.db.save_score(player_name, self.current_points, self.current_difficulty, self.selected_subjects)

