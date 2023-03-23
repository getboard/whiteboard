import logging
import tkinter

import context
import events_history
import modules.modules
import objects_storage
import event_handlers
from state_machine import StateMachine

import modules.text
import modules.move
import modules.zooming
import modules.drag_board


def create_context(root: tkinter.Tk) -> context.Context:
    logger = logging.Logger("global_logger")
    canvas = tkinter.Canvas(root, width=700, height=500, bg='white')
    canvas.place(x=50, y=50)
    state_machine = StateMachine(canvas)
    return context.Context(
        events_history.EventsHistory(),
        event_handlers.EventHandlers(),
        objects_storage.ObjectsStorage(),
        logger,
        canvas,
        state_machine,
    )


def main(log_file: str):
    root_window = tkinter.Tk(className="Whiteboard")
    root_window.geometry("800x600")

    ctx = create_context(root_window)
    modules.modules.init_modules(ctx)

    ctx.events_history.load_from_file_and_apply(ctx, log_file)

    root_window.mainloop()

    ctx.events_history.save_to_file(log_file)


if __name__ == "__main__":
    # FIX: throws exception if file doesn't exist
    main('event_log.txt')
