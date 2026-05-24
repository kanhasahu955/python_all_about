from abc import ABC, abstractmethod

from app.services.agent_events import agent_events


class BaseAgent(ABC):
    agent_name: str = ""

    def _start(self, state: dict) -> None:
        document_id = state.get("document_id")
        if document_id and self.agent_name:
            agent_events.publish_agent_started(document_id, self.agent_name)

    @abstractmethod
    def execute(self, state):
        pass
