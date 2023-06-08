from __future__ import annotations
from typing import Dict, List, Optional
import os
import time
import json
import logging

import git
import git.exc

import context

_KIND_FIELD_NAME = 'kind'
_SYNC_PERIOD_IN_SEC = 5


class EventInfo:
    kind: str
    kwargs: dict

    @classmethod
    def from_payload(cls, payload: dict) -> EventInfo:
        event_info = EventInfo()
        event_info.kind = payload.pop(_KIND_FIELD_NAME)
        event_info.kwargs = payload
        return event_info

    def get_payload(self):
        payload = {_KIND_FIELD_NAME: self.kind}
        payload.update(self.kwargs)
        return payload


class EventsHistory:
    _local_events: list[EventInfo]

    _repo: git.Repo
    _path_to_repo: str
    _log_filepath_relative_to_the_repo: str
    _last_sync_object_versions: Dict[str, int]   # obj_id -> version
    _last_sync_ts = Optional[float]

    def __init__(self, repo: git.Repo, path_to_repo: str, log_filepath_relative_to_the_repo: str):
        self._local_events = []
        self._repo = repo
        self._path_to_repo = path_to_repo
        self._log_filepath_relative_to_the_repo = log_filepath_relative_to_the_repo
        self._last_sync_object_versions = {}
        self._last_sync_ts = None

    def add_event(self, kind: str, **event_kwargs):
        event_info = EventInfo()
        event_info.kind = kind
        event_info.kwargs = event_kwargs
        self._local_events.append(event_info)

    def _pull_main(self):
        self._repo.git.checkout('main')
        self._repo.git.reset('--hard', 'main')
        self._repo.remotes.origin.pull()

    def _push_main(self):
        self._repo.index.add([self._log_filepath_relative_to_the_repo])
        self._repo.index.commit('New events on the way to the repo 🚂🚂🚂')
        push_info_list = self._repo.remotes.origin.push()
        push_info_list.raise_if_error()

    def _revert_last_local_commit(self):
        self._repo.git.reset('HEAD~1', '--hard')

    def _try_to_merge(self, logger: logging.Logger):
        cur_sync_object_versions = {}
        path = self._get_path_to_log_file()
        with open(path, 'r') as file:
            for line in file:
                payload = json.loads(line)
                event_info = EventInfo.from_payload(payload)
                obj_id = event_info.kwargs.get('obj_id', None)
                if not obj_id:
                    logger.warn('No obj_id for event (source=repo), skipping the event')
                    continue
                cur_sync_object_versions[obj_id] = cur_sync_object_versions.get(obj_id, 0) + 1

        events_to_append: List[EventInfo] = []
        for event in self._local_events:
            obj_id = event.kwargs.get('obj_id', None)
            if not obj_id:
                logger.warn('No obj_id for event (source=local), skipping the event')
                continue

            last_sync_obj_ver = self._last_sync_object_versions.get(obj_id, 0)
            cur_sync_obj_ver = cur_sync_object_versions.get(obj_id, 0)
            if last_sync_obj_ver < cur_sync_obj_ver:
                logger.debug(
                    f'obj_ver for obj_id={obj_id} changed since last sync (last_ver={last_sync_obj_ver}, cur_ver={cur_sync_obj_ver}), skipping an event'
                )
                continue
            events_to_append.append(event)

        if events_to_append:
            with open(path, 'a') as file:
                for event in events_to_append:
                    file.write(f'{json.dumps(event.get_payload())}\n')

                    obj_id = event.kwargs.get('obj_id')
                    cur_sync_object_versions[obj_id] = cur_sync_object_versions.get(obj_id, 0) + 1

            try:
                self._push_main()
            except git.exc.GitCommandError as ex:
                self._revert_last_local_commit()
                raise

        self._last_sync_object_versions = cur_sync_object_versions

    def _get_path_to_log_file(self) -> str:
        return os.path.join(self._path_to_repo, self._log_filepath_relative_to_the_repo)

    def sync(self, ctx: context.Context):
        ctx.logger.debug('Syncing event log')
        while True:
            try:
                self._pull_main()
                self._try_to_merge(ctx.logger)
                self._last_sync_ts = time.time()
                break
            except git.exc.GitCommandError as ex:
                print(ex)
                ctx.logger.debug('Conflict on push, trying to sync again')

        self._local_events = []

    def apply_all(self, ctx: context.Context):
        path = os.path.join(self._path_to_repo, self._log_filepath_relative_to_the_repo)
        if not os.path.exists(path) or not os.path.isfile(path):
            return

        with open(path, 'r') as file:
            for line in file:
                payload = json.loads(line)
                event_info = EventInfo.from_payload(payload)
                handler = ctx.event_handlers.get_handler(event_info.kind)
                handler.apply(ctx, **event_info.kwargs)

    def get_last_sync_ts(self) -> Optional[float]:
        return self._last_sync_ts
