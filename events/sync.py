import time
import os
from typing import List
import tkinter
from tkinter import ttk

import git

import context
import state_machine
import objects_storage

_SYNC_PERIOD_IN_SEC = 15
_MS_IN_SEC = 1000


def _last_sync_was_long_ago(ctx: context.Context) -> bool:
    cur_ts = time.time()
    last_sync_ts = ctx.events_history.get_last_sync_ts()
    return last_sync_ts is None or last_sync_ts + _SYNC_PERIOD_IN_SEC < cur_ts


def _is_sync_needed(ctx: context.Context) -> bool:
    if ctx.state_machine.get_cur_state_name() != state_machine.StateMachine.ROOT_STATE_NAME:
        ctx.logger.debug('State machine is not in the root state, skipping sync')
        return False
    if not _last_sync_was_long_ago(ctx):
        ctx.logger.debug('too soon to sync events')
        return False
    return True


def _prepare_for_applying(ctx: context.Context):
    # The order is crucial here
    ctx.pub_sub_broker.reset()
    ctx.objects_storage.reset()
    ctx.canvas.delete('all')
    ctx.state_machine.reset()


def sync(ctx: context.Context, apply_events=True, force=False):
    if not force and not _is_sync_needed(ctx):
        return

    ctx.events_history.sync(ctx)
    if apply_events:
        _prepare_for_applying(ctx)
        ctx.events_history.apply_all(ctx)


def sync_periodic(ctx: context.Context):
    sync(ctx, apply_events=True, force=False)
    ON_EVENT_SYNCER = 'OnEventSyncer'
    if ctx.objects_storage.get_opt_by_id(ON_EVENT_SYNCER) is None:
        ctx.objects_storage.register_object_type(ON_EVENT_SYNCER, _OnEventSyncer)
        ctx.objects_storage.create(ON_EVENT_SYNCER, obj_id=ON_EVENT_SYNCER)
    ctx.root.after(_SYNC_PERIOD_IN_SEC * _MS_IN_SEC, lambda ctx=ctx: sync_periodic(ctx))


class _OnEventSyncer(objects_storage.Object):
    def __init__(self, ctx: context.Context, id: str, **kwargs):
        super().__init__(ctx, id, **kwargs)
        ctx.pub_sub_broker.subscribe(
            state_machine.StateMachine.STATE_CHANGED_NOTIFICATION,
            state_machine.StateMachine.PUB_SUB_ID,
            self.id,
        )

    def get_notification(self, ctx: context.Context, _, event: str, **kwargs):
        if event != state_machine.StateMachine.STATE_CHANGED_NOTIFICATION:
            return
        if kwargs['state_changed_to'] != state_machine.StateMachine.ROOT_STATE_NAME:
            return
        sync(ctx, apply_events=True, force=False)


def init_sync(ctx: context.Context):
    ctx.root.after(_SYNC_PERIOD_IN_SEC * _MS_IN_SEC, lambda ctx=ctx: sync_periodic(ctx))


def _get_available_log_files(repo: git.Repo, path_to_repo: str) -> List[str]:
    repo.git.checkout('main')
    repo.git.reset('--hard', 'main')
    repo.remotes.origin.pull()

    res = []
    for filename in os.listdir(path_to_repo):
        if os.path.isfile(os.path.join(path_to_repo, filename)):
            res.append(filename)
    return res


def _create_new_board(
    filename_entry: ttk.Entry, listbox: tkinter.Listbox, repo: git.Repo, path_to_repo: str
):
    # TODO: better checks here + make it verbose
    filename = filename_entry.get()
    filename_entry.delete(0, tkinter.END)
    if not filename or not filename.isprintable():
        return
    for existing_filename in listbox.get(0, tkinter.END):
        if filename == existing_filename:
            return

    file = open(os.path.join(path_to_repo, filename), 'a')
    file.close()
    listbox.insert(tkinter.END, filename)


def _set_open_button_state_to_normal(open_button: ttk.Button):
    open_button['state'] = 'normal'


def pick_log_file(repo: git.Repo, path_to_repo: str):
    window = tkinter.Tk(className='Choose board')
    window.geometry('400x300')

    available_log_files = _get_available_log_files(repo, path_to_repo)
    log_files_listbox = tkinter.Listbox()
    log_files_listbox.grid(row=1, column=0, columnspan=2, sticky=tkinter.EW, padx=5, pady=5)
    for log_file in available_log_files:
        log_files_listbox.insert(tkinter.END, log_file)

    new_log_filename_entry = ttk.Entry()
    new_log_filename_entry.grid(column=0, row=0, padx=6, pady=6, sticky=tkinter.EW)
    ttk.Button(
        text='Создать новую доску',
        command=lambda filename_entry=new_log_filename_entry, files_listbox=log_files_listbox, repo=repo, path_to_repo=path_to_repo: _create_new_board(
            filename_entry, files_listbox, repo, path_to_repo
        ),
    ).grid(column=1, row=0, padx=6, pady=6)

    open_button = ttk.Button(
        text='Открыть выбранную доску', command=lambda window=window: window.quit()
    )
    open_button.grid(row=2, column=1, padx=5, pady=5)
    open_button['state'] = 'disabled'
    log_files_listbox.bind(
        '<<ListboxSelect>>',
        lambda _, open_button=open_button: _set_open_button_state_to_normal(open_button),
    )

    window.mainloop()
    selected_indx = log_files_listbox.curselection()
    log_filename = log_files_listbox.get(selected_indx)
    window.destroy()
    return log_filename
