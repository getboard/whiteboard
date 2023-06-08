import logging
import tkinter
from tkinter import ttk

import git

import context
import events.event_handlers
import events.events_history
import events.sync
import objects_storage
import menu
import pub_sub
from state_machine import StateMachine
from utils import make_logger

import modules.modules
import modules.text
import modules.sticker
import modules.move
import modules.zooming
import modules.drag_board
import modules.connector
import modules.submenu
import modules.object_destroying
import modules.group


def _create_context(root: tkinter.Tk, logger: logging.Logger, repo: git.Repo, path_to_repo: str, log_filename: str) -> context.Context:
    ctx = context.Context()

    ctx.root = root

    ctx.logger = logger

    canvas = tkinter.Canvas(root, width=700, height=500, bg='white')
    canvas.pack(side='left', fill='both', expand=False)
    ctx.canvas = canvas

    ctx.events_history = events.events_history.EventsHistory(repo, path_to_repo, log_filename)
    ctx.event_handlers = events.event_handlers.EventHandlers()
    ctx.objects_storage = objects_storage.ObjectsStorage(ctx)

    ctx.pub_sub_broker = pub_sub.Broker()

    ctx.state_machine = StateMachine(ctx)
    ctx.property_bar = ttk.Frame(root)
    ctx.property_bar.pack(fill='both', expand=True, padx=10, pady=10)
    ctx.menu = menu.Menu(root)
    return ctx


def main():
    # TODO: take the path from somewhere
    logger = make_logger.make_logger()
    
    PATH_TO_REPO = './sync_repo'
    repo = git.Repo(PATH_TO_REPO)
    
    picked_log_filename = events.sync.pick_log_file(repo, PATH_TO_REPO)
    if picked_log_filename is None:
        return

    root_window = tkinter.Tk(className='Whiteboard')
    root_window.geometry('870x600')

    ctx = _create_context(root_window, logger, repo, PATH_TO_REPO, picked_log_filename)
    ctx.canvas.focus_set()
    modules.modules.init_modules(ctx)

    events.sync.sync(ctx, apply_events=True, force=True)
    events.sync.init_sync(ctx)
    root_window.mainloop()
    events.sync.sync(ctx, apply_events=False, force=True)


if __name__ == '__main__':
    main()
