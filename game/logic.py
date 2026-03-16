import json
import random
from dataclasses import dataclass
from pathlib import Path

from .data import GameData, Icon

QUESTIONS_PER_GAME = 20


@dataclass
class Question:
    icon: Icon
    choices: list[str]
    correct_index: int


class QuestionGenerator:
    def __init__(self, game_data: GameData):
        self._data = game_data

    def next_question(self) -> Question:
        icon = random.choice(self._data.icons)
        distractors = random.sample(
            [i for i in self._data.icons if i.title != icon.title],
            3,
        )
        choices = [icon.title] + [d.title for d in distractors]
        random.shuffle(choices)
        correct_index = choices.index(icon.title)
        return Question(icon=icon, choices=choices, correct_index=correct_index)


@dataclass
class SessionScore:
    correct: int = 0
    total: int = 0

    def record(self, was_correct: bool) -> None:
        self.total += 1
        if was_correct:
            self.correct += 1

    @property
    def percentage(self) -> float:
        if self.total == 0:
            return 0.0
        return self.correct / self.total * 100

    def __str__(self) -> str:
        return f"{self.correct} / {QUESTIONS_PER_GAME}"


class ScoreStore:
    _PATH = Path.home() / ".iso_icon_challenge_scores.json"
    MAX_SCORES = 5

    def __init__(self) -> None:
        self._scores: list[int] = self._load()

    def _load(self) -> list[int]:
        try:
            data = json.loads(self._PATH.read_text())
            return sorted(data, reverse=True)[: self.MAX_SCORES]
        except Exception:
            return []

    def add(self, percentage: float) -> None:
        score = round(percentage)
        self._scores = sorted(self._scores + [score], reverse=True)[: self.MAX_SCORES]
        self._PATH.write_text(json.dumps(self._scores))

    @property
    def top_scores(self) -> list[int]:
        return list(self._scores)
