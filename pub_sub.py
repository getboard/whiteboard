from __future__ import annotations
from typing import Dict, List

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

    def lock(self):
        self._is_locked = True

    def unlock(self):
        self._is_locked = False


class Broker:
    subscribers: Dict[str, Dict[str, List[str]]]

    def __init__(self):
        self.subscribers = dict()

    def add_publisher_event(self, publisher_id: str, event: str):
        if publisher_id not in self.subscribers:
            return
        self.subscribers[publisher_id][event] = []

    def add_publisher(self, publisher_id):
        self.subscribers[publisher_id] = dict()

    def publish(self, ctx: context.Context, publisher_id: str, event, **kwargs):
        if publisher_id in self.subscribers and event in self.subscribers[publisher_id]:
            for subscriber_id in self.subscribers[publisher_id][event]:
                subscriber: Subscriber = ctx.objects_storage.get_by_id(subscriber_id)
                if not subscriber.is_locked:
                    subscriber.get_notification(ctx, publisher_id, event, **kwargs)

    def subscribe(self, event: str, publisher_id: str, subscriber_id):
        if publisher_id not in self.subscribers:
            return
        if event not in self.subscribers[publisher_id]:
            return
        self.subscribers[publisher_id][event].append(subscriber_id)

    def unsubscribe(self, event: str, publisher_id: str, subscriber_id: str):
        if publisher_id in self.subscribers and event in self.subscribers[publisher_id]:
            if subscriber_id in self.subscribers[publisher_id][event]:
                self.subscribers[publisher_id][event].remove(subscriber_id)
