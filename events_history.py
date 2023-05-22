from __future__ import annotations
import os
import json

import git

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
    _local_events: list[EventInfo]

    _repo: git.Repo
    _filepath: str

    def __init__(self, path_to_repo: str, log_filepath: str):
        self._local_events = []
        self._repo = git.Repo(path_to_repo)
        self._filepath = log_filepath

    def add_event(self, kind: str, **event_kwargs):
        event_info = EventInfo()
        event_info.kind = kind
        event_info.kwargs = event_kwargs
        self._local_events.append(event_info)

    def _pull_main(self):
        self._repo.git.checkout('main')
        self._repo.git.reset('--hard', 'main')
        self._repo.remotes.origin.pull()

    def sync(self, ctx: context.Context):
        fetch_only = not self._local_events
        if fetch_only:
            ctx.logger.debug('No new local events, no push needed')
        
        self._pull_main()
        if fetch_only:
            self._apply_from_file(ctx)
        # TODO

    def _save_to_file(self, path: str):
        with open(path, 'w') as file:
            payloads = []
            for event in self._local_events:
                payloads.append(event.get_payload())
            json.dump(payloads, file, ensure_ascii=False, indent=None)

    def _apply_from_file(self, ctx: context.Context):
        if not os.path.exists(self._filepath) or not os.path.isfile(self._filepath):
            return

        with open(self._filepath, 'r') as file:
            event_payloads = json.load(file)
            for payload in event_payloads:
                event_info = EventInfo.from_payload(payload)
                handler = ctx.event_handlers.get_handler(event_info.kind)
                handler.apply(ctx, **event_info.kwargs)
