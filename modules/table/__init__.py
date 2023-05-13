import modules
import context

from . import handlers

from modules.table.object_types import Table


def bind_on_events(ctx: context.Context, table: Table):
    ctx.canvas.bind(
        '<Control-Button-3>', lambda event: handlers.create_table(ctx, table, event)
    )  # Win + MacOS
    # ctx.canvas.bind(
    #     '<Return>', lambda event: handlers.check(ctx, table, event)
    # )

    # ctx.canvas.bind('<Control-Button-5>', lambda event: handlers.zoom_on_wheel(ctx, event))  # Linux
    # ctx.canvas.bind('<Control-Button-4>', lambda event: handlers.zoom_on_wheel(ctx, event))  # Linux


@modules.modules.register_module('table')
def init_module(ctx: context.Context):
    TABLE = Table(ctx)
    # TABLE.add_card((12, "amina", "red", "none"))
    # TABLE.add_card((13, "adiya", "pink", "koten"))
    bind_on_events(ctx, TABLE)
