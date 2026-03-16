from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

BTN_PRIMARY = """
    QPushButton {
        background-color: #4a9eff;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 14px;
    }
    QPushButton:hover { background-color: #3a8eef; }
    QPushButton:pressed { background-color: #2a7edf; }
"""

BTN_SECONDARY = """
    QPushButton {
        background-color: #2d2d2d;
        color: #aaaaaa;
        border: 1px solid #444;
        border-radius: 8px;
        font-size: 14px;
    }
    QPushButton:hover { background-color: #3a3a3a; color: #cccccc; }
"""


class EndScreen(QWidget):
    replay_requested = pyqtSignal()
    quit_requested = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._build_ui()

    def show_result(self, correct: int, total: int, top_scores: list[int]) -> None:
        pct = round(correct / total * 100) if total else 0
        self._pct_label.setText(f"{pct}%")
        self._detail_label.setText(f"{correct} correct out of {total}")

        # Colour-code the percentage
        if pct >= 80:
            colour = "#2ecc71"
        elif pct >= 50:
            colour = "#f39c12"
        else:
            colour = "#e74c3c"
        self._pct_label.setStyleSheet(f"color: {colour};")

        # Rebuild the leaderboard rows
        for i, label in enumerate(self._score_rows):
            if i < len(top_scores):
                marker = " ◀ this game" if top_scores[i] == pct and not self._marked else ""
                if marker:
                    self._marked = True
                label.setText(f"#{i + 1}   {top_scores[i]}%{marker}")
                label.setVisible(True)
            else:
                label.setVisible(False)

        self._no_scores_label.setVisible(len(top_scores) == 0)
        self._marked = False  # reset for next call

    def _build_ui(self) -> None:
        self._marked = False
        self.setStyleSheet("background-color: #1e1e1e;")

        root = QVBoxLayout(self)
        root.setContentsMargins(60, 40, 60, 40)
        root.setSpacing(0)
        root.addStretch()

        # ── Game over heading ────────────────────────────────────────────────
        heading = QLabel("Game Over")
        heading.setFont(QFont("Helvetica", 22, QFont.Weight.Bold))
        heading.setStyleSheet("color: #888888;")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(heading)

        root.addSpacing(24)

        # ── Big percentage ───────────────────────────────────────────────────
        self._pct_label = QLabel("0%")
        self._pct_label.setFont(QFont("Helvetica", 72, QFont.Weight.Bold))
        self._pct_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self._pct_label)

        self._detail_label = QLabel("")
        self._detail_label.setFont(QFont("Helvetica", 14))
        self._detail_label.setStyleSheet("color: #888888;")
        self._detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self._detail_label)

        root.addSpacing(36)

        # ── Leaderboard ──────────────────────────────────────────────────────
        board_heading = QLabel("All-Time Top 5")
        board_heading.setFont(QFont("Helvetica", 13, QFont.Weight.Bold))
        board_heading.setStyleSheet("color: #555555; letter-spacing: 1px;")
        board_heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(board_heading)

        root.addSpacing(10)

        self._score_rows: list[QLabel] = []
        for _ in range(5):
            row = QLabel()
            row.setFont(QFont("Helvetica", 14))
            row.setStyleSheet("color: #cccccc;")
            row.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row.setVisible(False)
            self._score_rows.append(row)
            root.addWidget(row)
            root.addSpacing(4)

        self._no_scores_label = QLabel("No scores yet")
        self._no_scores_label.setFont(QFont("Helvetica", 13))
        self._no_scores_label.setStyleSheet("color: #444444;")
        self._no_scores_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._no_scores_label.setVisible(True)
        root.addWidget(self._no_scores_label)

        root.addSpacing(40)

        # ── Buttons ──────────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(16)

        replay_btn = QPushButton("Play Again")
        replay_btn.setFixedHeight(48)
        replay_btn.setStyleSheet(BTN_PRIMARY)
        replay_btn.clicked.connect(self.replay_requested)

        quit_btn = QPushButton("Quit")
        quit_btn.setFixedHeight(48)
        quit_btn.setStyleSheet(BTN_SECONDARY)
        quit_btn.clicked.connect(self.quit_requested)

        btn_row.addWidget(replay_btn)
        btn_row.addWidget(quit_btn)
        root.addLayout(btn_row)

        root.addStretch()
