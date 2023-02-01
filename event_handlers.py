import typing


class EventHandler:
    @classmethod
    def apply(cls, ctx, **kwargs):
        raise NotImplementedError("it's an abstract class")


class EventHandlers:
    handlers: typing.Dict[str, typing.Type[EventHandler]]

    def __init__(self):
        self.handlers = dict()

    def register_handler(self, handler_name: str, handler_type: typing.Type[EventHandler]):
        self.handlers[handler_name] = handler_type

    def get_handler(self, kind: str) -> typing.Type[EventHandler]:
        return self.handlers[kind]
