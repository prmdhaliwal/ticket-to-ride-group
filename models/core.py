from enum import Enum
from abc import ABC, abstractmethod

class CardColor(Enum):
    """Specific vehicle card colors for the London edition."""
    BLUE = "Blue"
    BLACK = "Black"
    PINK = "Pink"
    YELLOW = "Yellow"
    ORANGE = "Orange"
    WHITE = "White"
    LOCOMOTIVE = "Multi/Wild"

class Observer(ABC):
    """Interface for the Observer pattern (Tkinter UI will implement this)."""
    @abstractmethod
    def update(self):
        pass

class Subject(ABC):
    """Base class for objects that need to be observed."""
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def notify(self):
        for observer in self._observers:
            observer.update()