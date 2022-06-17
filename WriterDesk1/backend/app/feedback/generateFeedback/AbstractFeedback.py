from abc import ABC, abstractmethod

class AbstractFeedback(ABC):

    @abstractmethod
    def genFeedback(self, text, references=''):
        pass