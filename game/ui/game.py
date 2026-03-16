from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..logic import QUESTIONS_PER_GAME, Question, QuestionGenerator, SessionScore

ANSWER_DELAY_MS = 1500

STYLE_DEFAULT = """
    QPushButton {
        background-color: #2d2d2d;
        color: #cccccc;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 14px;
        font-size: 13px;
        text-align: left;
    }
    QPushButton:hover:enabled { background-color: #3a3a3a; border-color: #4a9eff; }
"""

STYLE_CORRECT = """
    QPushButton {
        background-color: #1a472a;
        color: #ffffff;
        border: 1px solid #2ecc71;
        border-radius: 8px;
        padding: 14px;
        font-size: 13px;
        text-align: left;
    }
"""

STYLE_WRONG = """
    QPushButton {
        background-color: #4a1a1a;
        color: #ffffff;
        border: 1px solid #e74c3c;
        border-radius: 8px;
        padding: 14px;
        font-size: 13px;
        text-align: left;
    }
"""


class GameScreen(QWidget):
    quit_requested = pyqtSignal()
    game_over = pyqtSignal(int, int)  # (correct, total)

    def __init__(self, generator: QuestionGenerator):
        super().__init__()
        self._generator = generator
        self._score = SessionScore()
        self._current: Question | None = None
        self._build_ui()

    def start_session(self) -> None:
        self._score = SessionScore()
        self._next_question()

    def _build_ui(self) -> None:
        self.setStyleSheet("background-color: #1e1e1e;")

        root = QVBoxLayout(self)
        root.setContentsMargins(40, 24, 40, 24)
        root.setSpacing(0)

        # ── Top bar ──────────────────────────────────────────────────────────
        top_bar = QHBoxLayout()

        quit_btn = QPushButton("← Quit")
        quit_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #666666;
                border: none;
                font-size: 13px;
            }
            QPushButton:hover { color: #aaaaaa; }
        """)
        quit_btn.clicked.connect(self.quit_requested)

        self._score_label = QLabel(f"0 / {QUESTIONS_PER_GAME}")
        self._score_label.setFont(QFont("Helvetica", 13))
        self._score_label.setStyleSheet("color: #888888;")

        top_bar.addWidget(quit_btn)
        top_bar.addStretch()
        top_bar.addWidget(self._score_label)
        root.addLayout(top_bar)

        # ── Image area ───────────────────────────────────────────────────────
        root.addSpacing(16)
        image_container = QWidget()
        image_container.setStyleSheet("background-color: #2b2b2b; border-radius: 12px;")
        image_container.setFixedHeight(260)
        img_layout = QVBoxLayout(image_container)
        img_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._image_label = QLabel()
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label.setFixedSize(200, 200)
        img_layout.addWidget(self._image_label)

        root.addWidget(image_container)

        # ── Feedback label ───────────────────────────────────────────────────
        root.addSpacing(12)
        self._feedback_label = QLabel("")
        self._feedback_label.setFont(QFont("Helvetica", 13, QFont.Weight.Bold))
        self._feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._feedback_label.setFixedHeight(24)
        root.addWidget(self._feedback_label)

        # ── Answer buttons ───────────────────────────────────────────────────
        root.addSpacing(12)
        self._answer_btns: list[QPushButton] = []
        for i in range(4):
            btn = QPushButton()
            btn.setStyleSheet(STYLE_DEFAULT)
            btn.setMinimumHeight(56)
            btn.setFont(QFont("Helvetica", 13))
            btn.clicked.connect(lambda checked, idx=i: self._on_answer(idx))
            self._answer_btns.append(btn)
            root.addWidget(btn)
            if i < 3:
                root.addSpacing(8)

        root.addStretch()

    def _next_question(self) -> None:
        self._current = self._generator.next_question()
        self._feedback_label.setText("")
        self._feedback_label.setStyleSheet("")

        pixmap = QPixmap(str(self._current.icon.image_path))
        self._image_label.setPixmap(
            pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                          Qt.TransformationMode.SmoothTransformation)
        )

        for i, btn in enumerate(self._answer_btns):
            btn.setText(self._current.choices[i])
            btn.setStyleSheet(STYLE_DEFAULT)
            btn.setEnabled(True)

    def _on_answer(self, index: int) -> None:
        if self._current is None:
            return

        correct = index == self._current.correct_index
        self._score.record(correct)
        self._score_label.setText(str(self._score))

        for btn in self._answer_btns:
            btn.setEnabled(False)

        for i, btn in enumerate(self._answer_btns):
            if i == self._current.correct_index:
                btn.setStyleSheet(STYLE_CORRECT)
            elif i == index and not correct:
                btn.setStyleSheet(STYLE_WRONG)

        if correct:
            self._feedback_label.setText("Correct!")
            self._feedback_label.setStyleSheet("color: #2ecc71;")
        else:
            self._feedback_label.setText("Wrong")
            self._feedback_label.setStyleSheet("color: #e74c3c;")

        is_final = self._score.total >= QUESTIONS_PER_GAME
        next_fn = self._finish_game if is_final else self._next_question
        QTimer.singleShot(ANSWER_DELAY_MS, next_fn)

    def _finish_game(self) -> None:
        self.game_over.emit(self._score.correct, self._score.total)
