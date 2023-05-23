import logging
import tkinter

import context
import events_history
import objects_storage
import event_handlers
import menu
import pub_sub
from state_machine import StateMachine
from table import Table

import modules.modules
import modules.text
import modules.sticker
import modules.move
import modules.zooming
import modules.drag_board
import modules.submenu


def create_context(root: tkinter.Tk) -> context.Context:
    canvas_width = 700
    common_height = root.winfo_height() - 10
    table_width = root.winfo_width() - canvas_width
    logger = logging.Logger('global_logger')

    canvas = tkinter.Canvas(root, width=canvas_width, height=common_height, bg='white')
    canvas.pack(side="left", fill="both", expand=False)
    ctx = context.Context()
    ctx.events_history = events_history.EventsHistory()
    ctx.event_handlers = event_handlers.EventHandlers()
    ctx.objects_storage = objects_storage.ObjectsStorage(ctx)
    ctx.logger = logger
    ctx.canvas = canvas
    ctx.menu = menu.Menu(root)
    ctx.state_machine = StateMachine(ctx)
    ctx.table = Table(root, ctx, table_width, common_height)
    ctx.pub_sub_broker = pub_sub.Broker()
    return ctx


def main(log_file: str):
    root_window = tkinter.Tk(className='Whiteboard')
    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()
    panel_height = 75
    root_window.geometry(f'{screen_width}x{screen_height - panel_height}+0+0')
    root_window.wm_state('zoomed')

    ctx = create_context(root_window)
    ctx.canvas.focus_set()
    modules.modules.init_modules(ctx)

    ctx.events_history.load_from_file_and_apply(ctx, log_file)

    root_window.mainloop()

    ctx.events_history.save_to_file(log_file)


if __name__ == '__main__':
    main('event_log.txt')
