import context
from events.event_handlers import EventHandler


class DestroyObjectHandler(EventHandler):
    @classmethod
    def apply(cls, ctx: context.Context, **kwargs):
        obj_id = kwargs['obj_id']
        ctx.objects_storage.destroy_by_id(obj_id)
