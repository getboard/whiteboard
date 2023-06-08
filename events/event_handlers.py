from typing import Type
from typing import Dict


class EventHandler:
    @classmethod
    def apply(cls, ctx, **kwargs):
        raise NotImplementedError("it's an abstract class")


class EventHandlers:
    handlers: Dict[str, Type[EventHandler]]

    def __init__(self):
        self.handlers = {}

    def register_handler(self, handler_name: str, handler_type: Type[EventHandler]):
        self.handlers[handler_name] = handler_type

    def get_handler(self, kind: str) -> Type[EventHandler]:
        return self.handlers[kind]
