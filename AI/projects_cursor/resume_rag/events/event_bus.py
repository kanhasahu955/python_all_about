from collections import defaultdict

class EventBus:

    def __init__(self):
        self.handlers = defaultdict(list)

    def subscribe(
        self,
        event_name,
        callback
    ):
        self.handlers[event_name].append(
            callback
        )

    def publish(
        self,
        event_name,
        payload
    ):

        for callback in self.handlers[event_name]:

            callback(payload)

event_bus = EventBus()