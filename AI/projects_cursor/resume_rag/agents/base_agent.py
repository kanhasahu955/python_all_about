from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    async def execute(self, state):
        pass