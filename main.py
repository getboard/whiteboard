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

import modules.modules
import modules.text
import modules.sticker
import modules.move
import modules.zooming
import modules.drag_board
import modules.submenu
import modules.object_destroying
import modules.group


def _make_logger() -> logging.Logger:
    logger = logging.Logger('global_logger')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s -  %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def _create_context(root: tkinter.Tk, repo: git.Repo, path_to_repo: str) -> context.Context:
    ctx = context.Context()

    ctx.root = root

    ctx.logger = _make_logger()

    canvas = tkinter.Canvas(root, width=700, height=500, bg='white')
    canvas.pack(side='left', fill='both', expand=False)
    ctx.canvas = canvas

    ctx.events_history = events.events_history.EventsHistory(repo, path_to_repo, 'aboba.json')
    ctx.event_handlers = events.event_handlers.EventHandlers()
    ctx.objects_storage = objects_storage.ObjectsStorage(ctx)

    ctx.pub_sub_broker = pub_sub.Broker()

    ctx.state_machine = StateMachine(ctx)
    ctx.property_bar = ttk.Frame(root)
    ctx.property_bar.pack(fill='both', expand=True, padx=10, pady=10)
    ctx.menu = menu.Menu(root)
    return ctx


def main():
    root_window = tkinter.Tk(className='Whiteboard')
    root_window.geometry('870x600')

    # TODO: take the path from somewhere
    PATH_TO_REPO = './sync_repo'
    repo = git.Repo(PATH_TO_REPO)

    # TODO:
    #   1) pull from repo
    #   2) show file picker
    #   3) pick file
    #   4) init ctx
    #   5) first sync
    #   6) init sync
    #   7) root mainloop
    #   8) final sync

    ctx = _create_context(root_window, repo, PATH_TO_REPO)
    ctx.canvas.focus_set()
    modules.modules.init_modules(ctx)

    events.sync.sync(ctx, apply_events=True, force=True)
    events.sync.init_sync(ctx)
    root_window.mainloop()
    events.sync.sync(ctx, apply_events=False, force=True)


if __name__ == '__main__':
    main()
