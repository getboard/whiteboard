from __future__ import annotations
from typing import Dict, List, Optional

import context


class Subscriber:
    id: str
    _is_locked: bool

    def __init__(self, id: str):
        self.id = id
        self._is_locked = False

    def get_notification(self, ctx: context.Context, publisher_id: str, event: str, **kwargs):
        pass

    @property
    def is_locked(self):
        return self._is_locked

    def lock_notifications(self):
        self._is_locked = True

    def unlock_notifications(self):
        self._is_locked = False


class Broker:
    _subscribers: Dict[str, Dict[str, List[str]]]

    def __init__(self):
        self._subscribers = {}

    def add_publisher_event(self, publisher_id: str, event: str):
        if publisher_id not in self._subscribers:
            # TODO: может тут лог добавить?
            return
        self._subscribers[publisher_id][event] = []

    def add_publisher(self, publisher_id):
        self._subscribers[publisher_id] = {}

    def remove_publisher(self, publisher_id):
        if publisher_id in self.subscribers:
            self.subscribers.pop(publisher_id)

    def publish(self, ctx: context.Context, publisher_id: str, event, **kwargs):
        if publisher_id in self._subscribers and event in self._subscribers[publisher_id]:
            for subscriber_id in self._subscribers[publisher_id][event]:
                subscriber: Optional[Subscriber] = ctx.objects_storage.get_opt_by_id(subscriber_id)
                if subscriber is not None and not subscriber.is_locked:
                    subscriber.get_notification(ctx, publisher_id, event, **kwargs)

    def subscribe(self, event: str, publisher_id: str, subscriber_id: str):
        if publisher_id not in self._subscribers:
            # TODO: может тут лог добавить?
            return
        if event not in self._subscribers[publisher_id]:
            # TODO: может тут лог добавить?
            return
        self._subscribers[publisher_id][event].append(subscriber_id)

    def unsubscribe(self, event: str, publisher_id: str, subscriber_id: str):
        if publisher_id in self._subscribers and event in self._subscribers[publisher_id]:
            if subscriber_id in self._subscribers[publisher_id][event]:
                self._subscribers[publisher_id][event].remove(subscriber_id)

    def reset(self):
        self._subscribers.clear()
