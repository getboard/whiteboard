import context
import modules
from . import handlers
from modules.sticker.states import create_sticker
from modules.sticker.states import edit_sticker
from . import object_types
from .consts import STICKER_MENU_ENTRY_NAME


def create_states(ctx: context.Context):
    ctx.state_machine.add_state(create_sticker.create_state(ctx.state_machine))
    ctx.state_machine.add_state(edit_sticker.create_state(ctx.state_machine))


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler('ADD_STICKER', handlers.AddStickerHandler)
    ctx.event_handlers.register_handler('EDIT_STICKER', handlers.EditStickerHandler)


def register_object_types(ctx: context.Context):
    ctx.objects_storage.register_object_type('STICKER', object_types.StickerObject)


def register_module_menu(ctx: context.Context):
    ctx.menu.add_command_to_menu(STICKER_MENU_ENTRY_NAME)


@modules.modules.register_module('sticker')
def init_module(ctx: context.Context):
    create_states(ctx)
    register_handlers(ctx)
    register_object_types(ctx)
    register_module_menu(ctx)
