from __future__ import annotations
import context
import modules
from . import handlers
from . import consts


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler(
        consts.DESTROY_OBJECT_EVENT_TYPE, handlers.DestroyObjectHandler
    )


@modules.modules.register_module(consts.OBJECT_DESTROYING_MODULE_NAME)
def init_module(ctx: context.Context):
    register_handlers(ctx)
