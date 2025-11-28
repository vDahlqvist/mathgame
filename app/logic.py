class GameManager:
    def __init__(self):
        pass

    def start_game(self):
        print("Game started")
        self._startTimer()

    def next_question(self):
        pass

    def check_answer(self, answer):
        print(f"Checking answer: {answer}")



    def _startTimer(self):
        """Start the question timer."""
        self.time_elapsed = 0  # Reset to 0
        self.timerWidget.setText(f"Time: {self.time_elapsed}s")
        self.timer.start(1000)  # Timer ticks every second (1000ms)
