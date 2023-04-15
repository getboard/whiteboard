import context
import modules
from modules.connector.states import connector_state
from modules.connector.object_types import Connector
from . import handlers


def create_states(ctx: context.Context):
    ctx.state_machine.add_state(connector_state.create_state(ctx.state_machine))


def register_handlers(ctx: context.Context):
    ctx.event_handlers.register_handler('ADD_CONNECTOR', handlers.AddConnectorHandler)


def register_object_types(ctx: context.Context):
    ctx.objects_storage.register_object_type('CONNECTOR', Connector)


@modules.modules.register_module('connector')
def init_module(ctx: context.Context):
    create_states(ctx)
    register_handlers(ctx)
    register_object_types(ctx)
