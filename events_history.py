from __future__ import annotations
import os
import json

import context


__KIND_FIELD_NAME = 'kind'


class EventInfo:
    kind: str
    kwargs: dict

    @classmethod
    def from_payload(cls, payload: dict) -> EventInfo:
        event_info = EventInfo()
        event_info.kind = payload.pop(__KIND_FIELD_NAME)
        event_info.kwargs = payload
        return event_info

    def get_payload(self):
        payload = {__KIND_FIELD_NAME: self.kind}
        payload.update(self.kwargs)
        return payload


class EventsHistory:
    _events: list[EventInfo]

    def __init__(self):
        self._events = []

    def add_event(self, kind: str, **event_kwargs):
        event_info = EventInfo()
        event_info.kind = kind
        event_info.kwargs = event_kwargs
        self._events.append(event_info)

    def save_to_file(self, path: str):
        with open(path, 'w') as file:
            payloads = []
            for event in self._events:
                payloads.append(event.get_payload())
            json.dump(payloads, file, ensure_ascii=False, indent=None)

    def load_from_file_and_apply(self, ctx: context.Context, path: str):
        if not os.path.exists(path) or not os.path.isfile(path):
            return

        with open(path, 'r') as file:
            event_payloads = json.load(file)
            for payload in event_payloads:
                event_info = EventInfo.from_payload(payload)
                self._events.append(event_info)
                handler = ctx.event_handlers.get_handler(event_info.kind)
                handler.apply(ctx, **event_info.kwargs)
