import context
from events.event_handlers import EventHandler
from . import consts


class CreateGroupHandler(EventHandler):
    @classmethod
    def apply(cls, ctx: context.Context, **kwargs):
        obj_id = kwargs['obj_id']
        children_ids = kwargs['children_ids']
        ctx.objects_storage.create(
            consts.GROUP_OBJECT_TYPE_NAME, obj_id=obj_id, children_ids=children_ids
        )
