from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class StartScreen(QWidget):
    start_requested = pyqtSignal()

    def __init__(self, icon_count: int):
        super().__init__()
        self._build_ui(icon_count)

    def _build_ui(self, icon_count: int) -> None:
        self.setStyleSheet("background-color: #1e1e1e;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("ISO Icon Challenge")
        title.setFont(QFont("Helvetica", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Match the icon to its official name")
        subtitle.setFont(QFont("Helvetica", 14))
        subtitle.setStyleSheet("color: #aaaaaa;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        count_label = QLabel(f"{icon_count:,} icons available")
        count_label.setFont(QFont("Helvetica", 12))
        count_label.setStyleSheet("color: #666666;")
        count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_btn = QPushButton("Start Game")
        start_btn.setFixedSize(200, 50)
        start_btn.setFont(QFont("Helvetica", 14))
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #3a8eef; }
            QPushButton:pressed { background-color: #2a7edf; }
        """)
        start_btn.clicked.connect(self.start_requested)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(count_label)
        layout.addSpacing(20)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
