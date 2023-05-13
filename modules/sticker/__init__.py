import context
import modules
from . import handlers
from modules.sticker.states import edit_sticker_text
from modules.sticker.states import change_sticker
from . import object_types


def create_states(ctx: context.Context):
    ctx.state_machine.add_state(edit_sticker_text.create_state(ctx.state_machine))
    ctx.state_machine.add_state(change_sticker.create_state(ctx.state_machine))


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler('ADD_STICKER', handlers.AddStickerHandler)
    ctx.event_handlers.register_handler('EDIT_STICKER', handlers.EditStickerHandler)


def register_object_types(ctx: context.Context):
    ctx.objects_storage.register_object_type('STICKER', object_types.StickerObject)


def register_module_menu(ctx: context.Context):
    STICKER_MODULE_NAME = 'sticker'
    ctx.menu.add_command_to_menu(STICKER_MODULE_NAME)


@modules.modules.register_module('sticker')
def init_module(ctx: context.Context):
    create_states(ctx)
    register_handlers(ctx)
    register_object_types(ctx)
    register_module_menu(ctx)
