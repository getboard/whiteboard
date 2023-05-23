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

def create_context(root: tkinter.Tk) -> context.Context:
    logger = logging.Logger('global_logger', level=logging.DEBUG)
    canvas = tkinter.Canvas(root, width=700, height=500, bg='white')
    canvas.pack(side='left', fill='both', expand=False)
    ctx = context.Context()
    # TODO: take the path from somewhere
    ctx.events_history = events.events_history.EventsHistory("./test_repo", "main_event_log.json")
    ctx.event_handlers = events.event_handlers.EventHandlers()
    ctx.objects_storage = objects_storage.ObjectsStorage(ctx)
    ctx.logger = logger
    ctx.canvas = canvas
    ctx.state_machine = StateMachine(ctx)
    ctx.property_bar = ttk.Frame(root)
    ctx.property_bar.pack(fill='both', expand=True, padx=10, pady=10)
    ctx.menu = menu.Menu(root)
    ctx.pub_sub_broker = pub_sub.Broker()

    button = tkinter.Button(root, text='Sync', command=lambda ctx=ctx: events.sync.sync(ctx))
    button.pack(expand=False)
    return ctx


def main():
    root_window = tkinter.Tk(className='Whiteboard')
    root_window.geometry('870x600')

    ctx = create_context(root_window)
    ctx.canvas.focus_set()
    modules.modules.init_modules(ctx)

    events.sync.sync(ctx)
    root_window.mainloop()
    events.sync.sync(ctx, apply_events=False)


if __name__ == '__main__':
    main()
