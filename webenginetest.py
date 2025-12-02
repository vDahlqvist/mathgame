from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import random

# Your question bank (simplified example)
QUESTIONS = {
    "algebra": {
        "easy": [
            {"question": r"Simplify: \frac{2x + 4}{2}", "answer": "x + 2"},
            {"question": r"Solve: 3x - 5 = 7", "answer": "x = 4"},
            {"question": r"Simplify: (x^2)(x^3)", "answer": "x^5"},
        ]
    }
}


class QuestionWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Math Game with LaTeX Display")

        # --- LAYOUT ---
        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- WEB ENGINE VIEW ---
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        # --- BUTTON ---
        btn = QPushButton("New Question")
        btn.clicked.connect(self.load_new_question)
        layout.addWidget(btn)

        # --- First question ---
        self.load_new_question()

    def load_new_question(self):
        """Picks a random question and displays it with MathJax."""
        q = random.choice(QUESTIONS["algebra"]["easy"])
        latex = q["question"]

        # Build HTML containing MathJax + your LaTeX
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
        <body style="font-size: 24px; padding: 20px;">
            <p><b>Question:</b></p>
            <p>\\({latex}\\)</p>
        </body>
        </html>
        """

        # Load HTML into the browser widget
        self.browser.setHtml(html)

        # MathJax kicks in automatically after loading


# --- APP EXECUTION ---
app = QApplication(sys.argv)
window = QuestionWindow()
window.show()
sys.exit(app.exec())
