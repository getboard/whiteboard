from __future__ import annotations
import time
import os

import context


class EventInfo:
    timestamp: int
    kind: str
    kwargs: dict

    @classmethod
    def parse(cls, raw: str):
        kwargs = {}
        for raw_pair in raw.split(','):
            key, value = raw_pair.split('=')
            kwargs[key] = value

        event_info = EventInfo()
        event_info.timestamp = int(kwargs.pop('timestamp'))
        event_info.kind = kwargs.pop('kind')
        event_info.kwargs = kwargs
        return event_info

    def serialize(self) -> str:
        res = f'timestamp={self.timestamp},kind={self.kind}'
        if self.kwargs:
            res += ',' + ','.join([f'{key}={value}' for key, value in self.kwargs.items()])
        return res


class EventsHistory:
    _events: list[EventInfo]

    def __init__(self):
        self._events = []

    def add_event(self, kind: str, **event_kwargs):
        event_info = EventInfo()
        event_info.timestamp = int(time.time())
        event_info.kind = kind
        event_info.kwargs = event_kwargs
        self._events.append(event_info)

    def save_to_file(self, path: str):
        with open(path, 'w') as file:
            for event in self._events:
                file.write(event.serialize() + '\n')

    def load_from_file_and_apply(self, ctx: context.Context, path: str):
        if not os.path.exists(path) or not os.path.isfile(path):
            return
        with open(path, 'r') as file:
            for line in file:
                event_info = EventInfo.parse(line.strip())
                self._events.append(event_info)
                handler = ctx.event_handlers.get_handler(event_info.kind)
                handler.apply(ctx, **event_info.kwargs)
