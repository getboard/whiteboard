import context
import modules
from . import handlers


OBJECT_DESTROYING_MODULE_NAME = 'object_destroying'
DESTROY_OBJECT_EVENT_TYPE = 'DESTROY_OBJECT'


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler(DESTROY_OBJECT_EVENT_TYPE, handlers.DestroyObjectHandler)


@modules.modules.register_module(OBJECT_DESTROYING_MODULE_NAME)
def init_module(ctx: context.Context):
    register_handlers(ctx)
