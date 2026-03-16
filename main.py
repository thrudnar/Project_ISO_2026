import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from game.data import GameData
from game.logic import QuestionGenerator, ScoreStore
from game.ui.end import EndScreen
from game.ui.game import GameScreen
from game.ui.start import StartScreen


class MainWindow(QMainWindow):
    def __init__(self, game_data: GameData):
        super().__init__()
        self.setWindowTitle("ISO Icon Challenge")
        self.setMinimumSize(640, 700)

        generator = QuestionGenerator(game_data)
        self._scores = ScoreStore()

        self._stack = QStackedWidget()
        self._start_screen = StartScreen(icon_count=len(game_data))
        self._game_screen = GameScreen(generator=generator)
        self._end_screen = EndScreen()

        self._stack.addWidget(self._start_screen)
        self._stack.addWidget(self._game_screen)
        self._stack.addWidget(self._end_screen)
        self.setCentralWidget(self._stack)

        self._start_screen.start_requested.connect(self._start_game)
        self._game_screen.quit_requested.connect(self._show_start)
        self._game_screen.game_over.connect(self._on_game_over)
        self._end_screen.replay_requested.connect(self._start_game)
        self._end_screen.quit_requested.connect(self._show_start)

    def _start_game(self) -> None:
        self._game_screen.start_session()
        self._stack.setCurrentWidget(self._game_screen)

    def _on_game_over(self, correct: int, total: int) -> None:
        self._scores.add(correct / total * 100)
        self._end_screen.show_result(correct, total, self._scores.top_scores)
        self._stack.setCurrentWidget(self._end_screen)

    def _show_start(self) -> None:
        self._stack.setCurrentWidget(self._start_screen)


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    print("Loading icon library…")
    game_data = GameData()
    print(f"Loaded {len(game_data):,} icons.")

    window = MainWindow(game_data)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
