import context
import modules
from modules.connector.states import connector_state
from modules.connector.object_types import Connector
from . import handlers
from .consts import CONNECTOR_MENU_ENTRY_NAME


def create_states(ctx: context.Context):
    ctx.state_machine.add_state(connector_state.create_state(ctx.state_machine))


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler('ADD_CONNECTOR', handlers.AddConnectorHandler)


def register_object_types(ctx: context.Context):
    ctx.objects_storage.register_object_type('CONNECTOR', Connector)


def register_module_menu(ctx: context.Context):
    ctx.menu.add_command_to_menu(CONNECTOR_MENU_ENTRY_NAME)


@modules.modules.register_module('connector')
def init_module(ctx: context.Context):
    create_states(ctx)
    register_handlers(ctx)
    register_object_types(ctx)
    register_module_menu(ctx)
