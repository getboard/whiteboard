import context
import modules
from . import handlers
from modules.text.states import edit_text
from modules.text.states import change_text
from . import object_types


def create_states(ctx: context.Context):
    ctx.state_machine.add_state(edit_text.create_state(ctx.state_machine))
    ctx.state_machine.add_state(change_text.create_state(ctx.state_machine))


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler('ADD_TEXT', handlers.AddTextHandler)
    ctx.event_handlers.register_handler('EDIT_TEXT', handlers.EditTextHandler)
    ctx.event_handlers.register_handler('CHANGE_FONT_TEXT', handlers.ChangeFontTextHandler)
    ctx.event_handlers.register_handler('CHANGE_FONT_SIZE_TEXT', handlers.ChangeFontSizeTextHandler)


def register_object_types(ctx: context.Context):
    ctx.objects_storage.register_object_type('TEXT', object_types.TextObject)


@modules.modules.register_module('text')
def init_module(ctx: context.Context):
    create_states(ctx)
    register_handlers(ctx)
    register_object_types(ctx)
